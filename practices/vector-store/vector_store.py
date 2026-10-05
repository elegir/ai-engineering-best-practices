"""vector_store.py — the store manifest, the benchmark record and the query object that stand between the product and its
approximate index.

Copy to <repo>/src/<package>/retrieval/vector_store.py. Replace <<S7_MODULE>> (where embedding_config_and_chunker.py landed;
the reference imports it from the sibling folder ../embeddings-and-chunking/), <<STORE_BACKEND>> (the real store behind the
`Backend` protocol — pgvector, Qdrant, Weaviate, turbopuffer; the shipped `ExactBackend` and `StubApproxBackend` are in-memory
stand-ins), <<FLAT_UNTIL>>, <<AVAILABLE_MEMORY_BYTES>>, <<REPLICAS>> and <<SELECTIVE_BELOW>> (README.md Adapt).

What this buys you (principles/18-vector-stores.md; the enforcement table in README.md names the demo step):
  * a STORE MANIFEST whose embedding fingerprint is COMPUTED from the EmbeddingConfig (`StoreManifest.for_config`) and checked
    against the configuration, the s7 IndexManifest's whole `index` block and what the backend reports it built; a `Store`
    cannot be constructed without that check, refuses a manifest mutated after it, and reads fingerprint, side and dimension
    from the s7 `Embedded` tag on every upsert and search (`check`, `Store.__init__`, `Store._accept`)                -> Verify 1
  * an EXACT index below a mandatory `flat_until`; an approximate spec under the threshold is refused (`IndexSpec`, `check`) -> Verify 2
  * VALIDATED parameters and a BENCHMARK RECORD bound to the manifest's fixture file (hash), the spec (hash) and the
    quantization (hash), re-read from disk and re-verified on every check; no record, a typed-in record, a stale record →
    refused (`IndexSpec.__post_init__`, `BenchmarkRecord`, `require_benchmark`)                                      -> Verify 3
  * a FROZEN, SIGNED `Query` carrying its tenant; a tenantless query under multi_tenant, a shared index that under-fills a
    tenant, a manifest without a two-tenant PROOF at the current spec and fixture → refused; `--check` RE-RUNS the proof
    from the fixture instead of trusting the stored one (`Query`, `search`, `run_tenant_proof`, `check`, `run_check`)  -> Verify 4
  * a FILTER STRATEGY per filter class whose selectivity is MEASURED by `run_benchmark` and stored in a record; a class with
    a typed selectivity or no record, post-filtering at or under the threshold, fewer than k results → refused
    (`Query.validate`, `search`, `filtered_recall`)                                                                  -> Verify 5
  * STORE QUANTIZATION that cannot be lossy without rescoring and whose before/after recall is COPIED FROM TWO BENCHMARK
    RECORDS, never typed (`Quantization`, `StoreManifest.set_quantization`, `check`)                                 -> Verify 6
  * a CAPACITY ESTIMATE recomputed from the manifest's counts and compared, per medium, with the placement's memory
    (`capacity_estimate`, `CapacityEstimate.resident`, `Placement`, `check`)                                         -> Verify 7
  * `--check --manifest <path> [--s7-manifest <path>]`: exit 2 malformed / no benchmark / proof fails on re-run / capacity
    overflow, 1 below the recall floor (`sampled_recall`, `run_check`) — the CI gate                                 -> Verify 9

What hash-binding does and does not do: a record bound to the fixture hash, the spec hash and the quantization hash catches a
STALE or CARELESS record (another fixture, an older parameter set, a typed-in file); it does not stop a forger who rewrites the
hashes too. The control against forgery is `--check` re-running the proof and the sampled recall from the fixture itself.

GRAPH_EDGE_BYTES is a DOCUMENTED APPROXIMATION: Weaviate's storage table (snapshot read 2026-10-05) counts "10B x 20 connections"
per node for the graph; this module uses 8 bytes per edge × 2 × m edges (HNSW's base layer holds up to 2·m neighbours per node
— Pinecone's Faiss chapter: "M_max0 set to M*2") — replace it with a measured value. Qdrant's resource guide (read 2026-10-05)
gives only "storing 1 million vectors with 1024 dimensions would require approximately 5.72 GB of RAM" — vectors × dimensions ×
4 bytes, no graph term; this reference adds the graph term as its own approximation, not as a vendor figure. Standard library
only; Python 3.10+. The demo runs every REFUSED line of the enforcement table plus the spoofs and exits 0.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime
import hashlib
import json
import math
import os
import sys
import tempfile
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, Protocol, Sequence

# <<S7_MODULE>> — the reference imports the s7 module from the sibling practice folder. Anything with the same fields works:
# EmbeddingConfig.fingerprint()/dimensions/dtype, Embedded.vector/fingerprint/side, IndexManifest.config_fingerprint/index.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "embeddings-and-chunking"))
from embedding_config_and_chunker import (EmbeddingConfig, Embedded, Embedder, IndexManifest, ChunkerRecord,  # noqa: E402
                                          ApproxTokenizer, make_stub_backend, DEMO_CONFIG)

INDEX_TYPES = ("flat", "hnsw", "ivf", "clustered")
QUANT_METHODS = ("none", "sq8", "bq1", "pq", "rq8", "rq4", "rq1")
ORIGINALS = ("ram", "disk", "object", "dropped")
MEDIA = ("ram", "ssd", "object")
TENANT_MODELS = ("none", "rls_with_partition", "rls_with_iterative_scan", "partial_index", "tenant_payload_index", "namespace")
PARTITIONED_MODELS = ("rls_with_partition", "partial_index", "namespace")   # the candidate list is drawn inside the tenant
STRATEGIES = ("auto", "in_graph", "pre", "iterative", "exact", "post")
DTYPE_BYTES = {"float32": 4, "bfloat16": 2, "float16": 2, "int8": 1, "uint8": 1, "binary": 1 / 8, "ubinary": 1 / 8}
QUANT_BYTES = {"none": None, "sq8": 1, "bq1": 1 / 8, "pq": 1 / 8, "rq8": 1, "rq4": 1 / 2, "rq1": 1 / 8}   # per dimension; pq ≈ 8 dims per byte
GRAPH_EDGE_BYTES = 8            # APPROXIMATION — see the module docstring; replace with a measured value
M_MAX = 128                     # this reference's ceiling: twice the top of Qdrant's "Typical values: between 8 and 64" (course, read 2026-10-05) and of its
                                # on-disk recipe (m 64, Optimize performance page); raise it only with a measured, dated note
SELECTIVE_BELOW = 0.10          # <<SELECTIVE_BELOW>> — pgvector README (read 2026-10-05): a condition matching 10 % of rows under-fills the default candidate list
MAX_SCAN_TUPLES = 20_000        # pgvector's hnsw.max_scan_tuples default (read 2026-10-05); the stub's iterative-scan bound
RECORD_KEYS = ("fixture", "fixture_hash", "k", "recall_at_k", "qps", "concurrency", "p99_ms", "memory_bytes", "build_seconds",
               "date", "spec_hash", "quantization_hash")


class VectorStoreError(ValueError):
    """Base class: every refusal below is one of these."""
class ManifestMismatch(VectorStoreError): ...
class SpecInvalid(VectorStoreError): ...
class ThresholdNotReached(VectorStoreError): ...
class BenchmarkRequired(VectorStoreError): ...
class TenantRequired(VectorStoreError): ...
class UnderFilled(VectorStoreError):
    def __init__(self, msg: str, returned: int = 0): super().__init__(msg); self.returned = returned
class QuantizationUnmeasured(VectorStoreError): ...
class CapacityExceeded(VectorStoreError): ...


def _h(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


def _file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def _iso_date(s: str, what: str) -> None:
    try: datetime.date.fromisoformat(s)
    except (TypeError, ValueError): raise BenchmarkRequired(f"{what} date {s!r} is not an ISO date (YYYY-MM-DD)")


# ------------------------------------------------------------------------------------------------------------- spec

@dataclass(frozen=True)
class IndexSpec:
    """Index type and parameters, validated at construction (Verify 3) with a mandatory exact-search threshold (Verify 2)."""
    type: str
    flat_until: Optional[int] = None            # <<FLAT_UNTIL>> — vectors below this count stay exact; mandatory
    m: Optional[int] = None
    ef_construction: Optional[int] = None
    ef_search: Optional[int] = None
    lists: Optional[int] = None
    probes: Optional[int] = None

    def __post_init__(self) -> None:
        if self.type not in INDEX_TYPES:
            raise SpecInvalid(f"index type {self.type!r} is not one of {INDEX_TYPES}")
        if not isinstance(self.flat_until, int) or isinstance(self.flat_until, bool) or self.flat_until <= 0:
            raise SpecInvalid("flat_until is mandatory: the vector count below which the index stays exact (a measured, positive integer)")
        graph, ivf = {"m", "ef_construction", "ef_search"}, {"lists", "probes"}
        given = {k for k in graph | ivf if getattr(self, k) is not None}
        if self.type == "hnsw":
            if given - graph: raise SpecInvalid(f"hnsw does not take {sorted(given - graph)}")
            if self.m is None or not 2 <= self.m <= M_MAX:
                raise SpecInvalid(f"m={self.m}: an HNSW node needs 2 ≤ m ≤ {M_MAX} (vendors ship 16; Qdrant's typical range is 8–64, read 2026-10-05)")
            if self.ef_construction is None or self.ef_construction < self.m:
                raise SpecInvalid(f"ef_construction={self.ef_construction} < m={self.m}: the build beam cannot be narrower than the edges it must choose")
            if self.ef_search is None or self.ef_search < 1: raise SpecInvalid("ef_search must be a positive integer (checked against k at query time)")
        elif self.type in ("ivf", "clustered"):
            if given - ivf: raise SpecInvalid(f"{self.type} does not take {sorted(given - ivf)}")
            if self.lists is None or self.lists < 1: raise SpecInvalid("lists must be a positive integer")
            if self.probes is None or not 1 <= self.probes <= self.lists:
                raise SpecInvalid(f"probes={self.probes} must satisfy 1 ≤ probes ≤ lists={self.lists}")
        elif given:
            raise SpecInvalid(f"a flat (exact) index takes no parameters, got {sorted(given)}")

    @property
    def approximate(self) -> bool:
        return self.type != "flat"

    def params(self) -> dict:
        return {k: v for k, v in asdict(self).items() if k not in ("type", "flat_until") and v is not None}

    def spec_hash(self) -> str:
        return _h({k: v for k, v in asdict(self).items() if k != "flat_until"})


@dataclass(frozen=True)
class Quantization:
    """Store-side quantization (Verify 6). `recall_before`/`recall_after` are filled by StoreManifest.set_quantization from two
    BenchmarkRecord files; values typed here are refused by StoreManifest.check()."""
    method: str = "none"
    rescore: bool = True
    oversampling: float = 1.0
    originals: str = "ram"
    recall_before: Optional[float] = None
    recall_after: Optional[float] = None

    def __post_init__(self) -> None:
        if self.method not in QUANT_METHODS: raise SpecInvalid(f"quantization {self.method!r} is not one of {QUANT_METHODS}")
        if self.originals not in ORIGINALS: raise SpecInvalid(f"originals {self.originals!r} is not one of {ORIGINALS}")
        if self.oversampling < 1: raise SpecInvalid("oversampling must be ≥ 1 (1 = no over-fetch)")
        if not self.lossy and self.originals == "dropped":
            raise SpecInvalid("method 'none' with originals 'dropped': there is nothing but the originals — the store would hold no vectors")
        if self.lossy and not self.rescore:
            raise QuantizationUnmeasured(f"{self.method} with rescore=False: every vendor pairs lossy quantization with rescoring against "
                                         "the originals (principle 18 §3.5); set rescore=True or stay at method='none'")

    @property
    def lossy(self) -> bool: return self.method != "none"
    @property
    def reversible(self) -> bool: return self.originals != "dropped"

    def quantization_hash(self) -> str:
        return _h({"method": self.method, "rescore": self.rescore, "oversampling": self.oversampling, "originals": self.originals})


NO_QUANT_HASH = Quantization().quantization_hash()


@dataclass(frozen=True)
class Placement:
    """Where vectors and index live (Verify 7). Anything off RAM needs the cold-latency budget the product absorbs."""
    vectors: str = "ram"
    index: str = "ram"
    pinned: bool = False                     # the quantized copy kept in RAM (Qdrant: `pinned` / `always_ram`)
    cold_latency_budget_ms: Optional[int] = None

    def __post_init__(self) -> None:
        for v in (self.vectors, self.index):
            if v not in MEDIA: raise SpecInvalid(f"placement {v!r} is not one of {MEDIA}")
        off_ram = self.vectors != "ram" or self.index != "ram"
        if off_ram and (not isinstance(self.cold_latency_budget_ms, int) or self.cold_latency_budget_ms <= 0):
            raise SpecInvalid(f"a placement off RAM needs cold_latency_budget_ms > 0 (got {self.cold_latency_budget_ms!r}): the cold-query latency the "
                              "product's budget absorbs (Eskildsen, CMU 2026-03-10: hundreds of ms on object storage)")


# -------------------------------------------------------------------------------------------------------- benchmark

@dataclass(frozen=True)
class BenchmarkRecord:
    """One benchmark run (Verify 3). Written by run_benchmark(); re-verified against the fixture file and the spec on every read.
    A filtered run also carries `filter_class` and the MEASURED `selectivity` (matching rows / rows on the exact backend)."""
    fixture: str
    fixture_hash: str
    k: int
    recall_at_k: float
    qps: float
    concurrency: int
    p99_ms: float
    memory_bytes: int
    build_seconds: float
    date: str
    spec_hash: str
    quantization_hash: str = NO_QUANT_HASH
    filter_class: Optional[str] = None
    selectivity: Optional[float] = None

    def validate(self) -> None:
        if self.k < 1 or not 0 <= self.recall_at_k <= 1 or self.qps <= 0 or self.concurrency < 1 or self.p99_ms < 0 \
                or self.memory_bytes <= 0 or self.build_seconds < 0:
            raise BenchmarkRequired("benchmark record has a field out of range (k ≥ 1, 0 ≤ recall ≤ 1, qps > 0, concurrency ≥ 1, memory > 0)")
        _iso_date(self.date, "benchmark record")
        if (self.filter_class is None) != (self.selectivity is None) or (self.selectivity is not None and not 0 < self.selectivity <= 1):
            raise BenchmarkRequired("a filtered record carries both filter_class and a measured selectivity in (0, 1]")

    def write(self, path: str) -> str:
        with open(path, "w", encoding="utf-8") as f: json.dump(asdict(self), f, indent=1)
        return path

    @classmethod
    def load(cls, path: str) -> "BenchmarkRecord":
        try:
            with open(path, encoding="utf-8") as f: d = json.load(f)
            missing = [k for k in RECORD_KEYS if k not in d]
            if missing: raise BenchmarkRequired(f"benchmark record {path} lacks {missing}: run run_benchmark(), do not type numbers")
            rec = cls(**{k: d[k] for k in RECORD_KEYS}, filter_class=d.get("filter_class"), selectivity=d.get("selectivity"))
        except (OSError, ValueError, TypeError) as e:
            if isinstance(e, BenchmarkRequired): raise
            raise BenchmarkRequired(f"benchmark record {path} cannot be read ({e.__class__.__name__})")
        rec.validate(); return rec


def verify_record(rec: BenchmarkRecord, spec: IndexSpec, quant_hash: str, fixture: Optional[str]) -> None:
    """The staleness check: the record must name the manifest's fixture, which must exist and hash the same, and be bound to
    THIS spec and THIS quantization. It catches a stale or careless record (another fixture, an older spec, typed numbers), not a
    forger who rewrites the hashes — `--check` re-runs the proof and the sampled recall for that (module docstring)."""
    if not fixture:
        raise BenchmarkRequired("the store manifest names no fixture: a benchmark record cannot be bound to nothing (set StoreManifest.fixture)")
    for f_ in {fixture, rec.fixture}:
        if not os.path.exists(f_):
            raise BenchmarkRequired(f"benchmark record points at fixture {f_!r}, which does not exist: numbers without a fixture are not a benchmark")
    if os.path.abspath(rec.fixture) != os.path.abspath(fixture):
        raise BenchmarkRequired(f"benchmark record was run on {rec.fixture!r}, the manifest's fixture is {fixture!r}")
    if _file_hash(fixture) != rec.fixture_hash:
        raise BenchmarkRequired(f"benchmark record was run on another fixture (hash {rec.fixture_hash} ≠ {_file_hash(fixture)}): re-run on the current fixture")
    if rec.spec_hash != spec.spec_hash():
        raise BenchmarkRequired(f"benchmark record is for another spec ({rec.spec_hash} ≠ {spec.spec_hash()}): a type or parameter change needs its own run")
    if rec.quantization_hash != quant_hash:
        raise BenchmarkRequired(f"benchmark record was run under another quantization ({rec.quantization_hash} ≠ {quant_hash})")


# ------------------------------------------------------------------------------------------------------- capacity

@dataclass(frozen=True)
class CapacityEstimate:
    vectors_bytes: int
    graph_bytes: int
    quantized_bytes: int
    replicas: int
    @property
    def total(self) -> int: return (self.vectors_bytes + self.graph_bytes + self.quantized_bytes) * self.replicas
    def resident(self, placement: Optional[Placement]) -> int:
        """Bytes that must sit in RAM under this placement (Verify 7): everything when no placement is decided; otherwise the
        vectors when they are in RAM, the graph when the index is in RAM, the quantized copy when pinned or when vectors are in RAM."""
        if placement is None: return self.total
        v = self.vectors_bytes if placement.vectors == "ram" else 0
        g = self.graph_bytes if placement.index == "ram" else 0
        q = self.quantized_bytes if (placement.pinned or placement.vectors == "ram") else 0
        return (v + g + q) * self.replicas
    def __str__(self) -> str:
        return (f"vectors {self.vectors_bytes / 2**30:.2f} GiB + graph {self.graph_bytes / 2**30:.2f} GiB + quantized copy "
                f"{self.quantized_bytes / 2**30:.2f} GiB, × {self.replicas} replicas = {self.total / 2**30:.2f} GiB")


def capacity_estimate(vector_count: int, dimensions: int, dtype: str, spec: IndexSpec, quant: Quantization, replicas: int) -> CapacityEstimate:
    """vectors × dimensions × bytes(dtype) + graph (m × 2 × GRAPH_EDGE_BYTES per node, an approximation of this reference) + the
    quantized copy when the originals stay, × replicas. The vendors' own arithmetic — pgvector's 4·d+8 / 2·d+8 / d/8+8 bytes per
    vector, Qdrant's "1 million vectors with 1024 dimensions… approximately 5.72 GB of RAM" (vectors only) — is in
    tuning-and-capacity.md §6."""
    if dtype not in DTYPE_BYTES: raise SpecInvalid(f"dtype {dtype!r} unknown to the capacity model")
    if replicas < 1 or vector_count < 0 or dimensions < 1: raise SpecInvalid("capacity needs replicas ≥ 1, vector_count ≥ 0, dimensions ≥ 1")
    vectors = int(math.ceil(vector_count * dimensions * DTYPE_BYTES[dtype]))
    graph = vector_count * spec.m * 2 * GRAPH_EDGE_BYTES if spec.type == "hnsw" else 0
    quantized = 0
    if quant.lossy:
        quantized = int(math.ceil(vector_count * dimensions * QUANT_BYTES[quant.method]))
        if not quant.reversible: vectors = 0                     # dropped originals: the quantized copy replaces them
    return CapacityEstimate(vectors, graph, quantized, replicas)


# -------------------------------------------------------------------------------------------------------- manifest

@dataclass(frozen=True)
class TenantProof:
    date: str
    k: int
    ef_search: Optional[int]
    tenant_a: str
    tenant_b: str
    results_a: int
    results_b: int
    cross_hits: int
    spec_hash: str
    tenant_model: str
    fixture_hash: str = ""


@dataclass
class StoreManifest:
    """The record beside the s7 IndexManifest. Build it with for_config(); never type embedding_fingerprint by hand — check()
    recomputes it from the configuration and refuses a disagreement (Verify 1)."""
    embedding_fingerprint: str
    dimensions: int
    dtype: str
    vector_count: int
    spec: IndexSpec
    tenant_model: str = "none"
    multi_tenant: bool = False
    quantization: Quantization = field(default_factory=Quantization)
    quantization_records: Optional[tuple[str, str]] = None     # (before, after) BenchmarkRecord paths
    placement: Optional[Placement] = None
    available_memory_bytes: int = 0                              # <<AVAILABLE_MEMORY_BYTES>>
    replicas: int = 1                                            # <<REPLICAS>>
    benchmark: Optional[str] = None                              # BenchmarkRecord path for the current spec + quantization
    fixture: Optional[str] = None                                # the fixture every record and proof is bound to
    tenant_proof: Optional[TenantProof] = None
    filter_classes: dict[str, dict] = field(default_factory=dict)  # name -> {"strategy": str, "record": path of the filtered run}
    recall_floor: float = 0.0

    def __post_init__(self) -> None: self._validate()

    def _validate(self) -> None:
        """Shared by __post_init__ and check(): a manifest mutated after construction is re-validated before it is trusted."""
        if not isinstance(self.spec, IndexSpec) or not isinstance(self.quantization, Quantization):
            raise SpecInvalid("spec must be an IndexSpec and quantization a Quantization")
        if self.placement is not None and not isinstance(self.placement, Placement): raise SpecInvalid("placement must be a Placement")
        if self.tenant_model not in TENANT_MODELS:
            raise SpecInvalid(f"tenant model {self.tenant_model!r} is not one of {TENANT_MODELS} — 'rls_only' is not a model: RLS is the "
                              "control, it needs a partition, a partial index or an iterative scan beside it (pgvector README, read 2026-10-05)")
        if self.multi_tenant and self.tenant_model == "none":
            raise SpecInvalid("multi_tenant holds but tenant_model is 'none': name the isolation model (tenant-isolation-in-the-store.md)")
        if not isinstance(self.replicas, int) or self.replicas < 1: raise SpecInvalid(f"replicas={self.replicas!r}: at least one copy must exist")
        if not isinstance(self.vector_count, int) or self.vector_count < 0: raise SpecInvalid("vector_count must be a non-negative integer")
        if not 0 <= self.recall_floor <= 1: raise SpecInvalid("recall_floor must be in [0, 1]")
        for name, fc in self.filter_classes.items():
            if not isinstance(fc, dict) or fc.get("strategy") not in STRATEGIES or not fc.get("record"):
                raise SpecInvalid(f"filter class {name!r} needs a strategy in {STRATEGIES} and the path of its filtered benchmark record (`record`)")
            if "selectivity" in fc:
                raise SpecInvalid(f"filter class {name!r} carries a typed selectivity: selectivity is measured by run_benchmark() and read from its record")

    @classmethod
    def for_config(cls, config: EmbeddingConfig, vector_count: int, spec: IndexSpec, **kw) -> "StoreManifest":
        return cls(config.fingerprint(), config.dimensions, config.dtype, vector_count, spec, **kw)

    def quant_hash(self) -> str:
        return self.quantization.quantization_hash()

    def index_block(self) -> dict:
        """The `index` block the s7 IndexManifest must carry for this store (type, params, quantization, placement). The repo
        writes it into the s7 manifest; check(s7_manifest=…) refuses a disagreement on any of the four keys."""
        return {"type": self.spec.type, "params": self.spec.params(),
                "quantization": self.quantization.method if self.quantization.lossy else None,
                "placement": self.placement.vectors if self.placement else "ram"}

    def set_quantization(self, q: Quantization, before_path: str, after_path: str) -> None:
        """Verify 6: the before/after recall comes from two benchmark records of the SAME spec and fixture — one under no
        quantization, one under `q` — never from a caller's numbers."""
        if q.recall_before is not None or q.recall_after is not None:
            raise QuantizationUnmeasured("recall_before/recall_after are copied from benchmark records; do not type them")
        before, after = BenchmarkRecord.load(before_path), BenchmarkRecord.load(after_path)
        verify_record(before, self.spec, NO_QUANT_HASH, self.fixture); verify_record(after, self.spec, q.quantization_hash(), self.fixture)
        self.quantization = dataclasses.replace(q, recall_before=before.recall_at_k, recall_after=after.recall_at_k)
        self.quantization_records = (before_path, after_path); self.benchmark = after_path

    def filter_selectivity(self, name: str) -> float:
        """Verify 5: the selectivity of a filter class is read from its filtered benchmark record, never from the manifest."""
        fc = self.filter_classes.get(name)
        if fc is None: raise SpecInvalid(f"filter class {name!r} is not recorded in the manifest (strategy, record): run the filtered benchmark before filtering on it")
        rec = BenchmarkRecord.load(fc["record"]); verify_record(rec, self.spec, self.quant_hash(), self.fixture)
        if rec.filter_class != name or rec.selectivity is None:
            raise SpecInvalid(f"filter class {name!r} has no measured selectivity: its record is not a filtered run of this class")
        return rec.selectivity

    def check(self, config: EmbeddingConfig, s7_manifest: Optional[IndexManifest] = None, backend: Optional["Backend"] = None,
              fixture: Optional[str] = None) -> None:
        self._validate()
        fp = config.fingerprint()
        if self.embedding_fingerprint != fp:
            raise ManifestMismatch(f"store manifest fingerprint {self.embedding_fingerprint} ≠ configuration {fp}: another model, version, dimension, dtype, metric or convention")
        if self.dimensions != config.dimensions or self.dtype != config.dtype:
            raise ManifestMismatch(f"store manifest ({self.dimensions}, {self.dtype}) ≠ configuration ({config.dimensions}, {config.dtype})")
        if s7_manifest is not None:
            if s7_manifest.config_fingerprint != fp:
                raise ManifestMismatch("the embedding (s7) manifest is bound to another configuration")
            theirs = dict(getattr(s7_manifest, "index", None) or {"type": "flat"}); mine = self.index_block()
            diffs = {k: (theirs.get(k), mine[k]) for k in mine if theirs.get(k) != mine[k]}
            if diffs:
                raise ManifestMismatch(f"embedding manifest's index block disagrees with the store manifest on {diffs}: one of them lies")
        if backend is not None and backend.index_type() != self.spec.type:
            raise ManifestMismatch(f"backend reports a {backend.index_type()!r} index, store manifest says {self.spec.type!r}")
        if self.spec.approximate and self.vector_count < self.spec.flat_until:
            raise ThresholdNotReached(f"{self.spec.type} at {self.vector_count:,} vectors under flat_until={self.spec.flat_until:,}: stay exact until the threshold is measured and crossed")
        fixture = fixture or self.fixture
        if self.quantization.lossy:
            if not self.quantization_records:
                raise QuantizationUnmeasured("lossy quantization with no before/after benchmark records: use set_quantization()")
            b, a = (BenchmarkRecord.load(p) for p in self.quantization_records)
            verify_record(b, self.spec, NO_QUANT_HASH, fixture); verify_record(a, self.spec, self.quant_hash(), fixture)
            if (self.quantization.recall_before, self.quantization.recall_after) != (b.recall_at_k, a.recall_at_k):
                raise QuantizationUnmeasured("quantization recall_before/recall_after disagree with the records they claim to come from")
        if self.spec.approximate:
            require_benchmark(self, fixture)
        for name in self.filter_classes: self.filter_selectivity(name)
        if self.multi_tenant:
            p = self.tenant_proof
            if p is None or p.spec_hash != self.spec.spec_hash() or p.tenant_model != self.tenant_model or (fixture and p.fixture_hash != _file_hash(fixture)):
                raise TenantRequired("multi_tenant manifest without a two-tenant proof at the current spec, tenant model and fixture: run run_tenant_proof()")
            if p.cross_hits or p.results_a < p.k or p.results_b < p.k:
                raise TenantRequired(f"tenant proof failed: {p.results_a}/{p.k} and {p.results_b}/{p.k} results, {p.cross_hits} cross-tenant hits")
            _iso_date(p.date, "tenant proof")
        est = capacity_estimate(self.vector_count, self.dimensions, self.dtype, self.spec, self.quantization, self.replicas)
        need = est.resident(self.placement)
        if need > self.available_memory_bytes:
            where = "unset" if self.placement is None else f"vectors on {self.placement.vectors}, index on {self.placement.index}, pinned={self.placement.pinned}"
            raise CapacityExceeded(f"{need / 2**30:.2f} GiB must be resident (estimate {est}) against the recorded memory {self.available_memory_bytes / 2**30:.2f} GiB "
                                   f"with placement {where}: decide a Placement or buy memory before the build")

    def digest(self) -> str:
        return _h(self._as_dict())

    def _as_dict(self) -> dict:
        d = asdict(self); d["spec"] = asdict(self.spec); d["quantization"] = asdict(self.quantization)
        d["placement"] = asdict(self.placement) if self.placement else None
        d["tenant_proof"] = asdict(self.tenant_proof) if self.tenant_proof else None
        return d

    def to_json(self, path: str) -> str:
        """Writes the manifest and, beside it, the s7 `index` block the embedding manifest must carry (`s7_index_block`)."""
        d = self._as_dict(); d["s7_index_block"] = self.index_block()
        with open(path, "w", encoding="utf-8") as f: json.dump(d, f, indent=1)
        return path

    @classmethod
    def from_json(cls, path: str) -> "StoreManifest":
        with open(path, encoding="utf-8") as f: d = json.load(f)
        d.pop("s7_index_block", None)
        d["spec"] = IndexSpec(**d["spec"]); d["quantization"] = Quantization(**d["quantization"])
        d["placement"] = Placement(**d["placement"]) if d.get("placement") else None
        d["tenant_proof"] = TenantProof(**d["tenant_proof"]) if d.get("tenant_proof") else None
        if d.get("quantization_records"): d["quantization_records"] = tuple(d["quantization_records"])
        return cls(**d)


