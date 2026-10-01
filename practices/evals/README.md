---
title: "Practice — evals and error analysis: a human reads traces first, binary graders one per failure mode, judges calibrated like classifiers, a 20-task regression suite reported as pass^k, judges gating every change and a production sample on a cadence"
type: practice
status: draft            # draft until principle 14 is confirmed against LIDR session 5 (2026-11-12) and a real repo passes Verify
date: 2026-10-01
last-reviewed: 2026-10-01
tags: [evals, error-analysis, open-coding, llm-as-judge, judge-calibration, pass-k, regression-suite, annotation, s5]
kind: capability
applies-when: "llm_calls"
when: day-0            # the error-analysis log, the first 20-task regression set and a code grader are day-0 ("evals get harder to build the longer you wait" — Anthropic 2026-01); judge calibration (4), the production sample (7, second half) and the weekly trace reading (8, ongoing) are first-user, stated inside eval-policy.md
reference-status: untested   # decision 0005 §3; only a field report moves it
routed: false          # unrouted until the routing gate of decision 0004 §6 (the previous module's day-0 files must pass Verify in one real repo); no row in practices/README.md, absent from ROUTER.md
principle: principles/14-evals-and-error-analysis.md
sources:
  - sources/2026-10-01-s05-context-memory-permissions-evals-digest.md
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://hamel.dev/blog/posts/evals/index.html
  - https://eugeneyan.com/writing/llm-evaluators/
  - https://eugeneyan.com/writing/eval-process/
  - https://www.promptfoo.dev/docs/intro/
  - https://deepeval.com/docs/getting-started
supersedes: null
superseded-by: null
---

# Evals and error analysis

## Solves
The product calls a model and one of these symptoms appears: "the agent feels worse" after a prompt, model or tool change and nobody can say on which inputs; a dashboard shows a quality score (a 0–1 from a tool, a 3.7 out of 5) that nobody can explain or reproduce; judge prompts were written before anyone had read the traces, so they grade things that never go wrong and miss the thing that does; a judge is reported as "agreeing 90 %" with a human on a set where 90 % of outputs are fine, so a judge that always says "pass" would score the same; a scenario that passes four runs out of five ships because the mean looked good; a valid solution fails the eval because it took a different tool path; failures are visible only as a number, never as a trace a person has read; the eval tool's default threshold decides a merge; a coding agent was told "evaluate my app" and returned a confident list of made-up priorities.

## Applies when
- The fact `llm_calls` holds (`../facts.md`): the product itself calls a model at runtime. Every LLM feature has failure modes that only its owner can name, so the error-analysis log, the first regression tasks and at least one code grader are day-0 artifacts. Judge calibration (assertion 4) and the production sample (assertion 7, second half) attach when the product has users — `eval-policy.md` states the stage per item.

