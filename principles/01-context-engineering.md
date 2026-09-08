---
title: "Context engineering — what the agent must know before it acts"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [context-engineering, documentation, standards]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Context engineering

## 1. The question this answers

What information must exist in a repository, and in what shape, so that any agent (and any person) produces work that matches how *this* project is built — consistently, regardless of who asks or how well they prompt?

## 2. Short answer

Write the project's tacit knowledge down, in the repo, as a small set of separate Markdown documents — stack, environment setup, architecture and file layout, data model, conventions per layer, and the end-to-end workflow with its definition of done — and reference all of them from one short base file. Make the agent *update* these documents as part of every task so they stay alive. Then daily prompts collapse to one-liners, and a junior with this context produces the same output as a senior.

## 3. Long explanation

### Why context beats prompts and models

The LIDR videos make the argument bluntly: the same task in another company would have different execution, validations and result, because the *project* is different. If you do not tell the agent your standards, it infers them from whatever files it happens to open — and two runs (or two developers) open different files and get different results. Prompt structure matters less every quarter as models improve; model choice matters less as vendors converge. What remains is context. Boris Cherny's team runs Claude Code with "surprisingly basic" configuration and a single shared `CLAUDE.md` — the leverage is in what the agent knows, not how it is asked.

### The recipe: three ingredients, one golden rule

Two ingredients are defined by the team and change rarely; the third arrives with each task.

**Ingredient 1 — Technical specifications.** One file per element:

- *Stack*: concrete technologies, versions, what each is for.
- *Development environment*: fully explained from zero — install, start everything, start only backend+frontend when the DB is up, seed the DB with realistic data, run unit tests, run integration tests, run e2e tests. If the agent cannot bring the environment up, it cannot verify anything and cannot work autonomously.
- *Architecture and file structure*: the style (hexagonal, DDD, MVC…) and where each kind of thing lives (repositories, services, routes, controllers, components).
- *Data model*: every table/entity in natural language — what each field is for, validation rules, relationships — ending with a Mermaid diagram. Non-technical people can read it or hand it to an assistant instead of interrupting developers.
- *Conventions per layer* (backend, frontend, mobile, QA, documentation): API design, test structure, naming, git workflow (branch naming, rebase policy, PR vs commit, merge target), design patterns in use, clean code/SOLID, form validation, error handling, logging and comments, security-by-design (XSS, CORS, SQL injection, secrets never in `.env` committed), performance. These are **long** — LIDR's backend standards exceed 1,000 lines for a small project — and include *how to do it, how not to do it, examples of both*.
- *API contract*: an OpenAPI file (`api-spec.yml`) generated and maintained by the agent.

**Ingredient 2 — Workflow.** The software development life cycle, as this team actually runs it, with a diagram: what happens systematically from a new requirement to production, who intervenes at each phase, what each role's *deliverable* is, and what makes each deliverable excellent. Written down, this becomes the **definition of done** the agent can check itself against: e.g. *developer delivers code + updated documentation + unit tests; tests are written first and fail (TDD); the full suite passes; new-feature coverage ≥ 90%; e2e tests pass in Playwright; the agent updates docs before declaring done.* If QA follows, QA's deliverable is new tests + a report.

**Ingredient 3 — The task.** The only thing that varies. With the machine prepared, prompts become: "document this task", "give me the plan by steps", "implement step 1", "write the unit tests" — or slash commands like `plan ticket`, `develop ticket`.

**Golden rule — share it.** The context is a team convention, committed to git, edited by everyone. That is what turns individual productivity into collective transformation: consistency across attempts and across people, independence from prompt skill, independence from seniority. When evaluation shows the flow is respected and the quality is good, "you can hand the car keys to the junior".

### How the documents get written and stay alive

Writing them takes days; LIDR calls it "the critical task for this year". The agent writes most of it: give it a **fixed index as a one-shot template** ("Expert architect, prepare a README with at least these sections… follow this structure") so it fills the index instead of inventing one, and ask it to be exhaustive and to act as the different domain experts per section. Then, crucially, the workflow document makes *updating the docs* a mandatory step of every task, so the source of truth stays alive and a human only reviews diffs. This is the answer to why documentation always rotted before: it lived elsewhere and nobody updated it.

### Where this sits relative to the harness

Context is the base of the pyramid (context → harness → loop). A loop built on disorganized context amplifies the disorder. So: context first, then hooks/tools/sensors, then automation.

### The pointer file

All of the above is referenced from one short base file (`CLAUDE.md` / `AGENTS.md`) — see `03-agent-instruction-files.md`. The base file says *where* things are; the documents say *what*. Long base files degrade adherence.

## 4. How to apply it in a repo

1. Inventory what exists: README, `CLAUDE.md`/`AGENTS.md`, `docs/`, `.cursor/rules`, wiki pages, Notion. List what is missing against the ingredient list above.
2. Create `docs/` with one file per element (suggested names: `stack.md`, `development-guide.md`, `architecture.md`, `data-model.md`, `backend-standards.md`, `frontend-standards.md`, `testing-standards.md`, `documentation-standards.md`, `workflow.md`, `api-spec.yml`). Spec-Boot (LIDR, MIT) provides a ready template of exactly these files.
3. For each file, prompt the agent with a fixed index and "be exhaustive; act as an expert in X". Review; correct; commit.
4. Put the workflow and definition of done in `workflow.md`, including "update the relevant doc before finishing" and the test/coverage gates.
5. Reduce `CLAUDE.md`/`AGENTS.md` to pointers into `docs/`.
6. Run one real task end to end and watch the agent's reasoning: it should go to `testing-standards.md`, not infer from test files. If it does not, the pointer or the doc is unclear.
7. Add MCPs only for context that cannot live in the repo (Jira/Notion for tasks, Context7 for library docs, Figma for designs).

## 5. Anti-patterns

- One giant `CLAUDE.md` holding the standards themselves (context burn, low adherence, rots).
- Standards that exist only in someone's head, Slack, or a wiki the agent cannot read — "anything not discoverable in the repository doesn't exist for the agent".
- Prose describing *current* system state without a mechanism to update it — it will be wrong within weeks. Pair it with the "update docs before done" gate or replace it with generated artifacts (OpenAPI, schema dumps).
- Duplicating a fact in several docs. One file per fact; link elsewhere.
- Copying another project's standards verbatim. They must describe *this* project's real conventions or the agent will fight the codebase.

## 6. Evidence & sources

- LIDR workshop hub §3 and videos B, C, D — `sources/2026-09-08-lidr-workshop-harness-engineering.md` (§3.3, §3.9).
- OpenAI Codex team: repo as system of record; `docs/` by category — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.1.
- SIGPLAN four-level hierarchy and single source of truth — same file, §3.4.
- Boris Cherny's shared `CLAUDE.md` practice — workshop entry §3.2.

## 7. Change log

- 2026-09-08 — created.
