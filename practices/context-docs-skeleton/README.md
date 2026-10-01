---
title: "Practice — context docs skeleton (the docs/ folder every repo needs)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [context-engineering, docs, standards, workflow]
kind: working-style
applies-when: "always"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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

## Reference implementation

The `docs/` skeleton in this folder plus `prompts/generate-docs.md`, which produces the first draft of each document from the repo. The skeleton's headings are the contract; the sample sentences inside are Python/Node-flavoured and are replaced wholesale.

## Stack-sensitive points

- `docs/stack.md` and `docs/development-guide.md` are the two documents that differ per stack; the rest (architecture, data model, workflow, standards) have the same headings everywhere.
- WordPress repos: the data model is largely WordPress's own (`wp_posts`, `wp_postmeta`, options); document the *custom* tables, post types and option keys, not core.
- Laravel: `docs/backend-standards.md` should state where the repo puts business logic (controllers vs actions vs services) — the framework allows all three and an agent will otherwise pick one per feature.

## Adapt

- Delete `frontend-standards.md` for pure backends/pipelines; for WordPress/PHP repos rename backend → `php-standards.md` and add a `wordpress-standards.md` (hooks, WP-CLI, plugin structure) using the same section pattern.
- In `data-model.md`, if the schema is large, document the core entities in prose and generate the rest (`prisma`, `alembic`, `wp db` dumps) into `docs/generated/`.
- `workflow.md` must reflect the *real* process. If there is no QA role, say so. If there is no CI, say "pre-commit is the gate".
- Replace every `<<PLACEHOLDER>>`.
- Add to the entry file (see `../agent-entry-file/`): one line per doc, when to read it.
- Put "update the relevant doc before declaring done" in `workflow.md` so the docs stay alive.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. A fresh agent session can run the unit tests using only `docs/development-guide.md`, without asking a question or exploring the tree — observer: agent — negative: the agent asks how to run tests, or opens configuration files to find out
2. Asked to add a small endpoint or function, the agent cites `docs/backend-standards.md` and `docs/testing-standards.md` in its reasoning instead of inferring style from existing test files — observer: agent — negative: the agent reads three existing tests "to see the convention"
3. Asked which table stores X and what links it to Y, the agent answers from `docs/data-model.md` — observer: agent — negative: the agent greps migrations to answer
4. `docs/README.md` lists every file in `docs/`, and the entry file links `docs/README.md` — observer: script — negative: a file in `docs/` absent from the index, or an index entry with no file
5. No document contains an unreplaced placeholder — observer: script — negative: a `<<…>>` token anywhere under `docs/`

**Example commands (Python / shell):** `ls docs | sort` vs the index; `grep -rn '<<' docs/`.

## Sources

- LIDR videos B and D (the `docs/` folder demo; the 1,000-line standards; TDD/coverage/e2e in the workflow) — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.3, §3.9.
- OpenAI `docs/` by category; SIGPLAN single source of truth — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.1, §3.4.
- Spec-Boot (LIDR) provides an equivalent template set (`api-spec.yml`, `data-model.md`, `development_guide.md`).

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
