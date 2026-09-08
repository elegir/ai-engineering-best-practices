---
title: "Practice — spec-driven (plan → approve → execute one task at a time)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [spec-driven-development, openspec, user-stories, plan-mode, commands]
principle: principles/04-spec-driven-development.md
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Spec-driven

## Solves

Work goes from "add SSO" straight to code. The agent guesses scope, builds too much or the wrong thing, and there is nothing to verify against or to review before tokens are spent. Symptoms: large diffs that mix concerns; "done" features that miss half the intent; rework; no acceptance criteria for the e2e tests.

## Applies when

- Any change bigger than one file or touching behavior users see.
- Brownfield repos (most): use the manual flow first, then OpenSpec's delta specs.

## Does not apply when

- Typo fixes, dependency bumps, one-line bug fixes with an obvious test.

## Files in this folder

| File | Copy to | Purpose |
|---|---|---|
| `specs/README.md` | `<repo>/specs/README.md` | Where specs live, naming, lifecycle (draft → approved → implemented → archived) |
| `dot-claude/commands/plan-ticket.md` | `<repo>/.claude/commands/` | `/plan-ticket <spec>`: ask-the-expert, then spec review, then atomized task list — no code |
| `dot-claude/commands/develop-task.md` | `<repo>/.claude/commands/` | `/develop-task T-00N`: one task, TDD, verify, docs, stop |
| `constitution.md` | `<repo>/specs/constitution.md` (or `docs/constitution.md`) | Non-negotiable rules any plan must respect (Spec-Kit idea, usable without Spec-Kit) |
| `openspec-quickstart.md` | read | Installing OpenSpec and mapping the manual flow to `/opsx:*` |
| Spec template | `../../templates/open-spec-user-story.md` | User-story format with SSO worked example |

## Adapt

- Fill `constitution.md` with the repo's real non-negotiables (from `docs/*-standards.md`); keep it under a page.
- In the commands, replace the model hints and the test commands.
- Decide the spec location (`specs/` by default; `openspec/changes/` if OpenSpec is adopted).
- Start manual (two or three changes), then install OpenSpec; keep the same story format inside its `specs/`.

## Verify

1. `/plan-ticket specs/<feature>.md` produces questions first, then a task list where each task has a verification command — and writes no code.
2. `/develop-task T-00N` implements exactly one task, test first, and stops with the definition-of-done checklist filled.
3. A reviewer can read the spec + diff + test output and approve without reading every line.

## Sources

- LIDR framework comparison, plan-high/execute-mid rule, ask-the-expert prompt, SSO homework — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.4, §3.9.
- OpenSpec: https://github.com/Fission-AI/OpenSpec · Spec-Kit: https://github.com/github/spec-kit · Superpowers: https://github.com/obra/superpowers

## Change log

- 2026-09-08 — created.
