---
title: "Market scan — course session 8 'Vector databases: architecture, indexing, scalability, performance': which videos, podcasts and written sources were considered, selected and transcribed (HNSW, filtering, quantization, object storage, pgvector, benchmarks)"
type: source
status: current
date: 2026-10-05
tags: [market-scan, vector-database, hnsw, indexing, filtering, quantization, pgvector, qdrant, weaviate, pinecone, turbopuffer, benchmarks, s8, lidr-ai-engineering]
sources:
  - sources/raw/2026-10-05-market-scan-s08-vector-databases/
  - sources/catalog-written-canon.md
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 8: vector databases

**What this file is.** The log of the scan (steps 1–2 of the module cycle). The digest (step 3) is a separate entry.

## 1. Context

- **Topic map (LIDR session 8, 2026-12-03).** What a vector index is and why exact search stops scaling · HNSW and its parameters (`M`, `efConstruction`, `ef`) and the other ANN families (IVF, PQ, flat, disk-based) · filtering with ANN (pre- vs post-filtering, filterable graphs, payload indexes) · compression and quantization (PQ, SQ, BQ; recall vs memory) · storage architecture (memory, disk, object storage; serverless) · multi-tenancy and isolation at the index layer · operational tuning (recall-latency-memory presets, capacity planning) · choosing a store (Postgres/pgvector vs a dedicated engine) · how to benchmark (ANN-Benchmarks protocol: recall@k, QPS, p99, memory). Embeddings and chunking are session 7 (`principles/17-embeddings-and-chunking.md`); hybrid search and reranking are session 10.
- **Written canon** (step 1b, 19 items registered in `sources/catalog-written-canon.md` §Session 8, all `NEW` to `scripts/written-filter.py`): the HNSW paper (arXiv 1603.09320), Pinecone's Faiss/HNSW chapter and ANN-algorithms guide, Weaviate's vector-index and quantization concept pages and its ANN benchmark page, Qdrant's *Filterable HNSW* (2019-11-24), *Complete guide to filtering*, *Resource optimization guide*, *Optimize performance* docs, benchmarks page and the two Essentials-course pages, the pgvector README and the 0.8.0 release note, the ANN-Benchmarks site and repository, Pinecone's hybrid-search doc, the DeepLearning.AI × Weaviate course. Seventeen pages were snapshotted by the main session into `canon-snapshots/` (pgvector and ann-benchmarks READMEs and the Pinecone doc as markdown; the rest as stripped HTML; `qdrant.tech/articles/filtrable-hnsw/` is a redirect stub — the real page is `/filterable-hnsw/` and that is what was snapshotted). Not snapshotted: the live ANN-Benchmarks site (plots) and the course page.
- **Reuse (step 1a).** Read again for the digest: the s7 parks listed in `sources/scan-log.md` row 8 — MongoDB on quantization inside the index (`yt-YqQ0laSZCxM…`), Radu Gheorghe on packed bits and phased ranking in Vespa (`yt-0KUHkwkThyc…`), Qdrant on multi-vector storage (`yt-Fai9aY1PMCA…`), the Weaviate late-chunking post's storage figure (`weaviate-late-chunking.md`); from s6, Supabase *RAG with permissions* (RLS as the tenant boundary in Postgres) and the s5/s6 permission-model notes; from s2, IBM *Is RAG still needed* (`yt-UabBYexBD4k…`) for the long-context-versus-index framing.
- **Method.** `streamers/youtube-scraper` runs `z0fK2SSauSOYK5vOm` (8 queries × 15, last 12 months → 103 items) and `BTfFfezmFxl6hZby1` (canon, 8 queries × 8, no `dateFilter` → 35 items; two queries returned an empty row). `scripts/scan-filter.py`: 97 new in the dated run (2 parked resurfaced, 4 decided), 33 new in the canon run (2 parked — Notion from s6 and IBM from s7, both taken now). The three reference feeds were read on 2026-10-04 for s7 and their s8 matches are already registered as candidates (Turbopuffer and *Rise and fall of the vector DB category* on Latent Space; Weaviate's Bob van Luijt on Chain of Thought; pgai Vectorizer on the AI Engineering Podcast); none re-read. Transcripts: `johnvc/YoutubeTranscripts` run `2IRYu84fMSJmo2vYv` (input schema re-read first — `youtube_url`), dataset `ER23egubze3THcWOc`, 13 of 13 with captions (two manual: Postgres.FM, IBM). Speakers recorded in every raw header from the transcript opening and the video description (s7 method-log rule). Cost about US$0.30.
- **Queries.** Dated: "vector database architecture HNSW explained 2026" · "pgvector vs Pinecone vs Qdrant vs Weaviate benchmark 2026" · "vector search filtering pre-filter post-filter HNSW" · "vector quantization binary scalar product quantization recall memory" · "vector database scaling billions of vectors production" · "do you need a vector database Postgres pgvector 2026" · "ANN benchmarks recall latency tradeoff vector index" · "multi-tenant vector database isolation namespaces". Canon: CMU Database Group Weaviate lecture · Yury Malkov HNSW · Qdrant filterable HNSW · pgvector Jonathan Katz · Turbopuffer object storage · Dilocker compression · Pinecone Edo Liberty · LanceDB/Milvus internals.
- **What the search taught.** The authoritative voice on this module is **one venue**: the CMU Database Group seminars, where the founders or architects of Qdrant (2023), Weaviate (2023, 2025), Pinecone (2021) and turbopuffer (2026) each gave an hour on internals to a database audience. The Postgres side is carried by Jonathan Katz (Postgres.FM 2024-01; PGConf.EU 2024-11). The last-12-months window is almost entirely "do you need a vector database" opinion pieces, vendor-comparison listicles and beginner explainers — none with original evidence; the only fresh primary items are the two Qdrant Essentials modules (2025-10) and the ClickHouse short (2026-01). No Yury Malkov talk exists on YouTube with captions (the HNSW author appears only on the Weaviate podcast audio, catalogued in the Project doc; the paper abstract is snapshotted). Simon Eskildsen (turbopuffer) appears three times in the selection — the CMU talk, the Notion case with Mickey Liu, and Jason Liu's session; the three are kept because the audiences differ (database researchers, a data-engineering conference, RAG practitioners) and the Notion session is the only *user-side* cost case found.

## 2. Selection criteria

The authority test of the pilot. Reach floor 5k/500 unless primary. Exceptions recorded: Katz at PGConf.EU (286 views) by authorship; the ClickHouse short (648 views) as a cheap primary on HNSW inside an OLAP engine. Target: 13 items, about 8 h 15 min — at the top of the 5–8 h band because four of them are hour-long founder lectures that are the canon for this module.

## 3. Selected — transcribed (13)

| Title | Speaker | Channel | Date | Length | Authority | Serves | Raw file |
|---|---|---|---|---|---|---|---|
| Qdrant: open-source vector search engine and vector database | Andrey Vasnetsov (Qdrant) | CMU Database Group | 2023-09 | 1 h 03 m | primary, academic venue | HNSW, filterable graph, payload index, quantization | `yt-bU38Ovdh3NY-…` |
| Weaviate: an architectural deep dive | Etienne Dilocker (Weaviate) | CMU Database Group | 2023-10 | 1 h 04 m | primary, academic venue | HNSW in Go, compression, hybrid, multi-tenancy | `yt-4sLJapXEPd4-…` |
| turbopuffer: object-storage-native database for search | Simon Eskildsen (turbopuffer) | CMU Database Group | 2026-03 | 1 h 09 m | primary, academic venue, 2026 | storage architecture, cost, cold/warm tiers | `yt-pqoRNwNaxfs-…` |
| The Pinecone vector database system | Edo Liberty (Pinecone) | CMU Database Group | 2021-11 | 1 h 07 m | canon | why a dedicated engine; index families | `yt-8LXotdzX_84-…` |
| The Weaviate vector database — AI-native applications | Etienne Dilocker (Weaviate) | CMU Database Group | 2025-02 | 12 m | primary, 2025 | the ecosystem view | `yt-pHB-m-ZITw4-…` |
| pgvector — Postgres.FM 081 | Jonathan Katz, with Michael Christofides and Nikolay Samokhvalov | PostgresTV | 2024-01 | 49 m | reference podcast + contributor | pgvector internals, HNSW vs IVFFlat, when Postgres is enough | `podcast-vvImP6A_dDU-…` |
| Dissimilarity search: implementing in-memory vector search algorithms in PostgreSQL | Jonathan S. Katz | PostgreSQL Europe | 2024-11 | 54 m | primary conference (exception) | HNSW in Postgres, 0.8.0 iterative scans, filtering | `yt-XeJIo8Mo66g-…` |
| Billion-scale vector storage for RAG | Simon Eskildsen, hosted by Jason Liu | Jason Liu | 2025-11 | 51 m | primary practitioner session | production lessons at scale | `yt-l2N4DT35PKg-…` |
| Qdrant Essentials — vector quantization | Qdrant presenter | Qdrant | 2025-10 | 8 m | primary vendor course | SQ/BQ/PQ trade-offs | `yt-oExGyAEOpP4-…` |
| Qdrant Essentials — filterable HNSW | Qdrant presenter | Qdrant | 2025-10 | 5 m | primary vendor course | pre/post filtering | `yt-VJVHU47IAik-…` |
| How Notion cut millions from their vector DB bill | Simon Hørup Eskildsen and Mickey Liu (Notion) | AI Council | 2025-05 | 34 m | user-side case (parked by s6) | cost at scale, migration | `yt-_yb6Nw21QxA-…` |
| Approx vector search in ClickHouse | ClickHouse presenter | ClickHouse | 2026-01 | 4 m | vendor short (exception) | HNSW outside dedicated engines | `yt-sBQiHWl3qYw-…` |
| What is a vector database? | Martin Keen (IBM) | IBM Technology | 2025-03 | 10 m | corporate explainer (parked by s7) | entry framing | `yt-gl1r1XV0SLw-…` |


*Correction (2026-10-05, found by the digest step).* Two "Serves" cells above promise content the talk does not deliver. Dilocker (CMU 2023-10, `yt-4sLJapXEPd4`) announced a multi-tenancy section and then skipped it for time — "I would have another section on multi-tenancy, but I don't want to go even more over" — and said one sentence on hybrid search; multi-tenancy at the index layer comes from the Weaviate docs and the Qdrant guides in `canon-snapshots/`, not from this talk. Katz (PGConf.EU 2024-11, `yt-XeJIo8Mo66g`) names iterative scans and defers them — "iterative search we're not going to talk about today, that's a feature about to come out"; the mechanism is in the pgvector README and the 0.8.0 release note. The lesson for the scan step: a "Serves" cell is written from the transcript, not from the title or the abstract.

## 4. Considered — not transcribed (every item is in `sources/media-registry.json` with its reason)

- **Parked (5):** CMU Lance columnar format (Chang She, 2023-10) and the CMU intro-class concurrency-control talk with Weaviate (2024-11) → s8 validation pass; the Geek Narrator and Database School interviews with Eskildsen → duplicates of the CMU talk, validation pass only; freeCodeCamp vector-search RAG tutorial (MongoDB, 2023-12) → s9. The four RSS episodes parked by s7 stay candidates for the validation pass.
- **Discarded (111):** "do you need a vector database" opinion pieces (Macro Lens ×2, CodeRash, Stack Current…); vendor-comparison listicles and 2026 "ultimate guides" (Analytics Vidhya, Aishwarya Srinivasan, Sukrid, Learn AI Bytes…); beginner explainers (Fireship, codebasics, AssemblyAI); CEO business interviews (No Priors, Unsupervised Learning); CMU seminars surfaced by the canon query but off topic (vectorized execution, Redshift, Firebolt, Convex); below-floor tutorials.
- **Not found:** a Yury Malkov talk with captions; the Qdrant filterable-HNSW canon query returned no video (the article and the course module stand in).

## 5. Still to do

Digest with the impact table; principle 18 (draft: vector stores — index, filter, compress, place) and a practice folder (practices/vector-store, to be created) created **unrouted** (routing gate, decision 0004 §6 — to be revisited after this module, per Martin 2026-10-04). Hybrid search and reranking passages (Dilocker 2023, Pinecone doc) stay with s10.

## 6. Raw notes

`sources/raw/2026-10-05-market-scan-s08-vector-databases/` — 13 transcripts, 17 canon snapshots, two search result files (103 + 35).
