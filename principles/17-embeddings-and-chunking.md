---
title: "Embeddings and chunking — a pooled, lossy, topic-level vector; chunk from the element tree and measure the chunker on your corpus; shortlist the model on a benchmark, decide on your eval set, pin the configuration per index; buy context recovery, fine-tuning, multi-vector or vision retrieval only against a before/after"
type: principle
status: draft              # draft until LIDR session 7 (2026-11-26) confirms or contradicts
date: 2026-10-04
last-reviewed: 2026-10-05
tags: [embeddings, chunking, vector-representation, mteb, matryoshka, quantization, input-type, contextual-retrieval, late-chunking, colbert, colpali, fine-tuning, chunk-evaluation, s7]
sources:
  - sources/2026-10-04-s07-embeddings-chunking-digest.md
  - sources/2026-10-04-market-scan-s07-embeddings-chunking.md
  - https://research.trychroma.com/evaluating-chunking
  - https://www.anthropic.com/engineering/contextual-retrieval
  - https://arxiv.org/abs/2409.04701
  - https://weaviate.io/blog/late-chunking
  - https://weaviate.io/blog/chunking-strategies-for-rag
  - https://www.pinecone.io/learn/chunking-strategies/
  - https://developers.openai.com/api/docs/guides/embeddings
  - https://docs.voyageai.com/docs/embeddings
  - https://docs.cohere.com/docs/embeddings
  - https://arxiv.org/abs/2210.07316
  - https://jxnl.co/writing/2024/05/11/low-hanging-fruit-for-rag-search/
  - https://github.com/langchain-ai/rag-from-scratch
supersedes: null
superseded-by: null
---

# Embeddings and chunking

## 1. The question this answers

When a product retrieves by similarity: how is text turned into a vector and what can that vector *not* represent; into what units is the corpus cut and how is the choice measured; how is the model chosen, configured and pinned so two vectors stay comparable; when do context recovery, fine-tuning, multi-vector or vision retrieval earn their cost?

## 2. Short answer

An embedding is a **pooled, lossy, topic-level representation**: it finds what a passage is about, not an exact identifier, a date, a negation or a table cell — those are lexical and structural problems (session 10). **Chunk for the generator's unit and the model's limit, from the parsed element tree**: baseline a recursive splitter at roughly 200–400 tokens of the model's tokenizer, no overlap, or the page or element boundary when the parser gives one; a table is one chunk or row groups with the header repeated; a heading never stands alone. **Measure before changing anything**: questions with verbatim excerpts from your corpus, token-level recall, precision and intersection-over-union for the chosen chunker and one alternative — deterministic, cheap, no judge. **Recover context only where the measurement shows the gap** (late chunking, chunk-specific prefixes, multi-representation indexing). **Shortlist the model on the closest benchmark task, language, maximum input and cost; decide on your eval set.** Embed queries and documents with the provider's two conventions through one code path. **Pin model, version, dimensions, dtype and metric** in one configuration recorded in `docs/stack.md` and the index manifest; a change re-embeds everything behind a new index. Fine-tune the reranker first, the embedding model when real query–document pairs exist. Multi-vector and vision retrieval buy fidelity on visual documents at known storage and token costs — pixels where the parse breaks. Files: `practices/embeddings-and-chunking/`.

## 3. Long explanation

Transcripts and snapshots: `sources/raw/2026-10-04-market-scan-s07-embeddings-chunking/` (file ids in §6); s6 means `sources/raw/2026-10-01-market-scan-s06-data-audit-cleaning-privacy/`. Vendor numbers (dimension sets, token limits, prices, Anthropic's and Chroma's percentages) live only in the practice files, with the date read.

### 3.1 What an embedding is, and what it is not

**The object.** Lance Martin (LangChain, 2024-04-17): documents are split because "embedding models actually have limited context windows", "each document is compressed into a vector". Nils Reimers, then at Cohere (2022-12-20): "a pooling operation, for example you take the mean" over the token vectors; training "push[es] these positive pairs close together". Unstructured (2024-07-17, s6 snapshot): "This compression is inherently lossy."

