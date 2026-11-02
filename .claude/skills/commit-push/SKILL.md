---
name: commit-push
description: Commit, and only when asked, push data-shuffle-marketing changes the way this repo does it. English messages, attribution trailer, handoff before push.
disable-model-invocation: true
argument-hint: "push (optional): also push after committing"
---

# Commit (and push only if asked)

1. `git status --short` and `git diff --stat`. Only the files from this task.
   Never `.env`, `output/` or `CURRENT_WORK.md`.
2. Message in English, `type(scope): lowercase summary`. Scopes: facts, brand,
   strategy, prompts, scripts, content, ads, docs, claude. A prompt run keeps
   its own message (`plan: 2026-11 ...`, `make-week: ...`).
3. Last line: `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
4. **Push only if José asked in this turn.** Run the `handoff` skill first.
   Never `--force`.
5. Report the short hash, the branch, and whether it was pushed.
