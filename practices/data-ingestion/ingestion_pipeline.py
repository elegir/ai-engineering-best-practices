"""ingestion_pipeline.py — the ONE path by which a document becomes elements in the product's index.

Copy to <repo>/src/<package>/ingestion/pipeline.py. Replace <<PARSER>> (the real parser behind the `Parser` adapter —
Docling, Unstructured, a vendor API), <<CORPUS_PATH>> and point `Store` at the real backend (a table with an `owner`
and a `tenant` column, Row Level Security where the store is Postgres). Nothing else in the repo writes to the index:
every document goes audit -> parse -> scrub -> envelope -> upsert, and every removal goes through `tombstone()` or
`erase_subject()`.

What this buys you (principles/16-data-for-ai-products.md):
  * an AUDIT REPORT per corpus — counts by type, duplicates by content hash, empty or garbled pages by text density,
    PII hits by class, date coverage, sources with no owner — and `sync_corpus()` REFUSES to run without one, with
    a stale one (parser version differs) or with sources that have no owner                                        -> Verify 1
  * a PARSER ADAPTER returning typed ELEMENTS (text | title | table | image | list | code) with page, bounding box
    and confidence, and three views per element: markdown, html, embedding text                                    -> Verify 2, 3
  * an ENVELOPE on every element: source id, filename, title, page, element type, content hash, owner and tenant,
    sensitivity, region, ingested-at, parser version — the owner comes from the corpus manifest or the job refuses
    the document, the tenant is ALWAYS the ingestion identity's (a manifest tenant that differs is refused)         -> Verify 2, 8
  * a PII SCRUB before anything is indexed: checksum + regex classes, placeholders with a REVERSIBLE DICTIONARY kept
    outside the index, quarantine for the classes that must never be masked (Gambill 2026-06; Huyen 2024-07)       -> Verify 6, 9
  * IDEMPOTENT UPSERT by document hash: noop / replace / tombstone — a second run over an unchanged corpus
    adds nothing                                                                                                    -> Verify 5
  * an ERASURE that reaches the index, the answer cache, the eval set and the logs, proves each with `mentions()`,
    and records `erased_at` against the policy deadline                                                            -> Verify 7
  * a tenant filter applied as the first predicate of every read (the stand-in for RLS)                            -> Verify 8

Branches every demo run exercises (recorded in the practice's change log):
  audit report over a built-in corpus (counts by type, one duplicate, one garbled page, planted PII of four classes,
  date coverage with one undated source, one source with no owner); `sync_corpus` refused with no report, with a stale
  report (parser version differs) and with an ownerless source in the report; the fake parser producing title / text /
  table / list / image / code elements with page and bbox; a table element whose html view keeps the cells and whose
  embedding text is a sentence; the envelope negative (empty owner refused by the model) and the pipeline negative (an
  ownerless document refused by `tag_owner`); a manifest tenant that differs from the job's refused; scrub: email and
  phone masked with reversible placeholders and unmasked from the dictionary, a card number (Luhn-valid) and a
  secret-shaped string quarantined with a reason, a 16-digit order id that fails Luhn kept, a card number with spaces
  classified as card and not as phone; first ingestion inserts; second ingestion of the unchanged corpus is all NOOP
  (zero new elements, zero duplicates); a changed document REPLACES its elements; a removed document is TOMBSTONED
  within the job's tenant only (another tenant's documents untouched); the planted PII not RETRIEVABLE through
  `search()`; two tenants with overlapping content — a read for one never returns the other's elements; a missing
  tenant on read refused; erasure of one subject removes its elements, cached answers, eval cases and log lines with
  `erased_at` inside the policy window, `mentions()` zero everywhere; the real negative — a cache entry written without
  the subject tag survives the erasure and the proof reports it. The demo uses only `Store` protocol methods.

Python idioms, not required (decision 0005 §3): pydantic models, the in-memory dict store, the line-based fake parser.
A real store is a table (or pgvector) whose tenant predicate is an RLS policy; a real parser is wired behind
`Parser.parse()`. Requires: Python 3.10+; `pydantic` only for the typed models.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import Iterable, Literal, Optional, Protocol

from pydantic import BaseModel, Field, field_validator

PARSER_VERSION = "fake-parser/0.1"           # a real adapter reports the library or API version it wraps
PII_POLICY = {                               # class -> "mask" (reversible placeholder) | "quarantine" (never indexed)
    "email": "mask",
    "phone": "mask",
    "card": "quarantine",                    # checksum tier: Luhn
    "secret": "quarantine",                  # key-shaped strings
}
MIN_TEXT_DENSITY = 0.55                      # share of alphanumeric or space characters below which a page is "garbled"
MIN_PAGE_CHARS = 20                          # fewer characters than this and the page counts as "empty"

ElementType = Literal["text", "title", "table", "image", "list", "code"]


# ----------------------------------------------------------------------------------------------------------- documents

class RawDocument(BaseModel):
    """What the corpus hands the pipeline: bytes already read as text (the fake parser is text-only), plus the facts the
    audit and the envelope need. `owner` / `tenant` come from the corpus manifest or the ingestion job, never from a user
    request (Verify 8 negative: a tenant filter decided by the caller)."""
    source_id: str
    filename: str
    content: str
    owner: Optional[str] = None
    tenant: Optional[str] = None
    sensitivity: Literal["public", "internal", "confidential", "personal"] = "internal"
    region: Optional[str] = None
    document_date: Optional[str] = None      # ISO date of the source, for date coverage

    @property
    def pages(self) -> list[str]:
        """Pages are separated by form feeds in the text the fake parser reads; a real adapter has real pages."""
        return self.content.split("\f") if "\f" in self.content else [self.content]

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()[:16]

    @property
    def extension(self) -> str:
        return os.path.splitext(self.filename)[1].lower() or "(none)"


# ------------------------------------------------------------------------------------------------------------- elements

class Element(BaseModel):
    """One typed region of a parsed page with its provenance. Three views: the reasoning model reads `to_markdown()` or,
    for a complex table, `to_html()`; the embedding model reads `to_embedding_text()` (Abraham 2026-09; Liu 2024)."""
    type: ElementType
    text: str
    page: int
    bbox: Optional[tuple[float, float, float, float]] = None
    confidence: float = 1.0
    rows: Optional[list[list[str]]] = None   # tables only
    caption: Optional[str] = None            # images only

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(f"{self.type}|{self.page}|{self.text}".encode("utf-8")).hexdigest()[:16]

    def to_markdown(self) -> str:
        if self.type == "title":
            return f"# {self.text}"
        if self.type == "table" and self.rows:
            head, *body = self.rows
            lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
            lines += ["| " + " | ".join(r) + " |" for r in body]
            return "\n".join(lines)
        if self.type == "image":
            return f"![{self.caption or 'image'}]"
        if self.type == "code":
            return f"```\n{self.text}\n```"
        return self.text

    def to_html(self) -> str:
        if self.type == "table" and self.rows:
            trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in self.rows)
            return f"<table>{trs}</table>"
        return f"<p>{self.text}</p>"

    def to_embedding_text(self) -> str:
        """A natural-language rendering: a table becomes sentences, an image its caption, code its first line."""
        if self.type == "table" and self.rows and len(self.rows) > 1:
            head, *body = self.rows
            sentences = ["; ".join(f"{h} is {c}" for h, c in zip(head, r)) for r in body]
            return "Table with columns " + ", ".join(head) + ". " + ". ".join(sentences) + "."
        if self.type == "image":
            return f"Image: {self.caption or 'no caption'}"
        if self.type == "code":
            return "Code: " + self.text.splitlines()[0] if self.text else "Code"
        return self.text


class Parser(Protocol):
    """The adapter every real parser hides behind. Docling, Unstructured or a vendor API returns its own element graph;
    the adapter maps it to `Element`s so the rest of the pipeline never sees a library type."""
    version: str

    def parse(self, doc: RawDocument) -> list[Element]: ...


class FakeParser:
    """Line-based stand-in for the demo: `#` title, `|` table rows, `- ` list, `[image: ...]`, fenced code, else text.
    A page's lines are given increasing y coordinates so every element carries a bounding box."""
    version = PARSER_VERSION

    def parse(self, doc: RawDocument) -> list[Element]:
        out: list[Element] = []
        for pno, page in enumerate(doc.pages, start=1):
            lines = page.splitlines()
            i, y = 0, 0.0
            while i < len(lines):
                line = lines[i].rstrip()
                i += 1
                if not line.strip():
                    continue
                if line.startswith("```"):
                    code = []
                    while i < len(lines) and not lines[i].startswith("```"):
                        code.append(lines[i]); i += 1
                    i += 1
                    out.append(Element(type="code", text="\n".join(code), page=pno, bbox=(0, y, 100, y + 5 * max(1, len(code)))))
                elif line.startswith("|"):
                    rows = [[c.strip() for c in line.strip("|").split("|")]]
                    while i < len(lines) and lines[i].startswith("|"):
                        cells = [c.strip() for c in lines[i].strip("|").split("|")]
                        if not all(set(c) <= set("-: ") for c in cells):
                            rows.append(cells)
                        i += 1
                    out.append(Element(type="table", text="\n".join(" ".join(r) for r in rows), rows=rows, page=pno,
                                       bbox=(0, y, 100, y + 5 * len(rows)), confidence=0.9))
                elif line.startswith("# "):
                    out.append(Element(type="title", text=line[2:], page=pno, bbox=(0, y, 100, y + 5)))
                elif line.startswith("- "):
                    items = [line[2:]]
                    while i < len(lines) and lines[i].startswith("- "):
                        items.append(lines[i][2:]); i += 1
                    out.append(Element(type="list", text="\n".join(items), page=pno, bbox=(0, y, 100, y + 5 * len(items))))
                elif line.startswith("[image:"):
                    out.append(Element(type="image", text="", caption=line[7:].rstrip("]").strip(), page=pno,
                                       bbox=(0, y, 100, y + 30), confidence=0.7))
                else:
                    out.append(Element(type="text", text=line, page=pno, bbox=(0, y, 100, y + 5)))
                y = out[-1].bbox[3] + 1 if out and out[-1].bbox else y + 6
        return out


