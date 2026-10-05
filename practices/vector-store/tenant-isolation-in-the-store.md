# Tenant isolation in the store — the control, the recall companion, the proof

Full part of this practice (`full-when: retrieval and multi_tenant`); the day-0 obligation it refines is `../data-ingestion/README.md` Verify 8 and `../data-ingestion/privacy-compliance-checklist.md` §4. Copy into `<repo>/docs/privacy.md` §tenant isolation. Replace `<<TENANT_MODEL>>`, `<<TENANT_A>>`, `<<TENANT_B>>`, `<<K>>`, `<<EF_SEARCH>>`; delete the per-store sections the repo does not use. Principle: `../../principles/18-vector-stores.md` §3.4, §3.7. Sources (read 2026-10-05, snapshots in `../../sources/raw/2026-10-05-market-scan-s08-vector-databases/canon-snapshots/` unless noted): pgvector README (`pgvector-readme.md`); Qdrant *A complete guide to filtering* (`qdrant-vector-search-filtering.md`) and *Filterable HNSW* (`qdrant-filtrable-hnsw.md`); Weaviate *Vector indexing* (`weaviate-vector-index-concepts.md`); Simon Eskildsen, turbopuffer, hosted by Jason Liu (2025-11-04, `yt-l2N4DT35PKg-…`) and at AI Council (2025-05-29, `yt-_yb6Nw21QxA-…`); Andrey Vasnetsov, Qdrant, CMU (2023-09-15, `yt-bU38Ovdh3NY-…`); Supabase *RAG with permissions* (s6 snapshot, `../../sources/raw/2026-10-01-market-scan-s06-data-audit-cleaning-privacy/canon-snapshots/supabase-rag-with-permissions.md`, read 2026-10-01). Dilocker's 2023 CMU talk announced a multi-tenancy section and skipped it (scan log *Correction*, 2026-10-05): nothing here is attributed to it.

## 1. The sentence that changes the day-0 rule

pgvector README: **"sharing an approximate index between tenants means vectors from one tenant can affect recall (and speed) for other tenants. For tenant isolation, use list partitioning or separate tables."** And, on filtering: "With approximate indexes, filtering is applied *after* the index is scanned. If a condition matches 10 % of rows, with HNSW and the default `hnsw.ef_search` of 40, only 4 rows will match on average." (This file and `tuning-and-capacity.md` §3 are the two homes of that sentence in the KB; the principle and the other practices point here.)

Row Level Security is a filter. Supabase's rule stands — "RLS is always applied even as new queries and application logic is introduced", so it is the **control** on Postgres (`../../principles/16-data-for-ai-products.md` §3.7) — but on an approximate index the policy is applied to the candidate list *after* the scan. A tenant who owns 1 % of a shared HNSW index gets, at `ef_search` 40, well under *k* results: no leak, no error, an answer built from three chunks when ten existed. The percolation reason (Vasnetsov 2019-11-24; principle 18 §3.4): remove 99 % of a graph's nodes and what remains is disconnected.

**What `multi_tenant` now requires — three parts, not one:**

1. **Control** — the store enforces the tenant predicate: RLS on Postgres; the store's native partition, namespace or tenant index elsewhere. An application `WHERE` clause is defence in depth, never the control.
2. **Recall companion** — the index is built so the predicate does not starve the candidate list: a partition or table per tenant, a partial index when tenants are few, `hnsw.iterative_scan` when the index must stay shared, a tenant payload index with filter-aware edges, a namespace.
3. **Proof** — two tenants with overlapping content, the production index and `ef`, *k* results each, zero cross-tenant hits, a tenantless query refused (`vector_store.py`: `run_tenant_proof()`, `Query.validate()`, README Verify 4). `StoreManifest.check()` refuses a `multi_tenant` manifest whose proof is missing or was run under another spec.

The model is named in the store manifest (`tenant_model`); `rls_only` is not a value the manifest accepts.

## 2. Per store — the mechanism, the vendor's warning, the companion

