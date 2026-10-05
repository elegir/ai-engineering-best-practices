# Store selection — Postgres with pgvector until the facts say otherwise

Copy into `<repo>/docs/stack.md` §vector store. Replace the facts table (`<<VECTOR_COUNT>>`, `<<TENANTS>>`, `<<WRITE_RATE>>`, `<<REEMBED_CADENCE>>`, `<<QPS>>`, `<<LATENCY_BUDGET_MS>>`, `<<EMBED_P50_MS>>`, `<<AVAILABLE_MEMORY_BYTES>>`, `<<ON_CALL>>`) and the decision block (`<<DECISION_DATE>>`). Principle: `../../principles/18-vector-stores.md` §3.6, §3.9. Sources (transcripts in `../../sources/raw/2026-10-05-market-scan-s08-vector-databases/`, snapshots in its `canon-snapshots/`, read 2026-10-05): Andrey Vasnetsov, Qdrant, CMU (2023-09-15, `yt-bU38Ovdh3NY-…`); Etienne Dilocker, Weaviate, CMU (2023-10-08, `yt-4sLJapXEPd4-…`); Simon Eskildsen, turbopuffer, CMU (2026-03-10, `yt-pqoRNwNaxfs-…`), hosted by Jason Liu (2025-11-04, `yt-l2N4DT35PKg-…`) and with Mickey Liu, Notion, AI Council (2025-05-29, `yt-_yb6Nw21QxA-…`); Jonathan Katz with Michael Christofides and Nikolay Samokhvalov, Postgres.FM (2024-01-19, `podcast-vvImP6A_dDU-…`); the ClickHouse presenter (2026-01-28, `yt-sBQiHWl3qYw-…`); pgvector README (`pgvector-readme.md`).

## 1. The rule

**The system of record stays the database; a dedicated vector engine is a derived index.** Vasnetsov (2023), who sells one: a search engine "should not be even used as a primary storage of data especially considering that the full update of vectors… due to… a new version of the model is just a common operation"; "search engines are rarely the source of Truth". Eskildsen (2026-03) from the same side: turbopuffer runs "at a read committed isolation level" and "you could never just like hot swap a relational database". **Day zero is pgvector in the same PostgreSQL with exact search**, recorded by the s7 manifest's `index: flat` (`../stack-defaults.md`, shapes A, B and D). Eskildsen (2025-11): "you could probably get away with PG vector" for a small case; Christofides (2024-01): "the transactional nature… being able to join things together… lower maintenance overhead".

## 2. The facts that decide (fill before choosing; this is the record Martin reads — README Verify 8)

| Fact | Value for this repo | Why it matters (source) |
|---|---|---|
| Vector count today and in a year | `<<VECTOR_COUNT>>` | Against `index-selection-table.md`'s threshold and bands; the README's 32 TB per table and partitioning are Postgres's ceiling (`pgvector-readme.md`) |
| Data and tenants already in Postgres | yes / no; `<<TENANTS>>` tenants | Joins, RLS, one backup, one on-call runbook (Christofides); a tenant per partition or table (README) |
| Filter selectivity and tenant count | the filter classes of the store manifest with their selectivity | Selective filters and small tenants break a shared graph (principle 18 §3.4, §3.7); Qdrant's planner, Weaviate's ACORN variant, pgvector's iterative scan are the store-side fixes (`tuning-and-capacity.md` §3) |
| Write rate and re-embedding cadence | `<<WRITE_RATE>>` upserts/day; re-embed every `<<REEMBED_CADENCE>>` | HNSW inserts cost about two searches each (Vasnetsov); "it costs money to keep these indexes up to date… driven by the economics of creating the embeddings" (Eskildsen, hosted by Jason Liu, 2025-11-04); Notion re-embeds billions of chunks monthly (Mickey Liu 2025-05) |
| QPS and latency budget, including the embedding call | `<<QPS>>` at p99 ≤ `<<LATENCY_BUDGET_MS>>` ms; embedding call P50 `<<EMBED_P50_MS>>` ms from the product's region | "they're not thinking about the latency of the embedding model… The P50 latency you get is 300 milliseconds. Well, it doesn't matter that the turbopuffer latency is 8 milliseconds when it takes 300 milliseconds to create a query vector" (Eskildsen, hosted by Jason Liu, 2025-11-04, `yt-l2N4DT35PKg-…`; the only place this figure lives in the KB) |
| Memory against the capacity estimate | `<<AVAILABLE_MEMORY_BYTES>>` vs `capacity_estimate()` (`tuning-and-capacity.md` §6) | An in-RAM index that does not fit is refused before the build (README Verify 7) |
| Cold-latency tolerance | the product's worst acceptable cold query | Object-storage-native stores: a cold query "can easily be 500 to 1,000 milliseconds" and the write P99 "is around 100 milliseconds" (Eskildsen, CMU 2026-03-10, `yt-pqoRNwNaxfs-…`); "100 to 200 milliseconds" for writes (Eskildsen, hosted by Jason Liu, 2025-11-04, `yt-l2N4DT35PKg-…`) |
| Who is on call | `<<ON_CALL>>` | Linear's reason to move, as told by Eskildsen (2025-11): "hands-free… didn't need anyone… on call"; a self-hosted engine is a second database to operate |

