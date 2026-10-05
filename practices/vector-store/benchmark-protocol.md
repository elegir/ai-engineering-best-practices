# Benchmark protocol — the repo's own corpus, exact search as ground truth, comparisons only at equal recall

Copy into `<repo>/docs/eval-policy.md` §vector store; the fixture lives under `<repo>/evals/retrieval/` (the same fixture as `../embeddings-and-chunking/chunk-eval-harness.md`). Replace `<<K>>`, `<<CONCURRENCY>>`, `<<FLOOR>>`, `<<FIXTURE_PATH>>`, `<<MANIFEST_PATH>>`, `<<SAMPLE_SIZE>>`, `<<SCHEDULE>>`. Principle: `../../principles/18-vector-stores.md` §3.8, §3.10. Sources (read 2026-10-05, snapshots in `../../sources/raw/2026-10-05-market-scan-s08-vector-databases/canon-snapshots/`): the `erikbern/ann-benchmarks` README (`ann-benchmarks-readme.md`); Weaviate *ANN benchmark* (`weaviate-ann-benchmarks.md`); Qdrant *Vector database benchmarks* (`qdrant-benchmarks.md`); pgvector README (`pgvector-readme.md`); Etienne Dilocker, Weaviate, CMU (2023-10-08, `yt-4sLJapXEPd4-…`); Jonathan Katz, PGConf.EU (2024-11-04, `yt-XeJIo8Mo66g-…`); Edo Liberty, Pinecone, CMU (2021-11-05, `yt-8LXotdzX_84-…`).

## 1. Why your own benchmark, and why the vendors' pages only shortlist

ANN-Benchmarks (README): "At this point, ann-benchmarks is no longer actively maintained… consider… VIBE"; its plots are "as of April 2025"; its datasets are "approximately 100-1000 dimensions" and must fit in RAM (big-ann-benchmarks beyond). Its protocol is current; its rankings are not. The vendors adapt the protocol and each concludes it is fastest — Qdrant's page: "Are we biased? Probably, yes." Liberty (2021): accuracy "depends on data"; Katz (2024-11): "measure performance and recall". **Rule:** a vendor's page shortlists stores (`store-selection.md` §5); only a run on this repo's corpus and queries decides an index, a parameter, a quantization or a placement (README Verify 3, 8).

## 2. The dataset and the ground truth

