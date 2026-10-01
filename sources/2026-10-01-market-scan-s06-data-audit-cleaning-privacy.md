---
title: "Market scan — course session 6 'Data-driven AI: audit, cleaning, architecture by data type, privacy and compliance': which videos, podcasts and written sources were considered, selected and transcribed"
type: source
status: current
date: 2026-10-01
tags: [market-scan, data-ingestion, document-parsing, docling, unstructured, reducto, data-quality, data-centric-ai, pii, privacy, gdpr, s6, lidr-ai-engineering]
sources:
  - sources/raw/2026-10-01-market-scan-s06-data-audit-cleaning-privacy/
  - sources/catalog-written-canon.md
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 6: data-driven AI (audit, cleaning, architecture by data type, privacy)

**What this file is.** The log of the scan (steps 1–2 of the module cycle). The digest (step 3) is a separate entry.

## 1. Context

- **Topic map (LIDR session 6, 2026-11-19).** Auditing and cleaning data for AI products · architecture by data type (PDFs, tables, HTML, images, databases) · privacy and compliance (PII, GDPR/EDPB, OWASP LLM02/LLM08, tenant isolation at the data layer). Chunking strategies belong to session 7 and were not selected here.
- **Written canon** (step 1b, 13 items registered in `sources/catalog-written-canon.md` §Session 6): LlamaIndex ingestion docs, Unstructured chunking concepts and best-practices blog, the Docling technical report and repo, Supabase *RAG with permissions*, Presidio, OWASP LLM Top 10 2025 (LLM02/LLM08), EDPB and EDPS positions on generative AI, Chip Huyen's *Building a generative AI platform*, Barnett's *Seven failure points*, two courses. Twelve pages were snapshotted by the main session into `canon-snapshots/` for the digest (the OWASP PDF and the EDPS PDF were not; the EDPB news page and the OWASP landing page were).
- **Reuse (step 1a).** Read again for the digest: Jerry Liu *document context layer* (s2), Lance Martin and Manus context engineering (s2, "select" and file-system context), the s5 Files-API and permissions material (`practices/memory-and-permissions/external-context-notes.md`, `permission-model.md`), the s4 injection rows of the threat model.
- **Method.** `streamers/youtube-scraper` runs `L3uhtni7OsyXg1ag8` (8 queries × 15, last 12 months → 88 items) and `Jfe9gpmsVHF6Q9SYK` (canon, 8 queries × 8, no date filter → 57 items). `scripts/scan-filter.py`: 83 new in the dated run, 5 already decided. Three reference feeds read directly: 6 + 13 + 3 titles matched; none selected (two parked, one discarded). Transcripts: `johnvc/YoutubeTranscripts` run `TSrhL2qQbuez1giET`, dataset `CjWneo9p9hXoDQpOA`, 11 of 11 with captions. Cost about US$0.40.
- **Queries.** "document parsing pipeline PDF tables RAG ingestion Docling Unstructured" · "data quality audit RAG corpus cleaning deduplication" · "PII detection redaction LLM pipeline Presidio anonymization" · "GDPR generative AI personal data RAG compliance privacy" · "RAG ingestion pipeline production data pipeline LLM 2026" · "document AI OCR layout extraction LLM 2026" · "data curation for LLM applications quality over quantity" · "multi-tenant RAG data isolation row level security vector"; canon run: Reducto, Docling, Unstructured, LlamaParse talks, Andrew Ng data-centric AI, Presidio, privacy engineering, data engineering for RAG.
- **What the search taught.** The market's authoritative voice on this module is the **document-parsing vendors and their founders** (Reducto, LlamaIndex, IBM/Docling) plus one data-centric-AI canon talk (Ng, 2022). The audit/cleaning bullet has almost no conference material of its own — it lives inside the parsing talks ("the PDF is the bug") and one data-engineering practitioner video. The privacy bullet is carried by the written canon (EDPB, OWASP, Presidio, Supabase RLS) plus two explainers (IBM 2026-09, GOTO/Jarmul 2026-01); no reference podcast covered it. "Local LLM" and chunking tutorials were the noise.

