---
title: "0006 — The catalogue is complete and agnostic: every reviewed practice is routed with its evidence status visible; the routing gate of 0004 §6 is retired; the KB never applies anything — a repo navigates, chooses and adapts"
type: decision
status: accepted
date: 2026-10-05
tags: [decision, routing, catalogue, agnostic, promotion, evidence, governance]
sources:
  - decisions/0004-day-one-for-blank-and-existing-repos.md
  - decisions/0001-knowledge-base-structure.md
  - decisions/0003-applicability-by-facts.md
  - decisions/0005-contract-first-practices-and-stacks.md
  - sources/method-log.md
supersedes: null
superseded-by: null
---

# 0006 — A complete, agnostic catalogue

## Context

Martin restated the purpose of this repository on 2026-10-04, after module 8: *any* of his repositories — AI SDR, Content Central, WordPress Fleet, a new multi-tenant Laravel platform, something not yet imagined — must be able to **navigate the whole catalogue of practices, see which ones are good and applicable to it, and take the best ones for its own best practice**. The KB does not apply practices to anybody; it is the star the repos steer by. That purpose was already written in three places: decision 0001 (the KB writes nothing into other repos; each repo copies, adapts and owns its files), decision 0003 (practices attach on observable facts of the repo — `retrieval`, `multi_tenant`, `acts_on_world` — never on a project's or a stack's name) and decision 0005 (a practice is a contract plus one reference; each repo researches its own stack).

One rule contradicted it. Decision 0004 §6 added a **routing gate**: a new practice enters the routing table "only after the previous module's day-0 files have passed Verify in one real repo". The gate was meant to keep routing from outrunning evidence. In practice it did something else. Between 2026-10-01 and 2026-10-05 six capability practices were produced through the full four-step cycle — written canon registered, market scanned, digest with impact table, principle and practice, mandatory clean-context review with 15 to 30 findings fixed each — and all six sit in the repository as `routed: false`: `structured-outputs/`, `evals/`, `memory-and-permissions/`, `data-ingestion/`, `embeddings-and-chunking/`, `vector-store/`. A repository that declares `retrieval: yes` and runs `scripts/applies.py` today is told nothing about ingestion, chunking or vector stores; the catalogue it navigates is a third smaller than the catalogue that exists. The gate's own precondition (installing `llm-gateway` in a real repo) never happened, because the course modules arrive weekly and the field work depends on Martin's machine and time; at that pace the gate would hold the catalogue incomplete for months. A gate that nobody can pass is not a sensor; it is a hole in the catalogue.

## Decision

### 1. The catalogue is complete

Every practice that has passed the mandatory clean-context review (`playbooks/ingest-new-source.md` step 2c) **is routed**: it has a row in `practices/README.md`, appears in `ROUTER.md` and `practices/bundles.md`, and `scripts/applies.py` proposes it when its `applies-when` line holds. The `routed: false` key stays in the vocabulary for one purpose only — a folder that is still being written, between its first commit and its review — and never as a status a finished practice lives in.

### 2. Evidence is visible, not hidden

What the gate tried to protect is carried by two fields that every routed row already shows: `status: draft | current` (whether the course or a real adoption has confirmed the content) and `reference-status: untested | field-tested | reference` (whether anyone has run the files in a real repository). A repository's agent reads both before copying anything — `ROUTER.md` prints them per row — and the implementation prompt (`practices/prompt-library/implement-practice.md`) tells it to treat an `untested` reference as a contract to satisfy, not a file to trust. Promotion is unchanged from 0004 §6 and 0005 §3: only a field report moves `reference-status`, only a course confirmation or an adoption moves `status`.

### 3. The KB never applies; the repo navigates, chooses and adapts

Written here so it is not re-litigated: this knowledge base proposes. It writes nothing into any other repository (0001). It does not know, and does not care, whether the consumer is AI SDR or a Laravel platform; it knows the consumer's *facts* (0003). It gives one reference implementation and a contract; the consumer's agent researches its own stack and reports back (0005). Routing a practice means *listing it in the catalogue a repo can see*, not applying it. Working on this repository is never a reason to touch another one.

### 4. The routing gate of 0004 §6 is retired

The sentence "a new practice enters `practices/README.md`'s table and the router only after the previous module's day-0 files have passed Verify in one real repo" no longer applies. What replaces it is the review (step 2c) as the entry condition, and the two visible fields as the honesty mechanism. The acceptance test of 0004 §8 (two bootstraps, field reports) stands as the model for how evidence is produced; it is not a precondition for listing.

### 5. Order within the catalogue

The six practices take their place in the ordering rule of `practices/facts.md` as capability practices: by stage (`when`) first, then by triggering fact. Within the `retrieval` family the day-0 order follows the data: `data-ingestion` (elements and envelope) → `embeddings-and-chunking` (reads them) → `vector-store` (first-user, reads the s7 manifest). `structured-outputs` and `evals` are day-0 on `llm_calls`, after `llm-api-calls`; `memory-and-permissions` is first-user on `multi_turn`, after `context-management`.

## Consequences

- `applies.py --explain retrieval` now lists `data-ingestion`, `embeddings-and-chunking` and `vector-store` (the last deferred to first-user); `llm_calls` adds `structured-outputs` and `evals`; `multi_turn` adds `memory-and-permissions`. Every row says `untested` until a field report arrives — which is true, and which the consumer is told.
- `playbooks/ingest-new-source.md` step 3b: a new practice is created `routed: false` **during the module** and routed in the same publish as its review fixes; `CONVENTIONS.md` §4b and `practices/_template/README.md` say so.
- `ROUTER.md` and `practices/bundles.md` are regenerated; the 2 KB budget of the router is checked by `kb-check.sh` as before (if the router grows past it, the fix is shorter rows, not fewer practices).
- The first field report on any of the six closes the loop 0004 §6 wanted; `practices/adoptions.md` is where it lands.
- Still open and unchanged by this decision: the Laravel two-arm experiment (0005 §10), the AI SDR field report, the interactive read of Martin-observer assertions in the two bootstrap repos.

## Change log

- 2026-10-05 — created, from Martin's restatement of the KB's purpose on 2026-10-04 ("tiene que poder navegar todo este catálogo y saber qué es bueno y aplicable para su propia mejor práctica… no es que vos estás haciendo esto para ya aplicárselo a esos repositorios") and the observation that the 0004 §6 gate had kept six reviewed practices out of the catalogue.
