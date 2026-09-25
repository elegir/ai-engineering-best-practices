---
title: "Playbook — scan the market (YouTube, podcasts) for the best current material on one course module, select by authority, transcribe, and log it"
type: playbook
status: current
date: 2026-09-24
last-reviewed: 2026-09-24
tags: [market-scan, apify, youtube, podcasts, transcripts, courses]
sources:
  - sources/2026-09-24-market-scan-s12-intro-to-agents.md
  - CONVENTIONS.md
supersedes: null
superseded-by: null
---

# Scan the market for one module

**Why this exists.** Martin uses course syllabi (LIDR, Coursera, JHU…) only as a *map of topics*. For each topic, the knowledge base should hold what the most authoritative voices in the market are saying *now*, with a visible trail of what was considered and why. This playbook produces that trail for one module: a dated log in `sources/`, verbatim transcripts in `sources/raw/`, and a row in `sources/scan-log.md`. Digesting the material into principles and practices is a separate step (`playbooks/ingest-new-source.md`).

**Input.** One module: its topic bullets (from the syllabus) and its session date. Optionally, the written canon already catalogued for it.

**Output.** `sources/YYYY-MM-DD-market-scan-sNN-<slug>.md` (sections 1–6 below), `sources/raw/YYYY-MM-DD-market-scan-sNN-<slug>/` (transcripts + search-result JSON), an updated row in `sources/scan-log.md`, an `INDEX.md` line. One commit, published with `playbooks/publish-change.md`.

**Tools.** Apify, via the Apify MCP server in Claude Desktop / Claude Code:

| Step | Actor | Why this one | Cost order (2026-09) |
|---|---|---|---|
| YouTube search | `streamers/youtube-scraper` (official Apify) | Search by query with YouTube's own filters (upload date, sort, type); returns channel, subscribers, views, date, duration | ~$0.003 per video returned |
| Podcast discovery | `automation-lab/podcast-scraper` (Apple Podcasts search) → then read each authoritative show's RSS directly | Apple search finds *shows*; episodes are cheaper and more precise from the RSS feed | ~$0.001 per show |
| Transcripts (captions) | `johnvc/YoutubeTranscripts` | Cheapest; returns plain text + metadata; works for any YouTube URL including podcast episodes that also publish on YouTube | ~$0.00001 per video |
| Transcripts (audio only, no captions) | `memo23/video-audio-transcriber` (Whisper; accepts podcast RSS and mp3 URLs) | Only when there is no YouTube version with captions | ~$0.05 per minute |

## Steps

1. **Write the topic map.** Copy the module's bullets into the "Context" section of the new source entry. Turn them into 5–8 search queries: two or three per bullet, phrased like a practitioner would ("AI agent tool use function calling", not "tools"). Include one query with the current year ("… 2026") to catch trend content, and one with the canonical term of art (e.g. "ReAct", "Model Context Protocol").

2. **Search YouTube.** Run `streamers/youtube-scraper` with `searchQueries` = the list, `maxResults` = 15 per query, `dateFilter` = `year`, `sortingOrder` = `relevance`, `videoType` = `video`, no shorts, no streams, `transcriptionAndSubtitle` = `NONE` (transcripts come later and cheaper). Save the result set (title, url, channel, subscribers, views, date, duration, query) as `youtube-search-results.json` in the raw folder. Expect 80–120 items, of which 10–15 will survive.

3. **Search podcasts.** Run `automation-lab/podcast-scraper` in `search` mode with 2–3 queries; save as `apple-podcasts-search-results.json`. From the shows returned, keep only those with real authority (as of 2026-09: *Latent Space*, *AI Engineering Podcast*, *Chain of Thought*; add others when they earn it). Fetch each show's RSS (`feedUrl` in the results) and list episodes from the last 12 months whose titles match the module's terms. Record every matching episode in the log, even the ones assigned to *other* modules — the log is where future scans start.

4. **Select by authority.** Apply the test in the pilot entry (`sources/2026-09-24-market-scan-s12-intro-to-agents.md` §2): primary source > academic/reference conference > recognised practitioner or reference podcast > corporate education channel > trend signal. Discard by rule: no-code/"sell agents" marketing, low-reach paper re-explanations, off-topic, non-English/Spanish. **Add the canon talks** that the "last year" filter hides (reference talks older than 12 months listed in the written catalogue). Target: 10–15 items, 5–8 hours of audio, at least one podcast episode.

5. **Transcribe.** Run `johnvc/YoutubeTranscripts` with all selected URLs (`languages: ["en"]`, `output_formats: ["text"]`, `include_metadata: true`). For a podcast episode, first search YouTube for the episode title — most reference podcasts publish there with captions; only fall back to Whisper if there is none. Download the dataset (`https://api.apify.com/v2/datasets/<id>/items?clean=true&format=json`).

6. **Write the raw files.** One file per item: `yt-<videoId>-<slug>.md` or `podcast-<videoId>-<slug>.md`, with the frontmatter and the one-line provenance header used in the pilot folder (title, channel, upload date, duration, caption type, extraction date, actor, dataset id, which scan selected it). Verbatim text, whitespace normalised, paragraph breaks every ~900 characters. Never edit the words.

7. **Write the log entry** (`sources/YYYY-MM-DD-market-scan-sNN-<slug>.md`) with these sections: 1 Context (trigger, topic map, method with actor names and run ids, cost, queries) · 2 Selection criteria · 3 Selected — transcribed (table: title, channel, date, length, authority level, which bullet it serves, raw file) · 4 Considered — not transcribed, with reason (group by channel; note candidates for other modules) · 5 Still to do · 6 Raw notes pointer. Status `current`; it is a snapshot.

8. **Track.** Update the module's row in `sources/scan-log.md` (stage → `transcribed`), add the entry to `INDEX.md`, run `bash scripts/kb-check.sh`, publish with `bash scripts/kb-publish.sh market-scan-sNN "kb: market scan sNN <topic>"`.

9. **Next step (separate playbook).** Digest with `playbooks/ingest-new-source.md`: summary, detailed digest, claims to check, contested points, implications per repo, actions → new/updated `principles/` and `practices/`. Move the scan-log row to `digested`, then `principled`.

## Rules of thumb learned in the pilot (2026-09-24)

- YouTube search is ~80 % noise on agent topics; the authority test does the real work. Do not skip the "considered — not selected" table: it is what makes the next scan cheaper.
- Reference talks are often older than 12 months. Always merge the date-filtered scan with the written canon before selecting.
- Podcast episodes usually exist on YouTube with captions; check before paying for Whisper.
- Keep the YouTube id in the filename; titles change, ids do not.
- Log episodes that belong to *other* modules in the current entry's §4 and in the scan-log "Notes" column, so later scans start with candidates already in hand.
