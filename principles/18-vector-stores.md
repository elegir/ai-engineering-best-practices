---
title: "Vector stores — exact search until a measured threshold; an approximate index whose recall@k against exact search is recorded on your own fixture; filters, quantization, placement and tenants are decisions the manifest records and the benchmark proves; Postgres with pgvector is the store until the facts say otherwise"
type: principle
status: draft              # draft until LIDR session 8 (2026-12-03) confirms or contradicts
date: 2026-10-05
last-reviewed: 2026-10-05
tags: [vector-database, vector-store, hnsw, ivf, ann, recall, filtering, filterable-hnsw, iterative-scan, quantization, object-storage, pgvector, qdrant, weaviate, turbopuffer, multi-tenancy, capacity-planning, ann-benchmarks, s8]
sources:
  - sources/2026-10-05-s08-vector-databases-digest.md
  - sources/2026-10-05-market-scan-s08-vector-databases.md
  - https://arxiv.org/abs/1603.09320
  - https://github.com/pgvector/pgvector
  - https://www.postgresql.org/about/news/pgvector-080-released-2952/
  - https://github.com/erikbern/ann-benchmarks
  - https://www.pinecone.io/learn/series/faiss/hnsw/
  - https://www.pinecone.io/learn/a-developers-guide-to-ann-algorithms/
  - https://qdrant.tech/articles/filterable-hnsw/
  - https://qdrant.tech/benchmarks/
  - https://docs.weaviate.io/weaviate/concepts/vector-index
  - https://docs.weaviate.io/weaviate/concepts/vector-quantization
supersedes: null
superseded-by: null
---

# Vector stores

## 1. The question this answers

When a product retrieves by similarity over more vectors than it can scan on every query: which index, with which parameters, under which filters, compressed how, placed on which medium, isolated per tenant how, in which store, and measured against what?

## 2. Short answer

**Exact search until a measured threshold**; the approximate index is a first-user decision. **Above it, an approximate index whose recall@k against exact search is recorded** — with queries per second, p99 latency, memory and build time — on the repo's own fixture, compared across configurations **only at equal recall**. **HNSW in RAM** for throughput over a bounded corpus; a **clustered or hybrid index** when the vectors live on disk or object storage, change constantly or are mostly cold. **Filters break a graph** once roughly 1/k of its nodes survive: declare the strategy per filter class, measure filtered recall, and treat fewer than *k* results returned silently as a bug. **Store quantization is a second quantization** after the embedding configuration's dtype, recorded with oversampling, a rescoring flag and recall before and after; the originals' placement and reversibility are recorded. **Placement** is a manifest field with the cold-query and write-latency budget it implies. **A shared approximate index leaks recall across tenants even behind Row Level Security**: a partition, tenant index or namespace stands beside the control, and the two-tenant proof runs with the production index and asserts *k* results each. **The system of record stays the database**; Postgres with pgvector is the default store until size, tenants, write rate, memory, latency including the embedding call, or operations say otherwise. Files: `practices/vector-store/`.

## 3. Long explanation

