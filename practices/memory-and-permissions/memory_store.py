"""memory_store.py — the ONE module that writes to, reads from and forgets in the product's long-term memory.

Copy to <repo>/src/<package>/memory.py. Replace <<CONSOLIDATION_MODEL>>, <<EXTRACTION_MODEL>> and point `Store` at the
real backend (a table with an `owner` column is the day-one substrate). Nothing else in the repo appends to memory:
every write goes through `remember()` (extract -> consolidate), every read through `search()` (identity filter BEFORE
ranking), every removal through `forget()` (a status with a trail) or `erase()` (the hard path where law requires).

What this buys you (principles/15-memory-external-context-and-permissions.md):
  * a memory UNIT with owner scope, type, timestamps, source pointer, status and importance   -> recallable AND forgettable
  * extract -> consolidate: a candidate fact meets its nearest neighbours and a reasoning model
    picks ADD / UPDATE / FORGET / NOOP with a reason (Mem0, 2025-04)                          -> no contradictions, no duplicates
  * the identity filter is a predicate applied before similarity ranking                       -> one user's facts never rank for another
  * reads bounded by k and by characters, labelled by type                                     -> latency does not grow with the store
  * consolidation designed to run OFF the response path (call `remember()` from a queue)      -> the reply never waits for memory
  * forgetting = status + trail (Alake 2026-04); erasure = hard delete with its trail           -> audit by default, GDPR where it holds
  * include/exclude: secret-shaped strings and excluded fields never become a unit              -> no SSN, token or card in the store
  * namespace validation: no read or write outside the identity's scope, no traversal           -> the memory-tool handler duties, restated

Branches every demo run exercises (recorded in the practice's change log):
  two identities with overlapping facts — isolation on read; ADD; NOOP on a duplicate; UPDATE on a contradiction (the old
  unit becomes `forgotten` with the trail pointing at its successor); FORGET on an explicit retraction; a forgotten unit excluded
  from reads; `erase()` removing the unit and its trail; a secret-shaped string and an excluded field dropped at extraction
  (while a 16-digit order id without separators is kept); a crafted owner/namespace refused on `search`, `forget` and
  `erase` themselves (explicit `owner` argument); retention — `expire()` forgets units older than the retention window with
  the reason "retention"; a bounded read (k and characters); the decay score ordering recency x relevance x importance with
  an injected clock; `touch()` raising importance on an UPDATE and on a neighbour hit; the memory block labelled by type.

Python idioms, not required (decision 0005 §3): dataclasses, the in-memory dict store, the token-overlap relevance. A real
store uses the database's text or vector search for the neighbours and `search()`; the identity filter stays a query
predicate (a WHERE clause, a global scope) in every stack. Requires: Python 3.10+; `pydantic` only for the typed
consolidation decision.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Iterable, Literal, Protocol

try:
    from pydantic import BaseModel, ConfigDict, ValidationError
except ImportError:  # pragma: no cover
    BaseModel = object  # type: ignore
    ConfigDict = dict  # type: ignore
    ValidationError = ValueError  # type: ignore

CONSOLIDATION_MODEL = "<<CONSOLIDATION_MODEL>>"  # a REASONING-capable model: Mem0 found a small reasoning model beat a small chat model here
EXTRACTION_MODEL = "<<EXTRACTION_MODEL>>"
NEIGHBOURS = 5          # Mem0's s = 5 most similar existing memories per candidate
RECENT_MESSAGES = 10    # Mem0's m = 10 last messages in the extraction window
DEFAULT_K = 8           # reads are bounded: k units…
MAX_READ_CHARS = 2_000  # …and this many characters, whatever the store holds (context budget: principles/11)
HALF_LIFE_DAYS = 30.0   # recency decay for the retrieval score (Generative Agents 2023 via Alake: recency x relevance x importance)
EXCLUDED_FIELDS = ("ssn", "password", "card_number", "cvv", "api_key")   # include/exclude lists are per use case (Mem0): names of fields never written
# Secret SHAPES, not every long number: a card number is matched only with separators (4-4-4-4 or 4-6-5 groups) so that a
# 13–19-digit order id or tracking number is kept; a bare 16-digit string is NOT dropped — add Luhn here if the product handles cards.
SECRET_SHAPES = (re.compile(r"\bsk-[A-Za-z0-9_-]{8,}"), re.compile(r"\bAKIA[0-9A-Z]{12,}"),
                 re.compile(r"\b\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{4}\b|\b\d{4}[ -]\d{6}[ -]\d{5}\b"), re.compile(r"\b\d{3}-\d{2}-\d{4}\b"))  # tokens, AWS keys, card numbers with separators, US SSNs
_WORD = re.compile(r"[a-z_]+")

MemoryType = Literal["semantic", "episodic", "procedural"]
Status = Literal["active", "forgotten"]
Action = Literal["ADD", "UPDATE", "FORGET", "NOOP"]


# --- 1. The unit -----------------------------------------------------------------------------------------------
@dataclass
class MemoryUnit:
    """Every attribute exists so the unit can be recalled (owner, type, text, importance) and forgotten (timestamps, status,
    trail). `owner` is the identity scope — a user id, a tenant id, or `tenant:user`; `source` points at the exchange that
    produced it so a human can audit why the system believes it."""
    owner: str
    type: MemoryType
    text: str
    source: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    status: Status = "active"
    importance: float = 1.0           # how many later units or decisions depend on it; raised by `touch()`
    last_accessed: float = field(default_factory=time.time)
    trail: list[dict[str, Any]] = field(default_factory=list)   # dated entries: added / updated-by / forgotten / why


class Store(Protocol):
    """The substrate behind the handler. The MODEL may see files or file-like commands (Anthropic's memory tool); the store a
    multi-user product writes to is namespaced, concurrent and audited (digest §5). Only these five operations are needed."""
    def put(self, unit: MemoryUnit) -> None: ...
    def get(self, unit_id: str) -> MemoryUnit | None: ...
    def for_owner(self, owner: str) -> Iterable[MemoryUnit]: ...   # the identity filter lives HERE, before any ranking
    def delete(self, unit_id: str) -> None: ...                     # hard delete — used by erase() only
    def all(self) -> Iterable[MemoryUnit]: ...                      # for audit and tests, never for serving


class InMemoryStore:
    def __init__(self) -> None: self._d: dict[str, MemoryUnit] = {}
    def put(self, unit: MemoryUnit) -> None: self._d[unit.id] = unit
    def get(self, unit_id: str) -> MemoryUnit | None: return self._d.get(unit_id)
    def for_owner(self, owner: str) -> Iterable[MemoryUnit]: return [u for u in self._d.values() if u.owner == owner]
    def delete(self, unit_id: str) -> None: self._d.pop(unit_id, None)
    def all(self) -> Iterable[MemoryUnit]: return list(self._d.values())


# --- 2. Namespace validation (the memory-tool handler's duty, restated for a home-made store) ------------------------
_OWNER = re.compile(r"^[A-Za-z0-9_:-]{1,64}$")


def validate_namespace(identity: str, requested_owner: str) -> str:
    """The requesting identity may touch only its own scope. Rejects traversal and encoded tricks the way Anthropic's memory-tool
    page tells the handler to (canonicalise, refuse `../` and URL-encoded variants) — here the scope is a key, not a path."""
    if not _OWNER.match(requested_owner) or ".." in requested_owner or "%" in requested_owner or "/" in requested_owner:
        raise PermissionError(f"invalid namespace {requested_owner!r}")
    if requested_owner != identity:
        raise PermissionError(f"identity {identity!r} may not access namespace {requested_owner!r}")
    return requested_owner


# --- 3. Extract --------------------------------------------------------------------------------------------------
@dataclass
class Candidate:
    type: MemoryType
    text: str
    subject: str   # a normalised key the consolidator uses to find contradictions ("home_city", "drink_preference")


ExtractionModel = Callable[[str, list[str], str], list[Candidate]]   # (running summary, recent messages, new exchange) -> candidates


def _passes_exclusions(c: Candidate, excluded_fields: tuple[str, ...] = EXCLUDED_FIELDS) -> bool:
    """An excluded FIELD is matched as an exact key — the candidate's `subject` or a whole word of its text — never as a
    substring ("password" must not drop "passwordless login preferred"... but it does drop "password: hunter2")."""
    words = set(_WORD.findall(c.text.lower()))
    if c.subject in excluded_fields or any(f in words for f in excluded_fields):
        return False
    return not any(p.search(c.text) for p in SECRET_SHAPES)


def extract(exchange: str, summary: str, recent: list[str], model: ExtractionModel) -> list[Candidate]:
    """Mem0's extraction call sees the running summary, the last m messages and the new pair, and emits candidate memories.
    Exclusions are applied HERE so a secret never reaches consolidation, let alone the store (assertion 5)."""
    return [c for c in model(summary, recent[-RECENT_MESSAGES:], exchange) if _passes_exclusions(c)]


# --- 4. Consolidate ----------------------------------------------------------------------------------------------
class Decision(BaseModel):  # type: ignore[misc]
    """Reasoning first, then the action (same shape as every judge in this KB). `target` names the existing unit for UPDATE,
    FORGET and NOOP."""
    model_config = ConfigDict(extra="forbid")
    reasoning: str
    action: Action
    target: str | None = None
    new_text: str | None = None


ConsolidationModel = Callable[[Candidate, list[MemoryUnit]], str]   # returns the model's JSON text; parsed into Decision here


def touch(store: Store, unit: MemoryUnit, by: float = 0.1, now: float | None = None) -> None:
    """Importance = how many later units or decisions depend on this one: raised when the unit is a neighbour of a new
    candidate and when it is superseded by an UPDATE (its successor inherits it). Reads do not raise importance; they refresh
    recency (`last_accessed`) — the two dimensions stay separate."""
    unit.importance += by
    unit.updated_at = now or time.time()
    store.put(unit)


def neighbours(store: Store, owner: str, candidate: Candidate, k: int = NEIGHBOURS) -> list[MemoryUnit]:
    """The s most similar ACTIVE units of the same owner; each hit is touched (it now has one more unit depending on it).
    Token overlap stands in for vector similarity (idiom, not required)."""
    units = [u for u in store.for_owner(owner) if u.status == "active"]
    hits = sorted(units, key=lambda u: -_overlap(candidate.text, u.text))[:k]
    for u in hits:
        if _overlap(candidate.text, u.text) > 0:
            touch(store, u)
    return hits


def consolidate(store: Store, owner: str, candidate: Candidate, model: ConsolidationModel, source: str) -> Decision:
    """One candidate meets its neighbours; the reasoning model decides; this function APPLIES the decision and writes the trail.
    Never an unconditional append: ADD only when the model says so."""
    near = neighbours(store, owner, candidate)
    try:
        d = Decision.model_validate_json(model(candidate, near))
    except (ValidationError, ValueError) as e:
        d = Decision(reasoning=f"consolidator output did not parse ({str(e)[:60]}); defaulting to NOOP", action="NOOP")
    now = time.time()
    if d.action == "ADD":
        store.put(MemoryUnit(owner, candidate.type, candidate.text, source, trail=[{"at": now, "event": "added", "why": d.reasoning}]))
    elif d.action == "UPDATE" and d.target and (old := store.get(d.target)) and old.owner == owner:
        touch(store, old, now=now)  # being superseded is a dependency: the successor inherits the raised importance
        new = MemoryUnit(owner, old.type, d.new_text or candidate.text, source, importance=old.importance,
                         trail=[{"at": now, "event": "added", "why": d.reasoning, "supersedes": old.id}])
        store.put(new)
        old.status, old.updated_at = "forgotten", now
        old.trail.append({"at": now, "event": "superseded", "by": new.id, "why": d.reasoning})
        store.put(old)
    elif d.action == "FORGET" and d.target and (old := store.get(d.target)) and old.owner == owner:
        forget(store, owner, old.id, d.reasoning)
    # NOOP: nothing written; the reason is still returned so the write log shows the decision (assertion 1)
    return d


def remember(store: Store, identity: str, exchange: str, summary: str, recent: list[str],
             extractor: ExtractionModel, consolidator: ConsolidationModel, source: str) -> list[tuple[Candidate, Decision]]:
    """The write path. Call it OFF the response path: after the reply is sent (long-lived process) or from a queued job
    (request-scoped runtime). Three model calls at most per exchange, none on the critical path (Mem0: `add` async, `search` sync)."""
    owner = validate_namespace(identity, identity)
    return [(c, consolidate(store, owner, c, consolidator, source)) for c in extract(exchange, summary, recent, extractor)]


# --- 5. Read: identity filter first, then rank, then bound ------------------------------------------------------------
def _overlap(a: str, b: str) -> float:
    ta, tb = set(re.findall(r"\w+", a.lower())), set(re.findall(r"\w+", b.lower()))
    return len(ta & tb) / math.sqrt(len(ta) * len(tb)) if ta and tb else 0.0


def score(unit: MemoryUnit, query: str, now: float | None = None) -> float:
    """recency x relevance x importance (Generative Agents 2023, as relayed by Alake 2026-04 — verify the paper's exact form before
    tuning). A unit nobody references decays out of retrieval without being destroyed."""
    now = now or time.time()
    recency = 0.5 ** ((now - unit.last_accessed) / 86_400 / HALF_LIFE_DAYS)
    return (0.1 + recency) * (0.1 + _overlap(query, unit.text)) * unit.importance


def search(store: Store, identity: str, query: str, k: int = DEFAULT_K, max_chars: int = MAX_READ_CHARS,
           owner: str | None = None, now: float | None = None) -> list[MemoryUnit]:
    """FILTER by identity, THEN rank, THEN bound. `owner` is the namespace asked for (default: the identity's own) and is
    validated against the identity on this very path, so a foreign namespace is refused here, not only in a helper. The filter
    is `store.for_owner()` — a predicate on the store, never a post-hoc check on a ranked list (that is the post-filter placement;
    fine when most results are authorised — Pinecone/AuthZed 2026-01 — but a memory store is one namespace per owner, so
    pre-filtering is always right here). `now` is injectable so the memory eval can advance the clock between sessions."""
    owner = validate_namespace(identity, owner or identity)
    now = now or time.time()
    active = [u for u in store.for_owner(owner) if u.status == "active"]   # forgotten units never leave the store
    ranked = sorted(active, key=lambda u: -score(u, query, now))[:k]
    out, used = [], 0
    for u in ranked:
        if used + len(u.text) > max_chars:
            break
        out.append(u); used += len(u.text)
        u.last_accessed = now; store.put(u)   # a read refreshes recency, not importance
    return out


def as_prompt_block(units: Iterable[MemoryUnit]) -> str:
    """What enters the window is labelled by type with its purpose (Alake's memory-aware segments; assertion 8)."""
    by: dict[str, list[str]] = {}
    for u in units:
        by.setdefault(u.type, []).append(u.text)
    lines = ["<memory purpose=\"facts about this user from earlier sessions; may be stale — prefer what the user says now\">"]
    for t in ("semantic", "episodic", "procedural"):
        if by.get(t):
            lines.append(f"  <{t}>"); lines += [f"    - {x}" for x in by[t]]; lines.append(f"  </{t}>")
    return "\n".join(lines + ["</memory>"])


# --- 6. Forget vs erase --------------------------------------------------------------------------------------------
def forget(store: Store, identity: str, unit_id: str, why: str, owner: str | None = None, now: float | None = None) -> MemoryUnit:
    """A status change with a trail: the unit leaves recall, not the store ("you don't delete… you forget" — Alake). Audit keeps it.
    `owner` (default: the identity's own namespace) is validated against the identity before the unit is looked at."""
    owner = validate_namespace(identity, owner or identity)
    u = store.get(unit_id)
    if u is None or u.owner != owner:
        raise PermissionError("no such unit in this identity's namespace")
    u.status, u.updated_at = "forgotten", now or time.time()
    u.trail.append({"at": u.updated_at, "event": "forgotten", "why": why})
    store.put(u)
    return u


def expire(store: Store, identity: str, retention_days: float, now: float | None = None,
           types: tuple[str, ...] = ("episodic",), owner: str | None = None) -> list[MemoryUnit]:
    """Retention: every active unit of the given types whose `created_at` is older than the window is forgotten with the reason
    "retention" — a status change with a trail, like any other forgetting (memory-design.md §5). Run it from the same background
    job as consolidation. Expiry is a lifecycle rule, not guaranteed deletion: the erasure path is `erase()`."""
    owner = validate_namespace(identity, owner or identity)
    now = now or time.time()
    out = []
    for u in list(store.for_owner(owner)):
        if u.status == "active" and u.type in types and now - u.created_at > retention_days * 86_400:
            out.append(forget(store, identity, u.id, f"retention: older than {retention_days:g} days", owner, now))
    return out


def erase(store: Store, identity: str, unit_id: str, request_ref: str, owner: str | None = None) -> None:
    """The hard path where `personal_data` or `regulated` holds (right to erasure): the unit AND its trail leave the store. Only
    the erasure request's reference is kept in the application's audit log (outside the store), never the content."""
    owner = validate_namespace(identity, owner or identity)
    u = store.get(unit_id)
    if u is None or u.owner != owner:
        raise PermissionError("no such unit in this identity's namespace")
    store.delete(unit_id)
    print(f"[audit] erased unit {unit_id} for {identity} on request {request_ref}")  # <<replace with the app's audit log>>


# --- 7. Offline demo: every branch, no network ---------------------------------------------------------------------
def _fake_extractor(summary: str, recent: list[str], exchange: str) -> list[Candidate]:
    """Rules standing in for the extraction model: enough to produce the demo's candidates with a `subject` key."""
    out = []
    for m in re.finditer(r"I (?:live in|moved to|now live in) ([A-Z][a-z]+)", exchange):
        out.append(Candidate("semantic", f"lives in {m.group(1)}", "home_city"))
    if re.search(r"I (?:like|love|drink) coffee", exchange):
        out.append(Candidate("semantic", "likes coffee", "drink_preference"))
    if re.search(r"(?:don't|do not) drink coffee anymore", exchange):
        out.append(Candidate("semantic", "RETRACT likes coffee", "drink_preference"))
    if "api key" in exchange.lower():
        out.append(Candidate("semantic", exchange.strip(), "credentials"))      # a secret-shaped candidate — must be dropped
    if "ssn" in exchange.lower():
        out.append(Candidate("semantic", "ssn is on file", "ssn"))               # an excluded field — must be dropped
    if m := re.search(r"order (\d{13,19})", exchange):
        out.append(Candidate("episodic", f"placed order {m.group(1)}", "order"))   # a long order id — must be KEPT
    if m := re.search(r"card (\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{4})", exchange):
        out.append(Candidate("semantic", f"pays with card {m.group(1)}", "payment"))  # a card number — must be dropped
    if "always answer in Spanish" in exchange:
        out.append(Candidate("procedural", "answer in Spanish", "language"))
    if "yesterday" in exchange:
        out.append(Candidate("episodic", "asked about flight refunds on 2026-09-30", "event"))
    return out


def _fake_consolidator(candidate: Candidate, near: list[MemoryUnit]) -> str:
    """Stands in for the reasoning model: same-subject neighbour with a different value -> UPDATE; same text -> NOOP;
    a retraction -> FORGET; otherwise ADD. The real model receives the candidate and the neighbours' texts and returns this JSON."""
    subj_words = {"home_city": "lives in", "drink_preference": "coffee", "language": "answer in"}
    key = subj_words.get(candidate.subject, candidate.text)
    same = [u for u in near if key in u.text]
    if candidate.text.startswith("RETRACT "):
        tgt = next((u for u in same if u.text == candidate.text[len("RETRACT "):]), None)
        return json.dumps({"reasoning": "the user retracted the fact", "action": "FORGET", "target": tgt.id if tgt else None})
    for u in same:
        if u.text == candidate.text:
            return json.dumps({"reasoning": "already known, identical", "action": "NOOP", "target": u.id})
        return json.dumps({"reasoning": f"contradicts {u.text!r}; the newer statement wins", "action": "UPDATE",
                           "target": u.id, "new_text": candidate.text})
    return json.dumps({"reasoning": "new fact with no neighbour on the subject", "action": "ADD"})


def _demo() -> int:
    store = InMemoryStore()
    log: list[str] = []

    def write(identity: str, exchange: str, src: str) -> None:
        for c, d in remember(store, identity, exchange, "", [], _fake_extractor, _fake_consolidator, src):
            log.append(f"{identity:<6} {d.action:<6} {c.text!r:<42} — {d.reasoning}")

    # session 1 — two identities, overlapping facts
    write("alice", "I live in Lisbon and I love coffee.", "conv-a1#3")
    write("bob", "I live in Madrid and I like coffee too. Also: always answer in Spanish.", "conv-b1#2")
    write("alice", "I love coffee.", "conv-a1#9")                                   # duplicate -> NOOP
    write("alice", "Here is my api key sk-live-ABCDEFGHIJKLMNOP for the tool.", "conv-a1#11")   # secret -> dropped
    write("bob", "my ssn is 123-45-6789", "conv-b1#7")                              # excluded field -> dropped
    write("alice", "yesterday I asked about refunds", "conv-a2#1")                  # episodic
    write("bob", "I placed order 4111222233334444 and paid with card 4111 2222 3333 4444", "conv-b2#3")  # order kept, card dropped
    print("\n== write log (extract -> consolidate; nothing appended unconditionally)")
    print("\n".join(log))
    assert sum(1 for l in log if "NOOP" in l) == 1 and not any("sk-live" in u.text or "ssn" in u.text or "card" in u.text for u in store.all())
    assert any(u.text == "placed order 4111222233334444" for u in store.all()), "a 16-digit order id without separators is kept"

    # isolation on read: alice never sees bob's city, bob never sees alice's; asking for bob's namespace as alice is refused
    try:
        search(store, "alice", "city", owner="bob"); raise AssertionError("foreign namespace must be refused on search")
    except PermissionError as e:
        print(f"search refused: {e}")
    a = search(store, "alice", "where does the user live")
    b = search(store, "bob", "where does the user live")
    assert all(u.owner == "alice" for u in a) and any("Lisbon" in u.text for u in a) and not any("Madrid" in u.text for u in a)
    assert all(u.owner == "bob" for u in b) and any("Madrid" in u.text for u in b)
    print("\n== read for alice (identity filter before ranking):\n" + as_prompt_block(a))
    print("== read for bob:\n" + as_prompt_block(b))

    # contradiction -> UPDATE: the old unit is forgotten with a trail pointing at its successor
    log.clear(); write("alice", "I moved to Porto last week.", "conv-a3#4"); print("\n" + "\n".join(log))
    a = search(store, "alice", "home city")
    assert any("Porto" in u.text for u in a) and not any("Lisbon" in u.text for u in a)
    old = next(u for u in store.all() if u.text == "lives in Lisbon")
    assert old.status == "forgotten" and old.trail[-1]["event"] == "superseded" and store.get(old.trail[-1]["by"]).text == "lives in Porto"
    assert old.importance > 1.0 and store.get(old.trail[-1]["by"]).importance == old.importance, "touch(): neighbour hit + supersession raise importance; successor inherits"
    print(f"old unit {old.id} status={old.status}, importance={old.importance:.1f}, trail -> superseded by {old.trail[-1]['by']}")

    # explicit retraction -> FORGET (status, not delete); excluded from reads; still in the store for audit
    log.clear(); write("alice", "I don't drink coffee anymore.", "conv-a3#9"); print("\n" + "\n".join(log))
    coffee = next(u for u in store.all() if u.owner == "alice" and u.text == "likes coffee")
    assert coffee.status == "forgotten" and coffee not in search(store, "alice", "coffee") and store.get(coffee.id) is not None
    print(f"forgotten unit {coffee.id} excluded from reads, kept with trail {[(e['event']) for e in coffee.trail]}")

    # erase: the hard path — unit and trail gone; bob erasing alice's unit (explicit owner) is refused first
    try:
        erase(store, "bob", coffee.id, "x", owner="alice"); raise AssertionError
    except PermissionError as e:
        print(f"erase refused: {e}")
    erase(store, "alice", coffee.id, request_ref="dsar-2026-10-01-07")
    assert store.get(coffee.id) is None

    # retention: an episodic unit older than the window is forgotten with the reason "retention"; semantic units are not
    clock = time.time()
    episodic = next(u for u in store.all() if u.owner == "alice" and u.type == "episodic")
    assert not expire(store, "alice", retention_days=30, now=clock), "nothing expires on day 0"
    expired = expire(store, "alice", retention_days=30, now=clock + 31 * 86_400)
    assert [u.id for u in expired] == [episodic.id] and episodic.status == "forgotten" and episodic.trail[-1]["why"].startswith("retention")
    assert episodic not in search(store, "alice", "refunds", now=clock + 31 * 86_400)
    assert next(u for u in store.all() if u.text == "lives in Porto").status == "active"
    print(f"retention: {len(expired)} episodic unit forgotten after 31 days ({episodic.trail[-1]['why']}); semantic units untouched")

    # namespace: a crafted owner is refused (alice cannot read bob, traversal shapes rejected)
    for bad in ("bob", "../bob", "alice%2F..", "alice/bob"):
        try:
            validate_namespace("alice", bad); raise AssertionError(bad)
        except PermissionError as e:
            print(f"refused: {bad!r} -> {e}")
    for kwargs in ({}, {"owner": "bob"}):
        try:
            forget(store, "alice", next(u for u in store.all() if u.owner == "bob").id, "attempt", **kwargs); raise AssertionError
        except PermissionError:
            print(f"refused: alice forgetting bob's unit (owner={kwargs.get('owner', 'alice')})")

    # bounded read: k and characters
    for i in range(20):
        store.put(MemoryUnit("bob", "episodic", f"event {i} " + "x" * 300, f"bulk#{i}"))
    r = search(store, "bob", "event", k=5, max_chars=1_000)
    assert len(r) <= 5 and sum(len(u.text) for u in r) <= 1_000
    print(f"\nbounded read for bob: {len(r)} units, {sum(len(u.text) for u in r)} chars (k=5, max 1000) from a store of {len(list(store.for_owner('bob')))}")

    # decay ordering with an injected clock: an old, unaccessed unit ranks below a fresh one of equal relevance
    t0 = time.time()
    stale = MemoryUnit("bob", "semantic", "prefers window seats", "old", last_accessed=t0 - 200 * 86_400)
    fresh = MemoryUnit("bob", "semantic", "prefers aisle seats", "new", last_accessed=t0)
    assert score(fresh, "seat preference", now=t0) > score(stale, "seat preference", now=t0)
    assert abs(score(fresh, "seat preference", now=t0) - score(stale, "seat preference", now=t0 - 200 * 86_400)) < 1e-9, "same clock distance, same score"
    print("decay: fresh unit outranks a 200-day-old one of equal relevance; the clock is an argument, not time.time()")

    # a consolidator that returns garbage -> NOOP, never an exception, never an append
    n_before = len(list(store.all()))
    d = consolidate(store, "bob", Candidate("semantic", "likes tea", "drink_preference"), lambda c, n: "not json", "x")
    assert d.action == "NOOP" and len(list(store.all())) == n_before
    print(f"unparseable consolidator output -> {d.action}: {d.reasoning[:60]}")
    print("\ndemo: every documented branch exercised offline (no model call, no network)")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--demo", action="store_true", help="offline run of every branch with a fake extractor and consolidator")
    a = p.parse_args(argv)
    if a.demo:
        return _demo()
    p.print_help(); return 2


if __name__ == "__main__":
    sys.exit(main())