# ------------------------------------------------------------------------------------------------------------- PII scrub

_PII_PATTERNS = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"(?<!\d)(?:\+?\d{1,3}[ -]?)?(?:\(?\d{2,4}\)?[ -]?)\d{3,4}[ -]\d{3,4}(?!\d)"),
    "card": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "secret": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{8,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,})\b"),
}


def luhn_ok(digits: str) -> bool:
    d = [int(c) for c in digits if c.isdigit()]
    if len(d) < 13:
        return False
    total, parity = 0, len(d) % 2
    for i, n in enumerate(d):
        if i % 2 == parity:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


class ReversibleDictionary(BaseModel):
    """placeholder -> original value, scoped to one tenant. Lives OUTSIDE the index (a secret store under the tenant
    scope), so a leak of the index leaks placeholders, not values (Huyen 2024-07; Verify 9 negative: the dictionary
    beside the embeddings)."""
    tenant: str
    mapping: dict[str, str] = Field(default_factory=dict)
    counters: dict[str, int] = Field(default_factory=dict)

    def placeholder(self, pii_class: str, value: str) -> str:
        for k, v in self.mapping.items():
            if v == value and k.startswith(f"[{pii_class.upper()}_"):
                return k
        n = self.counters.get(pii_class, 0) + 1
        self.counters[pii_class] = n
        key = f"[{pii_class.upper()}_{n}]"
        self.mapping[key] = value
        return key

    def unmask(self, text: str) -> str:
        for k, v in self.mapping.items():
            text = text.replace(k, v)
        return text


