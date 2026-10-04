"""embedding_config_and_chunker.py — the ONE path by which text becomes vectors in the product's index.

Copy to <repo>/src/<package>/retrieval/embedding_config_and_chunker.py. Replace <<TOKENIZER>> (the model's real tokenizer
behind the `Tokenizer` protocol — tiktoken's cl100k_base for OpenAI's third-generation models, OpenAI guide read
2026-10-04 — the shipped `ApproxTokenizer` is a DECLARED APPROXIMATION), <<EMBED_BACKEND>> (the provider SDK call behind
`make_stub_backend`; the shipped stub is a deterministic hashed bag of tokens so everything here runs offline) and the
<<MODEL_ID>> / <<MODEL_VERSION>> / <<DIMENSIONS>> / <<SUPPORTED_DIMENSIONS>> / <<DTYPE>> / <<METRIC>> /
<<MAX_INPUT_TOKENS>> / <<INPUT_TYPE>> values from the provider's page on adoption day (embedding-config-and-versioning.md §7).

What this buys you (principles/17-embeddings-and-chunking.md; the enforcement table in README.md names the demo step):
  * ONE PINNED CONFIGURATION per index — model, version, dimensions, dtype, metric, query/document conventions — that
    refuses an unpinned model, an undeclared dimension, an unsupported dtype or metric, a docs/stack.md record or an index
    manifest that disagrees (`EmbeddingConfig`, `matches_stack_record`, `IndexManifest.check`)                    -> Verify 1
  * ONE EMBED PATH with a mandatory `side` ("query" | "document") that applies the provider's convention itself and
    returns TAGGED vectors (`Embedded`: vector, fingerprint, side, model); the index reads the tag, never a caller's
    string: a query-side vector cannot be upserted, a document-side vector cannot be searched with, a vector of another
    configuration is refused; a backend dimension that is neither the configured nor the native one is refused
    (`Embedder.embed`, `Index.upsert`, `Index.search`)                                                               -> Verify 2
  * a DECLARED CHUNKER counting in the model's tokens (size = prefix + body), refusing a chunk over the maximum input,
    recorded in the manifest with the tokenizer's name, which must match the configuration's
    (`Chunker.chunk` -> `_enforce_limit`, `IndexManifest.check`)                                                   -> Verify 3
  * a STRUCTURE-AWARE CHUNKER over data-ingestion's elements (table standalone or row groups with the header repeated,
    a table under two rows refused; a title carried FORWARD into the next chunk, never alone, never backwards; an
    oversize element handed to the recursive splitter; by-page option; metadata prefix on every chunk) and
    `check_structure()` as the mechanical check (prefix, lone heading, trailing heading, split or merged table row)  -> Verify 4
  * an INDEX THAT CANNOT BE BUILT without an eval record whose question count is re-counted from the fixture file and
    whose >= 2 compared chunkers each carry the four metrics (`require_eval`, `Index.build`); token-level
    recall / precision / Precision_Omega / IoU (`chunk_eval`)                                                        -> Verify 5
  * an UPSERT that refuses a tagged vector of another fingerprint or dimension (`Index.upsert`)                       -> Verify 7
  * `--check --fixture <path>`: exit 2 when the set is missing, malformed, too small (MIN_QUESTIONS is a floor the flag
    cannot lower) or the chunker arguments are invalid; exit 1 below the floor — the CI gate                       -> Verify 9

Branches every `--demo` run exercises (recorded verbatim in README.md's change log): every refusal above, each printed as a
REFUSED line, plus the positive path: two chunkers compared on a generated 60-question fixture. Standard library only;
Python 3.10+. Element duck typing: anything with `.type`, `.text`, `.page`, `.rows`, `.caption` and `to_embedding_text()`
works — the `Element` of ../data-ingestion/ingestion_pipeline.py does; the demo ships a minimal `DemoElement`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field, asdict
from typing import Callable, Optional, Protocol, Sequence, Union

MIN_QUESTIONS = 50          # chunk-eval-harness.md §3: fewer questions than this and the eval record is refused; a FLOOR, not a default
METRIC_KEYS = ("recall", "precision", "precision_omega", "iou")
SUPPORTED_DTYPES = ("float32", "bfloat16", "float16", "int8", "uint8", "binary", "ubinary")
SUPPORTED_METRICS = ("cosine", "dot", "euclidean")
SIDES = ("query", "document")
CHROMA_SEPARATORS = ["\n\n", "\n", ".", "?", "!", " ", ""]   # LangChain's default plus ".", "?", "!" (Chroma 2024-07-03)


class RetrievalConfigError(ValueError):
    """Base class: every refusal below is one of these, so a caller can catch the family."""


class UnpinnedConfig(RetrievalConfigError): ...
class ConfigMismatch(RetrievalConfigError): ...
class SideRequired(RetrievalConfigError): ...
class ChunkTooLarge(RetrievalConfigError): ...
class ManifestIncomplete(RetrievalConfigError): ...
class StructureViolation(RetrievalConfigError): ...
class EvalRequired(RetrievalConfigError): ...


# ------------------------------------------------------------------------------------------------------------ tokenizer

class Tokenizer(Protocol):
    name: str
    def encode(self, text: str) -> list[tuple[int, int]]: ...   # (start, end) character span per token


class ApproxTokenizer:
    """<<TOKENIZER>> — a deterministic APPROXIMATION: one token per run of word characters and one per punctuation mark.
    It over-counts short English slightly and under-counts code and non-Latin text; it exists so the chunkers and the
    harness run offline. Wire the model's tokenizer here and keep the span contract: a list of (start, end) offsets."""
    name = "approx-words-v1 (declared approximation; replace with the model's tokenizer)"
    _piece = re.compile(r"\w+|[^\w\s]", re.UNICODE)

    def encode(self, text: str) -> list[tuple[int, int]]:
        return [(m.start(), m.end()) for m in self._piece.finditer(text)]


def count_tokens(tok: Tokenizer, text: str) -> int:
    return len(tok.encode(text))


# ---------------------------------------------------------------------------------------------------------- the config

def _plain(x):
    """JSON round trip: tuples become lists, so a record read back from docs/stack.md or a JSON file compares equal."""
    return json.loads(json.dumps(x))