**What it is not** — four speakers who do not cite each other. Reimers, hosted by Jason Liu (2025-05-22), shows "just embeddings" failing on a customer name, a year and a country: "embedding models are like very very c[oar]se grain topic driven" (captions: "cost grain"). Jason Liu on TWIML with Sam Charrington (2024-11-11): "I love coffee and I hate coffee… similar on a dating app". Anthropic (2024-09-19): an embedding "could miss the exact 'TS-999' match". Liu's blog (2024-05-11): "what is the latest… fundamentally does not embed anything". **Position:** identifiers, dates, ranges, negations and table cells go to lexical search, filters and structure (session 10); this principle states the boundary and stops.

**Two vendor facts for the configuration** (OpenAI's guide): the v3 models have a knowledge cutoff, so newer vocabulary is the out-of-domain case of §3.6; the vectors are normalised, so cosine and dot product rank identically. Radu Gheorghe (Vespa, 2026-08-31) agrees: dot product on normalised vectors, Hamming distance on bits.

### 3.2 Chunking — why, the commandment, the baseline and the levels

**Why, and the commandment.** Chunks exist for the model's maximum input (in tokens — Unstructured), for representation quality (not "averaging all its chapters" — Weaviate, 2025-09-04) and for the generator's attention (Greg Kamradt, 2024-01-08, quoting Anton Troynikov: distracting context "does tend to measurably destroy the performance"). Kamradt's commandment: "your goal is not to chunk for chunking sake". Weaviate's gate: "Does my data need chunking at all?" — FAQs, product descriptions and posts usually do not. The human test, identical in Pinecone (2025-06-28) and Weaviate: a chunk that makes sense "to a human… will make sense to the language model".

**Levels one to three.** *Fixed-size*: "I don't know anybody that does this in production" (Kamradt). *Overlap*: "between 10 % and 20 %" (Weaviate) — but see §3.3. *Tokens, not characters*: count with the model's tokenizer — Dave Ebbelaar (2025-02-13, s6) wraps it so Docling's hybrid chunker counts the model's tokens. *Recursive*: a prioritised separator list — paragraphs, lines, sentences, words, characters; "my go-to splitter" (Kamradt), "a solid default choice" (Weaviate). Chroma (Smith and Troynikov, 2024-07-03) found LangChain's default separators produced "very short chunks" and added sentence punctuation — the reference chunker's list. *Document-aware*: Markdown headers, code by function, HTML by tag. Kamradt's 2024 go-to of thousands of *characters* is dated opinion superseded by §3.3.

**Element-aware chunking — the s6 parsing output, now with rules.** After parsing (`16-data-for-ai-products.md` §3.5), chunking recombines typed elements. Unstructured (concepts page, s6 snapshot): "combine two or more consecutive text elements into each chunk that fits"; "Table elements are always treated as standalone chunks", a large one "chunked by rows"; by title, no chunk spans "two different sections". Docling's hybrid chunker (Ebbelaar) splits what is too large and stitches what is too small. **Page-level as the baseline**: "honestly a pretty strong baseline" (Jerry Liu, 2024-07-23, s6); humans write "to adhere to page boundaries" (Reimers 2025). Tables keep the natural-language view for the embedding model and the HTML for the generator (`16` §3.5); Jason Liu on TWIML: a table goes in "a separate index". **Metadata in the chunk text** (Liu's blog): "include file and document metadata as additional text in each chunk" — path, title, author, date, tags; on TWIML a "Modified by" token alone served a tenth of one client's questions. The reference `StructureAwareChunker` implements these rules; `check_structure()` fails on a split table row, a lone heading or a missing prefix.

**Levels four and five.** Kamradt's semantic chunker cuts where neighbouring sentence groups' embeddings diverge most — "experimental", "more expensive… slower"; Chroma: the percentile "is a relative metric", the splitter "is greedy"; their cluster variant requires "chunks to be re-computed as data is added". Kamradt's agentic chunker extracts propositions and assigns them by an agent-like loop — "slow and… expensive". Chroma's LLM chunker tags small pieces and asks where to split, at "tens of minutes" per corpus; rewriting the corpus "suffered from hallucinations"; next-token entropy and attention values gave no "clear signal for semantic boundaries". **Position:** semantic and LLM chunking first-user and eval-gated; agentic skipped by default; hierarchical, chunk expansion, adaptive and post-chunking are dated rows in `practices/embeddings-and-chunking/chunking-decision-table.md`.

### 3.3 Evaluating a chunker — Chroma's token-level method and what it found