def require_benchmark(manifest: StoreManifest, fixture: Optional[str] = None) -> BenchmarkRecord:
    """Verify 3: an approximate spec is accepted only with a record for THIS spec, THIS quantization and THE manifest's fixture."""
    if not (fixture or manifest.fixture):
        raise BenchmarkRequired("the store manifest names no fixture: a benchmark record cannot be bound to nothing (set StoreManifest.fixture)")
    if not manifest.benchmark:
        raise BenchmarkRequired(f"{manifest.spec.type} spec with no benchmark record: run run_benchmark() on the repo's fixture first")
    rec = BenchmarkRecord.load(manifest.benchmark)
    verify_record(rec, manifest.spec, manifest.quant_hash(), fixture or manifest.fixture)
    return rec


# ----------------------------------------------------------------------------------------------------------- query

@dataclass(frozen=True)
class Query:
    """A query that knows its tenant and its filters. Frozen and signed so an accidental mutation after construction is caught;
    the CONTROL is the store's own tenant predicate (RLS, partition, namespace) — this object only carries the value to it."""
    embedded: Embedded
    k: int
    tenant: Optional[str] = None
    filters: dict = field(default_factory=dict)       # filter class name -> value
    strategy: str = "auto"
    _sig: str = field(default="", repr=False, compare=False)

    def _signature(self) -> str: return _h([getattr(self.embedded, "fingerprint", None), self.k, self.tenant, sorted(self.filters.items()), self.strategy])
    def __post_init__(self) -> None: object.__setattr__(self, "_sig", self._signature())

    def validate(self, manifest: StoreManifest) -> None:
        if self._sig != self._signature(): raise TenantRequired("query was altered after construction (tenant, k, filters or strategy): build a new Query")
        if not isinstance(self.embedded, Embedded): raise ManifestMismatch("only vectors tagged by the s7 Embedder query this store")
        if self.embedded.fingerprint != manifest.embedding_fingerprint:
            raise ManifestMismatch(f"query embedded under {self.embedded.fingerprint}, store is {manifest.embedding_fingerprint}")
        if self.embedded.side != "query": raise ManifestMismatch(f"a {self.embedded.side}-side vector cannot query the store")
        if self.k < 1 or self.strategy not in STRATEGIES: raise SpecInvalid("k ≥ 1 and a known strategy are required")
        if manifest.multi_tenant and not self.tenant:
            raise TenantRequired("query without a tenant under multi_tenant: the store's tenant predicate needs a value (Verify 4)")
        if manifest.spec.type == "hnsw" and manifest.spec.ef_search < self.k:
            raise SpecInvalid(f"ef_search={manifest.spec.ef_search} < k={self.k}: the candidate list bounds the result count (pgvector README, read 2026-10-05)")
        for name in self.filters:
            sel = manifest.filter_selectivity(name)                 # refuses an unrecorded class or one with no measured selectivity
            if sel <= SELECTIVE_BELOW and (self.strategy == "post" or manifest.filter_classes[name]["strategy"] == "post"):
                raise SpecInvalid(f"filter {name!r} is selective (measured {sel:.1%} of rows ≤ {SELECTIVE_BELOW:.0%}) and strategy=post: post-filtering a fixed "
                                  f"candidate list returns fewer than k (principle 18 §3.4); use in_graph, pre, iterative or exact")


