#!/usr/bin/env bash
# Blocks the em dash (U+2014) in anything written here. Exit 2 feeds the
# message back to Claude so it fixes the file itself.
f=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
[ -f "$f" ] || exit 0
if grep -n "$(printf '\342\200\224')" "$f" >&2; then
  echo "Em dash found in $f (lines above). Use a comma, parentheses, or a plain hyphen with spaces (CLAUDE.md rule 1)." >&2
  exit 2
fi
