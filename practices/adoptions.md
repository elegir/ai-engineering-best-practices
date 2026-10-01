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

This table is the KB's evidence that any of its copyable material works. One row per adoption (one practice in one repo), added by `playbooks/adopt-variant.md` step 6 from a field report (`templates/field-report.md`). A practice with no row here must have `reference-status: untested` in its README (the router reads the README; `playbooks/adopt-variant.md` is the only step that changes it). The flow is: field report → ingest (impact table) → row here → status change on the practice or variant.

| Date | Practice | Repo | Stack | Door | Outcome (assertions pass / total; n.a. with reason) | Tokens | Minutes | Errors caught by Verify | Report |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-01 | `hooks-and-guards` | shape-b-pipeline (sandbox acceptance repo, newsflow) | Python 3.11 | blank | 6/7 pass with negatives; 7 n.a. (lefthook, gitleaks not installable) | ≈33k of 268k (8 practices) | 13 (whole bootstrap) | 0 | `sources/2026-10-01-field-report-shape-b-bootstrap.md` |
| 2026-10-01 | `verification` | shape-b-pipeline | Python 3.11 | blank | 1, 2, 6 pass with negatives; 3, 4 handed to Martin; 5 trivially | ≈33k | 13 | 1 (missing `httpx` under the tool interpreter) | same |
| 2026-10-01 | `agent-entry-file` | shape-b-pipeline | Python 3.11 | blank | 1, 4, 5, 6 pass; 2, 3 need an interactive session | ≈33k | 13 | 0 | same |
| 2026-10-01 | `context-docs-skeleton` | shape-b-pipeline | Python 3.11 | blank | 4, 5 pass; 1–3 need an interactive session | ≈33k | 13 | 1 (index vs deleted doc) | same |
| 2026-10-01 | `security-baseline` (core + full) | shape-b-pipeline | Python 3.11 | blank | 2, 9 pass; 1, 3, 5, 8 n.a.; 4, 6, 7 handed to Martin | ≈33k | 13 | 1 (ruff S106) | same |
| 2026-10-01 | `prompt-library` | shape-b-pipeline | Python 3.11 | blank | 5 pass; 1–4 handed to Martin | ≈33k | 13 | 0 | same |
| 2026-10-01 | `spec-driven` | shape-b-pipeline | Python 3.11 | blank | 4 pass (vacuous); 1–3 handed to Martin | ≈33k | 13 | 0 | same |
| 2026-10-01 | `llm-api-calls` | shape-b-pipeline | Python 3.11 | blank | 1, 2, 4, 6, 9 pass; 3 n.a.; 5, 7 handed; **8 fail** (no eval yet) | ≈33k | 13 | 0 (SDK path not executed) | same |

## Reading the numbers

- **Tokens / minutes** per adoption are what decision 0005 §8 compares against the 100,000-token threshold: two adoptions in one stack above it mean the KB ships that stack's variant for every routed practice instead of relying on the implementation prompt.
- **Errors caught by Verify** is the count of wrong API or framework calls the contract detected (hallucinated method, wrong field, duplicated retry layer). High numbers with an absent `stack-notes/<stack>.md` are the signal to write the notes; high numbers with the notes present mean the notes are wrong.
- An adoption whose report has no numbers is not recorded here; it is sent back.

## Change log

- 2026-10-01 — first eight rows from the shape-B bootstrap (decision 0004 §8, first arm); `hooks-and-guards` promoted to `reference-status: field-tested` (every script/agent assertion passed with its negative; 7 n.a. for missing tools). The others stay `untested` until their `Martin`/`agent` assertions are judged in an interactive session or, for `llm-api-calls`, an eval exists.
- 2026-09-30 — created, empty (decision 0005 §7; first debate attack 17: "the KB never measures its own usefulness").