class Backend(Protocol):
    def index_type(self) -> str: ...
    def upsert(self, row_id: str, vector: Sequence[float], tenant: Optional[str], payload: dict) -> None: ...
    def search(self, vector: Sequence[float], k: int, tenant: Optional[str], filters: dict, ef_search: Optional[int], iterative: bool) -> list[str]: ...


def _dot(a, b) -> float: return sum(x * y for x, y in zip(a, b))


class ExactBackend:
    """<<STORE_BACKEND>> — the day-0 store and the ground truth: every row scored, predicates applied before ranking."""
    def __init__(self): self.rows: dict[str, tuple[list[float], Optional[str], dict]] = {}
    def index_type(self) -> str: return "flat"
    def upsert(self, row_id, vector, tenant, payload): self.rows[row_id] = (list(vector), tenant, dict(payload))
    def _match(self, row, tenant, filters):
        _, t, p = row
        return (tenant is None or t == tenant) and all(p.get(k) == v for k, v in filters.items())
    def count(self, tenant=None, filters=None) -> int:
        return sum(1 for r in self.rows.values() if self._match(r, tenant, filters or {}))
    def search(self, vector, k, tenant, filters, ef_search=None, iterative=False) -> list[str]:
        cand = [(rid, _dot(vector, v)) for rid, (v, t, p) in self.rows.items() if self._match((v, t, p), tenant, filters)]
        return [rid for rid, _ in sorted(cand, key=lambda x: -x[1])[:k]]