## 3. The candidates, and the triggers to move

| Store | Fits when | Does not fit when | Evidence (dated) |
|---|---|---|---|
| **PostgreSQL + pgvector** (default) | data and tenants already there; corpus within one node's RAM and disk; moderate QPS; joins and RLS matter | the index no longer fits memory; QPS or write rate beyond one node and sharding is unwanted; cold data dominates the bill | pgvector README (HNSW, IVFFlat, `halfvec`, iterative scans, partitioning, 32 TB per table); Katz 2024-01 and 2024-11; Eskildsen, hosted by Jason Liu, 2025-11-04 ("get away with PG vector") |
| **Dedicated engine in RAM/SSD** (Qdrant, Weaviate, Pinecone and others) | tens of millions of vectors per node with filters, payload indexes and quantization inside the store; QPS beyond Postgres | a small corpus (a second database for nothing); the engine would become the system of record | Vasnetsov 2023 (BASE vs ACID, "think about postgres and elasticsearch"); Dilocker 2023 ("it's just engineering. There are trade-offs"); vendor pages, read 2026-10-05 |
| **Object-storage-native** (turbopuffer) | billions of vectors, many namespaces, mostly cold; storage economics dominate; a vendor on call is acceptable | the product cannot absorb cold queries of hundreds of milliseconds or writes of 100–200 ms; data residency forbids the provider | "Object storage is the only stateful dependency" (Eskildsen, CMU 2026-03-10, `yt-pqoRNwNaxfs-…`); the price ladder he states, speaker's figures per talk: RAM "around $5 per gigabyte" (Jason Liu, 2025-11-04, `yt-l2N4DT35PKg-…`), replicated SSD "about 60 cents" (AI Council, 2025-05-29, `yt-_yb6Nw21QxA-…`; also Jason Liu 2025-11), object storage "2 cents per gigabyte" (all three talks), a fully cached object-storage design "about 12 cents per gigabyte" (AI Council, 2025-05-29); NVMe "maybe five times or four times slower than accessing memory if you use them correctly… about a 100x cheaper than DRAM" and "16 kilobytes of vectors from 1 kilobyte of text" (Jason Liu, 2025-11-04) |
| **OLAP with a vector index** (ClickHouse) | the vectors sit beside analytical data already in the warehouse | the warehouse is cold for interactive queries ("half a second" cold — ClickHouse presenter, 2026-01) | ClickHouse (2026-01-28): `vector_similarity` index "at the moment can only be hnsw" |

**Triggers to leave the default**, each a measurement, not a feeling: the capacity estimate exceeds the Postgres node's memory and a disk tier is not enough; p99 at production concurrency misses the budget *after* the embedding call is subtracted; the write rate or the re-embedding cadence makes the HNSW rebuilds the dominant cost; a tenant count that outgrows list partitioning; cold data whose storage bill is "a 10x cheaper storage architecture" elsewhere (Eskildsen's phrase for why customers moved, 2025-11); nobody to run a second database.

## 4. Two dated cases (statements by the companies' own engineers; no independent measurement)

- **Notion** (Mickey Liu, software engineer on the data platform team, AI Council 2025-05-29): "over 10 billion chunks… about 15 billion embeddings on a monthly basis at a peak of 100,000 embeddings per minute"; "about 100 QPS at peak"; recall tracked by "mean reciprocal rank and normalized discounted cumulative gain"; after moving to an object-storage-native store, "on track to save around a few million dollars annually… a p50 of 50 to 70 milliseconds". The lesson that transfers: the re-embedding cadence, not query volume, was the cost driver.
- **Linear** (as told by Eskildsen, hosted by Jason Liu, 2025-11-04): moved for operations — "hands-free… didn't need anyone… on call" — not for query speed.

## 5. The decision block

```
Decision date: <<DECISION_DATE>>
Store: PostgreSQL + pgvector (default) | <engine>
Facts (from §2): vectors <<VECTOR_COUNT>>; tenants <<TENANTS>>; writes <<WRITE_RATE>>/day; re-embed <<REEMBED_CADENCE>>;
                 <<QPS>> QPS at p99 ≤ <<LATENCY_BUDGET_MS>> ms with the embedding call at P50 <<EMBED_P50_MS>> ms;
                 memory <<AVAILABLE_MEMORY_BYTES>> vs estimate; on call: <<ON_CALL>>
Shortlist came from: (a vendor's page or benchmark may be named HERE, as the shortlist only)
Decided by: (the facts above and the benchmark record of benchmark-protocol.md — never a ranking)
Revisit when: (the trigger of §3 that would change this)
```

The shortlist line may name a vendor's comparison; the "decided by" line may not. Every vendor's benchmark page says the others are slower (Qdrant's own page: "Are we biased? Probably, yes." — read 2026-10-05); rankings are not a fact.
