---
title: "Practice — verification (deterministic sensors per application type)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [testing, e2e, playwright, hurl, pytest, bats, evals, definition-of-done]
principle: principles/05-verification-loops.md
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Verification

## Solves

The agent declares "done" when the code compiles, because nothing lets it prove the feature works end to end. Symptoms: green unit tests, broken feature; screenshots pasted as "proof"; manual review of every line; regressions found by users. This practice gives every kind of application a **smoke test the agent can run in one command**, plus a definition-of-done checklist and a tiny harness eval.

## Applies when

- Any repo where an agent changes behavior. Install this **first** if the repo has no runnable test command — everything else in the KB assumes one exists.

## Does not apply when

- Nothing. Scale down to the smallest sensor (a health-check script) rather than skipping.

## Files in this folder

| Folder / file | For | Copy to |
|---|---|---|
| `web-playwright/` — `playwright.config.ts`, `e2e/smoke.spec.ts` | Web apps, WordPress front-ends, dashboards | `<repo>/playwright.config.ts`, `<repo>/e2e/` |
| `api-hurl/` — `smoke.hurl` | HTTP APIs (any language) | `<repo>/tests/api/` |
| `python-pytest/` — `test_smoke.py`, `conftest.py` | Python services, pipelines, scrapers, senders | `<repo>/tests/` |
| `cli-bats/` — `cli.bats` | CLIs and shell scripts (including WP-CLI / fleet scripts) | `<repo>/test/` |
| `definition-of-done.md` | Every repo | paste into `docs/workflow.md` §2 |
| `harness-evals.md` | Every repo once the harness exists | `<repo>/docs/harness-evals.md` |

## Adapt

- Pick the folder(s) matching the app. A repo can need two (API + UI).
- Replace `<<BASE_URL>>`, seed credentials, and the three or four "must never break" flows. Smoke = the flows that, if broken, make everything else irrelevant (login, the core transaction, the main pipeline step).
- Prefer accessibility-tree selectors (`getByRole`, `getByLabel`) over CSS; prefer text assertions over screenshots. Use screenshots only in a separate visual-regression job.
- Wire the smoke command into `.claude/hooks/stop-gate.sh` (`hooks-and-guards/`) and the full suite into CI. Do not put the agent in CI; the agent *writes* tests, CI *runs* them.
- For pipelines with side effects (emails, posts, payments): a `--dry-run` or sandbox mode is part of the sensor. If the code has none, adding it is the first task.

## Verify

1. One command runs the smoke suite in under ~60 s on a seeded local environment.
2. Break the core flow on purpose → the smoke suite fails with a readable message; the Stop hook refuses to finish.
3. `docs/workflow.md` §2 contains the definition-of-done checklist with the exact commands.
4. `docs/harness-evals.md` lists three tasks; running them after a harness change takes < 30 minutes.

## Sources

- LIDR: e2e mandatory; "give Claude a way to verify its work"; sensors after execution — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.6, §3.9.
- Practitioner guide §5: accessibility tree over screenshots; tools per app type (Playwright, Hurl, bats, Testcontainers); generate with agent, run without it — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.

## Change log

- 2026-09-08 — created.
