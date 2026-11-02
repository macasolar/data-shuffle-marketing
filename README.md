# data-shuffle-marketing

Content and social media automation for **Data-Shuffle**, a cooperativa of 7+
professionals in Panama: custom software, APIs and integrations, data and
analytics, AI automation, and Linux and Windows server infrastructure.

This repo holds the facts, the brand, the strategy and **the prompts**. The
prompts are the product: `ds run` (Python, `ds/`) feeds one to the Claude Agent SDK
with this repo as its working directory, so the same instructions work whether
a cron job runs them or you run them by hand in a session.

| Connector | What for |
|---|---|
| Metricool | Schedules and publishes to LinkedIn, Facebook, Instagram and Google Business Profile; analytics, including Meta and Google Ads |
| Canva | Video pieces (reels). Still images are rendered from HTML, see below |
| Meta Ads | Phase 2. The account exists, nothing is running yet |

The permanent rules are in [CLAUDE.md](CLAUDE.md). The two that matter most:
**every claim comes from `facts/`**, and **a blog post stops at a pushed
branch** so nothing reaches the live site without José merging it.

## The flow

A topic goes in, and what comes out is an article on the site plus the social
pieces that point at it.

```
ds run post --input '{"tema": "extraer datos de facturas en PDF"}'
        writes the post in website-data-shuffle, runs its validate,
        pushes a branch. You review the PR and merge, which deploys.

ds run week
        writes next week's social pieces: from posts published on the site,
        from facts, or both. Renders the images. Leaves them as draft.

ds run publish
        sends the approved pieces to Metricool's review queue.
        You approve on your phone and Metricool publishes.
```

Social does not need a blog post. A piece can come from a published article, or
straight from `facts/` and `strategy/pillars.md` when there is nothing to link
to. That is the normal case for a Google Business Profile post or an offer.

## Routine

**Monthly, at the start of the month**
1. `ds run plan` writes `content/YYYY-MM/plan.md` and one file per piece in
   state `idea`.
2. `ds run report` sums up the previous month in `reports/YYYY-MM.md` and
   appends to "Aprendizajes".

**Weekly, Monday**
1. `ds run post --input '{"tema": "<topic>"}'` for the week's article, if one is due. One a
   week is the ceiling the website repo sets, two a month the floor.
2. `ds run week` writes and renders the social pieces for the next 7 days.
3. **José reviews.** Change `estado: draft` to `estado: approved` in the file,
   or `rejected` with a note.
4. `ds run publish` sends them to Metricool for review. Approving there is the
   last gate before they go out.

**Every run is recorded.** `ds runs` lists the last ones with status, cost,
duration and error; each run's full trace is in `runs/<id>/`. Exit codes and
where to look are in [docs/SERVER.md](docs/SERVER.md).

**Whenever**
- Paste anything José says about the business, in text or as a voice note
  transcript, and the `add-fact` skill files it into `facts/` and closes the
  matching open question.

## Images

Still images are rendered from the HTML templates in `brand/templates/` with
headless Chrome (`ds render`). This is the method the website repo already
uses for its brand pieces, and the reason is in
`website-data-shuffle/brand/README.md`: rendering from the real logo SVG and
the real font files gives the actual brand, where an image model gives
something that resembles it.

Video (reels) goes through Canva, from the templates specified in
`brand/canva-templates.md`.

## Start here

1. Do [docs/SETUP.md](docs/SETUP.md): connectors and the one-time accounts.
2. Read [facts/OPEN-QUESTIONS.md](facts/OPEN-QUESTIONS.md). Most of `facts/` is
   already filled in from the website, so the list is short. Answer it with the
   `add-fact` skill.
3. Run the pilot: [docs/PILOT-CHECKLIST.md](docs/PILOT-CHECKLIST.md). The
   phases are in [docs/ROLLOUT.md](docs/ROLLOUT.md).
4. Production runs on the VM in Docker: [docs/SERVER.md](docs/SERVER.md).
