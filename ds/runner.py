"""Runs one stage end to end: validate, record, call the agent, classify, record."""

import asyncio
import json
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from claude_agent_sdk import ClaudeSDKError, CLINotFoundError, ResultMessage
from pydantic import ValidationError

from ds import agent, config, runs
from ds.stages import STAGES, build_prompt

log = logging.getLogger("ds.runner")

# HTTP statuses worth another attempt: rate limit, overload, upstream hiccups.
TRANSIENT = {429, 500, 502, 503, 504, 529}
RETRY_DELAYS = (30, 120)


@dataclass
class Report:
    run_id: str | None
    stage: str
    exit_code: int
    status: str
    error: str | None = None
    result: str | None = None
    cost_usd: float | None = None
    duration_ms: int | None = None
    run_dir: str | None = None

    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


def _classify(outcome: agent.Outcome | None, exc: BaseException | None) -> tuple[int, str | None]:
    if exc is not None:
        if isinstance(exc, CLINotFoundError):
            return config.ENVIRONMENT, f"Claude CLI not found: {exc}"
        return config.AGENT_FAILED, f"{type(exc).__name__}: {exc}"
    assert outcome is not None
    res = outcome.result
    if res is None:
        return config.AGENT_FAILED, "the agent stream ended without a result message"
    if res.subtype in ("error_max_turns", "error_max_budget_usd"):
        return config.LIMIT_HIT, f"{res.subtype} after {res.num_turns} turns"
    # The SDK can flag is_error on a `success` subtype; that is still a failure.
    if res.subtype != "success" or res.is_error:
        detail = "; ".join(str(e) for e in (res.errors or [])) or res.result or ""
        status = f" (HTTP {res.api_error_status})" if res.api_error_status else ""
        return config.AGENT_FAILED, f"{res.subtype}{status} {detail}".strip()
    return config.OK, None


def _retryable(outcome: agent.Outcome | None, exc: BaseException | None) -> bool:
    """Retry only a run that has not touched anything yet.

    Once a tool has run, the agent may have committed, pushed or scheduled a
    post. Running the stage again could do that twice, so a person decides.
    """
    if outcome is not None and outcome.tool_calls:
        return False
    if exc is not None:
        return isinstance(exc, ClaudeSDKError) and not isinstance(exc, CLINotFoundError)
    res = outcome.result if outcome else None
    return res is not None and res.api_error_status in TRANSIENT


def run_stage(
    name: str,
    payload: dict[str, Any],
    *,
    budget_usd: float | None = None,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> Report:
    stage = STAGES[name]
    try:
        parsed = stage.input.model_validate(payload)
    except ValidationError as err:
        return Report(None, name, config.BAD_INPUT, "rejected", error=str(err))

    if problem := config.auth_problem() or config.trust_problem():
        return Report(None, name, config.ENVIRONMENT, "rejected", error=problem)
    website = config.website_repo()
    if stage.needs_website and (website is None or not website.is_dir()):
        return Report(
            None,
            name,
            config.ENVIRONMENT,
            "rejected",
            error=f"WEBSITE_REPO is not set or not a directory: {website}",
        )

    root = config.runs_dir()
    try:
        with runs.exclusive(root):
            return asyncio.run(
                _run(
                    name,
                    parsed.model_dump(exclude_none=True),
                    build_prompt(stage, parsed, str(website or ""), config.today()),
                    budget_usd or stage.budget_usd,
                    website,
                    sleep,
                )
            )
    except runs.Busy as err:
        return Report(None, name, config.BUSY, "rejected", error=str(err))


async def _run(
    name: str,
    payload: dict[str, Any],
    prompt: str,
    budget: float,
    website: Any,
    sleep: Callable[[float], Awaitable[None]],
) -> Report:
    stage = STAGES[name]
    root = config.runs_dir()
    run_id = runs.new_run_id(name)
    run_dir = root / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "input.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    (run_dir / "prompt.md").write_text(prompt)

    db = runs.connect(root)
    model = config.model()
    runs.start(db, run_id, name, payload, model)
    log.info("run.start", extra={"run_id": run_id, "stage": name, "budget_usd": budget})
    started = time.monotonic()

    outcome: agent.Outcome | None = None
    exc: BaseException | None = None
    attempts = 0
    with (
        (run_dir / "events.jsonl").open("a") as events,
        (run_dir / "stderr.log").open("a") as stderr,
    ):
        for delay in (*RETRY_DELAYS, None):
            attempts += 1
            outcome, exc = None, None
            opts = agent.options(
                cwd=config.REPO,
                website=website,
                model=model,
                budget_usd=budget,
                max_turns=stage.max_turns,
                stderr=stderr,
            )
            try:
                outcome = await agent.run(prompt, opts, events)
            except Exception as err:  # classified below, never swallowed
                exc = err
            code, error = _classify(outcome, exc)
            if code == config.OK or delay is None or not _retryable(outcome, exc):
                break
            log.warning(
                "run.retry",
                extra={"run_id": run_id, "attempt": attempts, "error": error, "wait_s": delay},
            )
            await sleep(delay)

    res: ResultMessage | None = outcome.result if outcome else None
    text = (res.result if res else None) or (outcome.last_text if outcome else None)
    duration = int((time.monotonic() - started) * 1000)
    status = "success" if code == config.OK else "failed"
    runs.finish(
        db,
        run_id,
        status=status,
        exit_code=code,
        error=error,
        result_text=text,
        duration_ms=duration,
        cost_usd=res.total_cost_usd if res else None,
        num_turns=res.num_turns if res else None,
        tool_calls=outcome.tool_calls if outcome else 0,
        attempts=attempts,
        model_usage_json=res.model_usage if res else None,
        denials_json=res.permission_denials if res else None,
        session_id=res.session_id if res else None,
    )
    db.close()
    report = Report(
        run_id,
        name,
        code,
        status,
        error=error,
        result=text,
        cost_usd=res.total_cost_usd if res else None,
        duration_ms=duration,
        run_dir=str(run_dir),
    )
    (run_dir / "result.json").write_text(report.to_json())
    log.info(
        "run.end",
        extra={
            "run_id": run_id,
            "status": status,
            "exit_code": code,
            "cost_usd": report.cost_usd,
            "duration_ms": duration,
            "error": error,
        },
    )
    return report
