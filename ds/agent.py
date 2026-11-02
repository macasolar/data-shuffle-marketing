"""The only module that talks to the Claude Agent SDK.

Every message the agent produces is appended to events.jsonl as it arrives,
so a run that dies halfway still leaves a full record of what it did.
"""

import dataclasses
import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)

log = logging.getLogger("ds.agent")


@dataclass
class Outcome:
    result: ResultMessage | None
    tool_calls: int
    last_text: str


def options(
    *,
    cwd: Path,
    website: Path | None,
    model: str,
    budget_usd: float,
    max_turns: int,
    stderr: TextIO,
) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        cwd=str(cwd),
        # The website repo is a second root, so the blog run can write there
        # without it counting as outside the workspace.
        add_dirs=[str(website)] if website else [],
        system_prompt={"type": "preset", "preset": "claude_code"},
        # CLAUDE.md, .claude/settings.json (permissions and hooks), .mcp.json,
        # and this machine's own settings. What a run may do lives in those
        # reviewable files, not here.
        setting_sources=["user", "project", "local"],
        # Edits inside the two repos go through; every other tool call is
        # decided by the allow and deny lists in .claude/settings.json.
        permission_mode="acceptEdits",
        model=model,
        max_turns=max_turns,
        max_budget_usd=budget_usd,
        stderr=lambda line: print(line, file=stderr, flush=True),
    )


def _event(msg: Any) -> dict[str, Any]:
    is_instance = dataclasses.is_dataclass(msg) and not isinstance(msg, type)
    data = dataclasses.asdict(msg) if is_instance else repr(msg)
    return {
        "t": datetime.now(UTC).isoformat(timespec="milliseconds"),
        "type": type(msg).__name__,
        "data": data,
    }


async def run(prompt: str, opts: ClaudeAgentOptions, events: TextIO) -> Outcome:
    outcome = Outcome(result=None, tool_calls=0, last_text="")
    async for msg in query(prompt=prompt, options=opts):
        events.write(json.dumps(_event(msg), ensure_ascii=False, default=str) + "\n")
        events.flush()
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, ToolUseBlock):
                    outcome.tool_calls += 1
                    log.info("tool", extra={"tool": block.name})
                elif isinstance(block, TextBlock) and block.text.strip():
                    outcome.last_text = block.text
        elif isinstance(msg, ResultMessage):
            outcome.result = msg
    return outcome
