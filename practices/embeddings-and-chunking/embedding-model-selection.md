# Embedding model selection — shortlist on the closest benchmark task, decide on your own corpus

Copy into `<repo>/docs/stack.md` §embeddings; fill the candidate table and the decision block; date it. Principle: `../../principles/17-embeddings-and-chunking.md` §3.6 and §3.8. Sources (in `../../sources/raw/2026-10-04-market-scan-s07-embeddings-chunking/`, read 2026-10-04): Radu Gheorghe, Vespa, hosted by Hamel Husain (2026-08-31, `yt-0KUHkwkThyc-…`); Nils Reimers, then at Cohere (2022-12-20, `yt-apuDeylm1uE-…`); Weaviate's short (2025-01-28, `yt-djp4205tHGU-…`); Manav, Glean, hosted by Jason Liu (2025-03-05, `yt-jTBsWJ2TKy8-…`); Jason Liu with Sam Charrington, TWIML (2024-11-11, `podcast-wexpoR1R03A-…`); the MTEB abstract (`canon-snapshots/mteb-abstract.md`); the OpenAI embeddings guide (`canon-snapshots/openai-embeddings-guide.md`); the Voyage embeddings page (updated 2026-08-10, `canon-snapshots/voyage-embeddings-docs.md`); the Cohere embeddings page (`canon-snapshots/cohere-embeddings-docs.md`).

## 0. Why a leaderboard cannot decide

Hamel Husain's framing of the problem (2026-08-31): people "go to a leaderboard, and just like pick the best one without thinking too much about it, or just using an embedding model from the provider that they're using… you're leaving a lot on the table." Three reasons, from the benchmark's own authors and users. (1) **Benchmarks lose predictive power as the field overfits them** — Reimers, an MTEB co-author, 2022-12: "the predictive power of a benchmark… decreases… at some point you see some increase on a benchmark but this has like no meaning"; semantic textual similarity (STS) "has zero predictive power" for retrieval. (2) **No model dominates** — the MTEB abstract (arXiv 2210.07316): "8 embedding tasks covering a total of 58 datasets and 112 languages… no particular text embedding method dominates across all tasks". (3) **Document-level benchmarks cannot see your chunking** — Chroma 2024-07-03: MTEB-style retrieval is "evaluated with respect to the relevance of entire documents, rather than at the level of passages or tokens, meaning they cannot take chunking into account". The dated reason this matters out of domain: on BEIR (2021) "the best dense embedding approach, TAS-B, only was better on 8 out of 18 data sets than lexical search" (Reimers 2022-12) — 2021–22 numbers, kept as the historical reason for an in-domain check, not as a ranking.

## 1. Filter — the constraints that remove most candidates before any score

Radu's procedure (2026-08-31): "we're going to start by looking at MTEB" — "find the benchmark that look closest to your use case", restrict by size, look for models that "punch way above their weight"; then what MTEB does not cover. Record each filter as a row; a candidate that fails one is out.

| Filter | Question | Where the answer comes from |
|---|---|---|
| Task | Retrieval (asymmetric: short queries against long passages), not STS or clustering; the MTEB task family closest to the product | The leaderboard's task tabs, as the **shortlist** only |
| Language | "If you need the model to be multilingual, you should choose a multilingual model" (Radu) | The product's corpus and users; the model card |
| Maximum input | The unit the chunker produces must fit: "If you need this larger context, then you should choose a model that supports that" (Radu) | The provider page — OpenAI's third-generation models list "Max input 8192"; Voyage's 4-series lists "32,000" context tokens while `voyage-law-2` lists "16,000" — the limit is per model, not per vendor; read 2026-10-04, re-read on adoption |
| Knowledge cutoff vs corpus vocabulary | OpenAI's guide (read 2026-10-04): the v3 models "lack knowledge of events that occurred after September 2021"; a corpus whose vocabulary is newer is the out-of-domain case — a new product name or acronym gets the geometry of nothing | The model card; a sample of the corpus's rarest terms |
| Hosting | Closed APIs mean "rate limits and batch processing"; open models mean hosting them (Weaviate 2025-01-28); Liu (TWIML): "it's just annoying to own inference" | The repo's runtime (`stack-notes/`) |
| Cost and throughput | Document embedding is a one-off per index plus the re-embed on every change; query embedding is per request. OpenAI's own table (read 2026-10-04): `text-embedding-3-small` "~62,500" pages per dollar, MTEB 62.3 %; `text-embedding-3-large` "~9,615" pages per dollar, MTEB 64.6 % — the shape of a cost/quality trade-off, not a recommendation | Provider pricing on adoption day |
| Latency | Query-side latency at the product's percentile — the **query-time P50 of the embedding call from the product's region, measured** (added 2026-10-05, s8: "it doesn't matter that the turbopuffer latency is 8 milliseconds when it takes 300 milliseconds to create a query vector" — Eskildsen, 2025-11-04, `../../sources/raw/2026-10-05-market-scan-s08-vector-databases/yt-l2N4DT35PKg-jason-liu-turbopuffer-billion-scale-vector-storage.md`; the number goes into `../vector-store/store-selection.md` §2); Reimers 2022-12 on a 6-billion-parameter model "two magnitudes slower" for a small gain — "find a model that's not only good but also which is fast" | A timed call per candidate on the product's hardware |
| Dimensions, dtype, quantization | Does the model declare a Matryoshka dimension set and the dtypes the store needs (`embedding-config-and-versioning.md` §3–4)? Radu: "from running this on CPU, I would use the int8 quantization. If I run it on GPU, I would use FP16" | The provider page; the store's capabilities (session 8) |

