#!/usr/bin/env bash
# PreToolUse (Bash): nothing run from this repo publishes the website.
#
# The deploy fires on a merge to master, uploads over FTPS and pings IndexNow.
# An article that reaches master has been seen by nobody. The prompts already
# say to stop at a pushed branch; this is the part that does not rely on the
# prompt being followed.
#
# Quoted text (commit messages) is dropped first, so a commit that mentions
# "master" is not confused with a command that touches it.
cmd=$(jq -r '.tool_input.command // empty' | perl -0pe 's/"[^"]*"//g; s/\x27[^\x27]*\x27//g')

deny() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

printf '%s' "$cmd" | grep -Eq '\bgit\b.*\bpush\b.*\b(master|main)\b' \
  && deny "Pushing to master deploys the live site. Leave the branch pushed and say so in the summary; José merges."
printf '%s' "$cmd" | grep -Eq '\bgit\b.*\b(merge|rebase|cherry-pick)\b.*\b(master|main)\b' \
  && deny "Merging master publishes the site. That is José's decision, not this run's."
printf '%s' "$cmd" | grep -Eq '\bgit\b.*\bpush\b.*(--force|--delete|\s-f(\s|$))' \
  && deny "Force or delete push is never needed here."
printf '%s' "$cmd" | grep -Eq 'deploy\.sh|\blftp\b|indexnow' \
  && deny "Deploying and pinging search engines happen on merge to master, by a person."
printf '%s' "$cmd" | grep -Eq '\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r' \
  && deny "Recursive force delete. If a file really has to go, delete it by name."

exit 0
