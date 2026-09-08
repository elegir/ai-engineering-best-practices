---
title: "Spec-driven development — plan in writing before the agent implements"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [spec-driven-development, openspec, spec-kit, superpowers, spec-boot, plan-mode]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Spec-driven development (SDD)

## 1. The question this answers

How should work be handed to an agent so that what it builds is what was wanted, is reviewable before code exists, and can be verified afterwards — and which of the current frameworks should Martin use?

## 2. Short answer

Never let the agent go from a one-line request straight to code. First produce a written spec (user stories or MUST/SHOULD requirements plus a task list), review it, then execute one atomized task at a time, then verify against the spec. Use the strongest model to plan and a cheaper one to execute. For Martin's solo, brownfield repos start with **OpenSpec** (lightest; delta specs) on top of a Spec-Boot-style `docs/` context layer; consider **Superpowers** later if the agent keeps skipping tests; Spec-Kit only if auditability becomes a requirement.

## 3. Long explanation

### Why a spec

Agents tend to attempt everything at once (the one-shot problem) and declare "done" when it compiles. A spec fixes both: it forces the scope to be stated, lets a human approve before tokens are spent on code, and gives the sensors something to verify against. Boris Cherny: "most sessions start in plan mode… I go back and forth until I like the plan… a good plan is really important." The practitioner guide: separate planning from execution; humans approve; one feature at a time. LIDR's rule for models: **Opus plans and writes the spec exhaustively; Sonnet executes the atomized tasks.**

### The "ask the expert" step

Before the spec, make the agent interrogate you: *"Analyze the project and ask me anything you need to clarify before proposing a solution."* In LIDR's example the model produced ~25 questions across auth, seats, subscriptions/Stripe, personalization, reporting, chat, auditing, privacy, i18n, and scalability — questions a senior CTO admitted he sometimes forgets. Recommended 100% of the time for architecture and design, and in any area where you are not the expert. This matches Martin's existing rule that prompts are guided investigations, one problem per prompt, investigation before implementation.

### The open spec as user stories

The workshop's concrete format: a spec file in the repo, written as user stories with acceptance criteria, kept as continuous context for the agent. Homework was an SSO spec starting with *sign-up* and *login*. Template: `templates/open-spec-user-story.md`.

### The frameworks (state as of 2026-09-08)

| | OpenSpec (Fission-AI) | Spec-Kit (GitHub) | Superpowers (obra) | Spec-Boot (LIDR) |
|---|---|---|---|---|
| Kind | Lightweight SDD engine | Heavy SDD engine with gates | Behavioral skills plugin | Context/rules kit |
| Core idea | **Delta specs**: each change lists ADDED/MODIFIED/REMOVED vs current spec | `constitution → specify → clarify → plan → tasks → analyze → implement` | Socratic questioning → plan → subagent TDD (red/green/refactor), YAGNI, DRY forced; native worktrees | `docs/` template (`api-spec.yml`, `data-model.md`, `development_guide.md`) + symlinks so all copilots read the same rules |
| Install | `npm i -g @fission-ai/openspec && openspec init` | CLI (v0.10 changed flags; pre-June-2026 tutorials may be stale) | plugin | MIT repo |
| Strength | Minimal friction; brownfield-friendly; ~60k stars; 30+ assistants | Governance, audit trails, compliance presets, GitHub/Microsoft backing | Real execution discipline; zero external deps; 94% PR rejection rate = rigor | Copilot-agnostic single ruleset; free |
| Weakness | Multi-repo "Stores" in early beta | Heavy for small tasks; sequential; community split | No shareable spec doc for team review | Only the context layer; needs an engine on top |
| Use when | You want to start today on a real project | Org needs everything documented and auditable | Planning is fine but execution discipline is missing | Always, underneath whichever engine |

OpenSpec flow: `/opsx:explore` (optional thinking out loud) → `/opsx:propose` (proposal + specs + design + tasks) → `/opsx:apply` → `/opsx:archive` (delta merged into the permanent spec).

### Where SDD meets the workflow document

The spec is ingredient 3 (the task); the workflow document (`01-context-engineering.md`) already says TDD, docs update, e2e, coverage. SDD engines add the *artifacts* (proposal, spec, tasks) and the *gates* (`/analyze` in Spec-Kit; archive in OpenSpec). Do not adopt an engine before the context layer exists — LIDR's explicit ordering.

## 4. How to apply it in a repo

1. Ensure `docs/` context exists (`01-context-engineering.md`). If not, do that first.
2. Pick one small brownfield change. Run the "ask the expert" prompt. Answer the questions.
3. Write the open spec as user stories with acceptance criteria (`templates/open-spec-user-story.md`). Review it as if reviewing a PR.
4. Ask the strongest model, in plan mode, for an atomized task list. Approve.
5. Execute tasks one at a time with the cheaper model; each task ends with tests passing and docs updated.
6. Verify against the spec (sensors: unit, e2e). Archive/merge the spec.
7. After 2–3 changes done by hand this way, install OpenSpec and repeat with `/opsx:*`. Record the experience as a new source entry.

## 5. Anti-patterns

- Spec written *after* the code to justify it.
- A spec so long it becomes the design doc nobody reads; keep stories atomic.
- Adopting Spec-Kit's full ceremony for a ten-minute fix.
- Skipping the clarification step because "I know what I want" — the questions are the value.
- Letting the execution model re-plan; if the plan is wrong, go back to the planner.

## 6. Evidence & sources

- LIDR hub §4 framework comparison and videos C/D; homework — `sources/2026-09-08-lidr-workshop-harness-engineering.md` (§3.2, §3.4, §3.9).
- Practitioner guide "separate planning from execution"; SIGPLAN "specification-first" — `sources/2026-09-08-how-teams-structure-agent-knowledge.md`.

## 7. Change log

- 2026-09-08 — created.
