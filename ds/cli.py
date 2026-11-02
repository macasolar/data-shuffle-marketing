"""`ds`: the one command a scheduler, a person or a prompt calls.

    ds run <stage> [--input JSON | --input-file PATH] [--budget USD] [--dry-run]
    ds check [piece-id]
    ds render <template> <data.json> <out.png>
    ds runs [--limit N]

`ds run` prints one JSON object on stdout (the result) and logs JSON lines on
stderr and in runs/ds.log. The exit code says what kind of failure it was,
see ds/config.py.
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from pydantic import ValidationError

from ds import check, config, render, runs
from ds.stages import ALIASES, STAGES, build_prompt, resolve


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "t": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        skip = set(vars(logging.makeLogRecord({}))) | {"message", "asctime"}
        entry.update({k: v for k, v in vars(record).items() if k not in skip})
        if record.exc_info:
            entry["exc"] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False, default=str)


def setup_logging() -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    try:
        root = config.runs_dir()
        root.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(root / "ds.log"))
    except OSError as err:
        print(f"warning: no log file: {err}", file=sys.stderr)
    for h in handlers:
        h.setFormatter(JsonFormatter())
    logging.basicConfig(level=logging.INFO, handlers=handlers, force=True)


def cmd_run(args: argparse.Namespace) -> int:
    from ds.runner import Report, run_stage  # the SDK import is slow; only `run` needs it

    name = resolve(args.stage)
    if name is None:
        known = ", ".join([*STAGES, *ALIASES])
        print(
            Report(
                None,
                args.stage,
                config.BAD_INPUT,
                "rejected",
                error=f"unknown stage; known: {known}",
            ).to_json()
        )
        return config.BAD_INPUT
    try:
        raw = Path(args.input_file).read_text() if args.input_file else args.input
        payload = json.loads(raw) if raw else {}
        if not isinstance(payload, dict):
            raise ValueError("input must be a JSON object")
    except (OSError, ValueError) as err:
        print(Report(None, name, config.BAD_INPUT, "rejected", error=str(err)).to_json())
        return config.BAD_INPUT

    if args.dry_run:
        stage = STAGES[name]
        try:
            parsed = stage.input.model_validate(payload)
        except ValidationError as err:
            print(Report(None, name, config.BAD_INPUT, "rejected", error=str(err)).to_json())
            return config.BAD_INPUT
        print(build_prompt(stage, parsed, str(config.website_repo() or ""), config.today()))
        return config.OK

    report = run_stage(name, payload, budget_usd=args.budget)
    print(report.to_json())
    return report.exit_code


def cmd_check(args: argparse.Namespace) -> int:
    files = [f for f in check.pieces() if not args.id or f.stem == args.id]
    if not files:
        print(f"No piece with id {args.id}." if args.id else "No pieces in content/ yet.")
        return config.OK
    total = 0
    for file in files:
        problems = check.check_piece(file)
        if problems:
            total += len(problems)
            print(f"\n{file.relative_to(config.REPO)}", file=sys.stderr)
            for p in problems:
                print(f"  {p}", file=sys.stderr)
    if total:
        print(f"\n{total} problem(s) in {len(files)} piece(s).", file=sys.stderr)
        return config.FAILED_CHECK
    print(f"{len(files)} piece(s), no problems.")
    return config.OK


def cmd_render(args: argparse.Namespace) -> int:
    try:
        print(render.render(args.template, Path(args.data), Path(args.out)))
    except (render.RenderError, OSError, ValueError) as err:
        print(f"render: {err}", file=sys.stderr)
        return config.FAILED_CHECK
    return config.OK


def cmd_runs(args: argparse.Namespace) -> int:
    db = runs.connect(config.runs_dir())
    for row in runs.recent(db, args.limit):
        print(json.dumps(row, ensure_ascii=False))
    return config.OK


def version() -> str:
    # Read from the file, not package metadata: the Docker image runs the
    # mounted repo without installing it.
    return (config.REPO / "version.txt").read_text().strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ds", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", action="version", version=f"ds {version()}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("run", help="run one stage through the agent")
    p.add_argument("stage", help=f"one of {', '.join(STAGES)} (or {', '.join(ALIASES)})")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--input", help="stage input as a JSON object")
    src.add_argument("--input-file", help="path to a JSON file with the stage input")
    p.add_argument("--budget", type=float, help="override the stage's USD ceiling")
    p.add_argument("--dry-run", action="store_true", help="print the prompt, call nothing")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("check", help="mechanical check of the pieces in content/")
    p.add_argument("id", nargs="?")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("render", help="render a brand template to PNG")
    p.add_argument("template")
    p.add_argument("data")
    p.add_argument("out")
    p.set_defaults(fn=cmd_render)

    p = sub.add_parser("runs", help="list recent runs from runs/runs.db")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(fn=cmd_runs)

    args = parser.parse_args(argv)
    config.load_dotenv()
    setup_logging()
    return int(args.fn(args))