@dataclass(frozen=True)
class EmbeddingConfig:
    """Everything that makes two vectors comparable. Pinned once per index; a change creates a NEW index (Verify 7).
    `query_input_type` / `document_input_type` are the provider's convention — Voyage `query`/`document`, Cohere
    `search_query`/`search_document`, OpenAI none (all read 2026-10-04) — applied inside `Embedder.embed`, never by callers."""
    model: str                                  # <<MODEL_ID>>
    version: str                                # <<MODEL_VERSION>> — the provider's dated version or snapshot id
    dimensions: int                             # <<DIMENSIONS>> — must be one of `supported_dimensions`
    supported_dimensions: tuple[int, ...]       # <<SUPPORTED_DIMENSIONS>> — the Matryoshka set the provider declares; (native,) otherwise
    dtype: str = "float32"                      # <<DTYPE>>
    metric: str = "cosine"                      # <<METRIC>>
    max_input_tokens: int = 8192                # <<MAX_INPUT_TOKENS>>
    query_input_type: Optional[str] = None      # <<INPUT_TYPE>> for queries, or a literal prefix; None = provider has none
    document_input_type: Optional[str] = None   # <<INPUT_TYPE>> for documents
    tokenizer_name: str = ApproxTokenizer.name

    def __post_init__(self) -> None:
        if not self.model or not self.version.strip():
            raise UnpinnedConfig(f"model {self.model!r} has no version: pin the provider's dated version or snapshot id")
        if self.dimensions not in self.supported_dimensions:
            raise UnpinnedConfig(f"dimensions={self.dimensions} is not declared by the model (declared: {self.supported_dimensions}); "
                                 "truncation is allowed only to a declared Matryoshka dimension")
        if self.dtype not in SUPPORTED_DTYPES:
            raise UnpinnedConfig(f"dtype {self.dtype!r} is not one of {SUPPORTED_DTYPES}")
        if self.metric not in SUPPORTED_METRICS:
            raise UnpinnedConfig(f"metric {self.metric!r} is not one of {SUPPORTED_METRICS}")
        if self.max_input_tokens <= 0:
            raise UnpinnedConfig("max_input_tokens must be positive")

    @property
    def native_dimensions(self) -> int:
        return max(self.supported_dimensions)

    def fingerprint(self) -> str:
        pinned = (self.model, self.version, self.dimensions, self.dtype, self.metric,
                  self.query_input_type, self.document_input_type, self.tokenizer_name)
        return hashlib.sha256(json.dumps(pinned).encode("utf-8")).hexdigest()[:16]

    def stack_record(self) -> dict:
        """The block that goes into docs/stack.md (embedding-config-and-versioning.md §1). Generated, never typed."""
        d = asdict(self); d["fingerprint"] = self.fingerprint(); return _plain(d)

    def matches_stack_record(self, record: dict) -> None:
        """Verify 1: the stack document and the configuration must agree field by field (after a JSON round trip)."""
        mine, theirs = self.stack_record(), _plain(record)
        diffs = {k: (theirs.get(k), mine[k]) for k in mine if theirs.get(k) != mine[k]}
        if diffs:
            raise ConfigMismatch(f"docs/stack.md record disagrees with the configuration on {diffs}")


# ---------------------------------------------------------------------------------------------------------- embedders

@dataclass(frozen=True)
class Embedded:
    """A vector that knows where it came from. The index reads these fields; callers cannot hand it a bare list."""
    vector: tuple[float, ...]
    fingerprint: str
    side: str
    model: str


class Embedder:
    """The one code path. Callers pass `side`; the convention (input_type or prefix) is applied here (Verify 2)."""

    def __init__(self, config: EmbeddingConfig, backend: Callable[[list[str], Optional[str]], list[list[float]]]):
        self.config, self._backend = config, backend

    def embed(self, texts: Sequence[str], side: Optional[str] = None) -> list[Embedded]:
        if side not in SIDES:
            raise SideRequired(f"side must be one of {SIDES}, got {side!r}: a query is embedded as a query, a document as a document")
        cfg = self.config
        input_type = cfg.query_input_type if side == "query" else cfg.document_input_type
        out = []
        for v in self._backend(list(texts), input_type):
            if len(v) == cfg.dimensions:
                pass
            elif len(v) == cfg.native_dimensions and cfg.dimensions < cfg.native_dimensions:
                v = v[: cfg.dimensions]            # Matryoshka: native vector cut to a DECLARED dimension (checked at construction), then normalised
            else:
                raise ConfigMismatch(f"backend returned {len(v)} dimensions; the configuration declares {cfg.dimensions} "
                                     f"(native {cfg.native_dimensions}) — not truncating an undeclared length")
            v = _normalise(v) if cfg.metric in ("cosine", "dot") or len(v) < cfg.native_dimensions else v
            out.append(Embedded(tuple(v), cfg.fingerprint(), side, cfg.model))
        return out