class ScrubResult(BaseModel):
    text: str
    hits: dict[str, int] = Field(default_factory=dict)
    quarantined: bool = False
    reason: Optional[str] = None


def find_pii(text: str) -> dict[str, list[str]]:
    """Overlapping spans are resolved longest-class-first: `card` is matched before `phone`, and a span already
    claimed by an earlier class is not reported again by a later one (so "4111 1111 1111 1111" is one card, not a
    card plus two phone numbers)."""
    found: dict[str, list[str]] = {}
    claimed: list[tuple[int, int]] = []
    for cls in ("secret", "card", "email", "phone"):
        rx = _PII_PATTERNS[cls]
        for m in rx.finditer(text):
            val = m.group(0)
            if cls == "card" and not luhn_ok(val):
                continue                     # a 16-digit order id that fails the checksum is not a card
            if any(m.start() < e and m.end() > b for b, e in claimed):
                continue
            claimed.append((m.start(), m.end()))
            found.setdefault(cls, []).append(val)
    return found


def pii_scrub(text: str, dictionary: Optional[ReversibleDictionary] = None, policy: dict[str, str] = PII_POLICY) -> ScrubResult:
    """Mask the classes whose policy is `mask` (placeholder, reversible through the dictionary if one is given) and
    quarantine the element when any class with policy `quarantine` is present. Detection here is the checksum and regex
    tier; a real pipeline adds NER (Presidio) behind the same function — and keeps Presidio's own warning that no detector
    finds everything (presidio-readme.md, read 2026-10-01)."""
    found = find_pii(text)
    hits = {k: len(v) for k, v in found.items()}
    for cls, values in found.items():
        if policy.get(cls) == "quarantine":
            return ScrubResult(text="", hits=hits, quarantined=True, reason=f"{cls} present ({len(values)}); policy quarantine")
    out = text
    for cls, values in found.items():
        for v in values:
            ph = dictionary.placeholder(cls, v) if dictionary else f"[{cls.upper()}]"
            out = out.replace(v, ph)
    return ScrubResult(text=out, hits=hits)


# ------------------------------------------------------------------------------------------------------------- envelope

class Envelope(BaseModel):
    """Verify 2: what every indexed element carries. `owner` and `tenant` are mandatory — an element without them is
    refused before it reaches the store."""
    source_id: str
    filename: str
    title: Optional[str]
    page: int
    element_type: ElementType
    content_hash: str
    document_hash: str
    owner: str
    tenant: str
    sensitivity: str
    region: Optional[str]
    ingested_at: str
    parser_version: str
    bbox: Optional[tuple[float, float, float, float]] = None
    confidence: float = 1.0

    @field_validator("owner", "tenant")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("owner and tenant are mandatory on every indexed element")
        return v


class IndexedElement(BaseModel):
    id: str
    envelope: Envelope
    markdown: str
    html: str
    embedding_text: str
    subject_ids: list[str] = Field(default_factory=list)   # data subjects this element is about, for erasure


class Identity(BaseModel):
    """The identity that runs the ingestion job (writes owner / tenant) or the read (filters by tenant)."""
    tenant: str
    user: str


def tag_owner(doc: RawDocument, ingestion_identity: Identity) -> tuple[str, str]:
    """Owner: the corpus manifest's value, or the document is refused — there is no silent fallback to the job's user
    (Verify 2 negative: an element with no owner). Tenant: ALWAYS the ingestion identity's; a manifest that names a
    different tenant is refused, so no argument on this path can move a document into another tenant (Verify 8)."""
    if not doc.owner or not doc.owner.strip():
        raise ValueError(f"{doc.source_id}: no owner in the corpus manifest — refused (audit-checklist.md §3)")
    if doc.tenant and doc.tenant != ingestion_identity.tenant:
        raise PermissionError(f"{doc.source_id}: manifest tenant {doc.tenant!r} differs from the ingestion identity's "
                              f"{ingestion_identity.tenant!r} — refused")
    return (doc.owner, ingestion_identity.tenant)


# ------------------------------------------------------------------------------------------------------------- store

class Store(Protocol):
    def get_document_hash(self, tenant: str, source_id: str) -> Optional[str]: ...
    def list_documents(self, tenant: str) -> list[str]: ...
    def replace_document(self, tenant: str, source_id: str, document_hash: str, elements: list[IndexedElement]) -> None: ...
    def tombstone(self, tenant: str, source_id: str, reason: str) -> None: ...
    def search(self, identity: Identity, query: str, k: int = 5) -> list[IndexedElement]: ...
    def erase_subject(self, tenant: str, subject_id: str, now: Optional[datetime] = None,
                      requested_at: Optional[datetime] = None) -> "ErasureRecord": ...
    def mentions(self, tenant: str, subject_id: str) -> dict[str, int]: ...
    def scan_content(self, tenant: str, needle: str) -> dict[str, int]: ...
    def record_derived(self, tenant: str, place: Literal["cache", "eval_set", "log"], key: str, payload: dict,
                       subject_ids: list[str]) -> None: ...


ERASURE_WINDOW_DAYS = 30                     # the policy window of privacy-compliance-checklist.md §5


class ErasureRecord(BaseModel):
    """What an erasure returns: what was removed where, when, and whether it happened inside the policy window."""
    tenant: str
    subject_id: str
    removed: dict[str, int]
    requested_at: str
    erased_at: str
    deadline: str
    within_window: bool


