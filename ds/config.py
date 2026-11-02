"""Paths and environment, read in one place so every command agrees on them."""

import json
import os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent

# Every date a prompt sees is Panama's. The server's clock is UTC, which is
# already tomorrow from 19:00 in Panama.
TZ = ZoneInfo("America/Panama")


def today() -> date:
    return datetime.now(TZ).date()


# Exit codes, so a scheduler can tell "fix the input" from "look at the logs".
OK = 0
FAILED_CHECK = 1
BAD_INPUT = 2
AGENT_FAILED = 3
LIMIT_HIT = 4
ENVIRONMENT = 5
BUSY = 6


def load_dotenv(path: Path = REPO / ".env") -> None:
    """Fill os.environ from .env without overriding what is already set."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        key, sep, value = line.partition("=")
        key = key.strip()
        if sep and key.isupper() and not key.startswith("#"):
            os.environ.setdefault(key, value.strip())


def runs_dir() -> Path:
    return Path(os.environ.get("RUNS_DIR") or REPO / "runs")


def website_repo() -> Path | None:
    value = os.environ.get("WEBSITE_REPO", "").strip()
    return Path(value) if value else None


def model() -> str:
    return os.environ.get("MARKETING_MODEL") or "claude-opus-5-5"


def claude_config_file() -> Path:
    """Where the Claude CLI keeps per-project state, trust included."""
    custom = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(custom) / ".claude.json" if custom else Path.home() / ".claude.json"


def trust_problem(repo: Path = REPO) -> str | None:
    """Return why the repo is untrusted, or None.

    An untrusted workspace makes the CLI ignore every `permissions.allow`
    entry in .claude/settings.json. The run would still start, have each git,
    render and check command refused, and finish half done.
    """
    path = claude_config_file()
    try:
        projects = json.loads(path.read_text()).get("projects", {})
    except (OSError, ValueError):
        projects = {}
    if projects.get(str(repo), {}).get("hasTrustDialogAccepted") is True:
        return None
    return (
        f"{repo} is not trusted in {path}, so the CLI would ignore the allow list in "
        ".claude/settings.json. Open Claude Code in the repo once and accept the trust "
        f'dialog, or set projects["{repo}"].hasTrustDialogAccepted to true in that file.'
    )


def auth_problem() -> str | None:
    """Return why auth is misconfigured, or None.

    An empty variable is dropped first: the CLI may treat `KEY=` as set. Both
    set at once is refused, because the API key silently wins and the bill
    moves from the subscription to pay-per-token.
    """
    for key in ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN"):
        if key in os.environ and not os.environ[key].strip():
            del os.environ[key]
    if "ANTHROPIC_API_KEY" in os.environ and "CLAUDE_CODE_OAUTH_TOKEN" in os.environ:
        return (
            "Both ANTHROPIC_API_KEY and CLAUDE_CODE_OAUTH_TOKEN are set. "
            "The API key would win silently and bill per token. Keep one."
        )
    return None