**Why document-level metrics cannot see chunking.** Chroma: benchmarks like MTEB are "evaluated with respect to the relevance of entire documents", so they "cannot take chunking into account"; "nDCG@K… is less useful in the context of RAG". Radu: unjudged results count as zero in nDCG, so re-judge after every relevance change; for RAG precision matters most — "if you feed the LLM junk, you're going to get hallucination".

**The method.** An LLM generates "a query relevant to the documents, as well as excerpts from the corpus… We accept only excerpts which have full-text matches"; no compound questions; duplicates and off-topic excerpts filtered; cents per question (`practices/embeddings-and-chunking/chunk-eval-harness.md`). Score at the **token level**: recall, precision, **Precision_Ω** (precision if every chunk holding excerpt tokens were retrieved) and **IoU**, a Jaccard in which excerpt tokens count once and every retrieved token counts, so overlap is penalised. The reference `chunk_eval()` reproduces the four on a fixture, offline.

**What it found** (five corpora, one model, five chunks retrieved, deviations of tens of points — directions, not decimals; decision table). Recursive chunks of roughly 200–400 tokens with no overlap were "consistently high performing across all evaluation metrics"; cluster and LLM chunkers led on recall and efficiency, at a cost; the OpenAI Assistants default of a large chunk with half its size as overlap had "slightly below-average recall and the lowest scores across all other metrics"; "reducing chunk overlap improves IoU scores". Counter-case: a small model lost recall without overlap. Stated limits: synthetic questions "tend to generate a specific style", a small dataset.

**The practitioner's version.** Liu (TWIML): "given a text chunk can I generate a synthetic question… [and] check whether or not the question… finds the text chunk"; near-perfect recall means "the problem is too easy". Manav of Glean, hosted by Jason Liu (2025-03-05): Glean "unit test[s] our models" per behaviour; an LLM given a sentence "will just add like question words to the beginning". Liu's rule: "tests that are really fast really cheap" — not a judge. This is the retrieval-stage eval added to `14-evals-and-error-analysis.md` §3.3 and `practices/evals/eval-policy.md` §3 on 2026-10-04.

### 3.4 Query vs document — one model, two conventions, one code path

"Questions and documents are very different text objects" (Martin). Voyage and Cohere fix the asymmetry with a per-side `input_type` that prepends an instruction; OpenAI's guide has none (values in `practices/embeddings-and-chunking/embedding-config-and-versioning.md` §2, §7). Behind one model for both sides is Reimers' 2022 answer to "one model or two": DPR used two encoders, TAS-B one, and "the same model… work[s] totally better… for the out of domain setting" because an unseen word "still projects us to… roughly the same point in the vector space". **Position:** one pinned model, the provider's conventions applied by the code path, not the caller — `Embedder.embed()` refuses a call without a side (Verify 2).

### 3.5 Context recovery — three families; long context and the unit of retrieval

**The problem.** A chunk that "doesn't specify which company it's referring to" (Anthropic); a pronoun whose referent is "mentioned only in the first sentence" (Jina).

**Contextual retrieval** (Anthropic, 2024-09-19). Prepend "chunk-specific explanatory context to each chunk before embedding… and creating the BM25 index"; the prompt is on the page. Anthropic measured a large drop in top-20 retrieval failure, larger with contextual BM25 and reranking (percentages, cost and assumptions in the decision table; both are session 10). Alex (Anthropic) with Arjun (Pinecone), 2024-11-12: "studying all of your data before you go and index it". The chunker stays — chunking still "can affect retrieval performance". What did **not** work: generic summaries on chunks, "hypothetical document embedding, and summary-based indexing". Reimers on scale (2025): fine "for a thousand PDFs, but some customers have a billion PDFs".

**Late chunking** (Jina, arXiv 2409.04701; Weaviate, 2024-09-05). "chunking applied after the transformer model and just before mean pooling — hence the term late": document context in every chunk vector at the storage of naive chunking. Requirements (Weaviate): a long-context, mean-pooling model and a chunk-to-token-span mapping. Jina: "in all cases, late chunking improved the score", more for longer documents; on some datasets "no chunking performs best". Caution: "limited data available on its performance" (Weaviate); independent validation still needed (*Prompt Engineering*, 2024-10-11).

