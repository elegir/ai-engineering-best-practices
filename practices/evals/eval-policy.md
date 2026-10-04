# Eval policy — <<product>>

Copy to `<repo>/docs/eval-policy.md`; one per product; reviewed as code. It names who owns quality, what is measured and how, and the operating rules that keep the numbers meaningful. Principle: `../../principles/14-evals-and-error-analysis.md`. Sources: Anthropic *Demystifying evals for AI agents* (2026-01-09) and *Define success criteria* (read 2026-10-01); Husain (2024; 2025-09); Lucas, Nova Escola (2026-07); Shankar (2026-07); Yan (2024-08; 2025-04); DeepEval and promptfoo pages (read 2026-10-01) — digest `../../sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` §3.1–3.5.

## 1. Ownership

| Role | Who | Does |
|---|---|---|
| Label and rubric owner ("benevolent dictator") | <<name>> | reads traces, writes the log, names failure modes, decides every label; the only person whose taste counts |
| Eval infrastructure | <<name>> | the harness, the datastore, CI wiring, the viewer |
| Task contributors | <<product, ops, support>> | add regression tasks from real failures as PRs — "let them" (Anthropic 2026-01) |

Cross-functional at DoorDash (ops set the bar, product writes rubrics, ops annotate, engineering provides APIs and judges — 2026-08) and at Anthropic (an evals team owns infrastructure, domain experts contribute most tasks). For a solo operator all three rows are Martin; the point is that the *roles* stay distinct in the files.

## 2. What has a grader, and why

Only failure modes with a row in `evals/error-analysis.md` §3 marked **code grader** or **judge**. Four to seven judges is the expected ceiling (Shankar); more means the log is being skipped.

| Failure mode | Grader | Kind | Stage | Calibration record |
|---|---|---|---|---|
| <<Hallucinated listing data>> | `listing_fact` | code (state check against the listing record) | day-0 | n/a (deterministic) |
| <<Unconfirmed handoff>> | `evals/judges/handoff.md` v<<1>> | judge, binary + `unknown` | first-user | TPR <<>> TNR <<>> κ <<>> on <<date>>, n=<<>> |

Rules: binary per failure mode (Husain: a 1–5 scale is "a weasel way of not making a decision"; Shankar: "anti-Likert"); pairwise comparison only for a *subjective* criterion where both answers may be acceptable (Yan); a five-class scale only for a *graded decision* (`../structured-outputs/decision-vs-generation.md` rule 4); **a tool's 0–1 score with a default threshold (DeepEval's `GEval` at 0.5, read 2026-10-01) is a Likert scale in disguise until its threshold has been checked against labels** — map it to a verdict with a documented threshold or do not use it as a gate. The eval tool is the **runner and datastore** (test cases, traces, scores, datasets) — never the judge; the judge prompts and calibration records live in this repo. Lucas's complaint stands as the rule: the tool "assume[s] your judge is calibrated, so they go straight to give you a score. And I don't want a score."

## 3. Suites

| Suite | Purpose | Size | Target | Graduation |
|---|---|---|---|---|
| **Regression** | catch what used to work and broke | ≥ 20 tasks from real failures, grows from production | pass^k ≈ 100 % (floor: <<1.0>>) | a task is retired only when its feature is |
| **Capability** | what the product cannot do yet | <<n>> tasks | starts low, rises with work | moves to regression once it passes reliably |

**Lineage (added 2026-10-01, s6).** The golden set carries lineage — source trace or document, version, date, who labelled it — and passes the same gates as product data (contract, quality, AI approval, PII scrub: `../data-ingestion/audit-checklist.md` §5), because "evaluation data sets need lineage and quality controls. Otherwise, your evaluation numbers become just acting theater" (Gambill, 2026-06); an erasure request reaches the eval set too (`../data-ingestion/privacy-compliance-checklist.md` §5).

**Retrieval stage (added 2026-10-04, s7).** When `retrieval` holds, the regression suite includes a retrieval set: questions with verbatim excerpts from the corpus (generated and filtered, Chroma 2024-07; or real queries once they exist), graded deterministically on token-level recall, precision and IoU and on recall of the source chunk — no judge; run on every chunker, embedding-model or index change. nDCG-style metrics require every new result to be judged or it counts as irrelevant (Radu Gheorghe, Vespa, 2026-08). Harness and set-building rules: `../embeddings-and-chunking/chunk-eval-harness.md`.

Task rules (Anthropic 2026-01): a task is unambiguous — "two domain experts would independently reach the same pass/fail verdict"; every task has a **reference solution** that passes (a 0 % task is "most often a signal of a broken task"); the set is **balanced** (should-act and should-not-act cases); every **trial is isolated** (a clean environment; no shared files, databases or git history); graders check the **outcome or output, not the path** (an exact tool sequence makes "overly brittle tests"); **partial credit** on multi-part tasks; a suite at 100 % "provides no signal for improvement" — add capability tasks.

**k and the metric.** Every task runs **k = <<5>>** trials (≥ 5; `../llm-api-calls/failure-modes-and-mitigations.md` row 12). The reported metric is **pass^k** — all k trials pass — per task, with the worst case shown; pass@k (any one passes) is reported beside it for capability work only. 0.75 per trial over three trials is 42 % (Anthropic): the mean is not the product's reliability.

## 4. Gates and cadence

| When | What runs | Rule |
|---|---|---|
| Every change to a prompt, schema, tool set, model, judge or this policy | regression suite, k trials | merge blocked below the pass^k floor; a `BROKEN TASK` flag blocks until the task is fixed |
| Daily (first-user) | judges over a **production sample** at <<rate>> % | the rate is raised until the daily series is stable — Lucas started at 2 % ("very erratic"), stabilised "around 80 %"; record the series. **Stable means:** the last <<7>> daily rates lie within <<10>> points of their median (the harness's production job checks this and fails otherwise — Verify 7) |
| Weekly | one person reads <<n>> failed or sampled transcripts and logs them | "we do not take eval scores at face value until someone… reads some transcripts" (Anthropic) |
| On every judge or model change | re-calibrate on the held-out split; bump `version` | the judge in use must match its record (`eval_harness.py` refuses otherwise) |
| Quarterly | re-read the log; retire fixed failure modes; add new ones from "none of the above" | |

A judge never gates a send, a payment or a publish alone (`../../principles/05-verification-loops.md`); it gates a *merge* beside deterministic graders. The production sample is monitoring, not a unit test (s3 rule): page on deterministic expectations, read judge trends.

## 5. Closing the loop without a human (at-scale, optional)

Permitted only when (Uber, 2026-07): a **human-labelled golden set** exists on a representative cut with an objective guideline; the automated change (prompt or config rewrite) is **benchmarked against the golden set and registered only if it passes**; deterministic gates follow the model; rollback is one step. Prompt optimisation tooling is parked for session 16. Default here: <<not enabled>>.

## 6. Datastore and tools

| Need | Tool here | Note |
|---|---|---|
| Traces, test sets, scores, datasets | <<Langfuse / LangSmith / a table>> | API-first so the viewer and the harness read the same rows (DoorDash: "very stable APIs") |
| Runner | <<pytest / promptfoo / DeepEval>> | own graders; library thresholds disabled or calibrated |
| Viewer and annotation | `evals/review/` built from `annotation-ui-brief.md` | hours, not weeks (Husain 2024; Nurture Boss) |

Last reviewed: <<date>> by <<owner>>.
