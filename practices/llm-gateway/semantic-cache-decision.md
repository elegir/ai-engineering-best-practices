# Semantic cache — is it allowed on this route at all?

Fill once per route in the feature spec. Principle: `../../principles/12-llm-gateway-layer.md` §3.5. Sources: Percona/Valkey (2026-01; demo numbers are the vendor's), Redis canon pages, ManyChat (2026-08) — `../../sources/2026-09-30-s03-wrappers-digest.md` §3.5.

**What it is.** Embed the query → vector-search stored queries → above a similarity threshold return *that* query's stored answer → else call the model and store. A hit is **someone else's answer to a similar question**. It sits above provider prompt caching (`../context-management/`), which caches the prefix of *your own* request and never returns another request's output.

## Gate (all must be "yes", or the route gets no semantic cache)

```
Route: <<>>
[ ] The answer does not depend on who asks (no personalisation, no per-user data, no tenant-specific knowledge) — or the cache key includes tenant_id and the corpus is tenant-scoped
[ ] The answer does not depend on when it is asked beyond a TTL you can state (<<24 h / 7 d>>) — "who is the current president" cached 30 days is the canonical failure
[ ] The route does not call tools or act on the world (a cached answer must not replay a side effect)
[ ] A wrong-but-plausible answer is tolerable (an FAQ, documentation) — not for prices, legal/medical, or anything the user will act on without checking
[ ] You measured near-duplicate rate on real traffic: <<x %>> of queries have a semantically similar predecessor (vendor's "40–70 %" is unsourced; a long-tail user base gets ~0 % benefit)
```

## If allowed — the knobs

| Knob | Set to | Why |
|---|---|---|
| Similarity threshold | start at **0.90–0.95**, per domain | the demo's 0.85 returned the wrong question's answer ("Python" the language vs the snake); 0.95 rejected a legitimate 0.90 paraphrase — the band is narrow |
| Filters in the key | `tenant_id`, `domain/topic`, `language`, `model_id`, `prompt_version` | a new prompt or model invalidates old answers; cross-topic hits are the main false positive |
| TTL | short for volatile, long for docs | staleness is silent |
| Embedding model | pinned, versioned | changing it changes every similarity |
| Monitoring | hit rate, **false-positive rate** from a labelled near-miss set (≥ 20 pairs), p50 latency hit vs miss | "aim for 80 % hit rate" (vendor) pushes the threshold down and the error rate up; decide the threshold by false positives, not by hit rate |
| Pre-warming | top-N known questions | fine for FAQ routes |

Demo numbers for scale only (laptop, vendor, 2026-01): miss ≈ 6.5 s via the model; paraphrase hit ≈ 180 ms at 0.97 similarity.

## The one semantic-cache use nobody disputes

Cached model responses in **test pipelines**, keyed by exact prompt + model + version, because live LLM tests are flaky (ManyChat). That is a record/replay fixture, not a production cache — keep it in `tests/fixtures/llm/`.
