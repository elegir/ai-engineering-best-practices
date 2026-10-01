# Where does the knowledge live? Long context, cached corpus (CAG), retrieval, or agentic search

Copy into `<repo>/docs/architecture.md` §knowledge or the feature spec; answer once per corpus, date it. Principle: `../../principles/11-runtime-context-management.md` §3.4. Sources: IBM *Is RAG still needed?* (2026-03) and *CAG vs long context* (2026-05), Chan et al. arXiv 2412.15605, Lance Martin (2025-09), Manus (2025-10), Airbyte (2026-03) — `../../sources/2026-09-27-s02-context-caching-digest.md` §3.4. The retrieval pipeline itself (chunking, embeddings, reranking, metadata) is the RAG practice (sessions 9–11, pending); this file only decides *whether* you need one.

## Four strategies

| Strategy | What it is | Wins when | Loses when |
|---|---|---|---|
| **Long context** | Put the documents in the prompt on every call | Bounded corpus queried once or a few times; questions that need the *whole* corpus (comparisons, "what is missing", global summaries); simplicity matters | Re-reading tax on every call; the haystack dilutes attention past ~hundreds of k tokens; corpus does not fit |
| **Cached corpus (CAG / prompt caching)** | Put the documents in the *static prefix* and let the provider cache the KV state; the literature's "CAG" is the same idea with the cache persisted by you | Bounded, **stable** corpus queried repeatedly (a policy manual, a product's docs, one contract across a session); whole-corpus reasoning at ~10 % input price after the first call | Corpus changes often (every change recomputes the whole cache); corpus does not fit; session idle longer than the TTL |
| **Retrieval (RAG)** | Index the corpus; fetch the top chunks per query into the window | Unbounded or fast-changing corpus; per-user or per-tenant scoping; the question is local (one fact, one passage) | The retrieval lottery — silent failure when the right chunk is not returned; questions about *gaps* between documents; the pipeline's moving parts (chunking, embeddings, store, reranker, sync) |
| **Agentic search** | No index: the agent lists, greps and reads with bounded tools, guided by a curated manifest (`llms.txt`: file list + one-line descriptions) | Code and documentation for a coding or research agent; corpora with good names and structure; Martin's test: manifest + fetch beat a vector store on 3M tokens of docs | Very large or unstructured corpora; latency-critical single answers; when descriptions are poor (description quality is the dominant variable) |
| **Memory substrate** (added 2026-10-01, s5) | Not a corpus but what the product *learned* about a user or tenant: the model's interface may be files or file-like commands (Anthropic's memory tool, Claude Code's files); the substrate behind a multi-user handler is a namespaced store with an owner column, concurrency and audit (`../memory-and-permissions/memory_store.py`) | Facts that must outlive the session; per-user or per-tenant scoping; forgetting with a trail | A single-user agent (real files are fine); session-only state (the window and compaction cover it); "one database for everything" is the vendor's preference (Alake 2026-04), not a rule |

## The questions that decide

```
Corpus: <<name>>                                  Date: <<>>
1. Size in tokens today / in a year:              <<n / n>>          → fits the window with room for history? yes/no
2. Change rate:                                   <<static / daily / continuous>>
3. Query pattern:                                 <<once / repeated over a session / repeated across users>>
4. Question shape:                                <<local fact / whole-corpus reasoning / comparison across documents>>
5. Scoping needed (per user, tenant, role):       <<yes/no>>   (multi_tenant, personal_data in ../facts.md)
6. Consumer:                                      <<chat answer / coding or research agent with tools / batch job>>
7. Can the upstream API filter the way the question needs?  <<yes/no>>  (if no: pre-filter or pre-index outside the model, or the agent pages everything through its window)

Decision:  <<long context | cached corpus | retrieval | agentic search | hybrid: ...>>
Because:   <<the two or three answers above that decided it>>
Re-check:  <<when the corpus outgrows the window / when the model generation changes>>
```

## Rules of thumb

- **Fits, stable, asked repeatedly → cached corpus.** Prompt caching is "CAG as a service" (IBM); you get the paper's speed-up without managing a KV store.
- **Fits, asked once → long context.** No cache pays off for one query.
- **Needs the whole book → in the window**, cached if repeated. Retrieval cannot return "the gap between two documents".
- **Does not fit, or changes constantly → retrieval**, and expect to spend the effort on metadata at ingestion and reranking, not on the embedding model ("RAG is not dead, just the way we're doing it" — Tricot).
- **Code/docs for an agent → agentic search first**; write the manifest with good descriptions; index only when scale demands it (Manus: "an index for an enterprise knowledge base, not for a task").
- **Hybrids are normal**: a cached stable core (policies, schema, style guide) in the prefix plus retrieval for the changing tail (tickets, records) after it.
- **Whatever you choose, the haystack rule holds**: fewer, more relevant tokens beat more tokens, even when they fit and even when they are cached.