| Store | Mechanism (`tenant_model`) | Vendor's warning (read 2026-10-05) | Recall companion |
|---|---|---|---|
| **PostgreSQL + pgvector** | `rls_with_partition` — RLS policy + `PARTITION BY LIST (tenant_id)` with an HNSW index per partition; or separate tables; `partial_index` — one `CREATE INDEX … WHERE tenant_id = …` per tenant when tenants are few; `rls_with_iterative_scan` — one shared index with `SET LOCAL hnsw.iterative_scan = relaxed_order` and a `max_scan_tuples` the proof validated | the README sentence of §1; "If filtering by only a few distinct values, consider partial indexing… many different values, consider partitioning" | the partition / partial index / iterative scan **is** the companion; Supabase's example query lacks a `LIMIT` — add one ("Combine with `ORDER BY` and `LIMIT` to use an index", README) |
| **Qdrant** | `tenant_payload_index` — one collection, a keyword payload index on the tenant field marked `is_tenant: true` so vectors of a tenant are co-located and the graph keeps filter-aware edges per value (Vasnetsov 2023: "build hsw graph only based on payload… only build subgraphs for the specific user IDs") | "Users very frequently make the mistake of creating a separate collection for each tenant… out-of-memory (OOM) errors" (filtering guide) | the payload index declared **before** the load; the planner's cardinality switch |
| **Weaviate** | `namespace` (Weaviate's multi-tenancy): a per-tenant shard with a flat index "where each end user (i.e. tenant) has their own, isolated, dataset", or the dynamic index that becomes HNSW at the threshold ("by default 10,000"), one way | the dynamic index is "particularly useful in a multi-tenant setup" (docs); the switch is irreversible per tenant | isolation is the companion: no graph is shared |
| **turbopuffer** | `namespace` — "a prefix on S3" (Eskildsen, hosted by Jason Liu, 2025-11-04, `yt-l2N4DT35PKg-…`), "a table or a tenant" (Eskildsen, AI Council 2025-05-29, `yt-_yb6Nw21QxA-…`); a Cursor codebase or a Notion workspace per namespace, warmed "as soon as you open a codebase" (Jason Liu, 2025-11-04) | with no natural partitions, "the only thing that scales even now is sharding… you want the shards to be as large as possible" (Jason Liu, 2025-11-04) | isolation is the companion; cold namespaces pay the cold-query latency of `Placement` |
| **Memory store** (`../memory-and-permissions/memory_store.py`) | `namespace` — the owner or tenant the query carries, filtered before ranking | `../../principles/15-memory-external-context-and-permissions.md` §3.5 | the same mechanism: identity filter before ranking, never after a shared candidate list |

## 3. The proof (README Verify 4; `../data-ingestion/` Verify 8 wording of 2026-10-05)

Run with the **production** `IndexSpec` and `ef_search` (`<<EF_SEARCH>>`), on the production store, not the stub:

1. Two tenants `<<TENANT_A>>` and `<<TENANT_B>>` with **overlapping content** — the same documents ingested under both, so nearest neighbours cross tenants unless the control holds.
2. For a sample of queries per tenant, the query carries the tenant (`Query(embedded, k=<<K>>, tenant=…)`); assert **`<<K>>` results each** — fewer is the recall failure the README sentence describes, raised as `UnderFilled`, never returned silently.
3. Assert **zero cross-tenant hits** — the owner of every returned row is the query's tenant.
4. Assert **a tenantless query is refused** (`TenantRequired`) and an upsert without a tenant is refused.
5. Record the `TenantProof` on the store manifest (date, k, `ef_search`, both counts, cross hits, the spec hash, the tenant model and the fixture hash). The proof is void when the spec, the tenant model or the fixture changes: `StoreManifest.check()` compares the hashes. **The stored proof is never the evidence**: `--check` re-runs it from the fixture on every run — a hand-edited proof passes `check()` and fails the re-run (README enforcement table, rows 4 and 9).

The proof is part of the benchmark (`benchmark-protocol.md` §4, run 5) and of the CI gate (`--check` exits 2 without it).

## 4. What this file does not decide

Permission inheritance from shared sources into chunk metadata and permission filters as posting-list intersections are session 10; the store as an attack surface (tenant predicates an ORM can drop, payload fields as an injection path into filters, residency of vectors) is session 14 — `../security-baseline/threat-model-agentic.md` T20 is the entry point. This repo's model: `<<TENANT_MODEL>>`.
