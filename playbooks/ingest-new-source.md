---
title: "Playbook — ingest a new source (workshop, article, talk, experiment) into the knowledge base"
type: playbook
status: current
date: 2026-09-08
last-reviewed: 2026-09-24
tags: [ingest, sources, principles, index]
sources:
  - CONVENTIONS.md
supersedes: null
superseded-by: null
---

# Ingest a new source

**Input.** Raw material: a transcript, notes, a URL, a PDF, a recording summary, or Martin's own account of an experiment ("I tried rtk for a week; here is what happened"). Also valid: **a lesson from an agent failure** in one of the repos — those are sources too.

**Output.** A dated `sources/` entry (long, digested, English) **containing an impact table** (step 2b), verbatim raw material under `sources/raw/` when it exists, updated `principles/` and `practices/` only where the table says so, possibly a `decisions/` entry, and an `INDEX.md` line. One commit. This is the single procedure for *any* external information — a workshop, an article, a market scan, a lesson from an agent failure — so that every improvement to the KB is traceable to a source and a verdict.

## Steps

1. **Capture everything first.** Save raw material verbatim under `sources/raw/YYYY-MM-DD-slug/` (transcripts, page text, exported notes). For YouTube videos, extract transcripts (Apify `johnvc/YoutubeTranscripts` or similar) and save one file per video with a header noting title, channel, upload date, duration, language, extraction date. For web pages, save the full text. Note anything that could **not** be captured (videos without captions, images, PDFs) so the gap is visible.

2. **Write the source entry** from `templates/source-entry.md`, named `sources/YYYY-MM-DD-slug.md` with the *event* date. Follow `CONVENTIONS.md` §3: context; one-paragraph summary; detailed digest section by section in prose (explain terms; keep numbers, tool names, exact commands); claims worth checking; what is contested (including vendor interest); implications for Martin's repos, by repo; actions; raw-notes appendix pointing to `sources/raw/`.

2b. **Impact assessment — mandatory, and the reason this playbook exists.** The goal is to *improve* the knowledge base, not to append everything the source said. Before touching any principle or practice, build an **impact table** in the source entry (section "Impact assessment", after "What is contested"): one row per finding, with the columns *finding · where the KB stands today (file and section, or "absent") · verdict · action*. Verdicts, exactly these six:

   | Verdict | Meaning | What you do |
   |---|---|---|
   | **confirms** | The KB already says this | Add a dated change-log line "reviewed against `sources/…`; no change" to the principle; bump `last-reviewed`. Do not restate it. |
   | **refines** | The KB says it, but the source adds a sharper rule, a number, a mechanism or a counter-case | Edit the specific sentence or add one; change-log line says what changed and why. |
   | **new** | Nothing in the KB covers it and it is applicable | New section, principle or practice file. A principle change without a practice change is incomplete unless the finding is purely conceptual. |
   | **contradicts** | The source shows existing text is wrong or stale | Never overwrite silently: add the new position with its evidence, mark the old text superseded in place or set the file's status; change-log line. If the *source* is the one that is wrong (check against primary texts), record that in "Claims worth checking" and adopt nothing. |
   | **skip** | Opinion, hype, dated numbers, vendor marketing, or true-but-not-actionable | One line in the table saying why; nothing else. |
   | **park** | Belongs to another module or a principle that does not exist yet | Note the target module in the table and in `sources/scan-log.md`; nothing else now. |

   Skepticism rules while assigning verdicts: (a) *who benefits* — a vendor recommending its own protocol, product or model gets "refines/new" only for the mechanism, never for the preference; (b) *how old* — numbers and model names older than ~12 months are historical evidence, not current guidance; (c) *primary beats secondary* — when a corporate explainer or a community video disagrees with the specification or the paper, the spec wins and the disagreement is logged; (d) *one incident is one incident* — a single anecdote becomes "avoid X", never "vendor A is worse than vendor B"; (e) *already-known is the normal case* — expect a third or more of any good source to be "confirms"; recording that is the point, it is how the KB gains authority. Finish the table with a one-paragraph "net effect" (what was created, what was refined, what was parked), and then do only what the table says.

3. **Update principles.** For each topic the source touches, open the matching `principles/NN-*.md`:
   - If the source *confirms* the principle: add a change-log line "YYYY-MM-DD — reviewed against `sources/…`; no change" and bump `last-reviewed`.
   - If it *refines* it: edit the relevant section, cite the source, add a change-log line saying what changed and why.
   - If it *contradicts* it: do not overwrite. Add the new position with its evidence, mark the old text "(superseded 2026-…, see change log)" or, if fully obsolete, set the file to `status: superseded` and create the replacement.
   - If no principle exists for the topic: create one from `templates/principle.md`, status `draft` until Martin confirms.

3b. **Update practices.** For each *applicable* thing in the source (a config, script, prompt, template, checklist, tool install), add it to the matching `practices/<name>/` — as a new file, a new variant, or an edit — and update that practice's README ("Files", "Adapt", "Verify", "Sources", "Change log", `last-reviewed`). If no practice fits, create one from `practices/_template/` with status `draft`. Rule: a principle change without a practice change is incomplete unless the source was purely conceptual.

4. **Record decisions.** If Martin decided something ("all repos will use OpenSpec"), add `decisions/NNNN-slug.md` from `templates/decision.md`, status `accepted`, citing the source.

5. **Index.** Add one line to `INDEX.md` under the chronological log and, if new topics appeared, to the topic map.

6. **Publish.** Follow `playbooks/publish-change.md`: `bash scripts/kb-check.sh`, then `bash scripts/kb-publish.sh <slug> "kb: add YYYY-MM-DD <slug>; update principles NN, NN"`.

7. **Tell Martin** in plain language: what was added, which principles changed and how, what actions came out, what could not be captured.