class InMemoryStore:
    """Dict-backed stand-in. The four places an erasure must reach are modelled explicitly: `index`, `cache` (answers
    keyed by query), `eval_set` (golden cases) and `log` (lines that may quote content). The tenant predicate is applied
    first in `search()` — the stand-in for an RLS policy (supabase-rag-with-permissions.md, read 2026-10-01)."""

    def __init__(self) -> None:
        self.index: dict[str, IndexedElement] = {}
        self.documents: dict[tuple[str, str], str] = {}          # (tenant, source_id) -> document_hash
        self.tombstones: dict[tuple[str, str], str] = {}
        self.cache: dict[tuple[str, str], dict] = {}             # (tenant, query) -> {"answer", "subject_ids"}
        self.eval_set: list[dict] = []                           # {"tenant", "question", "answer", "subject_ids"}
        self.log: list[dict] = []                                # {"tenant", "line", "subject_ids"}

    def get_document_hash(self, tenant: str, source_id: str) -> Optional[str]:
        return self.documents.get((tenant, source_id))

    def list_documents(self, tenant: str) -> list[str]:
        return [sid for t, sid in self.documents if t == tenant]

    def replace_document(self, tenant: str, source_id: str, document_hash: str, elements: list[IndexedElement]) -> None:
        for eid in [k for k, e in self.index.items() if e.envelope.tenant == tenant and e.envelope.source_id == source_id]:
            del self.index[eid]
        for e in elements:
            self.index[e.id] = e
        self.documents[(tenant, source_id)] = document_hash
        self.tombstones.pop((tenant, source_id), None)

    def tombstone(self, tenant: str, source_id: str, reason: str) -> None:
        self.replace_document(tenant, source_id, "", [])
        del self.documents[(tenant, source_id)]
        self.tombstones[(tenant, source_id)] = reason

    def search(self, identity: Identity, query: str, k: int = 5) -> list[IndexedElement]:
        if not identity.tenant:
            raise PermissionError("a read without a tenant is refused")
        scoped = [e for e in self.index.values() if e.envelope.tenant == identity.tenant]   # predicate first
        words = set(re.findall(r"\w+", query.lower()))
        scored = [(len(words & set(re.findall(r"\w+", e.embedding_text.lower()))), e) for e in scoped]
        return [e for s, e in sorted(scored, key=lambda t: -t[0]) if s > 0][:k]

    def erase_subject(self, tenant: str, subject_id: str, now: Optional[datetime] = None,
                      requested_at: Optional[datetime] = None) -> ErasureRecord:
        now = now or datetime.now(timezone.utc)
        requested_at = requested_at or now
        removed = {"index": 0, "cache": 0, "eval_set": 0, "log": 0}
        for eid in [k for k, e in self.index.items() if e.envelope.tenant == tenant and subject_id in e.subject_ids]:
            del self.index[eid]; removed["index"] += 1
        for key in [k for k, v in self.cache.items() if k[0] == tenant and subject_id in v.get("subject_ids", [])]:
            del self.cache[key]; removed["cache"] += 1
        before = len(self.eval_set)
        self.eval_set = [c for c in self.eval_set if not (c["tenant"] == tenant and subject_id in c.get("subject_ids", []))]
        removed["eval_set"] = before - len(self.eval_set)
        before = len(self.log)
        self.log = [l for l in self.log if not (l["tenant"] == tenant and subject_id in l.get("subject_ids", []))]
        removed["log"] = before - len(self.log)
        deadline = requested_at + timedelta(days=ERASURE_WINDOW_DAYS)
        self.log.append({"tenant": tenant, "line": f"erasure of subject {subject_id}: {removed} at {now.isoformat()}", "subject_ids": []})
        return ErasureRecord(tenant=tenant, subject_id=subject_id, removed=removed, requested_at=requested_at.isoformat(),
                             erased_at=now.isoformat(), deadline=deadline.isoformat(), within_window=now <= deadline)

    def record_derived(self, tenant: str, place: Literal["cache", "eval_set", "log"], key: str, payload: dict,
                       subject_ids: list[str]) -> None:
        """Every derived copy (a cached answer, an eval case, a log line) is written WITH its subject ids, so the
        erasure can find it; a write that omits them is the negative the demo shows."""
        row = dict(payload, subject_ids=list(subject_ids))
        if place == "cache":
            self.cache[(tenant, key)] = row
        elif place == "eval_set":
            self.eval_set.append(dict(row, tenant=tenant, question=key))
        else:
            self.log.append(dict(row, tenant=tenant, line=key))

    def scan_content(self, tenant: str, needle: str) -> dict[str, int]:
        """The second proof: places whose CONTENT still names the subject, whatever their tags say."""
        return {
            "index": sum(1 for e in self.index.values() if e.envelope.tenant == tenant and needle in e.markdown),
            "cache": sum(1 for k, v in self.cache.items() if k[0] == tenant and needle in json.dumps(v)),
            "eval_set": sum(1 for c in self.eval_set if c["tenant"] == tenant and needle in json.dumps(c)),
            "log": sum(1 for l in self.log if l["tenant"] == tenant and needle in l.get("line", "") and not l["line"].startswith("erasure of subject")),
        }

    def mentions(self, tenant: str, subject_id: str) -> dict[str, int]:
        """The proof after an erasure: how many places still reference the subject by tag (must be all zero)."""
        return {
            "index": sum(1 for e in self.index.values() if e.envelope.tenant == tenant and subject_id in e.subject_ids),
            "cache": sum(1 for k, v in self.cache.items() if k[0] == tenant and subject_id in v.get("subject_ids", [])),
            "eval_set": sum(1 for c in self.eval_set if c["tenant"] == tenant and subject_id in c.get("subject_ids", [])),
            "log": sum(1 for l in self.log if l["tenant"] == tenant and subject_id in l.get("subject_ids", [])),
        }


# ------------------------------------------------------------------------------------------------------------- audit

