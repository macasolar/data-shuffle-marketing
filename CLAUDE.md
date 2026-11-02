# CLAUDE.md, permanent rules for data-shuffle-marketing

This repo is the content brain for **Data-Shuffle**, a cooperativa of 7+
professionals in Panama doing custom software, data, AI automation and server
infrastructure. It holds the facts, the brand, the strategy and the prompts.
The work itself is done by scripts in `scripts/` that run the prompts in
`prompts/` through the Claude Agent SDK, with Metricool (publishing and
analytics) and Canva (video) as connectors.

Talk to José in English unless he switches. Everything a visitor or a follower
reads goes in Spanish of Panama.

## Language split

Same rule as the website repo, by role rather than by file type:

- **English**: code, identifiers, code comments, commit messages, file and
  folder names, scripts, workflows, config, and this file.
- **Spanish**: anything that becomes copy. `facts/`, `brand/`, `strategy/`,
  `content/`, `reports/` and **the prompts in `prompts/`**. The prompts are
  Spanish on purpose: they are the instructions for writing Spanish posts, and
  translating them makes them worse at their job. The website repo settled the
  same question the same way for `claude/`.

## Rules

0. **A development session here modifies only this repo. Hard rule.** It
   binds the interactive agent working on this repo (VS Code, terminal) and
   any agent it spawns: no file in another repo is created, edited, moved or
   deleted, and no git command that changes another repo (add, commit, push,
   switch...) is run on it. Changes another repo needs go to José or to that
   repo's own agent. The hook `.claude/hooks/only-this-repo.sh` enforces it.
   It does **not** bind what this repo ships: the production code and the
   agents `ds run` starts may write to other repos through the path a stage
   defines (for example a `post/*` branch and PR in the website repo). The
   runner marks its agents with `DS_RUN=1`, and the hook lets them through.
1. **Never use the em dash** (U+2014), in any language, anywhere: posts, copy,
   comments, commit messages. Use a plain hyphen with spaces, a comma,
   parentheses, or restructure. A hook blocks it on write.
2. **Facts only from `facts/`.** Every factual claim (a number, a year, a
   client name, a technology we claim to work with, a price, a deadline) must
   exist in `facts/`. If it is not there, ask José or leave the claim out.
   Never fill a gap with general knowledge, and never invent a number.
3. **Fact freshness.** Each fact carries `Última confirmación: YYYY-MM-DD`. Do
   not use a price older than 90 days or a legal or regulatory fact older than
   180 days without asking José to reconfirm. A fact marked
   `> ⚠️ POR CONFIRMAR` is not used in anything published.
4. **The website is the other source.** Facts taken from
   `website-data-shuffle` (services, team, testimonials, the published posts)
   are already approved copy: they are published. They go into `facts/` with
   the file they came from as their source. What is **not** on the site and not
   in `facts/` does not exist.
5. **No file, no publishing.** Every piece is a file in `content/YYYY-MM/`
   (shape in `content/_templates/post.md`) before anything reaches Metricool.
6. **States:** `idea → draft → review → scheduled → published`, or `rejected`.
   `review` means it is sitting in Metricool's review queue waiting for José.
   Only José approves, in Metricool or by editing the file.
7. **The blog post stops at a pushed branch.** The blog run writes the post in
   the website repo, runs `npm run validate` there, commits and pushes a
   branch. It never merges to `master` and never deploys. Publishing the site
   is José's merge, and the social pieces for that post are written only once
   its URL is live.
8. **Log every external action** with date, ID and reason: `metricool_id` and
   `canva_design_id` in the piece's own file, ad actions in `ads/log.md`.
9. **Every run ends with a short summary for José**: what was done, what needs
   him, what broke.
10. **Decide with data.** Use real Metricool numbers to choose what to do more
    of. Learnings go in `strategy/pillars.md` under "Aprendizajes".

## Repo map

- `facts/` the only allowed source for claims. Gaps in `facts/OPEN-QUESTIONS.md`.
- `brand/` voice (`voice.md`), visual (`visual.md`), the HTML render templates
  (`templates/`) and the Canva video templates (`canva-templates.md`).
- `strategy/` pillars, cadence and phases (`cadence.md`), audiences.
- `prompts/` what each run actually tells Claude to do. The real work lives here.
- `ds/` the Python runner: `ds run` (stages, run records, logs), `ds render`
  (HTML template to PNG), `ds check` (mechanical content check), `ds runs`.
  Thin on purpose: logic that could be a prompt is a prompt. Tests in `tests/`.
- `content/YYYY-MM/` the month plan and one file per piece.
- `ads/` Meta Ads rules and log. Not automated yet, see `docs/ROLLOUT.md`.
- `reports/` monthly reports.
- `docs/` setup, pilot, phases.

## How a run works

`ds run <stage> --input '<json>'`, with stages `plan`, `post`, `week`,
`publish`, `report` (long names: the files in `prompts/`). Each one validates
its input, loads the matching prompt and runs it through the Claude Agent SDK
with this repo as the working directory. The prompt is the spec; the runner
only wires it up and records the run (`runs/runs.db`, `runs/<id>/`). In
production it runs in Docker on the VM, see `docs/SERVER.md`.

Running a prompt by hand in an interactive session is fine and does the same
thing: the prompts do not depend on the runner.

## Token discipline

- Ask the `metricool-lookup` agent for analytics instead of pulling raw numbers
  into the conversation.
- Review drafts with the `post-checker` agent rather than reading each file.
- Read only the `facts/` file a piece cites in `fuentes`, not the whole folder,
  except in `plan-month`.

## Session continuity

- `CURRENT_WORK.md` is gitignored, per machine, shown by the SessionStart hook.
  Check what it claims against `git log` before acting on it.
- It is rewritten only by the `handoff` skill: before any push, and when
  closing a session or switching tasks. Never mark work done unless verified.
- Push order: commit, handoff, push. `.claude/hooks/confirm-git-push.sh`
  refuses a push while `CURRENT_WORK.md` is missing or older than the last
  commit, and asks José to confirm otherwise.

## Other operating rules

- No secrets in the repo. Connectors are authorised per machine with `/mcp`,
  and `.env` holds the rest.
- Nothing is published outside a prompt run. During the pilot, schedule at
  least 3 days ahead so José can cancel.
- Small commits with clear English messages.
