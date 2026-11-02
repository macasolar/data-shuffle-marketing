"""The runner against a fake agent: no tokens, no network.

What matters here is the bookkeeping and the safety rules: every run gets a
row and a folder, failures get the right exit code, and a run that already
used a tool is never retried.
"""

import json
import sqlite3
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import pytest
from claude_agent_sdk import (
    AssistantMessage,
    CLIConnectionError,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)

from ds import agent, config, runner, runs


def result(
    subtype: str = "success", is_error: bool = False, status: int | None = None, cost: float = 0.42
) -> ResultMessage:
    return ResultMessage(
        subtype=subtype,
        duration_ms=1000,
        duration_api_ms=900,
        is_error=is_error,
        num_turns=3,
        session_id="s1",
        total_cost_usd=cost,
        result="Resumen para José",
        api_error_status=status,
        model_usage={"m": {"outputTokens": 10}},
    )


def text(t: str) -> AssistantMessage:
    return AssistantMessage(content=[TextBlock(text=t)], model="m")


def tool(name: str = "Bash") -> AssistantMessage:
    return AssistantMessage(content=[ToolUseBlock(id="t1", name=name, input={})], model="m")


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("RUNS_DIR", str(tmp_path / "runs"))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
    monkeypatch.delenv("WEBSITE_REPO", raising=False)
    # A trusted workspace in a throwaway Claude config, not the real one.
    claude = tmp_path / "claude"
    claude.mkdir()
    (claude / ".claude.json").write_text(
        json.dumps({"projects": {str(config.REPO): {"hasTrustDialogAccepted": True}}})
    )
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(claude))
    return tmp_path / "runs"


def fake_agent(monkeypatch: pytest.MonkeyPatch, *attempts: list[Any] | Exception) -> list[str]:
    """Each attempt is a list of messages to stream, or an exception to raise."""
    prompts: list[str] = []
    queue = list(attempts)

    async def query(prompt: str, options: Any) -> AsyncIterator[Any]:
        prompts.append(prompt)
        step = queue.pop(0)
        if isinstance(step, Exception):
            raise step
        for msg in step:
            yield msg

    monkeypatch.setattr(agent, "query", query)
    return prompts


async def no_sleep(_: float) -> None:
    pass


def row(root: Path, run_id: str) -> sqlite3.Row:
    db = runs.connect(root)
    return db.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()


def test_success_is_recorded(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prompts = fake_agent(monkeypatch, [text("trabajando"), tool(), result()])
    rep = runner.run_stage("plan-month", {"mes": "2026-12"}, sleep=no_sleep)

    assert rep.exit_code == config.OK and rep.status == "success"
    assert rep.result == "Resumen para José" and rep.cost_usd == 0.42
    assert "- mes: 2026-12" in prompts[0] and "## Entrada" in prompts[0]

    r = row(env, rep.run_id)
    assert (r["status"], r["exit_code"], r["tool_calls"], r["attempts"]) == ("success", 0, 1, 1)
    assert json.loads(r["model_usage_json"]) == {"m": {"outputTokens": 10}}

    run_dir = Path(rep.run_dir)
    events = [json.loads(line) for line in (run_dir / "events.jsonl").read_text().splitlines()]
    assert [e["type"] for e in events] == ["AssistantMessage", "AssistantMessage", "ResultMessage"]
    assert json.loads((run_dir / "result.json").read_text())["exit_code"] == 0
    assert (run_dir / "prompt.md").exists() and (run_dir / "input.json").exists()


def test_bad_input_spends_nothing(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prompts = fake_agent(monkeypatch)
    for stage, payload in [
        ("write-blog-post", {}),
        ("plan-month", {"mes": "2026-13"}),
        ("make-week", {"typo": 1}),
    ]:
        rep = runner.run_stage(stage, payload, sleep=no_sleep)
        assert rep.exit_code == config.BAD_INPUT, stage
    assert prompts == []


def test_both_auth_vars_are_refused(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "t")
    rep = runner.run_stage("make-week", {}, sleep=no_sleep)
    assert rep.exit_code == config.ENVIRONMENT and "bill" in rep.error


def test_empty_api_key_does_not_count(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "t")
    fake_agent(monkeypatch, [result()])
    assert runner.run_stage("make-week", {}, sleep=no_sleep).exit_code == config.OK


def test_untrusted_workspace_is_refused(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (Path(config.claude_config_file())).write_text(json.dumps({"projects": {}}))
    prompts = fake_agent(monkeypatch)
    rep = runner.run_stage("make-week", {}, sleep=no_sleep)
    assert rep.exit_code == config.ENVIRONMENT and "not trusted" in rep.error
    assert prompts == []


def test_blog_needs_website(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    rep = runner.run_stage("write-blog-post", {"tema": "facturas en PDF"}, sleep=no_sleep)
    assert rep.exit_code == config.ENVIRONMENT and "WEBSITE_REPO" in rep.error


def test_budget_hit_is_a_limit(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_agent(monkeypatch, [tool(), result("error_max_budget_usd", is_error=True)])
    rep = runner.run_stage("make-week", {}, sleep=no_sleep)
    assert rep.exit_code == config.LIMIT_HIT and row(env, rep.run_id)["status"] == "failed"


def test_transient_error_before_any_tool_is_retried(
    env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_agent(
        monkeypatch,
        CLIConnectionError("reset"),
        [result("error_during_execution", is_error=True, status=529)],
        [result()],
    )
    rep = runner.run_stage("make-week", {}, sleep=no_sleep)
    assert rep.exit_code == config.OK and row(env, rep.run_id)["attempts"] == 3


def test_failure_after_a_tool_is_never_retried(env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prompts = fake_agent(
        monkeypatch,
        [
            tool("mcp__metricool__createScheduledPost"),
            result("error_during_execution", is_error=True, status=529),
        ],
        [result()],
    )
    rep = runner.run_stage("publish-week", {}, sleep=no_sleep)
    assert rep.exit_code == config.AGENT_FAILED and len(prompts) == 1
    assert row(env, rep.run_id)["attempts"] == 1


def test_is_error_on_success_subtype_is_a_failure(
    env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_agent(monkeypatch, [result("success", is_error=True)])
    assert runner.run_stage("make-week", {}, sleep=no_sleep).exit_code == config.AGENT_FAILED


def test_second_run_is_refused_while_one_is_running(
    env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_agent(monkeypatch)
    with runs.exclusive(env):
        rep = runner.run_stage("make-week", {}, sleep=no_sleep)
    assert rep.exit_code == config.BUSY


def test_today_is_panama_not_utc(monkeypatch: pytest.MonkeyPatch) -> None:
    from datetime import UTC, datetime

    import ds.config as cfg

    class Late(datetime):
        @classmethod
        def now(cls, tz=None):  # type: ignore[no-untyped-def,override]
            # 02:00 UTC on Nov 2 is still 21:00 on Nov 1 in Panama.
            return datetime(2026, 11, 2, 2, 0, tzinfo=UTC).astimezone(tz)

    monkeypatch.setattr(cfg, "datetime", Late)
    assert cfg.today().isoformat() == "2026-11-01"
