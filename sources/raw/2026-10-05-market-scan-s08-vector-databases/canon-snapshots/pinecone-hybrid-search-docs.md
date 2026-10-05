# Snapshot — https://docs.pinecone.io/guides/search/hybrid-search.md

Fetched 2026-10-05 by the main session with curl (markdown as served; verbatim).

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.pinecone.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Hybrid search overview

> Combine keyword and semantic retrieval in Pinecone with a text-match filter on a dense search, or by fusing separate searches with reciprocal rank fusion.

Hybrid search combines a keyword signal with a semantic signal so a single query benefits from both. Keyword retrieval (full-text BM25 or sparse vectors) matches specific tokens like product codes, error strings, and names. Semantic retrieval (dense vectors) matches on meaning, so a query still finds an answer phrased with different words. Each method misses what the other catches, and hybrid search closes that gap.

<Note>
  "Hybrid" isn't one fixed method. Qualify what you are combining: full-text (BM25) plus dense, sparse plus dense, or a keyword filter plus dense. This page uses those qualifiers throughout.
</Note>

## Combine signals

Pinecone gives you three ways to combine a keyword signal with a dense signal. [Metadata filtering](/guides/search/filter-by-metadata) is a separate lever that composes with all of them: it narrows the candidate pool before ranking, so an out-of-scope document can't compete for a result slot.

| Pattern | How it works | When to use it |
| - | - | - |
| Filter, then rank | A [text-match filter](/guides/search/filter-by-metadata#text-match-filters) (`$match_phrase`, `$match_all`, `$match_any`) on a full-text field narrows the candidates, then a `dense_vector` search ranks what remains, all in one request. | Document and text workloads on the Documents API. One index, one call, and no score normalization. |
| Client-side fusion | Run a keyword search and a dense search separately, then merge the two ranked lists with [reciprocal rank fusion (RRF)](/guides/search/reciprocal-rank-fusion). | When you want both signals to contribute to the ranking, not just to filter. Works on either API. |
| Server-side combination (Vectors API) | Store a dense vector and a sparse vector on each record in a single vector index. Pinecone combines both in one query, and you set the dense/sparse balance client-side by scaling the query vectors before you send them (an `alpha` weighting). | Existing vector and records workloads on the Vectors API. |

RRF is a fusion method, not a synonym for hybrid search. It's one way to merge ranked lists, while "hybrid search" is the broader approach of combining signals. See [Reciprocal rank fusion](/guides/search/reciprocal-rank-fusion).

## Choose an approach

For a new document or text workload, use the Documents API. Declare a `dense_vector` field and one or more full-text `string` fields in one schema, then either filter a dense search with a text-match filter or run a keyword search and a dense search and fuse them with RRF. See [Full-text search](/guides/search/full-text-search) and the [multi-signal schema example](/guides/index-data/data-modeling#schema-patterns).

For an existing vector or records workload, use the Vectors API.

## Hybrid search on the Vectors API

The Vectors API supports two patterns:

* [Use a single index for dense and sparse vectors](/guides/search/hybrid-search/single-index): Store both vectors per record and set the dense/sparse balance client-side by scaling the query vectors before the request (an `alpha` weighting). This is the simplest single-request architecture, though the unbounded sparse scores need normalizing.
* [Use separate indexes for dense and sparse vectors](/guides/search/hybrid-search/separate-indexes): Store dense and sparse in two indexes linked by ID, query each, and merge the results client-side. This is more flexible, but there is more to manage.