Shortlist **two to four** survivors. Domain models (Voyage lists finance, law and code models beside general ones; Weaviate: domain models for industry terms, general models "will probably work well" for most) are candidates, not winners.

## 2. The eval set

Reuse the retrieval eval set of `chunk-eval-harness.md` (≥ 50 questions with verbatim excerpts, generated and filtered, or real queries with judged excerpts). The same set serves the chunker comparison and the model comparison; the model comparison holds the chunker fixed. Weaviate's rule, 2025-01-28: "I would always recommend running your own benchmarking tests".

## 3. Run every candidate under the same conditions

For each candidate: the same chunker and chunk set, the same k, the same questions; the real embedder (this is the one run that pays for embeddings — `embedding_config_and_chunker.py`'s `--check` with `<<EMBED_BACKEND>>` wired, run on demand, never in CI). Record recall, precision, Precision_Ω, IoU, query latency at the product's percentile, document throughput and cost per million tokens on the day.

| Candidate | Version / snapshot | Dimensions used | dtype | Max input | Recall@k | Precision | IoU | p95 query latency | Cost (per 1M tokens, date) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `<<CANDIDATE_1>>` | | | | | | | | | | |
| `<<CANDIDATE_2>>` | | | | | | | | | | |
| `<<CANDIDATE_3>>` | | | | | | | | | | |
| `<<CANDIDATE_4>>` | | | | | | | | | | |

Radu's caution on the small gains: "Do we have a performance problem? Cuz you may over optimize… if you have 2 million documents, then a lot of the performance issues… may not apply" — pick the simplest candidate within the measured range of the best.

## 4. Pin the winner (the record Martin reads — README Verify 6)

Decision `<<WINNER_DATE>>`: model `<<MODEL_ID>>`, version `<<MODEL_VERSION>>`, dimensions `<<DIMENSIONS>>` of the declared set `<<SUPPORTED_DIMENSIONS>>`, dtype `<<DTYPE>>`, metric `<<METRIC>>`, query convention `<<INPUT_TYPE>>` / document convention `<<INPUT_TYPE>>`, chosen over `<<CANDIDATE_2>>` (and the other candidates of the table) because of the recall, latency and cost figures recorded in the table above; the MTEB task used as the shortlist is named in the Leaderboard column and nowhere else. The block becomes the configuration of `embedding-config-and-versioning.md` §1 and its fingerprint goes into the index manifest. A record with one candidate, or with a rank and no numbers from the corpus eval set, is the negative of Verify 6.

## 5. The fine-tuning trigger

Fine-tuning the **embedding model** is "a much more constrained problem" than fine-tuning an LLM and "a lot easier" (Husain, 2026-08-31); Radu: "it's not a big cost… I think anybody should do it". Liu (TWIML, 2024-11-11) orders the targets: "the first thing to fine tune is likely going to be something like a Cohere reranker… probably for $50 you can get a fine-tuned reranker that outperforms anything off the shelf… I don't know whether fine-tuning embedding models is worth it just because… it's just annoying to own inference, but… that's the second easiest thing". This KB's position (digest §5): **reranker first (session 10), embedding model second**, and only when:

1. **Real query–document pairs exist above a threshold** — `<<N_PAIRS>>` judged pairs from production, not synthetic proxies. Radu's don't, in his words: "I can take the title and description of the product and train off of that. That did not work. You're supposed to train it based on what is actually going to happen" — the real queries. Glean (2025-03-05) trains on query–click pairs after unsupervised pairs (title–body, anchor, co-access) and retrains monthly with a full re-index.
2. **Inference is owned anyway** (an open model already hosted), or the provider offers fine-tuning of the model in use.
3. **The eval set shows the gap** that a better model would close (recall of the source chunk low on questions whose vocabulary is the corpus's).

The eval set is the training set in waiting: collect real pairs from day one. Depth — losses, hard-negative mining, LLM-judge labels, Glean's pipeline — is parked to session 16 (`../../sources/scan-log.md` row 16).
