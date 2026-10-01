---
title: "Practice — spec-driven (plan → approve → execute one task at a time)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [spec-driven-development, openspec, user-stories, plan-mode, commands]
kind: working-style
applies-when: "always"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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

## Reference implementation

`constitution.md`, `openspec-quickstart.md` and the two commands. Tool-neutral: Spec-Kit, OpenSpec or a hand-rolled `specs/` folder all satisfy the contract.

## Stack-sensitive points

- The verification command per task is the only stack-dependent element and comes from `../verification/`.
- Framework scaffolding generators (Laravel `artisan make:*`, Rails-style generators) tempt the agent to skip the test-first step; the develop-task command must name the test to write before the generator runs.

## Adapt

- Fill `constitution.md` with the repo's real non-negotiables (from `docs/*-standards.md`); keep it under a page.
- In the commands, replace the model hints and the test commands.
- Decide the spec location (`specs/` by default; `openspec/changes/` if OpenSpec is adopted).
- Start manual (two or three changes), then install OpenSpec; keep the same story format inside its `specs/`.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. Planning a ticket produces questions first, then a task list where every task has a verification command, and writes no code — observer: agent — negative: code written during planning, or a task without a check
2. Developing a task implements exactly one task, test first, and stops with the definition-of-done checklist filled — observer: agent — negative: two tasks in one run, or code before its test
3. The spec, the diff and the test output together let a reviewer approve without reading every line, and the review decision is recorded on the spec — observer: Martin — negative: a merge with no recorded approval
4. The constitution (non-negotiable rules) exists and every spec references it — observer: script — negative: a spec that does not point at it

**Example commands (Claude Code):** `/plan-ticket specs/<feature>.md`; `/develop-task T-00N`.

## Sources

- LIDR framework comparison, plan-high/execute-mid rule, ask-the-expert prompt, SSO homework — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.4, §3.9.
- OpenSpec: https://github.com/Fission-AI/OpenSpec · Spec-Kit: https://github.com/github/spec-kit · Superpowers: https://github.com/obra/superpowers

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
