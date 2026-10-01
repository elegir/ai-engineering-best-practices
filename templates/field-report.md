---
title: "Field report — <practice> in <repo> (<stack>)"
type: source
status: current
date: YYYY-MM-DD
tags: [field-report, <practice>, <stack>]
sources:
  - practices/<practice>/README.md
  - <repo URL or path>@<commit>
supersedes: null
superseded-by: null
---

# Field report — <practice> in <repo>

A field report is the only thing that moves a practice from `untested` to `field-tested` and a variant into the KB (decision 0005 §3, §7). It is written by the agent that adopted the practice, **in the consuming repo's session**, and saved here by the KB as `sources/YYYY-MM-DD-field-report-<repo>-<practice>.md`. Numbers are mandatory; "not counted" fails the report.

## 1. What was adopted

(A bootstrap adopts several practices at once: list them all here, give §2 one table per practice, and report §4 once for the whole run with the per-practice share estimated.)

- Practice: `practices/<practice>/` at `last-reviewed: YYYY-MM-DD` (this is the `verified-against` date of any variant born from this report).
- Repo and commit before / after: `<repo>@<sha>` → `<repo>@<sha>`.
- Stack and runtime: e.g. PHP 8.3 / Laravel 11 / PHP-FPM; Python 3.12 / FastAPI; Node 22.
- Door: existing repo (facts inferred) | blank repo (facts planned). Facts list as confirmed, with sources.
- Who ran it: agent + model, date, session length.

## 2. The contract — assertion by assertion

| # | Assertion (short) | Observer | Result | Evidence (command + exit code, quote, or "handed to Martin") | Negative performed? |
|---|---|---|---|---|---|
| 1 | … | script | pass / fail / n.a. (reason) | … | yes / no |

An assertion marked `n.a.` needs a *technical* reason about this repo, never "not needed".

## 3. Stack-sensitive points applied

Which bullets of `## Stack-sensitive points` applied here and what was done instead of the reference's mechanism. If `stack-notes/<stack>.md` was missing and the agent had to choose a package family alone, say so — that is a finding for the KB.

## 4. Cost (mandatory)

| Measure | Value |
|---|---|
| Tokens spent on this adoption (whole session, from the tool's own counter) | … |
| Wall-clock minutes | … |
| Wrong API / framework calls caught by Verify (hallucinated method, wrong field name, retry layer duplicated…) | … |
| Of those, how many the stack-notes would have prevented | … |

Decision 0005 §8: two adoptions in one stack above 100,000 tokens each → the KB ships that stack's variant proactively.

## 5. What the KB should change

One line per finding, in impact-table vocabulary (`playbooks/ingest-new-source.md` §2b): confirms / refines / new / contradicts / park. A wrong assertion, a missing stack-sensitive point, a placeholder that made no sense, a Verify line no agent can judge — these are the valuable part.

## 6. Files produced in the repo

Paths and a one-line purpose each. These are the candidate variant (`playbooks/adopt-variant.md`).