## 2. Selection criteria

The authority test of the pilot. Reach floor 5k/500 unless primary. Exceptions recorded: the two short IBM Docling explainers are taken because IBM Research authors Docling (primary by authorship); the IBM privacy explainer because the privacy bullet has no higher-authority video in the window. Target: 11 items, about 5 h 40 min — under the 5–8 h band's middle because the module's market is thin; the written canon is heavier than usual (12 snapshots).

## 3. Selected — transcribed (11)

| Title | Channel | Date | Length | Authority | Serves | Raw file |
|---|---|---|---|---|---|---|
| From ingestion to agents: document intelligence — Adit Abraham (Reducto) | AI Engineer | 2026-09 | 22 m | primary vendor talk | architecture by data type | `yt-0I07YAuF8xA-…` |
| My agent can't read a PDF? — Jerry Liu | DeepLearning.AI (AI Dev 26) | 2026-05 | 31 m | primary (LlamaIndex) | parsing for agents | `yt-80vV6fGIlWo-…` |
| Lessons from processing a billion pages — Reducto | Jason Liu | 2026-01 | 50 m | primary practitioner | parsing failure modes, audit | `yt-ybzR4LBY0Lo-…` |
| What is Docling? | IBM Technology | 2025-08 | 8 m | primary by authorship | PDF → structure | `yt-zSA7ylHP6AY-…` |
| Chunkless RAG with Docling | IBM Technology | 2026-08 | 7 m | primary by authorship | 2026 signal | `yt-vRZNJWw78BQ-…` |
| Building production RAG over complex documents | Databricks | 2024-07 | 1 h 22 m | canon (LlamaIndex at Data+AI Summit) | tables, layout, multimodal | `yt-dI_TmTW9S4c-…` |
| How to get your data ready for AI agents | Dave Ebbelaar | 2025-02 | 25 m | recognised practitioner | audit, cleaning, formats | `yt-9lBTS5dM27c-…` |
| Data-centric AI: from big data to good data — Andrew Ng | Databricks | 2022-07 | 26 m | canon | the audit/cleaning doctrine | `yt-avoijDORAlc-…` |
| AI is exposing your data | IBM Technology | 2026-09 | 11 m | corporate explainer (exception) | privacy | `yt-kyJ1vd7yEPc-…` |
| Hacking AI systems — Katharine Jarmul | GOTO Conferences | 2026-01 | 35 m | conference; privacy-engineering author | privacy, poisoning | `yt-lz0L0rRV7RE-…` |
| How to design a data pipeline that's LLM-ready | Chris Gambill | 2026-06 | 38 m | data-engineering practitioner | audit, contracts, quality | `yt-tkFr-4r906Q-…` |

## 4. Considered — not transcribed (every item is in `sources/media-registry.json` with its reason)

- **Parked (13 incl. RSS):** Notion's vector-DB bill and *RAG at 10 million documents* → s8; freeCodeCamp 7.5-hour production RAG course and AI Council *RAG in 2025* → s9; Cole Medin's strategy overview and multimodal RAG with tables → s10; Neo4j *hallucinations are a data architecture problem* → s10; AI Council data-engineering panel → s15; fine-tuning crash course and Datology *better data* → s16; the DeepLearning.AI *Document AI* course intro and Miradi's five-parser comparison → the s6 validation pass.
- **Discarded (118 + 1 RSS):** below the floor (most); chunking tutorials (session 7); "local LLM" and OCR-tool tutorials; vendor demos (SAP, Snowflake, Copilot Studio, Oracle); Starburst's federation episode.
- **Not found with captions:** none.

## 5. Still to do

Digest with the impact table; principle 16 (draft: data for AI products — audit, parsing by type, privacy) and a practice folder (practices/data-ingestion, to be created) created **unrouted**; the chunking bullet is explicitly left to session 7, which will reuse the Databricks and Reducto transcripts (registry `modules`).

## 6. Raw notes

`sources/raw/2026-10-01-market-scan-s06-data-audit-cleaning-privacy/` — 11 transcripts, 12 canon snapshots, two search result files (88 + 57).
