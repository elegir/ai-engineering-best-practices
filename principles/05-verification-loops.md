---
title: "Verification loops — give the agent a way to check its own work"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-24
tags: [testing, e2e, playwright, hooks, sensors, definition-of-done]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Verification loops

## 1. The question this answers

How do we stop moving the bottleneck from "writing code" to "reviewing code" — i.e. how does an agent verify its own output well enough that a human reviews decisions, not every line?

## 2. Short answer

Every repo needs deterministic **sensors** the agent can run without a human: formatter and linter (milliseconds), unit and integration tests (seconds), end-to-end tests through the real interface (Playwright for web, Hurl/pytest for APIs, bats for CLIs), and a written **definition of done** with coverage thresholds. Wire them into hooks so they run automatically (PostToolUse for lint/format, Stop for the suite) and make "tests pass" the condition for "done". Humans keep the business-logic judgment; machines keep the mechanical checks. "Give Claude a way to verify its work… it will double or triple the quality."

## 3. Long explanation

### The debate, and the resolution

Two extremes: hand-review everything (no efficiency gained) vs. trust tests 100% (a test passes while the business logic is wrong). The workshop's resolution is *build the right sensors* and keep humans on the decisions that matter: the spec (before) and the diff plus e2e evidence (after). Automated sensors remove the mechanical review; they do not remove the product review.

### Sensors by layer and speed

| Layer | Timing | Tooling | Wired via |
|---|---|---|---|
| Format + lint | ms | Biome/Oxlint (TS), Ruff (Py), gofumpt/golangci-lint (Go), rustfmt/clippy (Rust) | PostToolUse hook, auto-fix then return violations as JSON |
| Type check + unit | s | tsc, mypy, jest/pytest | pre-commit (Lefthook) |
| Integration + e2e | s–min | Playwright (web), Hurl/pytest/Postman (API), bats/pexpect (CLI), Testcontainers (DB) | Stop hook and CI |
| Security/errors | min | Snyk scan, Sentry lookups (via MCP) | before PR; background agent |
| Human review | h | PR review of spec + diff + test report | after everything above is green |

Push checks to the fastest layer that can host them; CI-only linters move to pre-commit, pre-commit formatters move to PostToolUse.

### End-to-end is mandatory, not optional

LIDR: e2e with Playwright or Cypress is part of the definition of done. Cherny: Claude tests every change through the Chrome extension, "opens a browser, tests the UI, iterates until the UX feels right." Without eyes on the running application, agents declare done as soon as compilation passes. Prefer **structured text over screenshots** — the accessibility tree (role/name/state) is the universal interface and is far cheaper in tokens (practitioner guide: Playwright CLI ~27K vs Playwright MCP ~114K per session on its tasks; screenshots only for visual/layout bugs). Strategy: use the MCP/agent to *generate* the test suite, then run the generated tests deterministically in CI without an agent in the loop.

### Tests as specs

"Tests can't lie when you run them." Where prose would describe behavior, write the test. TDD as the workflow document prescribes: write tests, see them fail, get approval, implement, see them pass, coverage ≥ 90% on new functionality, full suite green, report emitted.

### Definition of done as a checklist the agent runs

Written in `docs/workflow.md`; the agent verifies each item before claiming completion: code; tests written first and passing; e2e passing; docs updated; lint clean; security scan run; progress file updated; commit message per convention. A Stop hook can enforce the executable subset.

### The agent must not be able to cheat

Protect linter configs and test files' assertions from silent edits (PreToolUse), ban `--no-verify`, and keep the sensors in CI as the final arbiter. Then the feedback that comes back is trustworthy and the agent's self-correction loop actually converges.

### Evals for the harness itself

Beyond code tests: a small set of representative tasks run periodically to check the *agent + harness* still produce acceptable results after changes to instructions, tools or models. Start with three tasks and a pass/fail rubric.

## 4. How to apply it in a repo

1. List the sensors that exist and how each is run from the command line. Anything that needs a human click is not a sensor.
2. Add the missing fastest layers first: formatter + linter with a PostToolUse hook.
3. Make the unit suite runnable in one command and put it in a pre-commit hook.
4. Add one e2e path through the real interface (login, or the core flow). For WordPress/UI repos: Playwright. For pipelines/APIs: Hurl or pytest against a seeded DB.
5. Write the definition of done in `docs/workflow.md`; add a Stop hook that runs the executable subset.
6. Protect configs; ban bypasses.
7. Add a three-task eval and run it whenever the harness changes.

## 5. Anti-patterns

- "Run the tests" as a sentence in `CLAUDE.md` with no hook.
- Screenshots as the primary verification (token-expensive, non-deterministic).
- The agent editing tests to make them pass; the agent disabling lint rules.
- Coverage numbers without e2e — units can all pass while the feature is broken end to end.
- Putting the agent *inside* CI; generate tests with the agent, run them without it.

## 6. Evidence & sources

- LIDR poll and Granola summary ("e2e mandatory", "open spec → apply → verify → repeat"), Cherny's tip — `sources/2026-09-08-lidr-workshop-harness-engineering.md` (§3.2, §3.6, §3.9 video D).
- Practitioner guide §2 and §5 (hooks, layers, e2e tool comparison) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.

## 7. Change log

- 2026-09-08 — created.
- 2026-09-24 — reviewed against `sources/2026-09-24-s12-agents-digest.md`; no change to the recommendation. Two supporting quotations recorded: "if you don't have some mechanism to get feedback as you're iterating, you're not injecting any more signal, you're just going to have noise… the next limiting factor is verification" (Erik Schluntz, Anthropic, 2025-02); Notion (2026-04) runs three eval tiers — CI regression, launch report card per user journey, and "frontier headroom" evals held at ~30 % pass — parked for the evals principle (sessions 5/11/16).