class StubApproxBackend(ExactBackend):
    """A stand-in for a SHARED approximate index: the candidate list (ef_search) is drawn over the whole collection, THEN the
    tenant and filter predicates apply — pgvector's "filtering is applied after the index is scanned". `partitioned=True`
    draws the candidates inside the tenant's partition (list partitioning, a partial index, a namespace); `iterative=True`
    keeps widening the list until k results pass or MAX_SCAN_TUPLES is reached (hnsw.iterative_scan). One row in
    UNREACHABLE_EVERY is never reached (a node the graph lost — what percolation produces), so recall against exact is below 1 and
    the floor of Verify 9 can fail; exact search still sees every row."""
    UNREACHABLE_EVERY = 50
    def __init__(self, partitioned: bool = False): super().__init__(); self.partitioned = partitioned
    def index_type(self) -> str: return "hnsw"
    def _reachable(self, rid: str) -> bool: return int(hashlib.md5(rid.encode("utf-8")).hexdigest(), 16) % self.UNREACHABLE_EVERY != 0
    def search(self, vector, k, tenant, filters, ef_search=None, iterative=False) -> list[str]:
        ef = ef_search or 40
        pool = [(rid, _dot(vector, v)) for rid, (v, t, p) in self.rows.items()
                if self._reachable(rid) and (not self.partitioned or tenant is None or t == tenant)]
        pool.sort(key=lambda x: -x[1])
        limit = ef
        while True:
            out = [rid for rid, _ in pool[:limit] if self._match(self.rows[rid], tenant, filters)][:k]
            if len(out) >= k or not iterative or limit >= min(len(pool), MAX_SCAN_TUPLES): return out
            limit *= 2


