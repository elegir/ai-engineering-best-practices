---
title: "Playbook — ingest a new source (workshop, article, talk, experiment) into the knowledge base"
type: playbook
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [ingest, sources, principles, index]
sources:
  - CONVENTIONS.md
supersedes: null
superseded-by: null
---

# Ingest a new source

**Input.** Raw material: a transcript, notes, a URL, a PDF, a recording summary, or Martin's own account of an experiment ("I tried rtk for a week; here is what happened"). Also valid: **a lesson from an agent failure** in one of the repos — those are sources too.

**Output.** A dated `sources/` entry (long, digested, English), verbatim raw material under `sources/raw/` when it exists, updated `principles/`, possibly a `decisions/` entry, and an `INDEX.md` line. One commit.

## Steps

1. **Capture everything first.** Save raw material verbatim under `sources/raw/YYYY-MM-DD-slug/` (transcripts, page text, exported notes). For YouTube videos, extract transcripts (Apify `johnvc/YoutubeTranscripts` or similar) and save one file per video with a header noting title, channel, upload date, duration, language, extraction date. For web pages, save the full text. Note anything that could **not** be captured (videos without captions, images, PDFs) so the gap is visible.

2. **Write the source entry** from `templates/source-entry.md`, named `sources/YYYY-MM-DD-slug.md` with the *event* date. Follow `CONVENTIONS.md` §3: context; one-paragraph summary; detailed digest section by section in prose (explain terms; keep numbers, tool names, exact commands); claims worth checking; what is contested (including vendor interest); implications for Martin's repos, by repo; actions; raw-notes appendix pointing to `sources/raw/`.

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
