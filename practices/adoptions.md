---
title: "Adoptions — every time a real repo implemented a practice from this KB, with its field report and cost"
type: template
status: current
date: 2026-09-30
last-reviewed: 2026-09-30
tags: [adoptions, field-report, evidence, promotion]
sources:
  - decisions/0004-day-one-for-blank-and-existing-repos.md
  - decisions/0005-contract-first-practices-and-stacks.md
supersedes: null
superseded-by: null
---

# Adoptions

This table is the KB's evidence that any of its copyable material works. One row per adoption (one practice in one repo), added by `playbooks/adopt-variant.md` step 6 from a field report (`templates/field-report.md`). A practice with no row here is `reference-status: untested` whatever its README says; the router reads this. The flow is: field report → ingest (impact table) → row here → status change on the practice or variant.

| Date | Practice | Repo | Stack | Door | Outcome (assertions pass / total; n.a. with reason) | Tokens | Minutes | Errors caught by Verify | Report |
|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | *no adoption recorded yet (2026-09-30); first expected: AI SDR, `llm-api-calls` (steps 4–5 of the 2026-09-28 test), then the two-arm Laravel experiment of decision 0005 §10* | — | — | — | — |

## Reading the numbers

- **Tokens / minutes** per adoption are what decision 0005 §8 compares against the 100,000-token threshold: two adoptions in one stack above it mean the KB ships that stack's variant for every routed practice instead of relying on the implementation prompt.
- **Errors caught by Verify** is the count of wrong API or framework calls the contract detected (hallucinated method, wrong field, duplicated retry layer). High numbers with an absent `stack-notes/<stack>.md` are the signal to write the notes; high numbers with the notes present mean the notes are wrong.
- An adoption whose report has no numbers is not recorded here; it is sent back.

## Change log

- 2026-09-30 — created, empty (decision 0005 §7; first debate attack 17: "the KB never measures its own usefulness").