class AuditReport(BaseModel):
    corpus: str
    generated_at: str
    parser_version: str
    documents: int
    counts_by_type: dict[str, int]
    duplicates: list[list[str]]                 # groups of source ids sharing a content hash
    empty_pages: list[str]                      # "source_id:page"
    garbled_pages: list[str]
    pii_hits: dict[str, int]
    date_coverage: dict[str, Optional[str] | int]
    sources_without_owner: list[str]

    def is_stale(self, parser_version: str) -> bool:
        """Verify 1 negative: a report older than the parser version in use."""
        return self.parser_version != parser_version


def text_density(page: str) -> float:
    if not page:
        return 0.0
    good = sum(1 for c in page if c.isalnum() or c.isspace() or c in ".,;:!?'\"()-|#*[]/%$")
    return good / len(page)


def audit_report(corpus: Iterable[RawDocument], corpus_name: str, parser_version: str = PARSER_VERSION) -> AuditReport:
    docs = list(corpus)
    counts: dict[str, int] = {}
    by_hash: dict[str, list[str]] = {}
    empty, garbled, no_owner = [], [], []
    pii: dict[str, int] = {}
    dates = []
    undated = 0
    for d in docs:
        counts[d.extension] = counts.get(d.extension, 0) + 1
        by_hash.setdefault(d.content_hash, []).append(d.source_id)
        if not d.owner:
            no_owner.append(d.source_id)
        if d.document_date:
            dates.append(d.document_date)
        else:
            undated += 1
        for pno, page in enumerate(d.pages, start=1):
            if len(page.strip()) < MIN_PAGE_CHARS:
                empty.append(f"{d.source_id}:{pno}")
            elif text_density(page) < MIN_TEXT_DENSITY:
                garbled.append(f"{d.source_id}:{pno}")
        for cls, vals in find_pii(d.content).items():
            pii[cls] = pii.get(cls, 0) + len(vals)
    return AuditReport(
        corpus=corpus_name, generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        parser_version=parser_version, documents=len(docs), counts_by_type=counts,
        duplicates=[ids for ids in by_hash.values() if len(ids) > 1], empty_pages=empty, garbled_pages=garbled,
        pii_hits=pii, date_coverage={"earliest": min(dates) if dates else None, "latest": max(dates) if dates else None,
                                     "undated": undated},
        sources_without_owner=no_owner,
    )


# ------------------------------------------------------------------------------------------------------------- pipeline

class IngestResult(BaseModel):
    source_id: str
    action: Literal["insert", "replace", "noop", "quarantined"]
    elements: int = 0
    quarantined_elements: int = 0
    reasons: list[str] = Field(default_factory=list)


def ingest_document(doc: RawDocument, parser: Parser, store: Store, identity: Identity,
                    dictionary: Optional[ReversibleDictionary], subject_ids: Optional[list[str]] = None,
                    now: Optional[str] = None) -> IngestResult:
    """audit is done per corpus beforehand; this is parse -> scrub -> envelope -> upsert for one document."""
    owner, tenant = tag_owner(doc, identity)
    previous = store.get_document_hash(tenant, doc.source_id)
    if previous == doc.content_hash:
        return IngestResult(source_id=doc.source_id, action="noop")
    elements = parser.parse(doc)
    title = next((e.text for e in elements if e.type == "title"), None)
    indexed: list[IndexedElement] = []
    reasons: list[str] = []
    quarantined = 0
    stamp = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    for e in elements:
        scrub = pii_scrub(e.text, dictionary) if e.type != "image" else ScrubResult(text=e.text)
        if scrub.quarantined:
            quarantined += 1
            reasons.append(f"{doc.source_id} p{e.page} {e.type}: {scrub.reason}")
            continue
        clean = e.model_copy(update={"text": scrub.text,
                                      "rows": [[pii_scrub(c, dictionary).text for c in r] for r in e.rows] if e.rows else None})
        env = Envelope(source_id=doc.source_id, filename=doc.filename, title=title, page=e.page, element_type=e.type,
                       content_hash=clean.content_hash, document_hash=doc.content_hash, owner=owner, tenant=tenant,
                       sensitivity=doc.sensitivity, region=doc.region, ingested_at=stamp, parser_version=parser.version,
                       bbox=e.bbox, confidence=e.confidence)
        indexed.append(IndexedElement(id=f"{tenant}:{doc.source_id}:{clean.content_hash}", envelope=env,
                                      markdown=clean.to_markdown(), html=clean.to_html(),
                                      embedding_text=clean.to_embedding_text(), subject_ids=subject_ids or []))
    store.replace_document(tenant, doc.source_id, doc.content_hash, indexed)
    action = "insert" if previous is None else "replace"
    return IngestResult(source_id=doc.source_id, action=action, elements=len(indexed),
                        quarantined_elements=quarantined, reasons=reasons)


class AuditRefused(RuntimeError):
    """Verify 1 negative: an index built from a corpus with no report, a report older than the parser version in use,
    or a report that lists sources with no owner."""


def sync_corpus(corpus: list[RawDocument], parser: Parser, store: Store, identity: Identity,
                dictionary: Optional[ReversibleDictionary], report: Optional[AuditReport],
                subjects: Optional[dict[str, list[str]]] = None) -> list[IngestResult]:
    """Refuse without a current audit report; then upsert every document and tombstone the documents of the job's
    tenant that are no longer in the corpus (never another tenant's)."""
    if report is None:
        raise AuditRefused("no audit report for this corpus — run `--audit` first (Verify 1)")
    if report.is_stale(parser.version):
        raise AuditRefused(f"audit report is for parser {report.parser_version!r}, pipeline runs {parser.version!r} — regenerate (Verify 1)")
    if report.sources_without_owner:
        raise AuditRefused(f"audit report lists sources with no owner: {report.sources_without_owner} — fix the manifest (Verify 1, 2)")
    results = [ingest_document(d, parser, store, identity, dictionary, (subjects or {}).get(d.source_id)) for d in corpus]
    present = {d.source_id for d in corpus}
    for sid in store.list_documents(identity.tenant):
        if sid not in present:
            store.tombstone(identity.tenant, sid, "removed from corpus")
            results.append(IngestResult(source_id=sid, action="noop", reasons=["tombstoned: removed from corpus"]))
    return results