class Store:
    """The manifest, the two backends and the refusals in front of them. Construction RUNS manifest.check() against the
    configuration, the s7 manifest and the approximate backend (Verify 1); a manifest changed afterwards is refused."""
    def __init__(self, manifest: StoreManifest, config: EmbeddingConfig, approx: Backend, exact: Optional[ExactBackend] = None,
                 s7_manifest: Optional[IndexManifest] = None, fixture: Optional[str] = None):
        manifest.check(config, s7_manifest, backend=approx, fixture=fixture)
        self.manifest, self.config, self.approx, self.exact = manifest, config, approx, exact or ExactBackend()
        self._checked = manifest.digest()

    @classmethod
    def for_measurement(cls, manifest: StoreManifest, config: EmbeddingConfig, approx: Backend, exact: Optional[ExactBackend] = None) -> "Store":
        """The ONE way around the benchmark gate, for the run that produces the record: the manifest is validated and bound to the
        configuration and the backend's index type, but no record, proof or capacity is required yet. Use it in the benchmark job
        only; production code constructs `Store()`."""
        manifest._validate()
        if manifest.embedding_fingerprint != config.fingerprint(): raise ManifestMismatch("measurement store: manifest fingerprint ≠ configuration")
        if approx.index_type() != manifest.spec.type: raise ManifestMismatch(f"measurement store: backend reports {approx.index_type()!r}, manifest says {manifest.spec.type!r}")
        self = cls.__new__(cls); self.manifest, self.config, self.approx, self.exact = manifest, config, approx, exact or ExactBackend()
        self._checked = manifest.digest(); return self

    def recheck(self, s7_manifest: Optional[IndexManifest] = None, fixture: Optional[str] = None) -> None:
        """After a deliberate manifest change (a benchmark written, a proof recorded): check again, then accept the new digest."""
        self.manifest.check(self.config, s7_manifest, backend=self.approx, fixture=fixture); self._checked = self.manifest.digest()

    def _ensure_checked(self) -> None:
        if self.manifest.digest() != self._checked:
            raise ManifestMismatch("store manifest changed after check(): call recheck() before querying or writing")

    def _accept(self, e, side: str) -> None:
        if not isinstance(e, Embedded): raise ManifestMismatch("only vectors tagged by the s7 Embedder enter or query this store")
        if e.fingerprint != self.manifest.embedding_fingerprint:
            raise ManifestMismatch(f"vector embedded under {e.fingerprint}, store is {self.manifest.embedding_fingerprint}: rebuild behind a new manifest")
        if e.side != side: raise ManifestMismatch(f"a {e.side}-side vector cannot be used as a {side}")
        if len(e.vector) != self.manifest.dimensions: raise ManifestMismatch(f"vector has {len(e.vector)} dimensions, store has {self.manifest.dimensions}")

    def upsert(self, row_id: str, embedded: Embedded, tenant: Optional[str] = None, payload: Optional[dict] = None) -> None:
        self._ensure_checked(); self._accept(embedded, "document")
        if self.manifest.multi_tenant and not tenant: raise TenantRequired("upsert without a tenant under multi_tenant")
        for b in (self.approx, self.exact): b.upsert(row_id, embedded.vector, tenant, payload or {})

    def search(self, q: Query) -> list[str]:
        self._ensure_checked(); q.validate(self.manifest); self._accept(q.embedded, "query")
        if q.strategy == "exact": return self.exact.search(q.embedded.vector, q.k, q.tenant, q.filters)
        iterative = q.strategy == "iterative" or self.manifest.tenant_model == "rls_with_iterative_scan"
        out = self.approx.search(q.embedded.vector, q.k, q.tenant, q.filters, self.manifest.spec.ef_search, iterative)
        if len(out) < q.k:
            raise UnderFilled(f"{len(out)} of k={q.k} results passed the tenant/filter predicates after the approximate scan "
                              f"(tenant={q.tenant!r}, filters={q.filters}): a shared or post-filtered index lost recall — partition, iterate or go exact", len(out))
        return out


def recall_at_k(approx_ids: Sequence[str], exact_ids: Sequence[str]) -> float:
    return len(set(approx_ids) & set(exact_ids)) / max(1, len(exact_ids))


def sampled_recall(store: Store, queries: Sequence[Embedded], k: int, tenant: Optional[str] = None, filters: Optional[dict] = None) -> float:
    """Verify 9: the approximate index against exact search over the same vectors (Dilocker 2023: 'sampled brute force comparisons').
    An under-filled query counts as zero: fewer than k is a failure, not a lower recall."""
    tot = 0.0
    for e in queries:
        q = Query(e, k, tenant, filters or {}, "auto")
        try: approx = store.search(q)
        except UnderFilled: approx = []
        tot += recall_at_k(approx, store.search(dataclasses.replace(q, strategy="exact")))
    return round(tot / max(1, len(queries)), 4)


filtered_recall = sampled_recall    # the filtered run of benchmark-protocol.md §4: same function, filters passed


def run_benchmark(store: Store, queries: Sequence[Embedded], k: int, fixture: str, build_seconds: float, memory_bytes: int,
                  concurrency: int = 1, filters: Optional[dict] = None, filter_class: Optional[str] = None, date: Optional[str] = None,
                  strategy: str = "auto") -> BenchmarkRecord:
    """Writes the record Verify 3 requires: recall@k vs exact, QPS at the stated concurrency, p99, memory, build time, date, bound
    to the fixture hash, the spec hash and the quantization hash. A filtered run (`filters` + `filter_class`) also MEASURES the
    class's selectivity as matching rows / rows on the exact backend (Verify 5). `strategy` is the approximate strategy under
    test (`auto`, `iterative`, …); the ground truth is always exact. The reference measures the stub; the repo measures the store."""
    if (filters is None) != (filter_class is None): raise SpecInvalid("a filtered run names both filters and filter_class")
    lat = []; hits = 0.0
    for e in queries:
        t0 = time.perf_counter(); q = Query(e, k, None, filters or {}, strategy) if filters is None else Query(e, k, None, filters, "exact")
        if filters is not None:                                   # the approximate filtered run bypasses the strategy check: it is the measurement
            try: approx = store.approx.search(e.vector, k, None, filters, store.manifest.spec.ef_search, strategy == "iterative")
            except VectorStoreError: approx = []
            if len(approx) < k: approx = []
        else:
            try: approx = store.search(q)
            except UnderFilled: approx = []
        lat.append((time.perf_counter() - t0) * 1000); hits += recall_at_k(approx, store.exact.search(e.vector, k, None, filters or {}))
    lat.sort(); p99 = lat[min(len(lat) - 1, int(0.99 * len(lat)))]
    sel = round(store.exact.count(None, filters) / max(1, store.exact.count()), 4) if filters is not None else None
    return BenchmarkRecord(fixture, _file_hash(fixture), k, round(hits / len(queries), 4), round(len(queries) / max(1e-9, sum(lat) / 1000), 1),
                           concurrency, round(p99, 3), memory_bytes, build_seconds, date or datetime.date.today().isoformat(),
                           store.manifest.spec.spec_hash(), store.manifest.quant_hash(), filter_class, sel)


