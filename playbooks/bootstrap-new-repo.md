---
title: "Playbook — bootstrap a new repo: one paragraph of intent → planned facts → the router's list → the bundle's day-zero files, adapted and verified → the facts block in the entry file → first commit"
type: playbook
status: current
date: 2026-09-30
last-reviewed: 2026-09-30
tags: [bootstrap, day-one, blank-repo, planned-facts, bundles, greenfield]
sources:
  - decisions/0004-day-one-for-blank-and-existing-repos.md
  - decisions/0005-contract-first-practices-and-stacks.md
  - sources/2026-09-30-day-one-debate.md
  - sources/2026-09-30-stack-debate.md
supersedes: null
superseded-by: null
---

# Bootstrap a new repo

**Who runs this.** An agent inside a repository that has **no code yet** (a `git init` and maybe a README), on Martin's request. This is the blank-repo door (decision 0004 §3); an existing repo takes `which-practices-apply.md`. The routing fact `brownfield` decides: real commits older than a few weeks, a schema with migrations or a deploy that runs → not this playbook.

**Output.** The repo's day-zero harness, copied and adapted from the KB, every file's Verify passed, the facts block in the entry file, and one commit. Plus a field report (`templates/field-report.md`) — a bootstrap is an adoption of several practices at once and is measured like one (tokens, minutes, errors caught).

**Rules.** The KB writes nothing into the repo (decision 0001); the agent copies and the repo owns the files. Planned facts attach only `day-0` practices; the rest wait for the code. The bootstrap ships only what the bundle names — for a stack with no field-tested variant, capability practices arrive as contract + prompt + stack-notes, and the agent says so (decision 0005 §4). Explain each step to Martin before running it, one at a time.

## Step 0 — sync and read the router

`bash <kb>/scripts/kb-sync.sh --pull`; stop only on `ahead` or uncommitted changes. (`--pull` writes only inside the guide's `.git/` and is allowed even when the guide is otherwise read-only for the session — AGENTS.md "Rules when applying".) Read `<kb>/ROUTER.md` (under 2 KB) and `<kb>/practices/bundles.md`.

## Step 1 — one paragraph of intent

Ask Martin for one paragraph, in his words: what the product does, for whom, what it must never do. Do not ask a questionnaire. Then ask the **three intent questions** a repo cannot show, one at a time, in plain words:

1. "¿Va a cobrar dinero o manejar pagos?" → `regulated` (and usually `personal_data`)
2. "¿Va a servir a varias empresas o clientes cuyos datos no se pueden mezclar?" → `multi_tenant`
3. "¿Va a mandar, publicar o pagar solo, sin que alguien haga clic cada vez?" → `acts_on_world`

Plus the two workflow questions of `which-practices-apply.md` (`parallel_sessions`, `long_tasks`).

## Step 2 — planned facts

From the paragraph and the answers, write every fact of `practices/facts.md` as `<fact>: yes|no — planned <date> (<the sentence of Martin's that supports it>)`. `production` is `no — planned` until the first approved live run (a scheduled publisher with no human users still becomes `production: yes` the day it publishes for real — `practices/facts.md`); `brownfield` is `no`. Show the table in one screen; Martin corrects it. A planned fact **stays until the code contradicts it or Martin drops it**; later inference may upgrade it to `inferred`, never delete it (decision 0004 §1).

## Step 3 — the list

`python3 <kb>/scripts/applies.py --explain <fact>:planned <fact>:planned … parallel_sessions long_tasks` (asked facts without suffix; pass an asked fact only when the answer was yes — an absent fact is "no"). The output is the day-zero list, in order; practices marked *deferred* attach once the fact is inferred; every skip has its reason. Compare with the nearest shape in `practices/bundles.md` and note where this repo differs.

## Step 4 — the stack and the bundle

Pick the shape's default stack from `practices/stack-defaults.md` unless Martin names another. If a part of that stack cannot be installed on this machine (offline sandbox, missing database), record it as *planned* in `docs/stack.md` and build the walking skeleton with what runs (a CLI entry point and SQLite instead of a web framework and Postgres); the practices' assertions are judged against what runs; record it (with the interpreter version actually on the machine) in `docs/stack.md` as soon as `context-docs-skeleton` is copied in step 5. If the stack has no field-tested variant for a capability practice, say in one line: "for `<practice>` the KB gives the contract, the prompt and `stack-notes/<stack>.md`; no file is copied" — and plan that practice through `practices/prompt-library/implement-practice.md` after the working-style files are in.

## Step 5 — copy and adapt, in the router's order

For each practice in the list, in order: read its README (`## Files in this folder`, `## Adapt`), copy the day-zero files the bundle names, replace every `<<PLACEHOLDER>>`, and **run its `## Verify`** before moving to the next — a bootstrap that copies fourteen folders and verifies at the end is the thing the first debate attacked. Minimum sequence: `verification` (one smoke command, even if it only checks a health endpoint) → `context-docs-skeleton` → `agent-entry-file` → `hooks-and-guards` (`guard.py --selftest` must print OK) → `security-baseline` core (and full when planned) → the rest.

Two things the bundle does not spell out: (a) **a walking skeleton is part of day zero** — `verification`'s assertions 1, 2 and 6 need something to run, so the agent writes the minimal entry point, the configuration module with the dry-run switch, the one side-effecting module and a seeded test fixture before the smoke test can pass; keep it tiny and tested, not a feature. (b) `verification` assertion 2's stop-gate half is re-checked after `hooks-and-guards` is installed. When `session-state` is skipped (both asked facts "no"), every template line that names `PROGRESS.json` (entry file, spec commands, constitution, workflow, commit skill) is pointed at the open spec instead.

## Step 6 — the facts block

Paste the confirmed table from step 2 into the entry file's **Facts** section (`practices/agent-entry-file/AGENTS.md` template), each line with `planned <date>`. The entry file's session-start routine re-checks them against the code every session and reports upgrades (planned → inferred) or contradictions.

## Step 7 — first commit and field report

One commit: `chore(harness): bootstrap from AI-engineering KB (<kb commit>)` — the Conventional Commits shape the bootstrap's own `lefthook.yml` enforces. Then the field report (`templates/field-report.md`): every practice's assertions with evidence, tokens, minutes, errors caught, and what in the KB was wrong or missing. Martin passes it to the KB (`playbooks/adopt-variant.md`); it is the only evidence the bootstrap works (decision 0004 §8).

## Change log

- 2026-10-01 (shape A run, 23 min, 13 practices): `--pull` allowed in read-only sessions; offline-stack rule in step 4. Source `sources/2026-10-01-field-report-shape-a-bootstrap.md`.

- 2026-10-01 — first run (shape B, sandbox, 13 min): walking-skeleton rule, `production` wording, asked-facts rule, commit message shape, `PROGRESS.json` fallback, step order for `docs/stack.md`. Source `sources/2026-10-01-field-report-shape-b-bootstrap.md`.

- 2026-09-30 — created (decision 0004 §3; debate attacks 1, 4, 6 and 9 in `sources/2026-09-30-day-one-debate.md`; stack rules from decision 0005).
