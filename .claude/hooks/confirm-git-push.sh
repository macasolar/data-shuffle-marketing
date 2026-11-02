#!/usr/bin/env bash
# PreToolUse (Bash): no push before CURRENT_WORK.md is up to date (handoff
# skill), and none without José confirming it. Same gate as the website repo,
# one step stricter: a handoff older than the last commit is not up to date,
# so the push is refused instead of only reminded.
#
# Production runs (DS_RUN=1) are out of scope: CURRENT_WORK.md is the
# development session's handoff, not theirs.
[ "${DS_RUN:-}" = "1" ] && exit 0

input=$(cat)
# Drop heredoc bodies and quoted strings so "push" inside a commit message does not match.
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' \
  | perl -0777 -pe 's/<<-?\s*([\x27"]?)(\w+)\1([^\n]*\n).*?^\s*\2[ \t]*$/$3/gms; s/\x27[^\x27]*\x27//g; s/"(?:\\.|[^"\\])*"//g')
printf '%s' "$cmd" | grep -Eq '(^|[;&|[:space:]])git([[:space:]]+[^;&|[:space:]]+)*[[:space:]]+push([[:space:]]|$)' || exit 0

decide() {
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:$d,permissionDecisionReason:$r}}'
  exit 0
}

repo="${CLAUDE_PROJECT_DIR:-$PWD}"
handoff="$repo/CURRENT_WORK.md"
last_commit=$(git -C "$repo" log -1 --format=%ct 2>/dev/null || echo 0)
if [ ! -f "$handoff" ]; then
  decide deny "git push: CURRENT_WORK.md does not exist. Run the handoff skill first, then push."
fi
if [ "$(stat -c %Y "$handoff")" -lt "$last_commit" ]; then
  decide deny "git push: CURRENT_WORK.md is older than the last commit. Run the handoff skill to bring it up to date, then push."
fi
decide ask "git push: CURRENT_WORK.md is up to date. Confirm the push."