def run_tenant_proof(store: Store, queries_a: Sequence[Embedded], queries_b: Sequence[Embedded], tenant_a: str, tenant_b: str, k: int,
                     date: Optional[str] = None) -> TenantProof:
    """Verify 4: two tenants, overlapping content, the manifest's spec and ef_search; k results each and zero cross-tenant hits.
    The proof is bound to the fixture hash and the spec hash; `--check` re-runs it rather than trusting it."""
    m = store.manifest; owner = lambda rid: store.exact.rows[rid][1]
    def run(qs, tenant):
        n = k; cross = 0
        for e in qs:
            try: ids = store.search(Query(e, k, tenant, {}, "auto"))
            except UnderFilled as ex: n = min(n, ex.returned); continue
            n = min(n, len(ids)); cross += sum(1 for r in ids if owner(r) != tenant)
        return n, cross
    na, ca = run(queries_a, tenant_a); nb, cb = run(queries_b, tenant_b)
    proof = TenantProof(date or datetime.date.today().isoformat(), k, m.spec.ef_search, tenant_a, tenant_b, na, nb, ca + cb, m.spec.spec_hash(),
                        m.tenant_model, _file_hash(m.fixture) if m.fixture else "")
    if proof.cross_hits or na < k or nb < k:
        raise UnderFilled(f"shared approximate index: tenant {tenant_a} received {na} and tenant {tenant_b} received {nb} of k={k}, "
                          f"{proof.cross_hits} cross-tenant hits — the proof fails; partition, iterate or change the tenant model", min(na, nb))
    m.tenant_proof = proof; return proof


# ------------------------------------------------------------------------------------------------------ --check

def _load_s7(path: Optional[str]) -> Optional[IndexManifest]:
    if not path: return None
    with open(path, encoding="utf-8") as f: d = json.load(f)
    return IndexManifest(d["config_fingerprint"], d["dimensions"], ChunkerRecord(**d["chunker"]) if d.get("chunker") else None,
                         d.get("corpus_hash", ""), None, d.get("index") or {"type": "flat"})


