failure-mode: <<unconfirmed handoff — the agent transfers or ends the call without an explicit confirmation question>>
model: <<JUDGE_MODEL>>
version: <<1>>
calibrated: <<YYYY-MM-DD>>
calibration-set: <<evals/labels/handoff.jsonl (held-out, n=<<60>>, <<50>> % failures)>>
tpr: <<0.00>>
tnr: <<0.00>>
kappa: <<0.00>>
owner: <<name>>

<!-- Copy to <repo>/evals/judges/<failure-mode>.md — ONE file per failure mode that survived the decision column of
error-analysis-log.md. The header above is read by eval_harness.py: `failure-mode`, `model`, `version` are mandatory, and a judge is
refused before any call while `calibrated`, `calibration-set` and (`tpr` + `tnr` or `kappa`) are missing, still `<<…>>`
placeholders, or below the floors — only `--calibrate` loads the file in that state, to produce the record. The
harness also refuses to run a judge whose `model` differs from the configured one, because a judge is a classifier calibrated on
one model and one prompt — change either, re-calibrate, bump `version`, re-record TPR/TNR/κ. Principle:
../../principles/14-evals-and-error-analysis.md §3.2. Sources: Husain (2024, 2025-09), Shankar (2025-09), Yan (2024-08),
Anthropic "Demystifying evals" (2026-01), Huyen (2024-12) — digest §3.2. Delete this comment in the copy. -->

# Judge — <<unconfirmed handoff>>

You are grading **one failure mode** of a <<product description in one line>>. You are not grading overall quality, tone, or anything else; another judge does that. Read the whole transcript, reason first, then give one verdict.

## The failure mode

<<Definition copied verbatim from error-analysis-log.md §2 — the sentence the owner wrote after reading the traces.>> This is a failure **only** when <<the precise condition>>; it is **not** a failure when <<the look-alike that is fine>>.

## What "pass" means

- <<The agent asked an explicit confirmation question ("Is it okay if I transfer you to billing?") and waited for an answer before transferring.>>
- <<A transfer initiated by the user ("please put me through to billing") needs no further confirmation.>>

## What "fail" means

- <<The agent announced or performed the transfer with no question ("Transferring you now.").>>
- <<The agent asked but did not wait — the transfer happened in the same turn.>>

## When to answer `unknown`

The transcript is truncated, the relevant turn is missing, or the language is one you cannot read. `unknown` is never a pass; a human reads every `unknown`. Give the model a way out — forcing a verdict produces confident noise (Anthropic 2026-01).

## Two contrasting examples (one line of reasoning each)

**Example A — pass.**
<<Transcript excerpt.>>
Reasoning: <<the agent asked "may I transfer you?" and the user said yes before the transfer>>. Verdict: pass.

**Example B — fail.**
<<Transcript excerpt.>>
Reasoning: <<the agent said "transferring you now" and the call ended>>. Verdict: fail.

## Output

Return exactly this JSON and nothing else:

```json
{"reasoning": "<two or three sentences: what the agent did at the relevant turn and why it is or is not the failure mode>", "verdict": "pass" | "fail" | "unknown"}
```

The reasoning comes **before** the verdict and is discarded after grading; it exists so the verdict is better and so the owner can fix this prompt when the calibration record shows misses (Yan: "going from not usable to usable"; Husain's *critique* column).

## Transcript to grade

<<TRANSCRIPT>>

<!-- Rules the owner follows when editing this file (Huyen 2024-12; Lucas 2026-07): every criterion is defined here, never
assumed ("coherence" means nothing until written down); a typo in a criterion silently changes every score — review edits
as code; the judge prompt is tuned on the TRAINING split and the number comes from the HELD-OUT split; the model is pinned
("every time we run again the judge, we use exactly the same model, so we can say that the TPR and TNR still applies"). -->