Transcripts and snapshots: `sources/raw/2026-10-05-market-scan-s08-vector-databases/` (file ids in §6; speakers from the raw headers, never the channel; Eskildsen's three talks are dated per quote). Vendor and speaker numbers live only in `practices/vector-store/`, dated; this file keeps the rule and a pointer. Comparative claims stay in the digest's §4.

### 3.1 Why exact search stops scaling, and when no index is needed

Exact nearest-neighbour search is a scan — a distance to every vector per query: at 1,536 dimensions, "a million times 1,500 computations" (Jonathan Katz, then at AWS, Postgres.FM 2024-01-19). Edo Liberty (Pinecone, CMU 2021-11-05): "any kind of naive partitioning of the space is just going to blow up in your face immediately" in high dimension.

**Two properties that break database assumptions** (Andrey Vasnetsov, Qdrant, CMU 2023-09-15): an approximate index does not guarantee "the result will be the same for the same underlying data if you build the index multiple times" — it depends on insertion order — and "it's impossible to draw a clear line between relevant and irrelevant documents based solely on the vector similarity score". The pgvector README (read 2026-10-05) says the same: an index now changes a query's result. **Recall is the index's measure** — "the ultimate measurement of the quality of the system" (Katz, PGConf.EU 2024-11-04). Liberty's dissent marks the boundary with session 7: recall "is actually a very poor surrogate of quality" of the *answers*.

**When no index is needed.** Simon Eskildsen (turbopuffer, AI Council 2025-05-29): up to "hundreds of thousands" of vectors, "keep exhaustively search in memory because it's very simple… as you get into the millions… an approximate… index." Qdrant's course and Weaviate's dynamic index each state such a count (`practices/vector-store/index-selection-table.md` §2). **Position:** the walking skeleton runs exact search in the database it already has; the approximate index is a first-user decision with a recorded `flat_until` the repo measures (practice Verify 2); `17-embeddings-and-chunking.md`'s manifest records `index: flat` on day zero.

### 3.2 HNSW — mechanism, the three parameters, build cost, deletes

**Mechanism.** HNSW (Malkov and Yashunin, arXiv 1603.09320, abstract read 2026-10-05) is a proximity graph in layers. Etienne Dilocker (Weaviate, CMU 2023-10-08): from an entry point, follow the edges greedily with a visited list, stop "when we can't improve the scores anymore" — roughly half the graph never touched; upper layers hold fewer points with longer edges. The abstract: layer membership decays exponentially, giving logarithmic scaling; a neighbour-selection heuristic helps "at high recall and in case of highly clustered data".

**Three parameters, described identically by four vendors** (pgvector README, Qdrant course, Weaviate docs, Pinecone's Faiss chapter; defaults, ranges and presets in `practices/vector-store/tuning-and-capacity.md`). `M`, edges per node: memory and recall — "the most important parameter in terms of the quality of the index" (Katz). `ef_construction`, the build candidate list: graph quality against build time. `ef` (pgvector `hnsw.ef_search`), the query candidate list: recall against latency, and a cap on how many results a query returns. Pinecone's Faiss chapter: "efConstruction and efSearch do not affect index memory usage, leaving us only with M".

**Build and deletes.** An insert "is approximately two times more expensive than just searching" (Vasnetsov); pgvector builds fastest when the graph fits `maintenance_work_mem`, after the load. Random vectors make "a horrible graph" (Dilocker; Weaviate agrees) — never benchmark on synthetic vectors (§3.10). A graph cannot drop a node without risking disconnection: tombstone, then rebuild or repair — "a very costly process" (Dilocker); "Vacuuming can take a while for HNSW indexes" (pgvector). **Consequence for `16-data-for-ai-products.md` §3.6:** a deleted vector is hidden before it is gone, so the erasure proof *queries* the index at the production parameters; it never counts rows.

### 3.3 The other index families and the medium each suits

Pinecone's *Developer's guide to ANN algorithms* (2024-05-15) sorts the field into four families. **Hash-based**: "Almost no vector databases use hash-based indexing nowadays". **Tree-based**: break down at high dimension (Katz). **Clustered** (inverted file, IVF): k-means centroids, then the nearest lists — "fewer, longer sequential reads", "little space overhead", "fast for writes", lower throughput than a graph. **Graph**: "the fastest algorithms for in-memory vector search… They will not work in object storage". **Mixed**: a graph over the centroids of partitioned data (SPANN, HFresh, turbopuffer).

**IVFFlat in Postgres** (Katz; README): centroids are sampled from the data, so "Create the index after the table has some data"; under inserts "the centers start to skew" — kept for "transient or ephemeral workloads" (heuristics in the practice's table).

**Clustered indexes for disk and object storage** (Eskildsen, turbopuffer; each quote dated to its talk). A graph "is also not suitable for an OBIC [object] storage first or roundtrip sensitive database" (hosted by Jason Liu, 2025-11-04); a clustered index needs "two round trips". turbopuffer's index is incremental with **SPFresh** (split, merge and reassign clusters — "a concurrency and implementation nightmare… but this works unbelievably well at very large scale", CMU 2026-03-10), and **RaBitQ** quantization whose error bound decides what to re-rank with the full vector. Weaviate's **HFresh** (docs, v1.36) is the same family: posting lists on disk, a centroid graph in memory. **Position (digest §5):** the index follows the placement — a graph in RAM for throughput over a bounded corpus; clustered or hybrid when the data lives on disk or object storage, changes constantly or is mostly cold. The validation pass reads the SPFresh, RaBitQ and DiskANN papers.

### 3.4 Filtering — why it breaks the graph, and the four fixes

**The problem.** Post-filtering — take the top candidates, drop the ones the filter rejects — "risks to either turn the whole search into linear scan or return incomplete results" (Vasnetsov); Liberty: "needless to say that's logically broken and oftentimes you're left with nothing". Pre-filtering — restrict to allowed ids, then search — "nullifies the structure of the index" (Liberty). **The reason is percolation** (Vasnetsov's article, 2019-11-24, and his 2023 talk): with k edges per node a graph disconnects once about 1/k of its nodes remain — "if we have 10 connections per node after removing 90 percent of nodes the graph will become disconnected… the accuracy drops almost almost to zero"; raising `M` shifts the threshold at memory cost.

**Fix 1 — filter-aware edges.** For declared payload fields Qdrant builds a "subgraph for each value of this field and then merge the subgraph… into the main one… our graph will always stay connected", at a bounded edge overhead (Vasnetsov; the factor in `tuning-and-capacity.md` §3). Dilocker (CMU 2025-02-21) on a filter correlated with similarity: "either you lose the connectivity or… you keep scoring points that are never allowed by your filter" — Weaviate's answer is "a variation of acorn". **Fix 2 — a planner by cardinality.** The Qdrant Essentials presenter (2025-10-22): per segment, "based on filter cardinality, index availability and other thresholds" — graph walk, payload-index pre-filter or full scan as the filter narrows. ClickHouse (2026-01-28) exposes the switch as a setting. **Fix 3 — the iterative scan** (pgvector 0.8.0). The README's sentence that reorganises this KB's authorisation rule: "With approximate indexes, filtering is applied *after* the index is scanned" — a selective condition leaves only a fraction of the candidate list, so a query returns fewer than *k* (the README's worked example, with the default `ef_search`, is in `tuning-and-capacity.md` §3). `hnsw.iterative_scan` keeps scanning "until enough results are found", bounded by a tuple cap; few distinct values → "consider partial indexing", many → "consider partitioning" (settings in `tuning-and-capacity.md`). **Fix 4 — payload indexes declared before the load**: "create payload indexes before uploading any data so HNSW can build filter-aware links" (Qdrant course).

**Position (digest §5):** record the strategy per filter class with its measured selectivity in the store manifest, measure filtered recall against filtered exact search, and make a filtered query returning fewer than *k* fail loudly (practice Verify 5). `15-memory-external-context-and-permissions.md` §3.5's hit-rate rule now carries this caveat.

### 3.5 Store quantization — SQ, BQ, PQ, RQ, always with rescoring

**Why.** Dilocker (2023): float32 vectors at a popular model's dimension reach gigabytes at a million objects and terabytes at a billion (his arithmetic in `tuning-and-capacity.md` §6).

**Four methods** (factors, model caveats and parameters in `tuning-and-capacity.md`, dated). **Scalar (int8)**: one byte per dimension (Qdrant's go-to). **Binary**: a single bit per dimension with Hamming distance "in just two CPU instructions… bitwise [xor] and popcount" (Vasnetsov; factors in `tuning-and-capacity.md` §5); it wants high-dimensional embeddings — "test BQ with your own data" (Weaviate); Radu Gheorghe (Vespa, 2026-08-31, reused) agrees for scale. **Product (PQ)**: vector segments mapped to a trained codebook (Dilocker; codebook size in the practice); accuracy "starts dropping very very rapidly" until you over-fetch and rescore; Qdrant's presenter does not recommend it "due to the high accuracy loss". **Rotational (RQ, Weaviate)**: "no training phase", 8-, 4- and 1-bit variants.

**Rescoring and oversampling — every vendor.** "we do rescoring using original representation" (Vasnetsov); Qdrant exposes `oversampling` and `rescore`, Weaviate `rescoreLimit`; pgvector's "Re-rank by the original vectors for better recall" query — a wider inner `LIMIT`, the final one outside — is the smallest statement of the rule. **Where the originals live — the vendors disagree.** Qdrant "will always maintain the original uncompressed vectors… or even removing quantization entirely" (RAM is saved only when they move to disk); Weaviate: "once set on a collection, quantization can't be disabled".

**Position.** The store's quantization is a **second quantization** after `17` §3.7's dtype ladder, and a rebuild from stored vectors, never a re-embed. The store manifest records method, oversampling, rescoring flag, the originals' placement and recall before and after on the fixture; a lossy method with rescoring off and no measurement is refused (practice Verify 6); an irreversible store gets the before/after *first*. **The s7 parks close here.** Pete Johnson (MongoDB, 2026-01-29, reused): quantize at the model or "inside the index". Multi-vector storage: Weaviate's table puts late interaction at hundreds of times naive storage; Eskildsen (hosted by Jason Liu, 2025-11-04): "very hard to earn a return on… How much are you willing to pay for that extra 10 to 20 % of precision".

### 3.6 Storage architecture — memory, disk, object storage; placement as a manifest field

**The hierarchy and its economics** (Eskildsen, turbopuffer; his figures, dated per talk in `store-selection.md` §3). RAM, replicated SSD and object storage each cost an order of magnitude less than the last (Jason Liu, 2025-11-04; AI Council, 2025-05-29; CMU, 2026-03-10); NVMe is a few times slower than memory and far cheaper per gigabyte (Jason Liu, 2025-11-04); an object-storage read is tens to hundreds of milliseconds at the tail (CMU 2026-03-10). **Why vectors force it:** text becomes many times its size in vectors — "storage amplification" (Jason Liu, 2025-11-04; the arithmetic in `store-selection.md`); the 2023 founders named the gap — "separation of storage and compute… not solved yet" (Dilocker).

**Object-storage-native** (Eskildsen's definitions, CMU 2026-03-10 unless dated otherwise). "Object storage is the only stateful dependency. There's no east-west coordination. There is no consensus layer in a separate system"; coordination "with compare and swap directly on object storage". A load balancer hashes the **namespace** — "a prefix on S3" (Jason Liu, 2025-11-04), "a table or a tenant" (AI Council, 2025-05-29) — to a query node; reads go memory → NVMe → object storage; writes land in a write-ahead log on S3 and are acknowledged after it; autoscaled indexers compact in the background. Stated costs: a metadata round trip per strongly consistent query, cold queries and writes in the hundreds of milliseconds (figures per talk in `store-selection.md` §3) — "committing to object storage the new f-sync" (AI Council, 2025-05-29) — and read-committed isolation (CMU).

**Hot, warm and cold in the incumbents.** Weaviate's vector cache and tiers; Qdrant's `memory` tiers and memory-mapped files; Liberty (2021): "degrade between those gracefully". **The user's side** (Mickey Liu, Notion's data platform, AI Council 2025-05-29): billions of chunks re-embedded monthly, a tail latency and a saving the company states itself (`store-selection.md` §4). Eskildsen on the bill (Jason Liu, 2025-11-04): "re-embedding everything to switch models… sucks. And so don't fall into that trap" — `17` §3.7's pinning rule from the store's side. **Position:** placement — where vectors and index live, what is pinned — is a manifest field with the cold-query and write-latency budget it implies (practice `Placement`).

### 3.7 Multi-tenancy at the index layer — and the recall caveat on RLS

**Four stores, four mechanisms.** *Qdrant*: one collection, a keyword payload index marked as the tenant key to "co-locate vectors of the same tenant together"; a collection per tenant is the mistake that ends in "out-of-memory (OOM) errors" (filtering guide). *Weaviate*: a flat index "where each end user (i.e. tenant) has their own, isolated, dataset". *turbopuffer*: a namespace per tenant — a Cursor codebase, a Notion workspace — "completely separated". *Postgres*: the README — **"sharing an approximate index between tenants means vectors from one tenant can affect recall (and speed) for other tenants. For tenant isolation, use list partitioning or separate tables."** (Dilocker's 2023 talk skipped its multi-tenancy section — scan log *Correction*, 2026-10-05.)

**What this does to the RLS rule.** Supabase (s6 snapshot): semantic search "will continue to respect these RLS policies" — the enforcement point stands. But the pgvector README says what a policy *is* to an approximate index: a predicate "applied *after* the index is scanned". A tenant owning 1 % of a shared HNSW index gets, at the default candidate list, well under *k* results — a recall loss that looks like an empty corpus, not a breach. **Refinement (position):** RLS remains the control; recall needs a companion — `hnsw.iterative_scan`, a partial index when tenants are few, list partitioning when many — and the two-tenant proof of `practices/data-ingestion/` Verify 8 runs **with the approximate index present at the production `ef_search`** and asserts *k* results per tenant, not only zero cross-tenant hits. Elsewhere the control is the store's partition, namespace or tenant index; the memory-store namespace rule of `15` §3.5 is the same mechanism. A query without a tenant is refused when `multi_tenant` holds (practice Verify 4).

### 3.8 Tuning, monitoring recall, capacity, the embedding call in the budget

**Defaults unless low recall.** pgvector's tuning list (in the practice) ends with "use the defaults unless seeing low recall". Katz's higher `ef_construction` is a speaker's opinion against the default; Qdrant's three recipes and its segment rule (one segment per core for latency, few large ones for throughput) are in `tuning-and-capacity.md`.

**Monitoring recall.** Dilocker (2023): "occasionally do like sampled brute force comparisons and just see like does your recall drift over time"; pgvector gives the form — disable the index scan for the session and compare. The practice's `sampled_recall()` and `--check` run it with a recorded floor and an alert, on a schedule and after every change (Verify 9). **Napkin math** (Eskildsen, CMU 2026-03-10): a simple model of the system first — a gap of an order of magnitude is "a massive opportunity… or there's a bug in your understanding"; "This always beats profiling." **Capacity.** The vendors' arithmetic agrees: vectors × dimensions × bytes per value, plus the graph (edges per node × pointer size), plus replicas, plus the quantized copy when the originals stay (Qdrant's and pgvector's formulas in the practice). **Position:** the estimate is written before the build, compared with the placement's memory, and is a budget line of `practices/security-baseline/threat-model-agentic.md` T20 (Verify 7). **The embedding call** (Eskildsen, hosted by Jason Liu, 2025-11-04): a store's single-digit milliseconds do not matter when the embedding model takes hundreds to produce the query vector (his figures in `store-selection.md` §2) — the query-time P50 of the embedding call from the product's region is a selection criterion of `17` §3.6 and sits inside this module's latency budget.

### 3.9 Choosing the store

**Search engine or database** (Vasnetsov, 2023). BASE against ACID — "think about postgres and elasticsearch"; a search engine "should not be even used as a primary storage of data especially considering that the full update of vectors… due to… a new version of the model is just a common operation". Eskildsen (CMU 2026-03-10) agrees from the other side — read-committed isolation, "you could never just like hot swap a relational database". **Postgres is enough until it is not.** Eskildsen (Jason Liu, 2025-11-04): "you could probably get away with PG vector" for a small case; the reasons to leave are economics and operations (nobody on call). ClickHouse (2026-01) is the OLAP option. **Position (`store-selection.md`):** the facts that decide — corpus size against the exact-search threshold; data and tenants already in Postgres (joins, RLS, one backup); filter selectivity and tenant count; write rate and re-embedding cadence; QPS and latency budget including the embedding call; memory against the capacity estimate; cold-latency tolerance; who is on call. Postgres with pgvector is the default; a dedicated engine is a derived index, never the system of record; rankings are not a fact (Verify 8).

### 3.10 Benchmarking at equal recall

**ANN-Benchmarks** (README, read 2026-10-05; "no longer actively maintained… consider… VIBE") fixes the protocol: ground truth from exact search, many parameter values per algorithm, read only "the precision-performance frontier", single-threaded queries, no build "more than several hours", datasets that fit in RAM. **The vendors adapt the method, not the results.** Weaviate: recall@10 and recall@100, multi-threaded QPS, mean and p99, import time — "you cannot perform a single-threaded benchmark and extrapolate". Qdrant: "two results must be compared only when you have similar precision"; throughput and latency as two scenarios; "Are we biased? Probably, yes." **Position:** the repo benchmarks its own corpus and queries — the s7 fixture as dataset, exact search over the same stored vectors as ground truth — recording recall@k, QPS at production concurrency, p99, memory and build time per configuration and date; configurations are compared only at equal recall; a vendor's page only shortlists (`benchmark-protocol.md`; Verify 3).

## 4. How to apply it in a repo

The Verify of `practices/vector-store/README.md`, in order; the practice is `draft`, **first-user** and **unrouted** until the routing gate of `decisions/0004-day-one-for-blank-and-existing-repos.md` §6; it follows `embeddings-and-chunking/`.

1. Confirm `retrieval` (`practices/facts.md`); exact search in the existing database is the day-0 state (s7 manifest `index: flat`); install this folder when the corpus, the latency or the bill asks for an approximate index.
2. Write a `StoreManifest` bound to the embedding configuration's fingerprint — index type and parameters, store quantization, placement, tenant model, `flat_until` — beside the s7 manifest (Verify 1, 2).
3. Benchmark on the repo's fixture against exact search before the first approximate build and before every spec, quantization or placement change; the record lets the change through (Verify 3; `benchmark-protocol.md`).
4. When `multi_tenant` holds, name the isolation model, refuse tenantless queries, run the two-tenant proof with the production index and `ef` (Verify 4; `tenant-isolation-in-the-store.md`; `data-ingestion/` Verify 8).
5. Record the strategy per filter class; make an under-filled filtered result fail loudly; measure filtered recall (Verify 5).
6. Set store quantization only with method, oversampling, rescoring, originals' placement and a before/after (Verify 6); estimate capacity before the build (Verify 7).
7. Choose the store against `store-selection.md`'s facts (Verify 8); schedule the sampled exact comparison with a floor and an alert (Verify 9).

## 5. Anti-patterns

- An HNSW index at ten thousand vectors; a dedicated engine before Postgres ran out of anything.
- Index parameters copied from a vendor's benchmark page; a store chosen from a ranking.
- A shared approximate index behind RLS alone; a tenant proof that counts zero leaks and never counts results.
- A filtered or permissioned query trusted to return *k*; post-filtering a fixed candidate list on a selective filter.
- A binary or product-quantized index with rescoring off or with no recall before and after; irreversible quantization set unmeasured.
- A graph index on object storage; a vector store as the system of record.
- A capacity estimate written after the out-of-memory error; a build run before the load.
- Two configurations compared at different recall; a benchmark on random vectors.
- Recall never sampled in production; the embedding call outside the query budget.

## 6. Evidence & sources

- Digest and impact table — `sources/2026-10-05-s08-vector-databases-digest.md` (§3–§6); scan — `sources/2026-10-05-market-scan-s08-vector-databases.md` (with its 2026-10-05 *Correction*); canon — `sources/catalog-written-canon.md` §Session 8.
- Transcripts (speaker, date, file id): Andrey Vasnetsov, Qdrant (CMU, 2023-09-15, `yt-bU38Ovdh3NY`); Etienne Dilocker, Weaviate (CMU, 2023-10-08, `yt-4sLJapXEPd4`; 2025-02-21, `yt-pHB-m-ZITw4`); Simon Eskildsen, turbopuffer (CMU, 2026-03-10, `yt-pqoRNwNaxfs`; hosted by Jason Liu, 2025-11-04, `yt-l2N4DT35PKg`; with Mickey Liu, Notion, AI Council 2025-05-29, `yt-_yb6Nw21QxA`); Edo Liberty, Pinecone (CMU, 2021-11-05, `yt-8LXotdzX_84`); Jonathan Katz with Michael Christofides and Nikolay Samokhvalov (Postgres.FM 081, 2024-01-19, `podcast-vvImP6A_dDU`) and at PGConf.EU (2024-11-04, `yt-XeJIo8Mo66g`); the Qdrant Essentials presenter (2025-10-22, `yt-VJVHU47IAik`, `yt-oExGyAEOpP4`); the ClickHouse presenter (2026-01-28, `yt-sBQiHWl3qYw`); Martin Keen, IBM Technology (2025-03-24, `yt-gl1r1XV0SLw`).
- Reused: Pete Johnson, MongoDB (2026-01-29, `yt-YqQ0laSZCxM`, s7); Radu Gheorghe, Vespa, hosted by Hamel Husain (2026-08-31, `yt-0KUHkwkThyc`, s7); Qdrant on ColPali (2026-03-24, `yt-Fai9aY1PMCA`, s7); Weaviate *Late chunking* (s7 snapshot); Supabase *RAG with permissions* (s6 snapshot).
- Written canon (`canon-snapshots/`, read 2026-10-05): the HNSW abstract; the pgvector README and 0.8.0 release note (2024-11-11); the `erikbern/ann-benchmarks` README; Pinecone's Faiss *HNSW* chapter and *Developer's guide to ANN algorithms* (2024-05-15); Qdrant's *Filterable HNSW* (2019-11-24), filtering, resource and *Optimize performance* pages, benchmarks page and two Essentials pages; Weaviate's *Vector indexing*, *Compression* and *ANN benchmark* pages.

## 7. Change log

- 2026-10-05 — created from `sources/2026-10-05-s08-vector-databases-digest.md` (market scan for LIDR session 8); `draft` until the session on 2026-12-03. Practice `practices/vector-store/` created the same day, first-user and unrouted per decision 0004 §6; refinements to principles 11, 15, 16, 17, the glossary and nine practice files per the digest's §7.1–7.2. Hybrid search, phased ranking and facets parked to sessions 10 and 9, operations to 13 and 15, store security to 14.
