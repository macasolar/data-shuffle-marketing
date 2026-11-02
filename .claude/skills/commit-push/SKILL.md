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
   strategy, prompts, ds, content, ads, docs, claude. A prompt run keeps
   its own message (`plan: 2026-11 ...`, `make-week: ...`).
3. `.githooks/pre-commit` bumps `version.txt` and stages it in the same
   commit (`git config core.hooksPath .githooks` once per clone). Never edit
   `version.txt` by hand. If a commit fails after the bump, undo it with
   `git restore --staged --worktree version.txt`.
4. Last line: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
5. **Push only if José asked in this turn.** Commit, then run the `handoff`
   skill, then push: the push hook refuses a `CURRENT_WORK.md` older than the
   last commit, and asks José to confirm. Never `--force`.
6. Report the short hash, the version, the branch, and whether it was pushed.