def _normalise(v: Sequence[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def make_stub_backend(native_dimensions: int, tokenizer: Tokenizer) -> Callable[[list[str], Optional[str]], list[list[float]]]:
    """<<EMBED_BACKEND>> — a deterministic stub: each token hashes to one dimension with a sign; the input_type convention is
    prepended as text so the query and document vectors of one string differ, as they do on Voyage and Cohere."""
    def backend(texts: list[str], input_type: Optional[str]) -> list[list[float]]:
        vectors = []
        for t in texts:
            s = (f"{input_type}: {t}" if input_type else t)
            v = [0.0] * native_dimensions
            for a, b in tokenizer.encode(s):
                h = int(hashlib.md5(s[a:b].lower().encode("utf-8")).hexdigest(), 16)
                v[h % native_dimensions] += 1.0 if (h >> 8) % 2 else -1.0
            vectors.append(v)
        return vectors
    return backend


# ------------------------------------------------------------------------------------------------------------- chunks

@dataclass
class Chunk:
    text: str                                   # what is embedded: prefix + body
    tokens: int
    spans: list[tuple[str, int, int]] = field(default_factory=list)   # (doc_id, start, end) in the source text, for the harness
    kind: str = "text"                          # text | table | image | code
    page: Optional[int] = None


@dataclass(frozen=True)
class ChunkerRecord:
    strategy: str
    size: int
    overlap: int
    tokenizer_name: str
    options: str = ""


SIZE_RULE = "size counts prefix+body"


class Chunker:
    """Base: every chunker counts in the model's tokens — `size` is the whole embedded text, metadata prefix included —
    and refuses a chunk over the limit (Verify 3)."""
    strategy = "base"

    def __init__(self, config: EmbeddingConfig, tokenizer: Tokenizer, size: int, overlap: int = 0):
        if size <= 0 or overlap < 0 or overlap >= size:
            raise RetrievalConfigError(f"size must be positive and overlap smaller than size (got size={size}, overlap={overlap})")
        self.config, self.tok, self.size, self.overlap = config, tokenizer, size, overlap

    def record(self) -> ChunkerRecord:
        return ChunkerRecord(self.strategy, self.size, self.overlap, self.tok.name, SIZE_RULE)

    def _body_budget(self, prefix: str) -> int:
        budget = self.size - count_tokens(self.tok, prefix)
        if budget < 1:
            raise RetrievalConfigError(f"the metadata prefix alone is {count_tokens(self.tok, prefix)} tokens, size is {self.size}")
        return budget

    def _chunk_text(self, doc_id: str, text: str, prefix: str = "") -> list[Chunk]:
        raise NotImplementedError

    def chunk(self, doc_id: str, text: str, prefix: str = "") -> list[Chunk]:
        """The only public entry: the subclass splits, the base class counts and refuses."""
        return self._enforce_limit(self._chunk_text(doc_id, text, prefix))

    def _enforce_limit(self, chunks: list[Chunk]) -> list[Chunk]:
        for c in chunks:
            c.tokens = count_tokens(self.tok, c.text)
            if c.tokens > self.config.max_input_tokens:
                raise ChunkTooLarge(f"a chunk of {c.tokens} tokens exceeds the model's maximum input of {self.config.max_input_tokens}")
        return chunks

    def _window(self, doc_id: str, text: str, prefix: str, spans: list[tuple[int, int]]) -> list[Chunk]:
        """Slide a window of `size - prefix` tokens with `overlap` over token spans; a chunk's text is the source slice."""
        width = self._body_budget(prefix)
        out, i, step = [], 0, max(1, width - self.overlap)
        while i < len(spans):
            window = spans[i: i + width]
            a, b = window[0][0], window[-1][1]
            out.append(Chunk(prefix + text[a:b], 0, [(doc_id, a, b)]))
            if i + width >= len(spans):
                break
            i += step
        return out


class FixedTokenChunker(Chunker):
    """Level 1: fixed window in tokens with optional overlap ("I don't know anybody that does this in production" — Kamradt 2024-01)."""
    strategy = "fixed"

    def _chunk_text(self, doc_id: str, text: str, prefix: str = "") -> list[Chunk]:
        return self._window(doc_id, text, prefix, self.tok.encode(text))


class RecursiveChunker(Chunker):
    """Level 2–3: split on a prioritised separator list, merge pieces up to `size` tokens (prefix included); Chroma's
    separators by default. `overlap` is applied in tokens between consecutive chunks (0 recommended: Chroma found overlap
    lowers IoU)."""
    strategy = "recursive"

    def __init__(self, config, tokenizer, size, overlap=0, separators: Optional[list[str]] = None):
        super().__init__(config, tokenizer, size, overlap)
        self.separators = separators or CHROMA_SEPARATORS

    def record(self) -> ChunkerRecord:
        return ChunkerRecord(self.strategy, self.size, self.overlap, self.tok.name, f"{SIZE_RULE}; separators={self.separators!r}")

    def _split(self, text: str, seps: list[str], budget: int) -> list[str]:
        if count_tokens(self.tok, text) <= budget or not seps:
            return [text]
        sep, rest = seps[0], seps[1:]
        if sep == "":
            spans = self.tok.encode(text)
            return [text[spans[i][0]: spans[min(i + budget, len(spans)) - 1][1]] for i in range(0, len(spans), budget)]
        parts = [p + sep for p in text.split(sep)]
        parts[-1] = parts[-1][: -len(sep)] if parts[-1].endswith(sep) else parts[-1]
        pieces: list[str] = []
        for p in parts:
            pieces.extend(self._split(p, rest, budget) if count_tokens(self.tok, p) > budget else [p])
        return [p for p in pieces if p.strip()]

    def _chunk_text(self, doc_id: str, text: str, prefix: str = "") -> list[Chunk]:
        budget = self._body_budget(prefix)
        pieces, merged, cur = self._split(text, self.separators, budget), [], ""
        for p in pieces:
            if cur and count_tokens(self.tok, cur + p) > budget:
                merged.append(cur); cur = p
            else:
                cur += p
        if cur.strip():
            merged.append(cur)
        out, pos = [], 0
        for m in merged:
            a = text.find(m, pos); a = pos if a < 0 else a; b = a + len(m); pos = b
            out.append(Chunk(prefix + m, 0, [(doc_id, a, b)]))
        if self.overlap:
            for i in range(1, len(out)):
                tail = self.tok.encode(out[i - 1].text[len(prefix):])[-self.overlap:]
                if tail:
                    _, pa, pb = out[i - 1].spans[0]
                    out[i].text = prefix + out[i - 1].text[len(prefix) + tail[0][0]:] + out[i].text[len(prefix):]
                    out[i].spans.insert(0, (doc_id, pa + tail[0][0], pb))   # the overlap counts as retrieved tokens (IoU penalises it)
        return out


class StructureAwareChunker(Chunker):
    """Element-aware chunking over data-ingestion's `Element` list (Unstructured's rules, read 2026-10-01; Ebbelaar 2025-02):
    a table is one chunk, or row groups with the header repeated (a table under two rows is refused — nothing to embed);
    a title is carried FORWARD into the chunk of whatever follows it (paragraph, table, image), never left alone and
    never attached backwards; consecutive small text elements merge up to `size` (prefix included); a single text element
    over `size` is handed to `RecursiveChunker` with the same tokenizer and prefix (`options` says `oversize=recursive`);
    `by_page=True` never merges across pages; every chunk starts with the envelope's metadata prefix (Liu 2024-05: file
    path, title, author, date as text in the chunk). A title that is the LAST element of a document has nothing to carry
    into; it is appended to the last chunk as plain text (no heading marker) so no heading stands apart."""
    strategy = "structure-aware"

    def __init__(self, config, tokenizer, size, by_page: bool = False):
        super().__init__(config, tokenizer, size, 0)
        self.by_page = by_page
        self._recursive = RecursiveChunker(config, tokenizer, size, 0)

    def record(self) -> ChunkerRecord:
        return ChunkerRecord(self.strategy, self.size, 0, self.tok.name, f"{SIZE_RULE}; by_page={self.by_page}; oversize=recursive")

    def _chunk_text(self, doc_id: str, text: str, prefix: str = "") -> list[Chunk]:
        """Plain text has no tree: paragraphs become text elements on one page."""
        els = [DemoElement("text", m.group(), 1, span=(doc_id, m.start(), m.end())) for m in re.finditer(r"[^\n]+(?:\n(?!\n)[^\n]+)*", text)]
        return self.chunk_elements(doc_id, els, prefix)

    def chunk_elements(self, doc_id: str, elements: Sequence, prefix: str) -> list[Chunk]:
        out: list[Chunk] = []
        titles: list = []                                         # headings waiting for the next body
        buf: list = []                                            # pending text/list elements (titles included, in order)

        def heading(t) -> str:
            return f"# {t.text}\n"

        def flush():
            if buf:
                body = "\n".join(heading(e).rstrip("\n") if e.type == "title" else e.text for e in buf)
                spans = [sp for e in buf if (sp := getattr(e, "span", None))]       # plain-text elements carry their source span
                out.append(Chunk(prefix + body, 0, spans, "text", buf[0].page)); buf.clear()

        def take_titles() -> str:
            """Pop trailing titles off the text buffer and join them with the waiting ones: they move FORWARD."""
            while buf and buf[-1].type == "title":
                titles.insert(0, buf.pop())
            lead = "".join(heading(t) for t in titles); titles.clear()
            return lead

        for el in elements:
            if el.type == "table":
                lead = take_titles(); flush()
                out.extend(self._table_chunks(el, prefix, lead))
            elif el.type in ("image", "code"):
                lead = take_titles(); flush()
                out.append(Chunk(prefix + lead + el.to_embedding_text(), 0, [], el.type, el.page))
            elif el.type == "title":
                buf.append(el)
            else:
                lead = "".join(heading(t) for t in buf if t.type == "title") if all(e.type == "title" for e in buf) else ""
                alone = prefix + lead + el.text
                if count_tokens(self.tok, alone) > self.size:                      # one element over size: recursive split, title carried
                    lead = take_titles(); flush()
                    out.extend(self._recursive.chunk(doc_id, el.text, prefix + lead))
                    continue
                candidate = "\n".join([*(heading(e).rstrip("\n") if e.type == "title" else e.text for e in buf), el.text])
                if buf and (count_tokens(self.tok, prefix + candidate) > self.size or (self.by_page and buf[0].page != el.page)):
                    lead = take_titles(); flush()
                    for t in list(self._titles_from(lead)):
                        buf.append(t)
                buf.append(el)
        if buf and all(e.type == "title" for e in buf) and out:    # document ends with a heading: nothing to carry into
            out[-1].text += "\n" + "\n".join(e.text for e in buf); buf.clear()
        flush()
        return self._enforce_limit(out)

    @staticmethod
    def _titles_from(lead: str):
        for line in lead.splitlines():
            yield DemoElement("title", line[2:], None)

    def _table_chunks(self, table, prefix: str, lead: str = "") -> list[Chunk]:
        rows = table.rows or []
        if len(rows) < 2:
            raise StructureViolation(f"table on page {table.page} has {len(rows)} row(s): a header-only or unparsed table has nothing to embed")
        head, body = rows[0], rows[1:]
        groups, cur = [], []
        for r in body:
            trial = _rows_to_text([head, *cur, r])
            if cur and count_tokens(self.tok, prefix + lead + trial) > self.size:
                groups.append(cur); cur = [r]
            else:
                cur.append(r)
        if cur:
            groups.append(cur)
        return [Chunk(prefix + (lead if i == 0 else "") + _rows_to_text([head, *g]), 0, [], "table", table.page) for i, g in enumerate(groups)]


def _rows_to_text(rows: list[list[str]]) -> str:
    """The embedding-text view of a table (data-ingestion's `to_embedding_text`): columns named, one sentence per row."""
    head, *body = rows
    return "Table with columns " + ", ".join(head) + ". " + ". ".join("; ".join(f"{h} is {c}" for h, c in zip(head, r)) for r in body) + "."


_HEADING = re.compile(r"#\s*\S[^\n]*")


def check_structure(chunks: list[Chunk], elements: Sequence, prefix: str) -> None:
    """Verify 4 as a mechanical check: every chunk carries the prefix; no chunk is only a heading; no chunk ENDS with a
    heading (a heading apart from its first paragraph); every table row of every table element appears whole inside one
    chunk of kind table (no row split, no table merged with prose)."""
    for c in chunks:
        if prefix and not c.text.startswith(prefix):
            raise StructureViolation("a chunk does not start with the envelope's metadata prefix")
        body = c.text[len(prefix):].strip()
        if _HEADING.fullmatch(body):
            raise StructureViolation(f"a lone-heading chunk: {body[:40]!r}")
        last = body.rsplit("\n", 1)[-1].strip()
        if "\n" in body and _HEADING.fullmatch(last):
            raise StructureViolation(f"a chunk ends with a heading apart from its paragraph: {last[:40]!r}")
    for el in elements:
        if el.type == "table" and el.rows and len(el.rows) > 1:
            head = el.rows[0]
            for r in el.rows[1:]:
                sentence = "; ".join(f"{h} is {c}" for h, c in zip(head, r))
                holders = [c for c in chunks if sentence in c.text]
                if not holders:
                    raise StructureViolation(f"table row {r[:2]}… is split across chunks or missing")
                if any(ch.kind != "table" for ch in holders):
                    raise StructureViolation("a table row sits in a prose chunk: the table was merged with text")


PREFIX_FIELDS = ("filename", "title", "page", "document_date")


def metadata_prefix(envelope) -> str:
    """Render the envelope fields the chunk should carry as text — filename, title, page, document_date (Liu's blog,
    2024-05-11). Accepts data-ingestion's pydantic `Envelope` or a plain dict. Owner and tenant stay in metadata and are
    filtered in the store (principles/16 §3.7); they are never embedded — that is this folder's rule, not a privacy
    guarantee of data-ingestion's Verify."""
    get = envelope.get if isinstance(envelope, dict) else (lambda k, default=None: getattr(envelope, k, default))
    return " | ".join(f"{k}: {get(k)}" for k in PREFIX_FIELDS if get(k) is not None) + "\n"


# ----------------------------------------------------------------------------------------------------- manifest/index

@dataclass
class EvalRecord:
    fixture: str                    # path of the fixture file; `require_eval` re-counts its questions
    questions: int
    k: int
    compared: dict[str, dict]       # chunker label -> metrics (must carry METRIC_KEYS)
    chosen: str
    floor_recall: float
    date: str


@dataclass
class IndexManifest:
    config_fingerprint: str
    dimensions: int
    chunker: Optional[ChunkerRecord] = None
    corpus_hash: str = ""
    eval: Optional[EvalRecord] = None

    def check(self, config: EmbeddingConfig) -> None:
        if self.config_fingerprint != config.fingerprint():
            raise ConfigMismatch(f"manifest fingerprint {self.config_fingerprint} ≠ configuration {config.fingerprint()}: another model, version, dimension, dtype, metric or convention")
        if self.dimensions != config.dimensions:
            raise ConfigMismatch(f"manifest dimensions {self.dimensions} ≠ configuration {config.dimensions}")
        if self.chunker is None:
            raise ManifestIncomplete("manifest has no chunker record (strategy, size, overlap, tokenizer)")
        if self.chunker.tokenizer_name != config.tokenizer_name:
            raise ConfigMismatch(f"chunker counted with {self.chunker.tokenizer_name!r}, configuration pins {config.tokenizer_name!r}")


def require_eval(manifest: IndexManifest) -> None:
    """Verify 5: an index is built only after a comparison of at least two chunkers on at least MIN_QUESTIONS questions.
    The record is not trusted: the fixture file is opened and its questions re-counted; every compared entry must carry
    the four metrics."""
    ev = manifest.eval
    if ev is None:
        raise EvalRequired("no retrieval eval record: build the eval set and compare chunkers before the index")
    try:
        with open(ev.fixture, encoding="utf-8") as f:
            n_file = len(json.load(f)["questions"])
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise EvalRequired(f"eval fixture {ev.fixture} cannot be read ({e.__class__.__name__}): the record points at nothing usable")
    if ev.questions != n_file:
        raise EvalRequired(f"eval record says {ev.questions} questions, the fixture holds {n_file}: the record is stale or forged")
    if n_file < MIN_QUESTIONS:
        raise EvalRequired(f"eval set has {n_file} questions; at least {MIN_QUESTIONS} required")
    if len(ev.compared) < 2:
        raise EvalRequired(f"eval record compares {len(ev.compared)} chunker(s); the chosen one needs at least one alternative")
    for label, m in ev.compared.items():
        missing = [k for k in METRIC_KEYS if k not in m]
        if missing:
            raise EvalRequired(f"compared chunker {label!r} lacks metrics {missing}: run chunk_eval, do not type numbers")
    if ev.chosen not in ev.compared:
        raise EvalRequired("the chosen chunker is not among the compared ones")


class InMemoryIndex:
    """Stand-in for the store. Keep the refusals in front of any real store's own (Verify 1, 2, 5, 7)."""

    def __init__(self, manifest: IndexManifest, config: EmbeddingConfig):
        manifest.check(config); require_eval(manifest)
        self.manifest, self.config, self.rows = manifest, config, []

    @classmethod
    def build(cls, manifest: IndexManifest, config: EmbeddingConfig) -> "InMemoryIndex":
        return cls(manifest, config)

    def _accept(self, e: Embedded, side: str) -> None:
        if not isinstance(e, Embedded):
            raise ConfigMismatch("only vectors tagged by Embedder.embed enter or query this index")
        if e.fingerprint != self.manifest.config_fingerprint:
            raise ConfigMismatch(f"vector embedded under {e.fingerprint} ({e.model}), index is {self.manifest.config_fingerprint}: re-embed behind a new index")
        if e.side != side:
            raise SideRequired(f"a {e.side}-side vector cannot be used as a {side}: embed it with side={side!r}")
        if len(e.vector) != self.manifest.dimensions:
            raise ConfigMismatch(f"vector has {len(e.vector)} dimensions, index has {self.manifest.dimensions}")

    def upsert(self, chunk: Chunk, embedded: Embedded) -> None:
        self._accept(embedded, "document")
        self.rows.append((chunk, embedded.vector))

    def search(self, query: Union[str, Embedded], embedder: Optional[Embedder] = None, k: int = 5) -> list[Chunk]:
        if isinstance(query, str):
            if embedder is None or embedder.config.fingerprint() != self.manifest.config_fingerprint:
                raise ConfigMismatch("query embedder is not the index's configuration")
            query = embedder.embed([query], side="query")[0]
        self._accept(query, "query")
        q = query.vector
        scored = sorted(self.rows, key=lambda cv: -sum(a * b for a, b in zip(q, cv[1])))
        return [c for c, _ in scored[:k]]


# ---------------------------------------------------------------------------------------------------------- the eval

def make_eval_set(corpus: dict[str, str], llm: Optional[Callable] = None) -> dict:
    """ADAPTER STUB — Chroma's method (2024-07-03): for each sampled document ask an LLM for a question and the verbatim
    excerpts that answer it; keep only excerpts that match the corpus exactly; reject compound questions and
    near-duplicates; ~US$0.01 per question as Chroma reported. Wire the repo's one LLM client here; until then the demo
    uses `write_demo_fixture()`. Real user queries with their judged excerpts replace synthetic ones as they arrive."""
    raise NotImplementedError("wire the LLM client (chunk-eval-harness.md §2); the demo fixture is write_demo_fixture()")


def write_demo_fixture(path: str, corpus: dict[str, str], questions_per_doc: int) -> dict:
    """Tiny offline generator for the demo and tests ONLY: each question is a sentence of the corpus and its excerpt is
    that sentence's span — exact-match by construction, no LLM, deterministic."""
    qs = []
    for doc_id, text in corpus.items():
        for m in list(re.finditer(r"[^.!?]+[.!?]", text))[:questions_per_doc]:
            qs.append({"question": m.group().strip(), "excerpts": [{"doc": doc_id, "start": m.start(), "end": m.end()}]})
    fixture = {"corpus": corpus, "questions": qs, "generator": "write_demo_fixture (demo only)"}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=1)
    return fixture


def chunk_eval(fixture: dict, chunker: Chunker, embedder: Embedder, k: int) -> dict:
    """Token-level metrics (Chroma 2024-07-03): recall = excerpt tokens retrieved / excerpt tokens; precision = excerpt
    tokens retrieved / all retrieved tokens (overlap counted every time it is retrieved); IoU = excerpt tokens retrieved,
    once each, / (all retrieved tokens + excerpt tokens not retrieved); Precision_Omega = precision when exactly the chunks
    holding excerpt tokens are retrieved. Prefix tokens are not source tokens and are left out of the counts."""
    tok, corpus = chunker.tok, fixture["corpus"]
    chunks = [c for d, t in corpus.items() for c in chunker.chunk(d, t)]
    vecs = [e.vector for e in embedder.embed([c.text for c in chunks], side="document")]
    tokens_of = {d: tok.encode(t) for d, t in corpus.items()}

    def covered(doc: str, a: int, b: int) -> set[int]:
        return {i for i, (s, e) in enumerate(tokens_of[doc]) if s >= a and e <= b}

    chunk_tokens = [{(d, i) for d, a, b in c.spans for i in covered(d, a, b)} for c in chunks]
    sums = {m: 0.0 for m in METRIC_KEYS}
    for q in fixture["questions"]:
        qv = embedder.embed([q["question"]], side="query")[0].vector
        order = sorted(range(len(chunks)), key=lambda i: -sum(x * y for x, y in zip(qv, vecs[i])))[:k]
        excerpt = {(e["doc"], i) for e in q["excerpts"] for i in covered(e["doc"], e["start"], e["end"])}
        retrieved_multiset = sum(len(chunk_tokens[i]) for i in order)
        hit = set().union(*(chunk_tokens[i] for i in order)) & excerpt if order else set()
        holders = [i for i, ct in enumerate(chunk_tokens) if ct & excerpt]
        omega_total = sum(len(chunk_tokens[i]) for i in holders)
        sums["recall"] += len(hit) / (len(excerpt) or 1)
        sums["precision"] += len(hit) / (retrieved_multiset or 1)
        sums["iou"] += len(hit) / ((retrieved_multiset + len(excerpt) - len(hit)) or 1)
        sums["precision_omega"] += len(excerpt) / omega_total if holders else 0.0
    n = len(fixture["questions"]) or 1
    out = {m: round(v / n, 4) for m, v in sums.items()}
    out.update(chunks=len(chunks), questions=len(fixture["questions"]), k=k, chunker=asdict(chunker.record()))
    return out


# ------------------------------------------------------------------------------------------------------------- demo

class DemoElement:
    """Minimal stand-in with the duck-typed surface of data-ingestion's `Element` (type, text, page, rows, caption)."""
    def __init__(self, type: str, text: str, page, rows=None, caption=None, span=None):
        self.type, self.text, self.page, self.rows, self.caption, self.span = type, text, page, rows, caption, span

    def to_embedding_text(self) -> str:
        if self.type == "table" and self.rows and len(self.rows) > 1:
            return _rows_to_text(self.rows)
        if self.type == "image":
            return f"Image: {self.caption or 'no caption'}"
        return self.text


# The reference `--check` runs with THIS configuration and the stub embedder: it tests the chunker offline. In a repo,
# replace DEMO_CONFIG with the configuration read from the index manifest / docs/stack.md and the backend with the real one
# (README.md Adapt; chunk-eval-harness.md §5).
DEMO_CONFIG = dict(model="demo-embed-3", version="2024-01-25", dimensions=1536, supported_dimensions=(1536,), dtype="float32",
                   metric="cosine", max_input_tokens=8192, query_input_type="query", document_input_type="document")


def _demo_corpus() -> dict[str, str]:
    topics = ["refund policy", "shipping zones", "warranty terms", "account security", "billing cycles", "data retention"]
    verbs = ["is handled", "is reviewed", "is escalated", "is archived", "is billed", "is audited"]
    corpus = {}
    for n, topic in enumerate(topics):
        sentences = [f"Clause {n}.{i} of the {topic} states that item {i * 7 % 23} {verbs[i % 6]} within {i + 2} business days by team {chr(65 + i % 9)}."
                     for i in range(24)]
        corpus[f"doc-{n}"] = "\n\n".join(" ".join(sentences[j: j + 3]) for j in range(0, 24, 3))
    return corpus


def run_check(fixture_path: str, chunker_name: str, size: int, overlap: int, k: int, floor: float, min_questions: int) -> int:
    """Verify 9: exit 2 = no usable eval set or invalid arguments, exit 1 = below the floor, exit 0 = pass. Deterministic,
    no judge, offline. `min_questions` can only RAISE the floor MIN_QUESTIONS, never lower it."""
    floor_q = max(MIN_QUESTIONS, min_questions)
    if not os.path.exists(fixture_path):
        print(f"REFUSED: eval fixture {fixture_path} is missing (exit 2)"); return 2
    try:
        with open(fixture_path, encoding="utf-8") as f:
            fixture = json.load(f)
        questions = fixture["questions"]; fixture["corpus"]
    except (ValueError, KeyError, TypeError) as e:
        print(f"REFUSED: eval fixture {fixture_path} is malformed ({e.__class__.__name__}: {str(e)[:60]}) (exit 2)"); return 2
    if len(questions) < floor_q:
        print(f"REFUSED: eval fixture has {len(questions)} questions, fewer than {floor_q} (exit 2)"); return 2
    tok = ApproxTokenizer(); config = EmbeddingConfig(**DEMO_CONFIG)
    embedder = Embedder(config, make_stub_backend(config.native_dimensions, tok))
    try:
        cls = {"recursive": RecursiveChunker, "fixed": FixedTokenChunker, "structure-aware": StructureAwareChunker}[chunker_name]
        ch = cls(config, tok, size) if chunker_name == "structure-aware" else cls(config, tok, size, overlap)
    except RetrievalConfigError as e:
        print(f"REFUSED: chunker arguments invalid: {e} (exit 2)"); return 2
    m = chunk_eval(fixture, ch, embedder, k)
    print(f"check: {chunker_name} {size}/{overlap} k={k} → recall {m['recall']} precision {m['precision']} "
          f"precision_omega {m['precision_omega']} iou {m['iou']} ({m['chunks']} chunks, {m['questions']} questions)")
    if m["recall"] < floor:
        print(f"REFUSED: recall {m['recall']} is below the recorded floor {floor} (exit 1)"); return 1
    print(f"check: OK (floor {floor})"); return 0


def demo() -> int:
    passed = 0
    def ok(msg): nonlocal passed; passed += 1; print(f"  ok   {msg}")
    def refused(label, fn, exc=RetrievalConfigError):
        nonlocal passed
        try:
            fn()
        except exc as e:
            passed += 1; print(f"  REFUSED {label}: {str(e)[:120]}"); return
        print(f"  FAIL {label}: nothing was refused"); raise SystemExit(1)

    tok = ApproxTokenizer()
    tmp = tempfile.mkdtemp(prefix="s7-demo-")
    print(f"demo: tokenizer = {tok.name}")
    print("\n[1] one pinned configuration (Verify 1)")
    refused("unversioned model", lambda: EmbeddingConfig(**{**DEMO_CONFIG, "version": " "}), UnpinnedConfig)
    refused("undeclared dimension 512 on a model declaring (1536,)", lambda: EmbeddingConfig(**{**DEMO_CONFIG, "dimensions": 512}), UnpinnedConfig)
    refused("unsupported dtype int4", lambda: EmbeddingConfig(**{**DEMO_CONFIG, "dtype": "int4"}), UnpinnedConfig)
    config = EmbeddingConfig(**DEMO_CONFIG); ok(f"configuration pinned, fingerprint {config.fingerprint()}")
    record_path = os.path.join(tmp, "stack-record.json")
    json.dump(config.stack_record(), open(record_path, "w", encoding="utf-8"))
    config.matches_stack_record(json.load(open(record_path, encoding="utf-8")))
    ok("docs/stack.md record written to JSON, read back (tuples became lists) and matched against the configuration")
    refused("stack record read back with another version", lambda: config.matches_stack_record({**json.load(open(record_path, encoding="utf-8")), "version": "2023-11"}), ConfigMismatch)
    other = EmbeddingConfig(**{**DEMO_CONFIG, "model": "demo-embed-4", "dimensions": 1024, "supported_dimensions": (1024, 256)})
    refused("manifest built from another configuration", lambda: IndexManifest(other.fingerprint(), 1024, ChunkerRecord("fixed", 200, 0, tok.name)).check(config), ConfigMismatch)

    print("\n[3] a declared chunker counting in the model's tokens (Verify 3)")
    big = " ".join(f"word{i}" for i in range(9000))
    refused("a 9,000-token element under an 8,192-token limit", lambda: FixedTokenChunker(config, tok, 9000).chunk("big", big), ChunkTooLarge)
    rec = RecursiveChunker(config, tok, 60); ok(f"recursive chunker declared: {asdict(rec.record())}")
    refused("manifest without a chunker record", lambda: IndexManifest(config.fingerprint(), 1536, None).check(config), ManifestIncomplete)
    refused("manifest whose chunker counted with another tokenizer", lambda: IndexManifest(config.fingerprint(), 1536, ChunkerRecord("recursive", 60, 0, "cl100k_base")).check(config), ConfigMismatch)

    print("\n[4] chunks follow the element tree (Verify 4)")
    rows = [["Plan", "Refund window", "Fee"]] + [[f"Plan {i}", f"{10 + i} days", f"{i} USD"] for i in range(40)]
    elements = [DemoElement("title", "Refund policy", 1),
                DemoElement("text", "Refunds are granted within the window of the plan. " * 6, 1),
                DemoElement("text", "A fee applies to plans above the basic tier. " * 6, 1),
                DemoElement("table", "", 2, rows=rows),
                DemoElement("image", "", 2, caption="Flowchart of the refund decision")]
    prefix = metadata_prefix({"filename": "refunds.pdf", "title": "Refund policy", "page": 1, "document_date": "2026-03-01"})
    chunker = StructureAwareChunker(config, tok, 120)
    sa = chunker.chunk_elements("refunds", elements, prefix)
    check_structure(sa, elements, prefix)
    tables = [c for c in sa if c.kind == "table"]
    assert all(c.text[len(prefix):].startswith("Table with columns Plan, Refund window, Fee.") for c in tables)
    assert sa[0].text[len(prefix):].startswith("# Refund policy\nRefunds are granted"), sa[0].text[:80]
    assert all(c.tokens <= 120 for c in sa)
    ok(f"[title, text, text, table, image]: {len(sa)} chunks — title inside the first paragraph's chunk, the 40-row table in {len(tables)} row groups each starting with the header, the image as its caption, prefix on every chunk, every chunk ≤ 120 tokens prefix included")
    tt = chunker.chunk_elements("tt", [DemoElement("title", "Fees", 2), DemoElement("table", "", 2, rows=rows[:6])], prefix)
    check_structure(tt, [], prefix)
    assert len(tt) == 1 and tt[0].kind == "table" and tt[0].text[len(prefix):].startswith("# Fees\nTable with columns"), tt[0].text[:90]
    ok("[title, table]: one table chunk starting with '# Fees' — the title carried forward, no lone heading")
    tti = chunker.chunk_elements("tti", [DemoElement("text", "Refunds are granted within the window of the plan.", 1), DemoElement("title", "Decision flow", 1),
                                         DemoElement("image", "", 1, caption="Flowchart of the refund decision")], prefix)
    check_structure(tti, [], prefix)
    assert tti[0].kind == "text" and not tti[0].text.rstrip().endswith("Decision flow") and tti[1].text[len(prefix):].startswith("# Decision flow\nImage:"), [c.text for c in tti]
    ok("[text, title, image]: the title opens the image chunk, not the end of the paragraph")
    long_par = " ".join(f"sentence {i} of a very long paragraph about refunds." for i in range(400))
    assert count_tokens(tok, long_par) > 3000
    big_chunks = chunker.chunk_elements("big", [DemoElement("title", "Long section", 1), DemoElement("text", long_par, 1)], prefix)
    check_structure(big_chunks, [], prefix)
    assert len(big_chunks) > 20 and all(c.tokens <= 120 for c in big_chunks) and big_chunks[0].text[len(prefix):].startswith("# Long section\n")
    ok(f"a {count_tokens(tok, long_par):,}-token paragraph at size=120 handed to the recursive splitter: {len(big_chunks)} chunks, title on the first, record options {chunker.record().options!r}")
    refused("a header-only table (one row)", lambda: chunker.chunk_elements("h", [DemoElement("table", "", 1, rows=rows[:1])], prefix), StructureViolation)
    split_row = _rows_to_text(rows[:3]); cut = split_row.index("Plan 1")
    refused("a table row split across two chunks", lambda: check_structure([Chunk(prefix + split_row[:cut], 0, [], "table"), Chunk(prefix + split_row[cut:], 0, [], "table")],
                                                                              [DemoElement("table", "", 1, rows=rows[:3])], prefix), StructureViolation)
    refused("a table row inside a prose chunk", lambda: check_structure([Chunk(prefix + "Some prose. " + _rows_to_text(rows[:3]), 0, [], "text")],
                                                                          [DemoElement("table", "", 1, rows=rows[:3])], prefix), StructureViolation)
    refused("a lone-heading chunk", lambda: check_structure([Chunk(prefix + "# Refund policy", 0)], [], prefix), StructureViolation)
    refused("a chunk ending with a heading", lambda: check_structure([Chunk(prefix + "Refunds are granted within the window.\n# Fees", 0)], [], prefix), StructureViolation)
    refused("a chunk without the metadata prefix", lambda: check_structure([Chunk("Refunds are granted within the window.", 0)], [], prefix), StructureViolation)

    print("\n[5] no index without an eval record (Verify 5)")
    fixture_path = os.path.join(tmp, "fixture.json")
    fixture = write_demo_fixture(fixture_path, _demo_corpus(), 10)
    embedder = Embedder(config, make_stub_backend(1536, tok))
    manifest = IndexManifest(config.fingerprint(), 1536, rec.record(), corpus_hash="demo")
    refused("Index.build() with no eval record", lambda: InMemoryIndex.build(manifest, config), EvalRequired)
    r60 = chunk_eval(fixture, rec, embedder, k=5)
    manifest.eval = EvalRecord(fixture_path, len(fixture["questions"]), 5, {"recursive-60-0": r60}, "recursive-60-0", r60["recall"], "2026-10-04")
    refused("eval record naming one chunker only", lambda: InMemoryIndex.build(manifest, config), EvalRequired)
    f60 = chunk_eval(fixture, FixedTokenChunker(config, tok, 60, 20), embedder, k=5)
    manifest.eval.compared["fixed-60-20"] = f60
    small = os.path.join(tmp, "small.json"); write_demo_fixture(small, {"d": fixture["corpus"]["doc-0"]}, 4)
    forged = IndexManifest(config.fingerprint(), 1536, rec.record(), eval=EvalRecord(small, 60, 5, dict(manifest.eval.compared), "recursive-60-0", 0.5, "2026-10-04"))
    refused("eval record claiming 60 questions over a 4-question fixture", lambda: InMemoryIndex.build(forged, config), EvalRequired)
    typed = IndexManifest(config.fingerprint(), 1536, rec.record(), eval=EvalRecord(fixture_path, 60, 5, {"recursive-60-0": r60, "typed-in": {"recall": 0.99}}, "recursive-60-0", 0.5, "2026-10-04"))
    refused("compared chunker with typed-in numbers (metrics missing)", lambda: InMemoryIndex.build(typed, config), EvalRequired)
    for label, m in manifest.eval.compared.items():
        print(f"       {label:16s} recall {m['recall']:.3f}  precision {m['precision']:.3f}  precision_omega {m['precision_omega']:.3f}  iou {m['iou']:.3f}  chunks {m['chunks']}")
    index = InMemoryIndex.build(manifest, config); ok(f"index built after comparing recursive-60-0 and fixed-60-20 on {len(fixture['questions'])} questions re-counted from the fixture file")

    print("\n[2] one embed path with a side; the index reads the tag (Verify 2)")
    refused("embed(side=None)", lambda: embedder.embed(["hello"]), SideRequired)
    refused("embed(side='passage')", lambda: embedder.embed(["hello"], side="passage"), SideRequired)
    q, d = embedder.embed(["refund within 14 days"], side="query")[0], embedder.embed(["refund within 14 days"], side="document")[0]
    cos = sum(a * b for a, b in zip(q.vector, d.vector)); assert cos < 0.999, cos
    ok(f"the same text embedded as query and as document differs (cosine {cos:.3f}); each result is tagged (fingerprint, side, model)")
    chunks = rec.chunk("doc-0", fixture["corpus"]["doc-0"])
    refused("upsert of a QUERY-side vector", lambda: index.upsert(chunks[0], q), SideRequired)
    refused("search with a DOCUMENT-side vector", lambda: index.search(d, k=3), SideRequired)
    refused("backend returning 2048 dimensions for a model declaring (1536,)", lambda: Embedder(config, lambda texts, it: [[0.1] * 2048 for _ in texts]).embed(["x"], side="document"), ConfigMismatch)
    mrl = EmbeddingConfig(**{**DEMO_CONFIG, "model": "demo-mrl", "dimensions": 256, "supported_dimensions": (1024, 256)})
    cut_v = Embedder(mrl, make_stub_backend(1024, tok)).embed([fixture["corpus"]["doc-1"]], side="document")[0]
    assert len(cut_v.vector) == 256 and abs(math.sqrt(sum(x * x for x in cut_v.vector)) - 1) < 1e-9
    ok("a 1024-dimensional native vector cut to the DECLARED Matryoshka dimension 256 and normalised")

    print("\n[7] no index holds two configurations (Verify 7)")
    for c, e in zip(chunks, embedder.embed([c.text for c in chunks], side="document")):
        index.upsert(c, e)
    n = len(index.rows)
    other_same_dims = EmbeddingConfig(**{**DEMO_CONFIG, "model": "demo-embed-4"})
    other_embedder = Embedder(other_same_dims, make_stub_backend(1536, tok))
    refused("upsert of a vector from Embedder(other_config) with the SAME 1536 dimensions", lambda: index.upsert(chunks[0], other_embedder.embed([chunks[0].text], side="document")[0]), ConfigMismatch)
    refused("upsert of a hand-built 256-dimensional Embedded under the right fingerprint", lambda: index.upsert(chunks[0], Embedded((0.1,) * 256, config.fingerprint(), "document", config.model)), ConfigMismatch)
    refused("upsert of a bare list instead of an Embedded", lambda: index.upsert(chunks[0], [0.1] * 1536), ConfigMismatch)
    refused("search with an embedder of another model", lambda: index.search("fee", other_embedder, 3), ConfigMismatch)
    assert len(index.rows) == n; ok(f"index count unchanged at {n} after the refusals; search with the index's embedder returns {len(index.search('fee for plans', embedder, 3))} chunks")

    print("\n[9] the eval as a CI gate (Verify 9)")
    assert run_check(os.path.join(tmp, "missing.json"), "recursive", 60, 0, 5, 0.5, MIN_QUESTIONS) == 2; passed += 1
    bad = os.path.join(tmp, "bad.json"); open(bad, "w").write("{not json")
    assert run_check(bad, "recursive", 60, 0, 5, 0.5, MIN_QUESTIONS) == 2; passed += 1
    assert run_check(small, "recursive", 60, 0, 5, 0.5, 1) == 2; passed += 1          # --min-questions 1 cannot lower the floor of 50
    assert run_check(fixture_path, "recursive", 60, 60, 5, 0.5, MIN_QUESTIONS) == 2; passed += 1
    assert run_check(fixture_path, "recursive", 60, 0, 5, 0.99, MIN_QUESTIONS) == 1; passed += 1
    assert run_check(fixture_path, "recursive", 60, 0, 5, manifest.eval.floor_recall, MIN_QUESTIONS) == 0; passed += 1
    print(f"\ndemo: {passed} checks passed; fixture at {fixture_path}")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--demo", action="store_true", help="offline walk through every refusal of the enforcement table")
    p.add_argument("--check", action="store_true", help="CI gate: run the retrieval eval on --fixture; exit 2 missing/malformed/small/invalid args, 1 below floor")
    p.add_argument("--fixture", default="evals/retrieval/fixture.json")
    p.add_argument("--chunker", default="recursive", choices=["recursive", "fixed", "structure-aware"])
    p.add_argument("--size", type=int, default=200); p.add_argument("--overlap", type=int, default=0)
    p.add_argument("--k", type=int, default=5); p.add_argument("--floor", type=float, default=0.85)
    p.add_argument("--min-questions", type=int, default=MIN_QUESTIONS, help=f"may raise the floor above {MIN_QUESTIONS}, never lower it")
    a = p.parse_args(argv)
    if a.demo:
        return demo()
    if a.check:
        return run_check(a.fixture, a.chunker, a.size, a.overlap, a.k, a.floor, a.min_questions)
    p.print_help(); return 0


if __name__ == "__main__":
    sys.exit(main())