- **Dataset:** the retrieval fixture of `../embeddings-and-chunking/chunk-eval-harness.md` — the corpus the product serves, embedded under the pinned configuration, and real or generated questions. **Never random vectors**: they make "a horrible graph" (Dilocker 2023; Weaviate's FAQ) and their recall curve says nothing about yours.
- **Ground truth:** exact search over the **same stored vectors** — ANN-Benchmarks computes "ground truth data for the top-100 nearest neighbors"; pgvector's form is `SET LOCAL enable_indexscan = off` (or `Query(strategy="exact")` in `vector_store.py`), which bypasses the approximate index and scans. Recall@k is the share of the exact top-k the index returned; recall@k measures the index, the s7 eval measures retrieval against the question (principle 18 §3.1).
- **k:** the production `k` (`<<K>>`), plus recall@100 when the store returns candidates to a reranker (Weaviate reports "Recall@10 and Recall@100").

## 3. What one run records — the `BenchmarkRecord`

Written by `vector_store.py`'s `run_benchmark()`, bound to the fixture by hash and to the spec and quantization by hash, re-verified on every read; a record typed by hand is refused (README Verify 3):

| Field | Meaning | Source of the rule |
|---|---|---|
| `fixture`, `fixture_hash` | the fixture file and its SHA-256 (first 16 hex) | a record that does not match the current fixture is stale |
| `k`, `recall_at_k` | recall against exact search at the production k | ANN-Benchmarks; Katz |
| `qps`, `concurrency` | queries per second **at the stated concurrency** — two runs: throughput at `<<CONCURRENCY>>` (production), and single-thread latency | Weaviate: "you cannot perform a single-threaded benchmark and extrapolate"; Qdrant runs "RPS" and "latency" as two scenarios; ANN-Benchmarks saturates "only one CPU" |
| `p99_ms` | tail latency, not the mean | Weaviate reports mean and p99; Qdrant p95/p99 |
| `memory_bytes` | resident memory of the index process after the build | Qdrant caps memory "to ensure fairness"; the capacity estimate is checked against it |
| `build_seconds` | wall time of the build after the load | ANN-Benchmarks: "Avoid extremely costly index building (more than several hours)"; Weaviate reports import time |
| `date`, `spec_hash`, `quantization_hash` | when (ISO date, `--date` or the day of the run), and for exactly which `IndexSpec` and `Quantization` | a parameter change is a new spec and needs a new record |
| `filter_class`, `selectivity` | on a filtered run: the class name and its **measured** selectivity — matching rows / rows on the exact backend | the store manifest records a filter class by the path of this record, never by a typed number (README Verify 5) |

**What the binding is for.** The fixture, spec and quantization hashes make a stale or careless record fail (another fixture, an older spec, typed numbers); they do not stop someone who rewrites the hashes. The gate re-runs the proof and the sampled recall from the fixture (§6) rather than reading stored results.

**Include what production includes.** Weaviate: "Each request includes retrieving all the matched objects from disk… ann-benchmarks… only return the matched IDs" — measure the fetch of the rows the product needs, over the network the product uses; a dedicated engine's benchmark that omits the network round trip and the object fetch is not comparable with pgvector's in-database query.

## 4. The runs

1. **Baseline:** exact search at `<<K>>` — latency and QPS with no index. This is the number that says whether an index is needed at all (`index-selection-table.md` §2).
2. **Parameter sweep:** for each candidate spec, "Try many different values of parameters… ignore the points that are not on the precision-performance frontier" (ANN-Benchmarks). Plot recall against QPS; read the Pareto frontier.
3. **Equal-recall comparison:** "two results must be compared only when you have similar precision… most benchmarks miss this critical aspect" (Qdrant). Pick a target recall (the floor below) and compare QPS, p99, memory and build time **at that recall**; a faster configuration at lower recall is not faster.
4. **Filtered run:** the same, with each filter class applied (`tuning-and-capacity.md` §3), against **filtered exact** search — `run_benchmark(filters=…, filter_class=…)` in `vector_store.py`, which also measures the class's selectivity and writes the record the store manifest points at. Qdrant's filtered benchmark enriches datasets "with payload metadata and pre-generated filtering requests"; its page names the three outcomes to look for: "Speed boost", "Speed downturn", "Accuracy collapse… the HNSW graph becomes disconnected". A query that returns fewer than k is a failure, not a lower recall.
5. **Tenant run** (when `multi_tenant`): the two-tenant proof of `tenant-isolation-in-the-store.md` §3 with the production spec and `ef`.
6. **Quantization run:** before and after, same spec, same fixture — the two records `StoreManifest.set_quantization()` reads.

## 5. Reading a surprising number — Weaviate's debugging list (read 2026-10-05)

Before concluding the store is slow: the CPU architecture and core count of the machine; random or duplicate vectors in the dataset; disk speed where vectors or graph are on disk; a vector cache smaller than the collection (Weaviate: above about 2 million objects the cache setting matters); the embedding call's share of the measured latency (`tuning-and-capacity.md` §7); whether the benchmark client fetched objects or ids. Napkin math first (Eskildsen, CMU 2026-03-10): a model of the system, then the measurement; a gap of an order of magnitude is an opportunity or a misunderstanding.

## 6. The floor and the production monitor (README Verify 9)

- **Floor:** `<<FLOOR>>` = the recall@`<<K>>` of the accepted configuration on the day of the decision; lowered only with a dated note.
- **Monitor:** on `<<SCHEDULE>>` and after every spec, quantization, placement or size-band change, sample `<<SAMPLE_SIZE>>` production queries, run each against the approximate index and against exact search over the same vectors, and alert when recall falls below the floor — Dilocker (2023): "occasionally do like sampled brute force comparisons and just see like does your recall drift over time". `vector_store.py`'s `sampled_recall()` is the function; `--check --manifest <<MANIFEST_PATH>> --fixture <<FIXTURE_PATH>> --k <<K>> --floor <<FLOOR>>` is the gate (with `--s7-manifest <path>` to compare the embedding manifest's `index` block): exit 2 when the manifest is unusable (missing, malformed, no benchmark for the current spec, the s7 block disagreeing, capacity overflow) or when, under `multi_tenant`, the two-tenant proof **re-run from the fixture** under-fills or crosses tenants; exit 1 when the smallest per-tenant sampled recall is below the floor; exit 0 otherwise. The scheduled form of the monitor is operations (sessions 13 and 15).

## 7. Successors to read at the validation pass

VIBE (named by the ANN-Benchmarks README as its successor) and big-ann-benchmarks (billion scale) for the live protocols; the vendors' pages for method, never for results.