def load_folder(path: str) -> list[RawDocument]:
    """`--audit <dir>`: text-like files are read; other extensions are counted by type with empty content so the report
    still shows what the corpus holds. Owner / tenant / date come from a `manifest.json` beside the files if present."""
    manifest = {}
    mpath = os.path.join(path, "manifest.json")
    if os.path.exists(mpath):
        manifest = json.load(open(mpath, encoding="utf-8"))
    docs = []
    for root, _, files in os.walk(path):
        for fn in sorted(files):
            if fn == "manifest.json":
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, path)
            content = ""
            if os.path.splitext(fn)[1].lower() in (".txt", ".md", ".csv", ".html", ".json"):
                content = open(full, encoding="utf-8", errors="replace").read()
            meta = manifest.get(rel, {})
            docs.append(RawDocument(source_id=rel, filename=fn, content=content, owner=meta.get("owner"),
                                    tenant=meta.get("tenant"), region=meta.get("region"),
                                    sensitivity=meta.get("sensitivity", "internal"), document_date=meta.get("date")))
    return docs


# ------------------------------------------------------------------------------------------------------------- demo

def _demo_corpus() -> tuple[list[RawDocument], list[RawDocument]]:
    acme = [
        RawDocument(source_id="acme/policy.md", filename="policy.md", owner="acme-ops", tenant="acme", region="eu",
                    sensitivity="internal", document_date="2026-03-01",
                    content="# Refund policy\nRefunds are issued within 14 days of the request.\n"
                            "| Plan | Refund window | Fee |\n|---|---|---|\n| Basic | 14 days | 0 |\n| Pro | 30 days | 5 % |\n"
                            "- Contact support@acme.example or +44 20 7946 0958\n[image: refund flow chart]\n"
                            "```\nPOST /refunds {order_id}\n```"),
        RawDocument(source_id="acme/policy-copy.md", filename="policy-copy.md", owner="acme-ops", tenant="acme", region="eu",
                    document_date="2026-03-01",
                    content="# Refund policy\nRefunds are issued within 14 days of the request.\n"
                            "| Plan | Refund window | Fee |\n|---|---|---|\n| Basic | 14 days | 0 |\n| Pro | 30 days | 5 % |\n"
                            "- Contact support@acme.example or +44 20 7946 0958\n[image: refund flow chart]\n"
                            "```\nPOST /refunds {order_id}\n```"),
        RawDocument(source_id="acme/scan-07.pdf", filename="scan-07.pdf", owner="acme-ops", tenant="acme", region="eu",
                    document_date="2025-11-20",
                    content="# Invoice 2025-11\nTotal due 1,200 EUR for order 4111222233334445.\f"
                            "�#%&*^@!~}{]|[+=_)(*&^%$#@!�� ¬¦¬¦¬¦ ��%%$$##@@!!^^&&**(())__++==" + "\f" + "   "),
        RawDocument(source_id="acme/customer-note.txt", filename="customer-note.txt", owner=None, tenant="acme",
                    sensitivity="personal",
                    content="Customer Jane Roe (jane.roe@mail.example, +1 415 555 0133) paid with card 4111 1111 1111 1111.\n"
                            "Integration key sk-live-abcdefgh12345678 was shared by mistake."),
    ]
    beta = [
        RawDocument(source_id="beta/policy.md", filename="policy.md", owner="beta-admin", tenant="beta", region="us",
                    document_date="2026-01-15",
                    content="# Refund policy\nRefunds are issued within 60 days of the request.\n"
                            "| Plan | Refund window |\n|---|---|\n| Team | 60 days |"),
    ]
    return acme, beta


def _check(ok: bool, label: str, failures: list[str]) -> None:
    print(("  PASS " if ok else "  FAIL ") + label)
    if not ok:
        failures.append(label)


