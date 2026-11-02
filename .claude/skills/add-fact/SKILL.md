---
name: add-fact
description: File new facts from José into the right facts/ file. Takes free text or a voice-note transcript, usually answers to facts/QUESTIONNAIRE.md, updates the facts with today's Última confirmación, removes the resolved lines from facts/OPEN-QUESTIONS.md and commits. Use whenever José shares information about the cooperativa, the team, clients, services or prices.
---

# add-fact

Follow `CLAUDE.md`. Facts are written in Spanish of Panama. No em dashes.

## Steps

1. Read the input. Split it into individual facts. Map question numbers (Q1 to
   Q13) to `facts/QUESTIONNAIRE.md`.
2. Route each fact:
   - Team, contact, profiles, figures: `facts/company.md`
   - Services, technologies, what is no longer offered: `facts/services.md`
   - Prices, offers, what can be promised: `facts/offers.md`
   - Client questions and objections: `facts/faq.md`
   - Cases and testimonials: `facts/cases.md`, recording permission to name
     explicitly. Without a clear yes, `Permiso para nombrar: no`
   - Tone, tú or usted, emojis: `brand/voice.md`
   - Budget, zones, thresholds: `ads/playbook.md`
   - Who approves, best review day: `strategy/cadence.md`
3. Write each fact in the format that file already uses. Replace the old value,
   remove its `> ⚠️ POR CONFIRMAR` line, and set
   `Última confirmación: <today>`.
4. **Never infer past what José said.** If something is ambiguous, keep the ⚠️
   and ask. A price without saying whether it is monthly or one off is
   ambiguous.
5. **If a fact contradicts the website**, do not just overwrite it: say so. The
   site is published copy, so the two disagreeing means the site needs changing
   too. List it for José.
6. Remove the resolved lines from `facts/OPEN-QUESTIONS.md`, and add new ⚠️
   items there if the answer opened a question.
7. Say which pieces in `content/` already used the corrected fact.
8. Commit: `facts: <short description>`.

## Summary for José

Facts added or changed, one line each with its file. What is still open. New
questions. Pieces affected. Anything that contradicts the website.
