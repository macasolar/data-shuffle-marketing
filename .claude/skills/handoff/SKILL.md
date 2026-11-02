---
name: handoff
description: Write CURRENT_WORK.md so the next session can continue without this conversation. Run it whenever a push is requested (before pushing), and when closing a session or switching tasks. Do not run it in the middle of work.
argument-hint: "(optional) what to emphasise for the next session"
---

# Session handoff (`CURRENT_WORK.md`)

Writes `CURRENT_WORK.md` at the repo root. Order when pushing: **commit, then
handoff, then push**. `.claude/hooks/confirm-git-push.sh` refuses a push while
`CURRENT_WORK.md` is missing or older than the last commit.

 It is gitignored (this machine only)
and **rewritten whole**, never appended: the history lives in git, in the piece
files and in `ads/log.md`.

## Before writing

1. `git branch --show-current`, `git status --short`, `git log --oneline -10`.
2. The pipeline: `grep -h '^estado:' content/*/*.md | sort | uniq -c`
3. Open questions: `grep -c '^- \[ \]' facts/OPEN-QUESTIONS.md`
4. `strategy/cadence.md`: current `phase` and `auto_approve_evergreen`.
5. `cat version.txt` and `uv run ds runs --limit 5`: the version, and whether
   the last runs failed (status, exit code, error).
6. Only call **done** what was verified: the connector answered, the piece is
   visible in Metricool, the branch is on the remote. Everything else goes
   under "Not tested".

## Format (about 40 lines, English, not a copy of the conversation)

```markdown
# Work in progress, <branch>, <YYYY-MM-DD>
Task: <one line>
Version: <version.txt> | Last runs: <ok/failed, run ids if failed>
Phase: <n> | auto_approve_evergreen: <bool> | Open questions: <n>

## Status
- Done (verified): ...
- Pending: ...

## Pipeline
- idea <n> | draft <n> | review <n> | scheduled <n> | published <n> | rejected <n>
- Waiting on José: <ids, marking legal/price>

## External actions this session
- Metricool / Canva / website branch: <what, ID>

## Decisions
- <what was agreed and why> (durable rules go in CLAUDE.md or the right
  facts/strategy file, not here)

## Verification and blockers
- Tested: ...
- Not tested: ...
- Blockers / waiting on José: ...

## Next step
1. <concrete action> and how to verify it

Commits for this task: since <hash>
```

Do not list changed files one by one. Git has them.
