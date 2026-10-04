# Chunk evaluation harness — synthetic questions with verbatim excerpts, token-level metrics, a deterministic CI gate

Copy into `<repo>/docs/eval-policy.md` §retrieval and keep the fixture under `<repo>/evals/retrieval/`. Principle: `../../principles/17-embeddings-and-chunking.md` §3.3. Sources (in `../../sources/raw/2026-10-04-market-scan-s07-embeddings-chunking/`, read 2026-10-04): Chroma *Evaluating chunking strategies for retrieval* (2024-07-03, `canon-snapshots/chroma-evaluating-chunking.md`; code public at the page's repository link); Jason Liu with Sam Charrington, TWIML (2024-11-11, `podcast-wexpoR1R03A-…`) and *Low-hanging fruit for RAG search* (2024-05-11, `canon-snapshots/jxnl-low-hanging-fruit-rag-search.md`); Manav, Glean, hosted by Jason Liu (2025-03-05, `yt-jTBsWJ2TKy8-…`); Radu Gheorghe, Vespa (2026-08-31, `yt-0KUHkwkThyc-…`). Companion of `../evals/eval-policy.md` §3 (the retrieval stage, added 2026-10-04).

## 1. Why a separate, cheap, deterministic eval

Application evals (`../evals/`) judge the answer; they cannot say whether the chunker or the model lost the passage. Chroma's reason for token-level metrics: document-level benchmarks "cannot take chunking into account", and "nDCG@K… is less useful in the context of RAG because the rank order of retrieved documents is less important". Radu's blind spot: with nDCG, unjudged results count as zero, so "every time you change your relevance function, make sure you update all the documents that you compute NDCG off"; for RAG "your precision is going to be more important, because if you feed the LLM junk, you're going to get hallucination". Liu's cost rule (TWIML): "I want tests that are really fast really cheap that you should be running every 10 20 minutes" — and "why guess when we can test". No judge: the grader is set arithmetic over token offsets.

## 2. Building the set

**Chroma's method (2024-07-03).** "We sample from an LLM to generate a query relevant to the documents, as well as excerpts from the corpus… We accept only excerpts which have full-text matches within the corpus as valid." Previous queries are put in the prompt to avoid duplicates; compound questions are forbidden (the model had to include an "oath" not to use "and" — "GPT would not comply until we required it"); near-duplicate questions and off-topic excerpts are filtered by cosine thresholds. Cost at the time: "approximately $0.01" per question, so "1,000 questions would cost around $10", before filtering. Their concrete set: 472 queries over five corpora, 328,208 tokens.

**Glean's caveat (2025-03-05).** An LLM given a sentence "will just add like question words to the beginning… you don't want to learn just like exact lexical overlap" — ask for a paraphrase, not a question-word prefix; a set whose questions copy the excerpt's words rewards lexical overlap and says nothing about the embedding.

**Real queries replace synthetic ones.** As production questions arrive (and are judged — the excerpt that answered them), they enter the set and the synthetic ones retire; the number says whether the problem is hard. Liu (TWIML): Paul Graham essays gave "96 and 97 % recall… the problem is too easy"; GitHub issues "60 % recall" because "how to get started" needs a repository filter — a boundary of this module (filters are session 10), found by the eval.

**The adapter.** `make_eval_set()` in `embedding_config_and_chunker.py` is the documented stub to wire to the repo's one LLM client with the prompt shape above; `write_demo_fixture()` is the offline generator for the demo and tests only (each question is a corpus sentence, exact-match by construction).

**Fixture format** (`<repo>/evals/retrieval/fixture.json`):

```json
{"corpus": {"doc-id": "full text …"},
 "questions": [{"question": "…", "excerpts": [{"doc": "doc-id", "start": 120, "end": 310}]}],
 "generator": "make_eval_set (LLM, filtered) | real queries | write_demo_fixture (demo only)"}
```

## 3. Metrics — token level, with the IoU rule

Let *t_e* be the set of tokens of the question's excerpts and *t_r* the tokens of the *k* retrieved chunks, counted every time they are retrieved (overlap is retrieved twice). All four are means over questions; the tokenizer is the model's (the reference uses a declared approximation).

| Metric | Definition | What it tells you |
|---|---|---|
| **Recall** | excerpt tokens retrieved / all excerpt tokens | whether the answer came back at all |
| **Precision** | excerpt tokens retrieved / all retrieved tokens | how much of what the generator reads is the answer |
| **Precision_Ω** | precision "for the case that all chunks containing excerpt tokens are successfully retrieved" — "an upper bound on token efficiency" of the chunker itself, independent of the embedding model | how tight the chunk boundaries are |
| **IoU** | excerpt tokens retrieved, each counted once, / (all retrieved tokens + excerpt tokens not retrieved) — Chroma: "each t_e among t_r only once" in the numerator and "all retrieved tokens in |t_r| in the denominator", so overlap is penalised; "we can think of text chunks as bounding boxes" | the single number that trades recall against waste |

Prefix tokens (the metadata prefix of the structure-aware chunker) are not source tokens and are left out of every count; what the eval measures is the chunker's boundaries and the model's ranking.

## 4. Minimum size, what to compare, the report

- **Size:** at least **50 questions per corpus** (`MIN_QUESTIONS`; `require_eval()` refuses fewer); Chroma's deviations of ± 25–35 recall points on 472 questions are the reason to read directions, not decimals, at any size this harness will reach.
- **Compare:** the chosen chunker and **at least one alternative** with the same embedder and *k* (`require_eval()` refuses a one-chunker record); when comparing models, hold the chunker fixed (`embedding-model-selection.md` §3); when adopting a technique above the baseline (contextual prefix, late chunking, a dtype step, a dimension cut), one before/after row each (README Verify 8).
- **Report** (one row per candidate, in `docs/eval-policy.md` §retrieval): date, chunker record (strategy, size, overlap, tokenizer), embedding configuration fingerprint, *k*, questions, recall, precision, Precision_Ω, IoU, chunks produced, wall time. The chosen row's recall becomes **`<<FLOOR>>`**, lowered only with a dated note.

## 5. The CI rule (README Verify 9)

Run on every change to the chunker, the embedding configuration or the index manifest, with the **stub embedder** (offline, no key, deterministic) for the chunker's boundaries, and on demand with the real embedder for model decisions:

`python3 embedding_config_and_chunker.py --check --fixture <<FIXTURE_PATH>> --chunker <<STRATEGY>> --size <<SIZE>> --overlap <<OVERLAP>> --k <<K>> --floor <<FLOOR>>`

Exit codes: **2** — the fixture is missing, is not valid JSON or lacks `questions` / `corpus`, holds fewer than fifty questions (`--min-questions` can raise that floor, never lower it: `MIN_QUESTIONS` in the script is the minimum), or the chunker arguments are invalid (`--overlap >= --size`) — an index built with no eval set is the negative of Verify 5, and a run that "passes" with the set absent is the negative of Verify 9; **1** — recall@k below the floor; **0** — pass. The reference `--check` embeds with the **stub embedder** under `DEMO_CONFIG`: it is a chunker test and runs without a key. In the repo, point it at the configuration recorded in the index manifest (README Adapt) so the gate tests the chunker that the index actually uses; the real embedder is used for the model comparison of `embedding-model-selection.md` on demand, not on every push. The hook or CI job blocks the merge on anything but 0; a chunker or configuration change merged without the run is the negative. No LLM judge anywhere on this path: the s5 rule that code graders decide where code can decide (`../../principles/14-evals-and-error-analysis.md` §3.2) applied to retrieval.
