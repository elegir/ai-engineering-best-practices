---
title: "Practice — context docs skeleton (the docs/ folder every repo needs)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [context-engineering, docs, standards, workflow]
kind: working-style
applies-when: "always"
principle: principles/01-context-engineering.md
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Context docs skeleton

## Solves

The agent produces inconsistent code because nothing in the repo tells it how *this* project is built. Symptoms: the agent's reasoning shows it opening random files "to understand the conventions"; two runs of the same task give different structures; the agent asks how to run tests; it invents naming; it puts files in the wrong layer; junior and senior prompts produce different quality. The fix is a `docs/` folder with one document per element, referenced from the entry file, kept alive by the workflow.

## Applies when

- The repo has more than a weekend of work in it and will be touched by an agent more than once.
- Standards exist in someone's head, in chat history, or scattered across README paragraphs.
- Several agents/tools (Claude Code, Cursor, Codex) or several people work on it.

## Does not apply when

- Throwaway scripts or one-file experiments. Write a 10-line README instead.
- A framework already generates equivalent artifacts you keep current (e.g. OpenAPI from code annotations) — then link, don't duplicate.

## Files in this folder

| File | Copy to | Purpose |
|---|---|---|
| `docs/README.md` | `<repo>/docs/README.md` | Map of the docs folder; the entry file points here |
| `docs/stack.md` | `<repo>/docs/stack.md` | Technologies, versions, what each is for |
| `docs/development-guide.md` | `<repo>/docs/development-guide.md` | From zero to running; seed data; every test layer; per-worktree ports/DB |
| `docs/architecture.md` | `<repo>/docs/architecture.md` | Style, layers, where each kind of thing lives, dependency direction |
| `docs/data-model.md` | `<repo>/docs/data-model.md` | Every entity in natural language + Mermaid diagram |
| `docs/backend-standards.md` | `<repo>/docs/backend-standards.md` | The long one: API, DB, errors, logging, security, git workflow, examples good/bad |
| `docs/frontend-standards.md` | `<repo>/docs/frontend-standards.md` | Same for UI (delete if no UI) |
| `docs/testing-standards.md` | `<repo>/docs/testing-standards.md` | Unit/integration/e2e rules, coverage, anti-patterns, when tests run |
| `docs/documentation-standards.md` | `<repo>/docs/documentation-standards.md` | Which code change updates which doc; how to write |
| `docs/workflow.md` | `<repo>/docs/workflow.md` | Phases, roles, deliverables, **definition of done**, model policy |
| `prompts/generate-docs.md` | (use, don't copy) | The prompts that make an agent fill the skeletons exhaustively |

The skeletons contain the **index** (the section headings the workshop showed) plus guidance comments. The agent fills them; a human reviews. Expect `backend-standards.md` to reach ~1,000 lines when done properly.

## Adapt

- Delete `frontend-standards.md` for pure backends/pipelines; for WordPress/PHP repos rename backend → `php-standards.md` and add a `wordpress-standards.md` (hooks, WP-CLI, plugin structure) using the same section pattern.
- In `data-model.md`, if the schema is large, document the core entities in prose and generate the rest (`prisma`, `alembic`, `wp db` dumps) into `docs/generated/`.
- `workflow.md` must reflect the *real* process. If there is no QA role, say so. If there is no CI, say "pre-commit is the gate".
- Replace every `<<PLACEHOLDER>>`.
- Add to the entry file (see `../agent-entry-file/`): one line per doc, when to read it.
- Put "update the relevant doc before declaring done" in `workflow.md` so the docs stay alive.

## Verify

1. Start a fresh agent session and ask it to run the unit tests using only `docs/development-guide.md`. It must succeed without asking.
2. Ask it to add a small endpoint/function. In its reasoning it should cite `docs/backend-standards.md` and `docs/testing-standards.md`, not explore test files to infer style.
3. Ask a non-technical question about the data ("which table stores X and what links it to Y?"); the answer should come from `docs/data-model.md`.
4. `docs/README.md` lists every file in `docs/`; the entry file links `docs/README.md`.

## Sources

- LIDR videos B and D (the `docs/` folder demo; the 1,000-line standards; TDD/coverage/e2e in the workflow) — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.3, §3.9.
- OpenAI `docs/` by category; SIGPLAN single source of truth — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.1, §3.4.
- Spec-Boot (LIDR) provides an equivalent template set (`api-spec.yml`, `data-model.md`, `development_guide.md`).

## Change log
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