**Multi-representation indexing.** Kamradt: search "off of… a summary… or hypothetical questions". Martin: "decoupling raw documents and the unit you use for retrieval"; RAPTOR recurses cluster summaries across "the abstraction hierarchy" (`langchain-rag-from-scratch-readme.md`). Jerry Liu (2024): embed a table's summary, caption "or all three… link all of them to the same underlying data". **Contested** against Anthropic's "summary-based indexing… low performance": the units differ — a summary standing for a document versus a shared summary on every chunk. **Position (digest §5):** summaries find the document; chunk-level context must be chunk-specific; late chunking when the model allows it, contextual prefixes when BM25 must benefit or the corpus is bounded, multi-representation for tables, images and whole-document return — each against a before/after. None fixes a table split mid-row: the structure-aware chunker stays.

**Long context and the unit of retrieval.** Martin's multi-needle test: retrieval "drops with respect to the number of needles", "gets worse if you ask it to reason", needles at the start "are harder to retrieve than towards the end" — "there are no retrieval guarantees" in context stuffing (confirms `11-runtime-context-management.md` §3.1). His "document centric RAG" ("retrieve full documents") and Anthropic's rule that a knowledge base of a few hundred pages goes in the prompt whole (`11` §3.4) move the retrieval unit up without removing chunking from a large, changing corpus — hence the decision table's first question: which unit does the generator need?

### 3.6 Choosing the model — shortlist on benchmarks, decide on your corpus

**Benchmarks lose predictive power** (Reimers 2022; an MTEB author — Muennighoff, Tazi, Magne, Reimers, `mteb-abstract.md`): a benchmark gain can have "like no meaning"; semantic textual similarity has "zero predictive power". BEIR's 2021 finding that the best dense model beat lexical search on fewer than half its datasets (counts in `practices/embeddings-and-chunking/embedding-model-selection.md` §0) is the historical reason for an in-domain check. The MTEB abstract: "no particular text embedding method dominates across all tasks". Speed: a very large model is "two magnitudes slower" for a small gain. BEIR's blind spot — passage retrieval, no long PDFs — is Chroma's criticism three years later.