def run_demo() -> int:
    failures: list[str] = []
    acme, beta = _demo_corpus()
    parser = FakeParser()
    store: Store = InMemoryStore()
    ingest_acme = Identity(tenant="acme", user="ingest-job")
    ingest_beta = Identity(tenant="beta", user="ingest-job")
    dictionary = ReversibleDictionary(tenant="acme")
    read_acme, read_beta = Identity(tenant="acme", user="alice"), Identity(tenant="beta", user="bob")

    print("== 1. audit report (acme corpus) and the refusals of Verify 1 ==")
    report = audit_report(acme, "acme", parser.version)
    print(json.dumps(report.model_dump(), indent=1)[:1200])
    _check(report.counts_by_type == {".md": 2, ".pdf": 1, ".txt": 1}, "counts by type", failures)
    _check(report.duplicates == [["acme/policy.md", "acme/policy-copy.md"]], "duplicate pair found by content hash", failures)
    _check("acme/scan-07.pdf:2" in report.garbled_pages and "acme/scan-07.pdf:3" in report.empty_pages, "garbled page 2 and empty page 3 of the scan", failures)
    _check(set(report.pii_hits) == {"email", "phone", "card", "secret"}, f"PII hits by class: {report.pii_hits}", failures)
    _check(report.date_coverage == {"earliest": "2025-11-20", "latest": "2026-03-01", "undated": 1}, "date coverage with one undated source", failures)
    _check(report.sources_without_owner == ["acme/customer-note.txt"], "source with no owner named", failures)
    _check(not report.is_stale(parser.version) and report.is_stale("fake-parser/0.2"), "is_stale(): report version vs parser version", failures)
    for label, rep_ in (("no report", None), ("stale report", report.model_copy(update={"parser_version": "fake-parser/0.0"})), ("ownerless source in the report", report)):
        try:
            sync_corpus(acme, parser, store, ingest_acme, dictionary, rep_)
            _check(False, f"sync_corpus refused with {label}", failures)
        except AuditRefused as exc:
            _check(True, f"sync_corpus refused with {label}: {str(exc)[:60]}…", failures)
    _check(store.list_documents("acme") == [], "nothing indexed by the refused runs", failures)

    print("== 2. parser adapter: typed elements with provenance ==")
    els = parser.parse(acme[0])
    types = [e.type for e in els]
    print("  element types:", types)
    _check(types == ["title", "text", "table", "list", "image", "code"], "six element types from one page", failures)
    _check(all(e.bbox is not None and e.page == 1 for e in els), "every element has page and bbox", failures)
    table = next(e for e in els if e.type == "table")
    print("  table html:", table.to_html()[:80])
    print("  table embedding text:", table.to_embedding_text()[:110])
    _check("<td>Pro</td>" in table.to_html() and table.to_embedding_text().startswith("Table with columns Plan, Refund window, Fee. Plan is Basic"),
           "table keeps cells in html and has a sentence view for the embedding model", failures)

    print("== 3. envelope and tag_owner: owner mandatory, tenant from the job only ==")
    try:
        Envelope(source_id="x", filename="x", title=None, page=1, element_type="text", content_hash="0", document_hash="0",
                 owner="", tenant="acme", sensitivity="internal", region=None, ingested_at="now", parser_version="v")
        _check(False, "envelope with no owner refused", failures)
    except ValueError as exc:
        _check("mandatory" in str(exc), "envelope with no owner refused by the model", failures)
    ownerless = acme[3]
    try:
        ingest_document(ownerless, parser, store, ingest_acme, dictionary)
        _check(False, "ownerless document refused on the pipeline path", failures)
    except ValueError as exc:
        _check("no owner" in str(exc), "ownerless document refused on the pipeline path (tag_owner)", failures)
    foreign = acme[0].model_copy(update={"tenant": "beta"})
    try:
        ingest_document(foreign, parser, store, ingest_acme, dictionary)
        _check(False, "manifest tenant differing from the job's refused", failures)
    except PermissionError as exc:
        _check("differs" in str(exc), "manifest tenant differing from the job's refused", failures)
    _check(store.list_documents("acme") == [] and store.list_documents("beta") == [], "nothing indexed by the refused documents", failures)

    print("== 4. PII scrub: mask with a reversible dictionary, quarantine, checksum, overlap ==")
    masked = pii_scrub("Contact support@acme.example or +44 20 7946 0958", dictionary)
    print("  masked:", masked.text, masked.hits)
    _check(masked.text == "Contact [EMAIL_1] or [PHONE_1]" and dictionary.unmask(masked.text) == "Contact support@acme.example or +44 20 7946 0958",
           "email and phone masked with reversible placeholders; unmasked from the dictionary", failures)
    q = pii_scrub("paid with card 4111 1111 1111 1111", dictionary)
    _check(q.quarantined and q.reason.startswith("card") and q.hits == {"card": 1}, f"Luhn-valid card number quarantined as card only, not phone ({q.hits})", failures)
    s_ = pii_scrub("key sk-live-abcdefgh12345678", dictionary)
    _check(s_.quarantined and s_.reason.startswith("secret"), "secret-shaped string quarantined", failures)
    kept = pii_scrub("order 4111222233334445", dictionary)
    _check(not kept.quarantined and kept.text == "order 4111222233334445", "16-digit order id that fails Luhn kept", failures)

    print("== 5. idempotent upsert: insert, noop, replace, tombstone (within the job's tenant) ==")
    owned = [d.model_copy(update={"owner": "acme-support"}) if d.owner is None else d for d in acme]
    report_ok = audit_report(owned, "acme", parser.version)
    subjects = {"acme/customer-note.txt": ["jane-roe"]}
    r1 = sync_corpus(owned, parser, store, ingest_acme, dictionary, report_ok, subjects)
    print("  first run:", [(r.source_id, r.action, r.elements, r.quarantined_elements) for r in r1])
    n1 = len(store.search(read_acme, "refund policy days plan contact invoice total order", k=100))
    _check(all(r.action == "insert" for r in r1), "first run inserts every document", failures)
    note = next(r for r in r1 if r.source_id == "acme/customer-note.txt")
    _check(note.quarantined_elements == 2 and note.elements == 0, "both lines of the customer note quarantined (card, secret)", failures)
    r2 = sync_corpus(owned, parser, store, ingest_acme, dictionary, report_ok, subjects)
    n2 = len(store.search(read_acme, "refund policy days plan contact invoice total order", k=100))
    _check(all(r.action == "noop" for r in r2) and n2 == n1, f"second run over an unchanged corpus: all noop, still {n1} retrievable elements", failures)
    ids = [e.id for e in store.search(read_acme, "refund policy days plan contact invoice total order", k=100)]
    _check(len(ids) == len(set(ids)), "zero duplicate element ids", failures)
    changed = owned[0].model_copy(update={"content": owned[0].content.replace("14 days", "21 days")})
    r3 = ingest_document(changed, parser, store, ingest_acme, dictionary)
    hits = store.search(read_acme, "refunds issued days request", k=20)
    policy_hits = [e for e in hits if e.envelope.source_id == "acme/policy.md"]
    _check(r3.action == "replace" and any("21 days" in e.markdown for e in policy_hits) and not any("14 days" in e.markdown for e in policy_hits),
           "changed document replaces its elements", failures)
    beta_report = audit_report(beta, "beta", parser.version)
    sync_corpus(beta, parser, store, ingest_beta, None, beta_report)
    r4 = sync_corpus([changed] + owned[2:], parser, store, ingest_acme, dictionary, report_ok, subjects)
    _check("acme/policy-copy.md" not in store.list_documents("acme") and not any(e.envelope.source_id == "acme/policy-copy.md" for e in store.search(read_acme, "refund", k=100)),
           "removed document tombstoned and its elements gone", failures)
    _check(store.list_documents("beta") == ["beta/policy.md"], "another tenant's documents untouched by the acme sync (tombstones stay within the job's tenant)", failures)
    _check(store.search(read_acme, "4111 1111 1111 1111") == [] and store.search(read_acme, "sk-live-abcdefgh12345678") == [],
           "planted card number and secret not retrievable", failures)
    _check(store.search(read_acme, "support@acme.example") == [] and any("[EMAIL_1]" in e.markdown for e in store.search(read_acme, "Contact", k=20)),
           "planted email not retrievable; indexed only as its placeholder", failures)

    print("== 6. two tenants, overlapping content: tenant predicate first ==")
    hits_acme = store.search(read_acme, "refund window policy")
    hits_beta = store.search(read_beta, "refund window policy")
    print("  acme hits:", [(e.envelope.source_id, e.envelope.element_type) for e in hits_acme])
    print("  beta hits:", [(e.envelope.source_id, e.envelope.element_type) for e in hits_beta])
    _check(hits_acme and all(e.envelope.tenant == "acme" for e in hits_acme), "acme read returns only acme elements", failures)
    _check(hits_beta and all(e.envelope.tenant == "beta" for e in hits_beta), "beta read returns only beta elements", failures)
    try:
        store.search(Identity(tenant="", user="eve"), "refund")
        _check(False, "read without a tenant refused", failures)
    except PermissionError:
        _check(True, "read without a tenant refused", failures)

    print("== 7. erasure reaches index, cache, eval set and logs, inside the policy window ==")
    letter = RawDocument(source_id="acme/jane-letter.md", filename="jane-letter.md", owner="acme-support", tenant="acme",
                         sensitivity="personal", region="eu", content="Letter from jane.roe@mail.example asking for a refund.")
    ingest_document(letter, parser, store, ingest_acme, dictionary, subject_ids=["jane-roe"])
    store.record_derived("acme", "cache", "what did jane ask", {"answer": "a refund"}, ["jane-roe"])
    store.record_derived("acme", "cache", "refund window", {"answer": "21 days"}, [])
    store.record_derived("acme", "eval_set", "jane's refund", {"answer": "yes"}, ["jane-roe"])
    store.record_derived("acme", "eval_set", "pro refund window", {"answer": "30 days"}, [])
    store.record_derived("acme", "log", "answered jane-roe", {}, ["jane-roe"])
    before = store.mentions("acme", "jane-roe")
    t0 = datetime(2026, 10, 1, tzinfo=timezone.utc)
    rec = store.erase_subject("acme", "jane-roe", now=t0 + timedelta(days=3), requested_at=t0)
    after = store.mentions("acme", "jane-roe")
    print("  before:", before, "removed:", rec.removed, "after:", after, "erased_at:", rec.erased_at, "deadline:", rec.deadline)
    _check(before == {"index": 1, "cache": 1, "eval_set": 1, "log": 1} and all(v == 0 for v in after.values()),
           "erasure removed the subject from all four places and the proof is zero everywhere", failures)
    _check(rec.within_window and rec.erased_at < rec.deadline, "erased_at recorded inside the policy window", failures)
    late = store.erase_subject("acme", "nobody", now=t0 + timedelta(days=ERASURE_WINDOW_DAYS + 1), requested_at=t0)
    _check(not late.within_window, "an erasure after the deadline is flagged (within_window false)", failures)
    _check(store.scan_content("acme", "jane-roe") == {"index": 0, "cache": 0, "eval_set": 0, "log": 0}, "content scan agrees: no place still names the subject", failures)
    survivors = store.search(read_acme, "refund window", k=10)
    _check(any(e.envelope.source_id == "acme/policy.md" for e in survivors), "unrelated elements survive the erasure", failures)
    # the real negative: a cached answer about the subject written WITHOUT the subject tag — the erasure cannot see it,
    # so `mentions()` by tag reports zero while the answer is still there; `scan_content()` is what catches it.
    store.record_derived("acme", "cache", "jane refund status", {"answer": "jane-roe: refund approved"}, [])
    rec2 = store.erase_subject("acme", "jane-roe", now=t0 + timedelta(days=4), requested_at=t0)
    by_tag, by_content = store.mentions("acme", "jane-roe"), store.scan_content("acme", "jane-roe")
    print("  untagged cache entry after a second erasure — by tag:", by_tag, "by content:", by_content, "removed:", rec2.removed["cache"])
    _check(rec2.removed["cache"] == 0 and by_tag["cache"] == 0 and by_content["cache"] == 1,
           "negative: an untagged cached answer survives the erasure — the tag proof misses it, the content scan reports it (fix: every derived write carries its subject ids)", failures)

    print()
    if failures:
        print(f"DEMO FAILED: {len(failures)} check(s): {failures}")
        return 1
    print("DEMO OK: every branch in the module docstring exercised.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--demo", action="store_true", help="run the offline demo on the built-in corpus")
    ap.add_argument("--audit", metavar="DIR", help="audit a corpus folder (text-like files read; others counted)")
    ap.add_argument("--report", metavar="FILE", default="audit.json", help="where --audit writes the report")
    a = ap.parse_args()
    if a.demo:
        return run_demo()
    if a.audit:
        rep = audit_report(load_folder(a.audit), a.audit, PARSER_VERSION)
        json.dump(rep.model_dump(), open(a.report, "w", encoding="utf-8"), indent=1)
        print(f"audit report for {a.audit}: {rep.documents} documents, {len(rep.duplicates)} duplicate groups, "
              f"{len(rep.garbled_pages)} garbled pages, PII {rep.pii_hits}, {len(rep.sources_without_owner)} without owner -> {a.report}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
