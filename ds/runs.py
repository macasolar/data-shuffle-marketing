"""Run records: one SQLite row per run, one folder of files per run.

The row is inserted as `running` before the agent starts, so a run that
crashes or is killed still shows up, stuck in `running`, instead of vanishing.
"""

import fcntl
import json
import secrets
import sqlite3
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ds.config import REPO

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,           -- running, success, failed
    exit_code INTEGER,
    error TEXT,
    input_json TEXT NOT NULL,
    result_text TEXT,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    duration_ms INTEGER,
    cost_usd REAL,
    num_turns INTEGER,
    tool_calls INTEGER,
    attempts INTEGER,
    model TEXT,
    model_usage_json TEXT,
    denials_json TEXT,
    session_id TEXT,
    git_sha TEXT
);
CREATE INDEX IF NOT EXISTS runs_started ON runs (started_at);
"""


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def new_run_id(stage: str) -> str:
    return f"{datetime.now(UTC):%Y%m%dT%H%M%S}-{stage}-{secrets.token_hex(2)}"


def git_sha() -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout.strip() or None


def connect(root: Path) -> sqlite3.Connection:
    root.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(root / "runs.db")
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def start(
    db: sqlite3.Connection, run_id: str, stage: str, payload: dict[str, Any], model: str
) -> None:
    db.execute(
        "INSERT INTO runs (id, stage, status, input_json, started_at, model, git_sha)"
        " VALUES (?, ?, 'running', ?, ?, ?, ?)",
        (run_id, stage, json.dumps(payload, ensure_ascii=False), now(), model, git_sha()),
    )
    db.commit()


def finish(db: sqlite3.Connection, run_id: str, **fields: Any) -> None:
    fields["finished_at"] = now()
    for key in ("model_usage_json", "denials_json"):
        if key in fields and not isinstance(fields[key], str | None):
            fields[key] = json.dumps(fields[key], ensure_ascii=False, default=str)
    cols = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE runs SET {cols} WHERE id = ?", (*fields.values(), run_id))
    db.commit()


def recent(db: sqlite3.Connection, limit: int = 20) -> list[dict[str, Any]]:
    rows = db.execute(
        "SELECT id, stage, status, exit_code, started_at, duration_ms, cost_usd,"
        " num_turns, tool_calls, error FROM runs ORDER BY started_at DESC LIMIT ?",
        (limit,),
    )
    return [dict(r) for r in rows]


class Busy(Exception):
    pass


@contextmanager
def exclusive(root: Path) -> Iterator[None]:
    """One run at a time. Two runs editing content/ and committing at once
    would interleave their commits, so the second one is refused, not queued.
    """
    root.mkdir(parents=True, exist_ok=True)
    with open(root / ".lock", "w") as fh:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as err:
            raise Busy("another run is in progress") from err
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
