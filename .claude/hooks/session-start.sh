#!/usr/bin/env bash
# SessionStart: show the handoff from the last session, so it does not cost a Read.
f="${CLAUDE_PROJECT_DIR:-$PWD}/CURRENT_WORK.md"
[ -f "$f" ] || exit 0
echo "CURRENT_WORK.md from the last session (verify against git log before acting on it):"
cat "$f"
