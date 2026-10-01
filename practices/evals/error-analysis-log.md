# Error-analysis log — <<product / feature>>

Copy to `<repo>/evals/error-analysis.md`. This file is written **before** any grader or judge exists and is the only place a failure mode is born. Principle: `../../principles/14-evals-and-error-analysis.md` §3.1. Method: Hamel Husain and Shreya Shankar (Lenny's Podcast, 2025-09; Husain's channel, 2026-04 and 2026-07) — digest `../../sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` §3.1.

**Owner (the one person whose taste decides labels):** <<name, role>> — the "benevolent dictator" (Husain): for a legal product a lawyer, for a lesson planner a teacher, "oftentimes it is the product manager". A committee makes labelling "so expensive that you can't do it"; two annotators who disagree "more than if I was flipping a coin" mean the rubric is unclear (Lucas, Nova Escola, 2026-07), not that a vote is needed.

## 1. Open coding — one note per trace

Rules: open the trace in whatever tool shows the full transcript; read it "with your product hat on"; write **one short note about the most upstream error only**, specific enough to categorise later ("did not confirm the call transfer with the user", never "janky"). Keep going past a hundred until new traces stop producing new *kinds* of note (**theoretical saturation**). Do not write criteria before at least twenty of these rows exist (Shankar's *Who validates the validators*, 2024; Yan 2025-04): criteria drift is normal and expected.

| # | Date | Trace id | Most-upstream note (one, specific) | Owner |
|---|---|---|---|---|
| 1 | <<2026-10-01>> | <<trace-8f3a>> | <<did not confirm call transfer with user before transferring>> | <<name>> |
| 2 | <<2026-10-01>> | <<trace-91c0>> | <<quoted a price for a unit that is not in the listing data>> | <<name>> |
| 3 | <<2026-10-01>> | <<trace-a44e>> | <<asked the user for the move-in date twice in one turn>> | <<name>> |
| … | | | | |

Saturation note: <<"after 83 traces the last 20 produced no new kind of note; stopped on 2026-10-01">>

## 2. Axial coding — cluster, name, count

Hand the notes to an LLM using the words *open codes* and *axial codes*; rename anything generic ("capability limitations" is not actionable); map every note back to one category with a prompt that **includes "none of the above"**, so an incomplete taxonomy announces itself; then count. "Basic counting is the most powerful analytical technique in data science" (Husain). Expect a Pareto shape — "80 % of issues… caused by 20 % of failure modes" (Shankar). A rare failure may still come first if its worst case is severe (set the bar by reasoning about the worst case from the user's shoes — Shankar 2026-07).

| Failure mode (axial code) | Definition (one sentence the judge can use) | Count | Share | Worst case |
|---|---|---|---|---|
| <<Unconfirmed handoff>> | <<Agent transfers or ends the call without an explicit confirmation question>> | <<23>> | <<28 %>> | <<user dropped mid-issue>> |
| <<Hallucinated listing data>> | <<A price, unit or amenity not present in the retrieved listing>> | <<17>> | <<20 %>> | <<false promise, lease dispute>> |
| <<Repeated question>> | <<Asks for information already given in the conversation>> | <<9>> | <<11 %>> | <<annoyance>> |
| **None of the above** | notes that fit no row — if this grows, the taxonomy is incomplete | <<4>> | <<5 %>> | — |

## 3. Decision per failure mode

Not every failure needs an eval. "If it's obvious, do it… just fix your application" (Husain); judges only for "the pesky ones that you've described your ideal behavior in your agent prompt, but it's still failing" — "between four and seven" per product (Shankar). Code where code can decide (a format, a length, a JSON shape, a fact checkable against the system of record); a judge where it cannot.

| Failure mode | Decision | Why | Where |
|---|---|---|---|
| <<Unconfirmed handoff>> | **judge** | the prompt already says to confirm; still fails; needs reading the turn | `evals/judges/handoff.md` |
| <<Hallucinated listing data>> | **code grader** | every number can be checked against the listing record | `evals/harness.py` assertion `listing_fact` |
| <<Repeated question>> | **fix** | one prompt change removed it; re-check in the next log round | prompt v<<n>> |
| <<Tone too formal>> | **ignore** | owner's call: not a failure for this audience | — |

## 4. Loop

Error analysis is not a one-off. After each fix, re-read a sample (the trace read twice yields what the first pass missed — Shankar's "*matters*" example); when the production sample's judge rates move, open the failing traces and add rows here; when a new failure mode is proposed by the agent (annotation-ui-brief.md), it enters as a *proposal* until the owner confirms it. Last loop: <<date>>.
