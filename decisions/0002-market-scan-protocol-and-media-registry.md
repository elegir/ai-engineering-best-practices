---
title: "Improve the KB from the market with a fixed protocol, and keep a registry of every video/podcast ever considered (transcribed, applied, candidate, discarded)"
type: decision
status: accepted
date: 2026-09-24
tags: [decision, market-scan, media-registry, courses, apify]
sources:
  - sources/2026-09-24-market-scan-s12-intro-to-agents.md
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# 0002 — Market-scan protocol and media registry

## Context

Martin wants this knowledge base to be the "guiding star" that any of his projects can read at the very start to get the best current practices of agentic software development. Courses he follows (LIDR AI Engineering, Coursera, JHU…) are useful only as a **map of topics**; for each topic the KB should hold what the market's most authoritative voices are saying *now*, and it should be updatable later without re-doing work. On 2026-09-24 a pilot run for LIDR session 12 (introduction to agents) established the procedure: Apify search on YouTube and Apple Podcasts, RSS of the reference podcasts, selection by an explicit authority test, caption transcripts via Apify, and a written log of everything considered.

## Decision

1. **Every scan follows `playbooks/scan-market-for-module.md`** — search → filter against the registry → select by authority → transcribe → raw files → log entry → register → track. No ad-hoc "let me look for a few videos".
2. **`sources/media-registry.json` is the memory of what was considered.** One entry per video or podcast episode, keyed by YouTube id or episode URL, with `status` ∈ {transcribed, digested, applied, candidate, discarded}, the reason, the module and the scan entry that decided it. Discarded items are recorded with the same care as selected ones. `sources/media-registry.md` is a generated readable view.
3. **A new scan never re-examines a registered item.** `scripts/scan-filter.py` splits every new search result into new / parked candidates / already decided; only "new" is read. A discarded item is reconsidered only when its reason no longer holds, and that change is made explicitly in the registry with a note in the new log.
4. **Progress per module is tracked in `sources/scan-log.md`** with fixed stages (mapped → catalogued → scanned → transcribed → digested → principled → validated), so the state of the whole course — or any future course — is visible in one table.
5. **Written sources (docs, papers, blogs) are catalogued separately** from spoken media; the registry covers video and audio, which is where re-scanning would otherwise waste the most effort.

## Consequences

- Re-running a scan is cheap and produces only deltas; the KB can be refreshed per topic whenever the market moves.
- The registry grows monotonically and must be updated in the same commit as any scan or digest; `kb-check.sh` does not yet validate it (possible follow-up: check that every `raw` path in the registry exists and every transcript in `sources/raw/` is registered).
- Anyone reading the KB can see not only what it is based on but what it deliberately ignored and why.
