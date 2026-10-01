---
title: "Practice — verification (deterministic sensors per application type)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [testing, e2e, playwright, hurl, pytest, bats, evals, definition-of-done]
kind: working-style
applies-when: "always"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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
| `dry-run-and-approval.md` | **Only when `acts_on_world`** (sends, publishes, pays or writes third-party records on its own, LLM or not) | `<repo>/docs/dry-run-and-approval.md`; its rule 3 tests go into the smoke suite |

## Reference implementation

One folder per application type: `python-pytest/`, `web-playwright/`, `api-hurl/`, `cli-bats/`. They are the four shapes of the same contract (a seeded environment, a few must-not-break flows, one command). A PHP repo satisfies the contract with Pest/PHPUnit plus `api-hurl/` for its HTTP surface; nothing requires a port of `test_smoke.py`.

## Stack-sensitive points

- **The sensor differs by application type more than by language**: an HTTP API is smoked with Hurl in any language; a WordPress theme has no callable entry point, so its smoke is HTTP + WP-CLI checks (`hooks-and-guards/variants/php-wordpress.md`).
- **Seeding**: Python/Node repos seed a local database in the test fixture; Laravel has migrations + factories (`RefreshDatabase`); WordPress needs a fixture export or a disposable site — budget for it, the sixty-second target is hard there.
- **Dry-run switch** (assertion 6): an environment variable works everywhere; in WordPress prefer a constant in `wp-config.php` so a plugin cannot override it from the options table.

## Adapt

- Pick the folder(s) matching the app. A repo can need two (API + UI).
- Replace `<<BASE_URL>>`, seed credentials, and the three or four "must never break" flows. Smoke = the flows that, if broken, make everything else irrelevant (login, the core transaction, the main pipeline step).
- Prefer accessibility-tree selectors (`getByRole`, `getByLabel`) over CSS; prefer text assertions over screenshots. Use screenshots only in a separate visual-regression job.
- Wire the smoke command into `.claude/hooks/stop-gate.sh` (`hooks-and-guards/`) and the full suite into CI. Do not put the agent in CI; the agent *writes* tests, CI *runs* them.
- For pipelines with side effects (emails, posts, payments): a `--dry-run` or sandbox mode is part of the sensor. If the code has none, adding it is the first task. The full rule set — one switch, approval before the first live run, smoke tests that run the real path in dry-run mode — is `dry-run-and-approval.md`; copy it only when the repo's facts include `acts_on_world`.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. One command runs the smoke suite — the three or four flows that, if broken, make everything else irrelevant — in under about sixty seconds on a seeded local environment — observer: script — negative: more than one command, or a suite that needs a human step
2. Breaking the core flow on purpose makes the smoke suite fail with a readable message, and the stop gate refuses to end the session — observer: script — negative: a broken flow with a green suite
3. The definition-of-done checklist with the exact commands is in `docs/workflow.md` — observer: Martin — negative: "run the tests" without the command
4. `docs/harness-evals.md` lists three tasks, and running them after a harness change takes under thirty minutes — observer: Martin — negative: a harness change shipped without running them
5. Tests assert on text and structure (accessibility roles, response fields), not on screenshots, except in a separate visual-regression job — observer: Martin — negative: a smoke test that compares images — framework: beats
6. When `acts_on_world`: every side-effecting entry point has one dry-run switch, the smoke suite runs the real path in dry-run mode and asserts both the payload and the absence of the effect, live mode is refused outside production, and the first live run of anything new is capped and approved (`dry-run-and-approval.md` §Verify) — observer: script — negative: a sender with no dry-run mode, or a dry-run that still sends

**Example commands (Python / Node / PHP / shell):** `pytest tests/test_smoke.py -q`; `npx playwright test e2e/smoke.spec.ts`; `hurl --test tests/api/smoke.hurl`; `bats test/cli.bats`; `vendor/bin/pest --group=smoke`.

## Sources

- LIDR: e2e mandatory; "give Claude a way to verify its work"; sensors after execution — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.6, §3.9.
- Practitioner guide §5: accessibility tree over screenshots; tools per app type (Playwright, Hurl, bats, Testcontainers); generate with agent, run without it — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-30 — added `dry-run-and-approval.md`, a section that applies only when the repo's facts include `acts_on_world`; per `decisions/0004-day-one-for-blank-and-existing-repos.md` §7 (debate attack 2: the fintech moves money with no LLM, so the dry-run rule belongs here, not in `llm-gateway`). The practice stays `always`; the file is conditional.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