**The procedure** (Radu, 2026-08-31; Weaviate's short, 2025-01-28). Hamel Husain, introducing Radu on his channel: people "go to a leaderboard, and just like pick the best one". Radu: start at MTEB — "find the benchmark that look closest to your use case", restrict by size, look for models that "punch way above their weight"; then what MTEB does not cover — quantization, Matryoshka dimensions, latency and throughput, including the **query-time P50 of the embedding call from the product's region** (Eskildsen 2025-11: a store's 8 ms does not matter "when it takes 300 milliseconds to create a query vector") — and the hard constraints (multilingual, context length); against over-optimising: "Do we have a performance problem?" Weaviate: domain models for industry terms, general models for most; "run your own benchmarking tests". **Position:** a leaderboard shortlists by task, language and size; two to four candidates run on the corpus eval set with the same chunker; the record names the leaderboard only as the shortlist (Verify 6).

### 3.7 Dimensions, quantization and pinning

**Dimensions.** More dimensions mean "more space with which to get accuracy" at a storage cost; traditionally a new size means re-embedding (Pete Johnson, MongoDB, 2026-01-29). **Matryoshka** training orders the dimensions so "you can basically cut the… vector" (Radu; Johnson agrees). OpenAI, Voyage and Cohere declare which models allow it and which values (`embedding-config-and-versioning.md` §3); OpenAI: cutting after the fact means "you need to be sure to normalize". Radu saw a shorter vector win on one model and lose on another. **Rule:** truncate only to a declared dimension, in the one embed path, then normalise; a different dimension is a different configuration.

**Quantization, twice** (Radu). Of the model: int8 on CPU, half precision on GPU. Of the vectors: "if you go to bfloat16, you're probably not going to lose any… all the way down to bit vectors, but then you're going to lose something"; at scale, binary with Hamming first and "something more expensive to re-rank" (session 10). Voyage and Cohere expose output dtypes as parameters; MongoDB quantizes inside the index (session 8). Session 7's part: **dtype and dimension are configuration**, descended one measured step at a time — float32 → bfloat16 → int8 → binary. **The store side (s8, `18-vector-stores.md` §3.5):** quantization inside the index (scalar, binary, product, rotational) is a *second* quantization, recorded in the store manifest with its rescoring flag and a recall before and after; originals kept (Qdrant) or not (Weaviate); an index-type, parameter or store-quantization change is a **rebuild from the stored vectors, not a re-embed**.

**Versioning.** Voyage states that embeddings within one model series are compatible — not the norm: a vector is a coordinate in one model's space. Glean: "if your model does change… reindex everything"; Eskildsen (turbopuffer, 2025-11-04, `yt-l2N4DT35PKg-…`): "re-embedding everything to switch models… don't fall into that trap"; Vasnetsov (Qdrant, 2023-09-15): "the full update of vectors… is just a common operation" — the store must expect it. **Position:** one pinned model id, version, dimension, dtype, metric and pair of conventions per index, with one fingerprint in `docs/stack.md` and the manifest; a change creates a new index, re-embeds everything, is compared in shadow on the eval set and cut over; `Index.upsert()` refuses a foreign fingerprint or dimension (Verify 1, 7; `embedding-config-and-versioning.md` §6).

### 3.8 Fine-tuning, multi-vector, multimodal — when, and what it costs

**Fine-tuning: when.** Husain, as host, agreeing with Radu: the embedding is "a much more constrained problem… a lot easier to fine-tune" than an LLM. Radu: "anybody should do it". Liu (TWIML): a reranker first, the embedding model second — "annoying to own inference". The don't, from Radu's experiments: training on "the title and description of the product… did not work" — train on the real queries. Glean's pipeline (per-customer models, query–click pairs, monthly retrain and full re-index) is the at-scale form; its view that most enterprise questions need only "very basic signals" is session 10. **Position (digest §5):** collect real pairs from day one — the eval set is the training set in waiting; reranker first; embedding model when pairs exist and inference is owned anyway; never on proxies. Depth: session 16.

**Multi-vector and late interaction.** Martin on ColBERT: "an embedding or vector for every token"; for each query token take the maximum similarity over the document's tokens and sum — "very strong performance, latency is definitely a question". Weaviate: late interaction "performs no pooling step". Qdrant on **ColPali** (2026-03-24): it "extends the late interaction paradigm from text to visual documents", scored like ColBERT over image patches (figures in the decision table until the paper is read). Radu shows MaxSim as a re-ranking phase, never first. Storage is `18-vector-stores.md` §3.5: hundreds of times naive storage (Weaviate's table), and Eskildsen's verdict (2025-11) that it is "very hard to earn a return on" for the precision it buys.

**Multimodal: describe-then-embed vs native.** Kamradt (2024) embeds "a text summary of each image" because CLIP was "not quite there". Liu (TWIML): a bare "describe this image" prompt gave poor recall; a day and a half of prompt hill-climbing made the blueprint search usable (the description prompt is a hyperparameter measured by recall). Reimers (2025) on why CLIP failed for documents: caption training data, short text, low resolution and a **modality gap** between image and text embeddings; what carries: "if you cannot read it, you can't produce an embedding". **Vision-RAG** — embed the page image, retrieve, hand it to a VLM — "makes it so much easier" where "the parsing step breaks", at stated costs: an order of magnitude more tokens per page than its text, "higher rate of hallucination with vision LMs", weak multi-image synthesis. His rule is the position: text "when the PDF is text", pixels "if the PDF has complex visual elements" — `16` §3.4 from the embedding side. His remarks on a competitor's model are "speculation"; not carried.

## 4. How to apply it in a repo

The Verify of `practices/embeddings-and-chunking/README.md`, in order; the practice is `draft` and **unrouted** until the routing gate of `decisions/0004-day-one-for-blank-and-existing-repos.md` §6; it follows `data-ingestion/`.

1. Confirm `retrieval` (`practices/facts.md`) and that the knowledge is not better kept in the window (`practices/context-management/context-store-decision.md`); decide the generator's unit (`chunking-decision-table.md` §0).
2. Pin one `EmbeddingConfig` per index — model, version, declared dimension, dtype, metric, both conventions — in `docs/stack.md`; its fingerprint goes into the manifest (Verify 1).
3. Route every embedding call through one function with a mandatory side (Verify 2).
4. Declare the baseline chunker in the model's tokens (recursive 200–400, no overlap, or structure-aware over the element tree) in the manifest; refuse any chunk over the maximum input (Verify 3, 4).
5. Build the retrieval eval set (≥ 50 questions with verbatim excerpts) and compare the baseline with an alternative on token-level recall, precision and IoU **before** building the index (`chunk-eval-harness.md`; Verify 5); choose the model from two to four candidates on that set (`embedding-model-selection.md`; Verify 6).
6. Make the upsert refuse a foreign fingerprint or dimension; on any configuration change run the re-embed protocol (`embedding-config-and-versioning.md` §6; Verify 7).
7. Adopt context prefixes, late chunking, a dtype step, hierarchical indexing or fine-tuning only with a before/after row and a recorded cost (Verify 8); run the eval as the CI gate on every chunker, configuration or index change (Verify 9).

## 5. Anti-patterns

- A chunk size copied from a tutorial or left at a framework default; a large chunk with heavy overlap, unmeasured.
- Queries embedded as documents, or with no convention, where the provider expects one per side.
- Two models' vectors — or two dimension settings of one model — in one index after a quiet upgrade.
- A model picked from a leaderboard rank, or from the provider already in use, with no comparison on the corpus.
- A vector truncated to an undeclared dimension, or truncated without normalising.
- A table split mid-row or merged with prose; a heading indexed alone; chunks without the document's metadata.
- A generic summary prepended to every chunk; a context prefix or a binary index with no before/after beside it.
- An LLM judge grading retrieval where token offsets can decide; nDCG reported without re-judging new results.
- Fine-tuning on proxies instead of real query–document pairs; fine-tuning the embedding model before the reranker.
- A vision index for a corpus whose text parses cleanly.

## 6. Evidence & sources

- Digest and impact table — `sources/2026-10-04-s07-embeddings-chunking-digest.md` (§3, §5, §6); scan — `sources/2026-10-04-market-scan-s07-embeddings-chunking.md`; canon — `sources/catalog-written-canon.md` §Session 7.
- Transcripts (speaker, date, file id): Greg Kamradt (2024-01-08, `yt-8OJC21T2SL4`); Lance Martin, LangChain (2024-04-17, `yt-sVcwVQRHIc8`); Nils Reimers, Cohere (2022-12-20, `yt-apuDeylm1uE`); Radu Gheorghe, Vespa, hosted by Hamel Husain (2026-08-31, `yt-0KUHkwkThyc`); Manav, Glean, hosted by Jason Liu (2025-03-05, `yt-jTBsWJ2TKy8`); Arjun, Pinecone, and Alex, Anthropic (2024-11-12, `yt-u-ocR-2P_YA`); *Prompt Engineering* (2024-10-11, `yt-Hj7PuK1bMZU`); Weaviate (2025-01-28, `yt-djp4205tHGU`); Adam Lucek (2024-12-09, `yt-Pk2BeaGbcTE`); Pete Johnson, MongoDB (2026-01-29, `yt-YqQ0laSZCxM`); Nils Reimers, Cohere, hosted by Jason Liu (2025-05-22, `yt-npkp4mSweEg`); Jason Liu with Sam Charrington, TWIML (2024-11-11, `podcast-wexpoR1R03A`); Qdrant (2026-03-24, `yt-Fai9aY1PMCA`).
- Reused from s6: Jerry Liu (2024-07-23, `yt-dI_TmTW9S4c`); Dave Ebbelaar (2025-02-13, `yt-9lBTS5dM27c`); two Unstructured snapshots.
- Written canon (snapshots read 2026-10-04): Chroma (2024-07-03); Anthropic (2024-09-19); Jina abstract and README; Weaviate (2024-09-05, 2025-09-04); Pinecone (2025-06-28); OpenAI, Voyage and Cohere pages; MTEB abstract; Jason Liu's blog (2024-05-11).

## 7. Change log

- 2026-10-05 (s8) — refined against `sources/2026-10-05-s08-vector-databases-digest.md`: §3.7 gains the store side of the dtype ladder (quantization inside the index as a second, recorded quantization with rescoring and a before/after; a store or index change is a rebuild, not a re-embed) and is confirmed by Eskildsen and Vasnetsov on re-embedding; §3.6 gains the embedding call's query-time P50 as a selection criterion (Eskildsen 2025-11); §3.8's "Storage is session 8" now points at `18` §3.5. Forty-seven quotations (§3.1–§3.8) shortened to stay under 28 KB; the full wording is in the s7 digest.
- 2026-10-04 — created from `sources/2026-10-04-s07-embeddings-chunking-digest.md` (market scan for LIDR session 7); `draft` until the session on 2026-11-26. Practice `practices/embeddings-and-chunking/` created the same day, unrouted per decision 0004 §6; refinements to principles 11, 14, 16, 21, the glossary and four practice files per the digest's §7.1–7.2. Hybrid search, reranking and query translation parked to session 10, vector-store internals and multi-vector storage to session 8, fine-tuning depth to session 16.
