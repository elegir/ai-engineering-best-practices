---
title: "Domain — product management with agents (specs, discovery, definition of done)"
type: domain
status: draft
date: 2026-09-09
last-reviewed: 2026-09-09
domains: [product]
tags: [product, prd, user-stories, discovery, functional-docs]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Product management with agents

## What is different here

The agnostic practices assume a spec exists. This domain is about *producing* it: turning an idea into user stories with acceptance criteria an agent can execute and a test can verify, running discovery with an agent as the interviewer, and keeping functional documentation readable by non-technical people — the workshop's point that a data model or a workflow written in plain language lets product people ask the assistant instead of interrupting developers.

## How the agnostic layer applies

| Agnostic practice | In product terms | Extra constraint |
|---|---|---|
| `practices/spec-driven/` + `templates/open-spec-user-story.md` | The PRD is the input; stories are the unit; acceptance criteria name their tests | A story that needs "and" is two stories; out-of-scope is explicit |
| `practices/prompt-library/ask-the-expert.md` | Discovery interview: the agent asks the questions a senior PM forgets (roles, edge cases, compliance, i18n, scale) | Answers are recorded in the spec's "Clarifications resolved" |
| `practices/context-docs-skeleton/docs/workflow.md` | The definition of done has a product half (criteria met, functional doc updated) and a technical half | Product signs off on criteria, not on code |
| `principles/08-model-selection.md` | Discovery, PRDs and stories run on the mid tier (fast iteration); architecture on the top tier | |
| `practices/context-docs-skeleton/docs/data-model.md` | Natural-language model + Mermaid = the product team's reference | Non-technical readability is a review criterion |

## Vertical-specific practices (to create)

- `domains/product/practices/prd-to-stories/` — PRD template that decomposes into the open-spec story format; a prompt that turns a PRD into atomic stories with testable criteria and flags untestable ones.
- `domains/product/practices/discovery-interview/` — the ask-the-expert prompt specialized for product discovery (jobs-to-be-done, user roles, success metrics, risks).
- `domains/product/practices/functional-docs/` — Confluence-style functional documentation skeleton generated from specs and kept in the repo.

## Open questions this domain must answer before becoming `current`

- Where product specs live when the product spans several repos (OpenSpec "Stores" is beta) — one `specs/` repo vs per-repo.
- How to measure spec quality (rework rate, criteria that needed rewriting during implementation).
- Which metrics belong in the definition of done from the product side (adoption/telemetry hooks).

## Sources

- LIDR workshop: workflow deliverables (PRD/user story → ticket → code → tests → report → docs), functional documentation for non-technical readers, model table for discovery/PRD/stories, ask-the-expert — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.3, §3.9.

## Change log

- 2026-09-09 — created (draft).