## Does not apply when
- The only model in the picture is the coding agent working on the repo. The harness evals of `../verification/harness-evals.md` (three tasks, run after a harness change) cover that; this folder is for the *product's* model calls.
- The product's model output is never graded against a user-visible quality (an internal batch classification with a labelled ground truth is a plain classifier eval — precision/recall in the normal way, no judge needed).
- Guardrails at runtime (a check that blocks a reply or a tool call) are `../structured-outputs/guardrail-policy.md`; the calibration rules here apply to the judge tier of a guardrail, the placement rules there do not apply here (Yan's evaluator-offline vs guardrail-online split).
- Memory-specific eval cases (cross-session recall, contradiction, forgetting) are `../memory-and-permissions/memory-eval.md`, run through this folder's harness.
- Prompt optimisation as the *improve* step (GEPA, DSPy, Uber's auto-tuner) and observability tooling as the datastore are parked for sessions 16 and 15 (`../../sources/scan-log.md`).

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `error-analysis-log.md` | `<repo>/evals/error-analysis.md` | Open-coding log (date · trace id · most-upstream note · owner), axial-code table with counts and a "none of the above" row, saturation note, decision per failure mode (fix / code grader / judge / ignore) |
| `eval_harness.py` | `<repo>/evals/harness.py` | Python reference: tasks in JSONL (input, expected outcome or assertions, reference solution); isolated trial runner; binary graders — code assertions and an LLM judge returning `pass` / `fail` / `unknown` with a reasoning field first; k trials per task with pass^k and the worst case (the `credit` column is the mean partial credit, a diagnostic for multi-part tasks — never the reported number); a judge-calibration check over a labelled held-out set printing TPR, TNR, Cohen's κ and the confusion matrix, refusing agreement alone; a judge file is refused before any call when its header has no calibration record, placeholders, agreement only, rates below the floors or a placeholder model id; judge model and prompt version recorded with the run; `--demo` runs every branch offline |
| `judge-prompt-template.md` | `<repo>/evals/judges/<failure-mode>.md` | One judge per failure mode: definition from the log, pass/fail criteria, two contrasting examples, reasoning before verdict, the `unknown` out; header with model, version, calibration date, TPR/TNR |
| `eval-policy.md` | `<repo>/docs/eval-policy.md` | Owner; which failure modes have graders and why; capability vs regression suites; k and the pass^k floor; CI gate rule; production sample rate and stability check; cadence; the tool used as runner and datastore, never as judge |
| `annotation-ui-brief.md` | run as a prompt | Brief for the coding agent to build a review app from JSONL/CSV: viewer, in-situ notes, filters, cluster sampling, progress view, label export; the agent maintains the taxonomy and proposes instances, never adds failure modes alone |
| `stack-notes/python.md`, `stack-notes/php-laravel.md` | read | Python: pytest as runner (promptfoo/DeepEval optional; own graders), Langfuse/LangSmith as datastore; Laravel: PHPUnit/Pest data providers over the same JSONL, a queued job for the production sample, judge calls through the app's LLM client — under twenty lines, no code (decision 0005 §5) |

## Reference implementation

`eval_harness.py`: one module implementing assertions 3, 4, 5, 6 (the partial-credit half) and 7 (the run record) for Python, with the judge call left as a hook (`_real_judge()`) that must go through the repo's one LLM client module (`../llm-api-calls/`) so that judge calls are logged and cost-capped like every other call. It keeps tasks as data (`tasks.jsonl`), creates a clean environment per trial, grades the outcome (environment state) before the output text, parses the judge's answer into a typed `{reasoning, verdict}` object with `unknown` as the out, reports pass@k and pass^k with the worst case per task, flags a task whose reference solution fails its own graders as *broken* rather than as an agent failure, and computes TPR, TNR, Cohen's κ and the 2×2 matrix by hand for a judge against a labelled held-out set — refusing to ship a judge below the floors, refusing to *load* a judge whose header carries no calibration record (date, held-out set, TPR+TNR or κ), placeholders or a placeholder model id, and refusing to run a judge whose recorded model differs from the configured one (assertion 4's negatives, enforced by the script; only `--calibrate` loads a judge without a record, because it is producing one). The report's `credit` column is the mean partial credit — a diagnostic for multi-part tasks, not the reported number, which is pass^k. **Python idioms, not required** (decision 0005 §3): dataclasses, the JSONL loader, pydantic for the verdict. Any stack satisfies the contract by keeping tasks as data, isolating trials, returning binary-with-unknown verdicts, reporting pass^k, and keeping a calibration record next to each judge prompt. Other stacks: `stack-notes/<stack>.md` and, once a real repo passes Verify, `variants/<stack>/`.

## Stack-sensitive points

- **Tasks are data and graders are functions**, so the harness is language-neutral; what differs is the **test runner** that wraps it (pytest, PHPUnit/Pest, a plain CLI in CI) and how it reports a failed scenario.
- **Where the production sample runs**: a long-lived process can grade a sample on a timer; a request-scoped runtime (PHP-FPM, serverless) needs a cron or a queued job that pulls the day's traces from the datastore and calls the same graders.
- **Judge calls go through the repo's own LLM client** (one module instantiates the SDK — `../llm-api-calls/README.md` assertion 1) so they appear in the usage log with their own route and cost cap; a judge is a model call like any other.
- **κ and a confusion matrix need no library**; the reference computes them by hand so the calibration record does not depend on a package's definition of "agreement".
- **A clean environment per trial** means something different per product: a fresh temp directory and database for an agent that acts on files, a reset fixture for a chat feature, a sandbox reset for a coding agent — the cost of that reset bounds how many trials you can afford.

## Adapt
- `eval_harness.py`: set `<<JUDGE_MODEL>>` (one pinned model id; the registry of `../llm-gateway/model-registry.md` if the repo has one) and `<<JUDGE_CLIENT_IMPORT>>`; replace `make_env()` and `run_agent()` with the product's setup and entry point; keep `grade()` reading the outcome from `env["state"]` where the product has one; keep the floors as the values `eval-policy.md` states.
- `error-analysis-log.md`: delete the example rows after the first twenty real ones; the "none of the above" row is never deleted.
- `judge-prompt-template.md`: one copy per failure mode that survived the decision column of the log; the header fields are read by the harness — keep their names.
- `eval-policy.md`: fill the owner first; delete the suite you do not have yet (capability evals come after the regression suite exists); the production-sample section is first-user and may say "not yet" with a date.
- `annotation-ui-brief.md`: run once; keep the app in `<repo>/evals/review/`; re-run the brief when the taxonomy changes shape.
- Stacks: Python shown; PHP/Laravel in `stack-notes/php-laravel.md`; TypeScript is not a promised stack (decision 0005 §4) — implement from the contract with `../prompt-library/implement-practice.md` until a field-tested variant exists.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who judges it: `script` (a command's exit code), `agent` (observed in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's library. Stack-specific commands live only under *Example commands (Python)*. Assertions 1–3 and 5–6 are day-0; 4, the second half of 7 and 8 (an ongoing duty once there are users) are first-user (`eval-policy.md`).

1. An error-analysis log exists with at least twenty open-coded traces (date, trace id, one specific most-upstream note), an axial-code table with counts, and a decision per failure mode — observer: Martin — negative: a grader or judge whose failure mode has no row in the log
2. One named person owns labels and rubrics, and no judge criteria were written before that person had read at least twenty outputs — observer: Martin — negative: a rubric dated before the first twenty log entries, or two label owners with no reconciliation record
3. Every automated grader returns a binary verdict (or an enumerated one with an explicit `unknown`) for exactly one failure mode; any 0–1 or Likert score from a tool is mapped to a verdict by a documented, calibrated threshold before use — observer: script — negative: a numeric score averaged into one quality number, or a tool's default threshold gating a merge
4. Every LLM judge has a calibration record — held-out labelled set, TPR and TNR (or κ), confusion matrix, judge model and prompt version — and the judge in use matches it — observer: script — negative: a judge with no record, a record reporting agreement only, or a model changed since calibration
5. The regression suite holds at least twenty tasks from real failures, each with a reference solution that passes, each trial from a clean environment, each task run at least five times, and the report shows pass^k and the worst case per task — observer: script — negative: a mean hiding a failed run, a task at 0 % with no reference solution, or shared state between trials — framework: beats
6. Graders check the outcome or the output, not an exact tool sequence, and give partial credit on multi-part tasks — observer: Martin — negative: a valid solution failed because the path differed
7. The suite runs in CI on every change to a prompt, schema, tool set, model or eval policy, and a production sample is graded on the policy's cadence with its daily rate recorded and stable — stable meaning the last seven daily rates lie within ten points of their median, the window and tolerance being the numbers written in the eval policy — observer: script — negative: a merged change with no run, judges that never ran on production data, or a rate series outside the tolerance
8. Failed trials are readable in a viewer with annotation, and one trace per week has been read and logged — observer: Martin — negative: failures visible only as a number, or a month with no trace read

**Example commands (Python):** `python3 eval_harness.py --tasks evals/tasks.jsonl --trials 5 --report`; `python3 eval_harness.py --calibrate evals/judges/handoff.md --labels evals/labels/handoff.jsonl` (prints TPR, TNR, κ, matrix; non-zero below the policy floor); `pytest evals/`; `python3 eval_harness.py --demo` (offline, every branch, no placeholders needed).

## Sources
`sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` §3.1–3.5 and impact table §6 (rows 1–11, 13–17, 19, 21–23); primary texts listed in `principles/14-evals-and-error-analysis.md` §6. Vendor pages to re-read directly before promoting to `current`: the DeepEval quickstart (its `GEval` threshold and `JevEval` shape are dated 2026-10-01) and the promptfoo intro.

## Change log

- 2026-10-01 — created from the session-5 market scan digest (draft, **unrouted** per decision 0004 §6: no row in `practices/README.md`, absent from `ROUTER.md` until the previous module's day-0 files pass Verify in a real repo). Reference `eval_harness.py` run with `--demo` (offline, fake agent and fake judge, no network) on 2026-10-01: code grader pass and outcome check → pass^k; a task that passes 4 of 5 trials → pass@k `True`, pass^k `False`, worst case printed; a task whose reference solution fails its own grader → flagged `BROKEN TASK`, not counted against the agent; judge `pass` / `fail` / `unknown` verdicts with reasoning first; an unparseable judge answer → `unknown`; partial credit 0.67 on a three-part task; a judge file whose header names a different model than the configured one → refused; calibration over 10 labelled rows → TP 4, TN 3, FP 1, FN 1, unknown 1, TPR 0.80, TNR 0.75, κ 0.55 (checked by hand against the marginals) → below the κ floor, refused; an always-pass judge on a 10 %-failure set → agreement 0.90, TPR 0.00, κ 0.00. No field report yet.
- 2026-10-01 (review) — clean-context review: `JudgeSpec.load` now enforces assertion 4 before any call (requires `calibrated`, `calibration-set` and TPR+TNR or κ; refuses `<<…>>` placeholders, a placeholder model id, agreement-only records and values below the floors; `--calibrate` loads without a record because it produces one); partial credit counts failed checks instead of parsing the reason string; without pydantic a judged task still runs its code graders and returns `unknown` for the judge; the report column `mean` renamed `credit` (diagnostic, not the number). "Reason first, then discard" re-attributed to Anthropic's docs page. Verify 7 defines "stable"; assertion 8 classified first-user. `--demo` re-run 2026-10-01 after the changes: all earlier branches as above, plus five judge files refused before any call — no record, placeholders, agreement only, TPR 0.95 / TNR 0.40 below floor, `<<JUDGE_MODEL>>` — and the no-record file accepted only with `require_record=False`; the multi-part task's `credit` 0.67 asserted from counts.
