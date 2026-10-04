---
title: "Market scan — course session 7 'Embeddings and vector representation': which videos, podcasts and written sources were considered, selected and transcribed (chunking, embedding-model selection, late and contextual chunking, multi-vector)"
type: source
status: current
date: 2026-10-04
tags: [market-scan, embeddings, chunking, vector-representation, mteb, late-chunking, contextual-retrieval, colpali, s7, lidr-ai-engineering]
sources:
  - sources/raw/2026-10-04-market-scan-s07-embeddings-chunking/
  - sources/catalog-written-canon.md
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 7: embeddings and vector representation

**What this file is.** The log of the scan (steps 1–2 of the module cycle). The digest (step 3) is a separate entry.

## 1. Context

- **Topic map (LIDR session 7, 2026-11-26).** What an embedding is and what it is not · chunking (size, overlap, structure-aware, semantic, late, contextual, agentic) · choosing an embedding model (benchmarks, domain, dimensions, cost, versioning) · query vs document representation (`input_type`, instructions) · dimension reduction and quantization (Matryoshka, int8/binary) · fine-tuning embeddings on domain data · multi-vector and multimodal representation (ColBERT/ColPali) · evaluating a chunker and an embedding model on *your* corpus. Vector-database internals belong to session 8 and were not selected here; hybrid search and reranking belong to session 10.
- **Written canon** (step 1b, 18 items registered in `sources/catalog-written-canon.md` §Session 7, all `NEW` to `scripts/written-filter.py`): Pinecone *Chunking strategies*, Weaviate *Chunking strategies for RAG* (nine strategies, 2025-09-04) and *Late chunking*, the Jina late-chunking paper (arXiv 2409.04701) and its repository, the OpenAI embeddings guide, the MTEB paper and leaderboard, Jason Liu's *Low-hanging fruit for RAG search*, Chroma's *Evaluating chunking strategies for retrieval*, the Voyage and Cohere embeddings docs (`input_type`), Anthropic's *Contextual retrieval* (a cross-session anchor that had never been registered), Kamradt's companion notebook, the LangChain `rag-from-scratch` repository, and three courses (DeepLearning.AI × Qdrant *Retrieval optimization*, DeepLearning.AI × Vectara *Embedding models*, Jason Liu's Maven course). Thirteen pages were snapshotted by the main session into `canon-snapshots/` (the three vendor docs — OpenAI, Voyage, Cohere — as the markdown version the vendors serve at `<page>.md`; the two arXiv abstracts; two GitHub READMEs via raw.githubusercontent.com; the rest as stripped HTML). Not snapshotted: the live MTEB leaderboard (a JavaScript application; the digest cites the paper and does not quote rankings), the Kamradt notebook (the video is transcribed) and the three course pages.
- **Reuse (step 1a).** Read again for the digest: Databricks *Production RAG over complex documents* (`yt-dI_TmTW9S4c…`, s6: page-level chunking baseline, embedding many references to one chunk), Dave Ebbelaar (`yt-9lBTS5dM27c…`, s6: Docling hybrid chunker), Adit Abraham / Reducto (`yt-0I07YAuF8xA…`, s6: structure-aware chunk boundaries), IBM *Chunkless RAG with Docling* (`yt-vRZNJWw78BQ…`, s6; `modules` extended to s7 this scan), the s6 Unstructured snapshots (chunking concepts and the 2024 best-practices blog), the s2 context-engineering material on *select* (what a retrieval step owes the context window).
- **Method.** `streamers/youtube-scraper` runs `M5td8GiEGLBHM0zeU` (8 queries × 15, last 12 months → 99 items) and `Cz4uO3I4dB6hg8kFE` (canon, 8 queries × 8, no `dateFilter` → 57 items). `scripts/scan-filter.py`: 94 new in the dated run (3 parked candidates resurfaced, 2 already decided), 53 new in the canon run (1 parked, 3 decided — one of them the s2 IBM transcript, reusable). Three reference feeds read directly: Chain of Thought 1 title matched, Latent Space 17, AI Engineering Podcast 7 (its feed moved to `serve.podhome.fm`; the `/rss` path is a JavaScript redirect — recorded in `sources/method-log.md`); six episodes parked for s8/s10, none selected for s7. Transcripts: `johnvc/YoutubeTranscripts` run `VTR39Ua0sm7JfwUF7`, dataset `LObrxYWiTcbEbHfWi`, 13 of 13 with captions (all auto-generated), no Whisper. A first run (`gms0PHE8U2qfXaC0Y`) failed because the actor renamed its input key from `urls` to `youtube_url` since 2026-10-01 — method-log row. Cost about US$0.35.
- **Queries.** Dated: "chunking strategies RAG embeddings 2026" · "embedding model selection MTEB retrieval 2026" · "late chunking contextual retrieval embeddings" · "semantic chunking vs recursive chunking evaluation" · "text embeddings explained vector representation LLM 2026" · "fine-tuning embedding models retrieval domain" · "Matryoshka embeddings dimensions quantization binary" · "multimodal embeddings ColPali document retrieval 2026". Canon: Kamradt 5 levels · Lance Martin RAG from scratch · Anthropic contextual retrieval talk · Jina late chunking · Jason Liu embeddings fine-tuning · Weaviate chunking · Chroma evaluating chunking · Nils Reimers sentence transformers.
- **What the search taught.** The last-12-months window is almost pure noise for this module: of 94 new items, two reached the authority bar (Hamel Husain on embedding-model selection, 2026-08; MongoDB's five embedding choices, 2026-01) and one is a usable vendor short (Qdrant on ColPali). The market's authoritative voice is **older than the window**: Kamradt (2024-01), Lance Martin (2024-04), Reimers (2022-12), the Anthropic/Pinecone contextual-retrieval build (2024-11), the late-chunking explainers (2024-10), Jason Liu's office hours and the Glean case (2025). Chunking tutorials, "embeddings explained" beginner videos, interview-prep channels and LLM fine-tuning (not embedding fine-tuning) were the noise. No Jina video on late chunking exists; the paper, the repository README and the Weaviate validation blog carry that bullet. No reference podcast episode on embeddings in the window; the podcast requirement is met by the TWIML episode with Jason Liu (2024-11, YouTube captions).

## 2. Selection criteria

The authority test of the pilot (`sources/2026-09-24-market-scan-s12-intro-to-agents.md` §2). Reach floor 5k/500 unless primary. Exceptions recorded: the Qdrant ColPali short (277 views) is taken because Qdrant implements multi-vector search and the clip is the only primary voice on ColPali under five minutes; the Weaviate short on choosing a model (4 min) is cheap and from the vendor whose blog is the canon. Target: 13 items, about 9 h 50 min — **above the 5–8 h band** because the freeCodeCamp compilation (2 h 33 m) is the canon for three sessions (s7 indexing and embeddings, s9 flow, s10 query techniques) and is transcribed once for all three (registry `modules`); without it the scan is 7 h 17 m, inside the band.

## 3. Selected — transcribed (13)

| Title | Channel | Date | Length | Authority | Serves | Raw file |
|---|---|---|---|---|---|---|
| The 5 levels of text splitting for retrieval | Greg Kamradt | 2024-01 | 1 h 09 m | canon | chunking levels 1–5 | `yt-8OJC21T2SL4-…` |
| Learn RAG from scratch — Lance Martin | freeCodeCamp | 2024-04 | 2 h 33 m | canon (LangChain; also s9, s10) | indexing, embeddings, chunk-to-vector flow | `yt-sVcwVQRHIc8-…` |
| Sentence transformers and embedding evaluation — Nils Reimers | Cohere (Talking Language AI) | 2022-12 | 60 m | primary (MTEB co-author) | what embeddings are, how they are trained and evaluated | `yt-apuDeylm1uE-…` |
| Stop picking embedding models off the MTEB leaderboard | Hamel Husain | 2026-08 | 22 m | recognised practitioner, 2026 | model selection on your corpus | `yt-0KUHkwkThyc-…` |
| Inside Glean: fine-tuning embedding models | Jason Liu | 2025-03 | 47 m | primary enterprise case | domain fine-tuning | `yt-jTBsWJ2TKy8-…` |
| Build contextual retrieval with Anthropic and Pinecone | Pinecone | 2024-11 | 54 m | primary vendor implementation (also s10) | contextual chunking | `yt-u-ocR-2P_YA-…` |
| Stop losing context — late chunking | Prompt Engineering | 2024-10 | 17 m | practitioner explainer (paper snapshotted) | late chunking | `yt-Hj7PuK1bMZU-…` |
| How to choose an embedding model | Weaviate | 2025-01 | 4 m | vendor short | model selection | `yt-djp4205tHGU-…` |
| The best way to chunk text for RAG | Adam Lucek | 2024-12 | 33 m | practitioner with evaluation | chunker comparison | `yt-Pk2BeaGbcTE-…` |
| 5 core embeddings choices for developers | MongoDB (.local SF) | 2026-01 | 20 m | vendor conference | dimensions, quantization, model | `yt-YqQ0laSZCxM-…` |
| From text-RAG to vision-RAG | Jason Liu | 2025-05 | 51 m | primary practitioner (also s10) | multimodal / ColPali | `yt-npkp4mSweEg-…` |
| Why your RAG system is broken — Jason Liu | TWIML AI Podcast | 2024-11 | 58 m | reference podcast (also s10) | embeddings in the failure analysis | `podcast-wexpoR1R03A-…` |
| How ColPali models work | Qdrant | 2026-03 | 5 m | vendor short (exception) | multi-vector representation | `yt-Fai9aY1PMCA-…` |

## 4. Considered — not transcribed (every item is in `sources/media-registry.json` with its reason)

- **Parked (15 videos + 6 RSS episodes):** IBM sparse/dense/hybrid, Ebbelaar's hybrid-search guide, Jason Liu's reranking/embedding-fine-tuning and Superlinked sessions, Weaviate agentic RAG → s10; Reimers' four 2021–22 training talks and OpenSearch's domain-adapted neural search → s16 (fine-tuning); IBM *What is a vector database* → s8; Hugging Face agent memory → s5 validation; Jason Liu × Reducto CEO (2025-08) → s6 validation; Jason Liu planner/feedback office hours → s9. RSS: Turbopuffer, *Rise and fall of the vector DB category*, Weaviate's Bob van Luijt, pgai Vectorizer → s8; Exa neural search, GraphRAG → s10.
- **Discarded (117 + 2 clips):** below the floor (most); "embeddings explained" beginner explainers (IBM, Thu Vu, Aishwarya Srinivasan…); interview-prep channels; LLM fine-tuning rather than embedding fine-tuning (Sunny Savita, SDSC); Weaviate's one-minute shorts (the blog is the source); Kamradt's off-topic videos surfaced by the canon query; two Cohere clips cut from the selected Reimers talk.
- **Not found with captions:** none.

## 5. Still to do

Digest with the impact table; principle 17 (draft: embeddings and vector representation) and a practice folder (practices/embeddings-and-chunking, to be created) created **unrouted** (routing gate, decision 0004 §6). Hybrid search, reranking and query rewriting stay with s10 even where the transcripts cover them (Pinecone build, TWIML, Vision-RAG); the digest notes those passages as parked.

## 6. Raw notes

`sources/raw/2026-10-04-market-scan-s07-embeddings-chunking/` — 13 transcripts, 13 canon snapshots, two search result files (99 + 57).