def run_check(manifest_path: str, fixture_path: Optional[str], k: int, floor: float, s7_manifest_path: Optional[str] = None) -> int:
    """Verify 9: exit 2 = no usable manifest (missing, malformed, no benchmark, proof fails on re-run, capacity overflow), 1 =
    sampled recall below the floor, 0 = pass. The stored TenantProof is NOT trusted: under multi_tenant the proof is re-run from the
    fixture's two largest tenants; recall is sampled per tenant and the smallest counts. The reference embeds the fixture with the
    s7 stub embedder and runs the stub backends."""
    if not os.path.exists(manifest_path): print(f"REFUSED: store manifest {manifest_path} is missing (exit 2)"); return 2
    try: m = StoreManifest.from_json(manifest_path)
    except (ValueError, KeyError, TypeError, VectorStoreError) as e:
        print(f"REFUSED: store manifest {manifest_path} is malformed ({e.__class__.__name__}: {str(e)[:80]}) (exit 2)"); return 2
    config = EmbeddingConfig(**DEMO_CONFIG)
    fixture_path = fixture_path or m.fixture
    try:
        s7 = _load_s7(s7_manifest_path)
        with open(fixture_path, encoding="utf-8") as f: fx = json.load(f)
        corpus, queries = fx["corpus"], fx["queries"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"REFUSED: fixture {fixture_path!r} or s7 manifest {s7_manifest_path!r} unusable ({e.__class__.__name__}) (exit 2)"); return 2
    embedder = Embedder(config, make_stub_backend(config.native_dimensions, ApproxTokenizer()))
    approx = StubApproxBackend(partitioned=m.tenant_model in PARTITIONED_MODELS) if m.spec.approximate else ExactBackend()
    try: store = Store(m, config, approx, s7_manifest=s7, fixture=fixture_path)
    except VectorStoreError as e:
        print(f"REFUSED: {e.__class__.__name__}: {str(e)[:110]} (exit 2)"); return 2
    for rid, row in corpus.items():
        store.upsert(rid, embedder.embed([row["text"]], side="document")[0], row.get("tenant"), row.get("payload", {}))
    qs = embedder.embed(queries, side="query")
    tenants = sorted({r.get("tenant") for r in corpus.values() if r.get("tenant")}, key=lambda t: -store.exact.count(t))
    if m.multi_tenant:
        if len(tenants) < 2: print("REFUSED: multi_tenant manifest but the fixture holds fewer than two tenants: the proof cannot run (exit 2)"); return 2
        try:
            half = max(1, len(qs) // 2); proof = run_tenant_proof(store, qs[:half], qs[half:], tenants[0], tenants[1], k); store.recheck(s7, fixture_path)
            print(f"check: tenant proof re-run from the fixture — {tenants[0]} {proof.results_a}/{k}, {tenants[1]} {proof.results_b}/{k}, {proof.cross_hits} cross-tenant hits")
        except VectorStoreError as e:
            print(f"REFUSED: the stored tenant proof is not trusted; re-run from the fixture failed — {str(e)[:110]} (exit 2)"); return 2
    r = min(sampled_recall(store, qs, k, t) for t in (tenants if m.multi_tenant else [None]))
    floor = max(floor, m.recall_floor)
    print(f"check: sampled recall@{k} = {r} on {len(queries)} queries ({m.spec.type}, ef_search={m.spec.ef_search}, tenants={tenants if m.multi_tenant else 'n/a'})")
    if r < floor: print(f"REFUSED: recall {r} is below the floor {floor} (exit 1)"); return 1
    print(f"check: OK (floor {floor})"); return 0


# --------------------------------------------------------------------------------------------------------- demo

def _demo_fixture(path: str) -> dict:
    """400 rows: tenant-A owns 380, tenant-B 20 (5 % — a small tenant on a shared index); region=eu on every tenth row."""
    topics = ["refund policy", "shipping zones", "warranty terms", "account security", "billing cycles", "data retention"]
    corpus, queries = {}, []
    for t_i, (tenant, n) in enumerate((("tenant-A", 380), ("tenant-B", 20))):
        for i in range(n):
            topic = topics[i % 6]; region = "eu" if i % 10 == 0 else "us"
            corpus[f"{tenant}-{i}"] = {"text": f"Clause {t_i}.{i} of the {topic} states that item {i * 7 % 23} is handled within {i + 2} days by team {chr(65 + i % 9)}.",
                                       "tenant": tenant, "payload": {"region": region}}
    for i in range(12): queries.append(f"which clause of the {topics[i % 6]} covers item {i * 7 % 23}")
    with open(path, "w", encoding="utf-8") as f: json.dump({"corpus": corpus, "queries": queries}, f)
    return json.load(open(path, encoding="utf-8"))


def demo(date: str) -> int:
    passed = 0
    def ok(msg): nonlocal passed; passed += 1; print(f"  ok   {msg}")
    def refused(label, fn, exc=VectorStoreError):
        nonlocal passed
        try: fn()
        except exc as e: passed += 1; print(f"  REFUSED {label}: {str(e)[:120]}"); return
        print(f"  FAIL {label}: nothing was refused"); raise SystemExit(1)

    tmp = tempfile.mkdtemp(prefix="vector-store-demo-"); fixture = os.path.join(tmp, "fixture.json"); fx = _demo_fixture(fixture)
    config = EmbeddingConfig(**DEMO_CONFIG); tok = ApproxTokenizer()
    embedder = Embedder(config, make_stub_backend(config.native_dimensions, tok))
    other = Embedder(EmbeddingConfig(**{**DEMO_CONFIG, "model": "demo-embed-4"}), make_stub_backend(1536, tok))
    GiB = 2**30; FLAT = IndexSpec("flat", flat_until=100_000); HNSW = IndexSpec("hnsw", flat_until=100_000, m=16, ef_construction=64, ef_search=40)
    s7 = IndexManifest(config.fingerprint(), config.dimensions, ChunkerRecord("recursive", 200, 0, config.tokenizer_name))   # index block defaults to flat
    base = dict(available_memory_bytes=8 * GiB, fixture=fixture)
    def load(store):
        for rid, row in fx["corpus"].items(): store.upsert(rid, embedder.embed([row["text"]], side="document")[0], row["tenant"], row["payload"])
    print(f"demo: configuration {config.fingerprint()}; fixture {fixture} ({len(fx['corpus'])} rows, {len(fx['queries'])} queries); record date {date}")

    print("\n[1] a store manifest bound to the embedding configuration; a Store cannot exist unchecked (Verify 1)")
    exact = ExactBackend()
    refused("Store over a manifest whose fingerprint was hand-typed to 'deadbeef' (an Embedded forged with the same tag would otherwise pass _accept)",
            lambda: Store(StoreManifest("deadbeef", 1536, "float32", 4_000, FLAT, **base), config, ExactBackend()), ManifestMismatch)
    refused("store manifest bound to another EmbeddingConfig with the SAME 1536 dimensions",
            lambda: Store(StoreManifest.for_config(other.config, 4_000, FLAT, **base), config, ExactBackend()), ManifestMismatch)
    refused("Store(flat manifest, StubApproxBackend()): backend reports hnsw, store manifest says flat",
            lambda: Store(StoreManifest.for_config(config, 4_000, FLAT, **base), config, StubApproxBackend()), ManifestMismatch)
    refused("s7 manifest's index block says flat, store manifest says hnsw",
            lambda: StoreManifest.for_config(config, 250_000, HNSW, **base).check(config, s7_manifest=s7), ManifestMismatch)
    s7_wrong = IndexManifest(config.fingerprint(), config.dimensions, ChunkerRecord("recursive", 200, 0, config.tokenizer_name),
                             index={"type": "hnsw", "params": {"m": 32, "ef_construction": 64, "ef_search": 40}, "quantization": None, "placement": "ram"})
    refused("s7 index block agrees on type but says m=32 where the store manifest says m=16",
            lambda: StoreManifest.for_config(config, 250_000, HNSW, **base).check(config, s7_manifest=s7_wrong), ManifestMismatch)
    m_flat = StoreManifest.for_config(config, 4_000, FLAT, **base); store = Store(m_flat, config, exact, exact, s7_manifest=s7)
    refused("upsert of an Embedded from another configuration", lambda: store.upsert("x", other.embed(["t"], side="document")[0]), ManifestMismatch)
    refused("upsert of a bare list", lambda: store.upsert("x", [0.1] * 1536), ManifestMismatch)
    m_flat.vector_count = 5_000
    refused("search after the manifest was mutated behind the Store (digest changed, no recheck)", lambda: store.search(Query(embedder.embed(["q"], side="query")[0], 3)), ManifestMismatch)
    store.recheck(s7)
    ok(f"flat manifest built with for_config (fingerprint {m_flat.embedding_fingerprint}) checked at Store construction against the configuration, the s7 index block {m_flat.index_block()} and the exact backend; recheck() after a deliberate change")

    print("\n[2] exact until flat_until (Verify 2)")
    refused("spec without flat_until", lambda: IndexSpec("hnsw", m=16, ef_construction=64, ef_search=40), SpecInvalid)
    refused("HNSW spec at 4,000 vectors under flat_until=100,000", lambda: StoreManifest.for_config(config, 4_000, HNSW, **base).check(config), ThresholdNotReached)
    ok("flat spec at 4,000 vectors accepted; the HNSW spec is accepted at 250,000 vectors in step [3] once its record exists")

    print("\n[3] validated parameters and a benchmark record for THIS spec on THE manifest's fixture (Verify 3)")
    refused("m=1", lambda: IndexSpec("hnsw", flat_until=1, m=1, ef_construction=64, ef_search=40), SpecInvalid)
    refused(f"m={M_MAX + 1} above the reference ceiling", lambda: IndexSpec("hnsw", flat_until=1, m=M_MAX + 1, ef_construction=512, ef_search=40), SpecInvalid)
    refused("ef_construction=8 < m=16", lambda: IndexSpec("hnsw", flat_until=1, m=16, ef_construction=8, ef_search=40), SpecInvalid)
    refused("probes=200 > lists=100", lambda: IndexSpec("ivf", flat_until=1, lists=100, probes=200), SpecInvalid)
    m_h = StoreManifest.for_config(config, 250_000, HNSW, **base)
    qs = embedder.embed(fx["queries"], side="query")
    refused("ef_search=5 for k=10", lambda: Query(qs[0], 10).validate(StoreManifest.for_config(config, 250_000, dataclasses.replace(HNSW, ef_search=5), **base)), SpecInvalid)
    refused("HNSW spec with no benchmark record", lambda: m_h.check(config), BenchmarkRequired)
    typed = os.path.join(tmp, "typed.json"); BenchmarkRecord("/nonexistent/fixture.json", "0000000000000000", 10, 0.99, 5000.0, 1, 2.0, 1, 1.0, date, HNSW.spec_hash()).write(typed)
    m_h.benchmark = typed
    refused("benchmark record typed in with no fixture file", lambda: m_h.check(config), BenchmarkRequired)
    stale = os.path.join(tmp, "stale.json"); BenchmarkRecord(fixture, "1111111111111111", 10, 0.99, 5000.0, 1, 2.0, 1, 1.0, date, HNSW.spec_hash()).write(stale)
    m_h.benchmark = stale
    refused("benchmark record whose fixture hash differs from the fixture", lambda: m_h.check(config), BenchmarkRequired)
    baddate = os.path.join(tmp, "baddate.json"); BenchmarkRecord(fixture, _file_hash(fixture), 10, 0.99, 5000.0, 1, 2.0, 1, 1.0, "yesterday", HNSW.spec_hash()).write(baddate)
    m_h.benchmark = baddate
    refused("benchmark record dated 'yesterday'", lambda: m_h.check(config), BenchmarkRequired)
    # a measuring store: the manifest is not yet valid (no record), so measure through a provisional copy that skips the benchmark gate
    approx = StubApproxBackend(); m_h.benchmark = None
    probe = Store.for_measurement(m_h, config, approx); load(probe)
    rec = run_benchmark(probe, qs, 10, fixture, build_seconds=0.0, memory_bytes=1, date=date); m_h.benchmark = rec.write(os.path.join(tmp, "bench-hnsw-40.json"))
    store_h = Store(m_h, config, approx, probe.exact)
    refused("manifest that names no fixture (record present)", lambda: StoreManifest.for_config(config, 250_000, HNSW, available_memory_bytes=8 * GiB, benchmark=m_h.benchmark).check(config), BenchmarkRequired)
    m_128 = StoreManifest.for_config(config, 250_000, dataclasses.replace(HNSW, ef_search=128), benchmark=m_h.benchmark, **base)
    refused("ef_search 64 → 128 with the old record (spec hash differs)", lambda: m_128.check(config), BenchmarkRequired)
    ok(f"run_benchmark wrote {os.path.basename(m_h.benchmark)}: recall@10 {rec.recall_at_k}, {rec.qps} qps at concurrency {rec.concurrency}, p99 {rec.p99_ms} ms, "
       f"build {rec.build_seconds}s, {rec.date}, spec {rec.spec_hash}; HNSW accepted at 250,000 vectors; Store constructed over it")

    print("\n[4] the tenant travels inside the query; the proof needs k each and is re-run, never trusted (Verify 4)")
    refused("tenant model rls_only", lambda: StoreManifest.for_config(config, 250_000, HNSW, tenant_model="rls_only", **base), SpecInvalid)
    refused("tenant model none under multi_tenant", lambda: StoreManifest.for_config(config, 250_000, HNSW, multi_tenant=True, **base), SpecInvalid)
    m_mt = StoreManifest.for_config(config, 250_000, HNSW, multi_tenant=True, tenant_model="tenant_payload_index", benchmark=m_h.benchmark, **base)
    refused("multi_tenant manifest without a tenant proof (Store construction)", lambda: Store(m_mt, config, approx, store_h.exact), TenantRequired)
    shared = Store.for_measurement(m_mt, config, approx, store_h.exact)
    refused("query without tenant under multi_tenant", lambda: shared.search(Query(qs[0], 10)), TenantRequired)
    def mutate():
        q = Query(qs[0], 10, "tenant-A")
        try: q.tenant = "tenant-B"            # type: ignore[misc]
        except dataclasses.FrozenInstanceError: pass
        object.__setattr__(q, "tenant", "tenant-B")   # the frozen guard bypassed on purpose: the signature still catches the accident
        shared.search(q)
    refused("query built with tenant A then mutated to tenant B", mutate, TenantRequired)
    refused("shared approximate index: tenant B received fewer than k=10",
            lambda: run_tenant_proof(shared, qs[:6], qs[6:], "tenant-A", "tenant-B", 10, date), UnderFilled)
    m_mt2 = StoreManifest.for_config(config, 250_000, HNSW, multi_tenant=True, tenant_model="rls_with_partition", benchmark=m_h.benchmark, **base)
    part = StubApproxBackend(partitioned=True)
    for rid, (v, t, p) in store_h.exact.rows.items(): part.upsert(rid, v, t, p)
    probe2 = Store.for_measurement(m_mt2, config, part, store_h.exact)
    proof = run_tenant_proof(probe2, qs[:6], qs[6:], "tenant-A", "tenant-B", 10, date); Store(m_mt2, config, part, store_h.exact)
    forged = dataclasses.replace(m_mt, tenant_proof=dataclasses.replace(proof, tenant_model="tenant_payload_index"))
    forged_path = forged.to_json(os.path.join(tmp, "forged-proof.json"))
    forged.check(config)
    ok(f"a hand-edited manifest ({os.path.basename(forged_path)}) carrying a passing proof over a SHARED index passes in-process check(): hash-binding catches stale records, not forgery — step [9] shows --check re-running the proof and refusing it")
    ok(f"rls_with_partition: tenant-A {proof.results_a}/10, tenant-B {proof.results_b}/10, {proof.cross_hits} cross-tenant hits; proof bound to spec {proof.spec_hash} and fixture {proof.fixture_hash}")

    print("\n[5] filters: strategy per class, selectivity MEASURED, no silent under-fill (Verify 5)")
    refused("filter class with a typed selectivity 0.5", lambda: StoreManifest.for_config(config, 250_000, HNSW, benchmark=m_h.benchmark,
            filter_classes={"region": {"selectivity": 0.5, "strategy": "in_graph", "record": m_h.benchmark}}, **base), SpecInvalid)
    refused("filter class whose record is the unfiltered run (no measured selectivity)", lambda: Store(StoreManifest.for_config(config, 250_000, HNSW, benchmark=m_h.benchmark,
            filter_classes={"region": {"strategy": "in_graph", "record": m_h.benchmark}}, **base), config, approx, store_h.exact), SpecInvalid)
    frec = run_benchmark(store_h, qs, 10, fixture, 0.0, 1, filters={"region": "eu"}, filter_class="region", date=date)
    fpath = frec.write(os.path.join(tmp, "bench-hnsw-40-region.json"))
    m_f = StoreManifest.for_config(config, 250_000, HNSW, benchmark=m_h.benchmark, filter_classes={"region": {"strategy": "in_graph", "record": fpath}}, **base)
    store_f = Store(m_f, config, approx, store_h.exact)
    refused(f"strategy=post on a selective filter (measured selectivity {frec.selectivity:.0%})", lambda: store_f.search(Query(qs[0], 10, None, {"region": "eu"}, "post")), SpecInvalid)
    refused("filter class not recorded in the manifest", lambda: store_f.search(Query(qs[0], 10, None, {"team": "A"})), SpecInvalid)
    refused("filtered query under-filled: fewer than k=10", lambda: store_f.search(Query(qs[0], 10, None, {"region": "eu"})), UnderFilled)
    n_exact = len(store_f.search(Query(qs[0], 10, None, {"region": "eu"}, "exact")))
    ok(f"filtered run measured selectivity {frec.selectivity} (matching rows / rows on the exact backend) and filtered recall {frec.recall_at_k} with under-filled "
       f"queries counting as zero; strategy=exact returns {n_exact} of 10 for region=eu")

    print("\n[6] store quantization: rescoring, and a before/after from records (Verify 6)")
    refused("bq1 with rescore=False", lambda: Quantization("bq1", rescore=False, oversampling=3.0, originals="disk"), QuantizationUnmeasured)
    refused("method none with originals dropped", lambda: Quantization("none", originals="dropped"), SpecInvalid)
    bq = Quantization("bq1", rescore=True, oversampling=3.0, originals="disk")
    m_q = StoreManifest.for_config(config, 250_000, HNSW, benchmark=m_h.benchmark, **base)
    refused("bq1 with typed-in recall_before/recall_after and no record files",
            lambda: m_q.set_quantization(dataclasses.replace(bq, recall_before=0.98, recall_after=0.95), m_h.benchmark, m_h.benchmark), QuantizationUnmeasured)
    m_nb = StoreManifest.for_config(config, 250_000, HNSW, quantization=bq, **base)
    refused("quantization set on a manifest with no benchmark", lambda: m_nb.check(config), QuantizationUnmeasured)
    m_q.quantization = bq; probe_q = Store.for_measurement(m_q, config, approx, store_h.exact)
    after = run_benchmark(probe_q, qs, 10, fixture, 0.0, 1, date=date).write(os.path.join(tmp, "bench-bq1.json"))
    wrong = os.path.join(tmp, "bench-sq8.json"); m_q.quantization = Quantization("sq8", originals="disk"); probe_q = Store.for_measurement(m_q, config, approx, store_h.exact)
    run_benchmark(probe_q, qs, 10, fixture, 0.0, 1, date=date).write(wrong)
    m_q.quantization = Quantization()
    refused("after-record run under another quantization (hash differs)", lambda: m_q.set_quantization(bq, m_h.benchmark, wrong), BenchmarkRequired)
    m_q.set_quantization(bq, m_h.benchmark, after); Store(m_q, config, approx, store_h.exact)
    irreversible = dataclasses.replace(bq, originals="dropped")
    ok(f"bq1 (rescore, oversampling 3.0, originals on disk) set with recall before {m_q.quantization.recall_before} → after {m_q.quantization.recall_after} "
       f"copied from two records; reversible={m_q.quantization.reversible}. The irreversible variant (originals=dropped, reversible={irreversible.reversible}) is the row Martin reads BEFORE setting it")

    print("\n[7] capacity before the build, per medium (Verify 7)")
    big = StoreManifest.for_config(config, 1_000_000, HNSW, replicas=3, benchmark=m_h.benchmark, fixture=fixture, available_memory_bytes=8 * GiB)
    refused("1,000,000 × 1536 × float32, m=16, replicas=3 against 8 GB RAM, placement unset", lambda: big.check(config), CapacityExceeded)
    refused("placement on ssd without a cold-latency budget", lambda: Placement(vectors="ssd"), SpecInvalid)
    refused("placement with a negative cold-latency budget", lambda: Placement(vectors="ssd", cold_latency_budget_ms=-5), SpecInvalid)
    huge = StoreManifest.for_config(config, 1_000_000_000, HNSW, benchmark=m_h.benchmark, fixture=fixture, available_memory_bytes=1,
                                    placement=Placement(vectors="object", index="ram", cold_latency_budget_ms=800))
    refused("10⁹ vectors with the graph in RAM against 1 byte of memory (vectors on object storage)", lambda: huge.check(config), CapacityExceeded)
    big.placement = Placement(vectors="ssd", index="ram", cold_latency_budget_ms=800); big.check(config)
    est = capacity_estimate(1_000_000, 1536, "float32", HNSW, Quantization(), 3)
    big.tenant_model = "rls_only"
    refused("manifest mutated to tenant_model='rls_only' after construction, then check()", lambda: big.check(config), SpecInvalid)
    big.tenant_model = "none"; big.replicas = 0
    refused("manifest mutated to replicas=0 after construction, then check()", lambda: big.check(config), SpecInvalid)
    big.replicas = 3
    ok(f"estimate {est}; resident with vectors on ssd and graph in RAM = {est.resident(big.placement) / GiB:.2f} GiB (cold budget 800 ms), accepted")

    print("\n[9] the sampled exact comparison as a CI gate; the proof re-run from the fixture (Verify 9, 4)")
    m_h.recall_floor = rec.recall_at_k; mpath = m_h.to_json(os.path.join(tmp, "store-manifest.json"))
    s7path = os.path.join(tmp, "s7-manifest.json"); json.dump({"config_fingerprint": config.fingerprint(), "dimensions": 1536, "chunker": asdict(s7.chunker),
                                                                "index": m_h.index_block()}, open(s7path, "w"))
    assert run_check(os.path.join(tmp, "missing.json"), fixture, 10, 0.5) == 2; passed += 1
    bad = os.path.join(tmp, "bad.json"); open(bad, "w").write("{not json"); assert run_check(bad, fixture, 10, 0.5) == 2; passed += 1
    nob = dataclasses.replace(m_h, benchmark=os.path.join(tmp, "nowhere.json")).to_json(os.path.join(tmp, "no-bench.json")); assert run_check(nob, fixture, 10, 0.5) == 2; passed += 1
    assert run_check(forged_path, fixture, 10, 0.5) == 2; passed += 1          # the forged proof of step [4]: re-run under-fills tenant B
    s7flat = os.path.join(tmp, "s7-flat.json"); json.dump({"config_fingerprint": config.fingerprint(), "dimensions": 1536, "chunker": asdict(s7.chunker)}, open(s7flat, "w"))
    assert run_check(mpath, fixture, 10, 0.5, s7flat) == 2; passed += 1        # s7 manifest still says flat
    assert run_check(mpath, fixture, 10, 0.99, s7path) == 1; passed += 1
    mt_path = m_mt2.to_json(os.path.join(tmp, "store-manifest-mt.json"))
    assert run_check(mt_path, fixture, 10, 0.5) == 0; passed += 1              # multi_tenant: proof re-run, recall per tenant, smallest counts
    assert run_check(mpath, fixture, 10, 0.5, s7path) == 0; passed += 1
    print(f"\ndemo: {passed} checks passed; manifest at {mpath}")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--demo", action="store_true", help="offline walk through every refusal of the enforcement table")
    p.add_argument("--check", action="store_true", help="CI gate: exit 2 malformed/no benchmark/proof fails/capacity, 1 below floor")
    p.add_argument("--manifest", default="retrieval/store-manifest.json"); p.add_argument("--fixture", default=None)
    p.add_argument("--s7-manifest", default=None, help="the embedding (s7) manifest JSON; its index block must agree with the store manifest")
    p.add_argument("--k", type=int, default=10); p.add_argument("--floor", type=float, default=0.95)
    p.add_argument("--date", default=datetime.date.today().isoformat(), help="the date stamped on records the demo writes (default: today)")
    a = p.parse_args(argv)
    if a.demo: _iso_date(a.date, "--date"); return demo(a.date)
    if a.check: return run_check(a.manifest, a.fixture, a.k, a.floor, a.s7_manifest)
    p.print_help(); return 2


if __name__ == "__main__":
    sys.exit(main())
