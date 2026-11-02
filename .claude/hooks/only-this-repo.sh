#!/usr/bin/env bash
# PreToolUse (Write, Edit, MultiEdit, NotebookEdit, Bash): a development
# session here writes only inside this repo. Other repos, the website above
# all, are read, never changed from here (CLAUDE.md, rule 0).
#
# Production runs are out of scope: `ds run` sets DS_RUN=1 for its agents,
# whose stages may write elsewhere through the path they define.
[ "${DS_RUN:-}" = "1" ] && exit 0
#
# File tools: the target path must be inside the repo. Claude's own state
# (~/.claude: memory, settings) and temp dirs stay writable.
# Bash: a command that names another repo AND does something that writes is
# refused. Reading another repo (cat, grep, git log) is fine.
input=$(cat)
repo=$(cd "${CLAUDE_PROJECT_DIR:-$PWD}" && pwd -P)

deny() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

path=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' <<<"$input")
if [ -n "$path" ]; then
  case "$path" in /*) ;; *) path="$PWD/$path" ;; esac
  path=$(realpath -m "$path")
  case "$path" in
    "$repo"|"$repo"/*|"$HOME"/.claude/*|/tmp/*) exit 0 ;;
  esac
  deny "Only data-shuffle-marketing may be modified from here (CLAUDE.md rule 0). $path is outside it. Hand the change to José or to that repo's own agent."
fi

# Quoted text is dropped first, so a commit message that mentions the website
# is not taken for a command that touches it.
cmd=$(jq -r '.tool_input.command // empty' <<<"$input" | perl -0pe 's/"[^"]*"//g; s/\x27[^\x27]*\x27//g')
[ -n "$cmd" ] || exit 0

# Another repo named in the command: the website by name or by its paths, or
# any sibling checkout under the parent folder.
other='website-data-shuffle|web-data-shuffle|/work/website|\$\{?WEBSITE_REPO'
parent=$(dirname "$repo")
if printf '%s' "$cmd" | grep -Eq "$other" \
   || printf '%s' "$cmd" | grep -F "$parent/" | grep -vqF "$repo"; then
  writes='\bgit\b[^|;&]*\b(add|commit|push|switch|checkout|merge|rebase|reset|restore|mv|rm|stash|tag|cherry-pick|apply|am)\b|\b(rm|mv|cp|tee|touch|mkdir|rmdir|ln|chmod|truncate|install)\b|\bsed\b[^|;&]*\s-i|\bperl\b[^|;&]*\s-i|\bnpm\s+(ci|install|i|run)\b|\bgh\s+(pr\s+(create|merge|edit|close|comment)|repo\s+(edit|delete|rename|archive)|api\b[^|;&]*(-X|--method)\s*(POST|PUT|PATCH|DELETE))'
  # A redirect is a write only when it lands in another repo; 2>&1 is not.
  redirect=">>?[[:space:]]*[^&[:space:]]*($other|$parent/)"
  if printf '%s' "$cmd" | grep -Eq "$writes" \
     || { printf '%s' "$cmd" | grep -Eo "$redirect" | grep -vqF "$repo"; }; then
    deny "This command would change another repo. Only data-shuffle-marketing may be modified from here (CLAUDE.md rule 0). Reading it is fine."
  fi
fi

exit 0
