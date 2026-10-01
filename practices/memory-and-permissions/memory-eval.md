# Memory eval — the cross-session cases that prove the store works

Copy to `<repo>/evals/memory/` as `cases.jsonl` plus this README; run through `../evals/eval_harness.py` with `k = 5` and the pass^k floor at 1.0 (`../evals/eval-policy.md` §3). Principle: `../../principles/15-memory-external-context-and-permissions.md` §3.3. Sources: Alake (2026-04 — "every memory unit… evaluated against LongMemEval, LoCoMo or MemBench"); Mem0 paper (2025-04 — LOCOMO as the benchmark; numbers are the vendor's); Arize's long-session eval (s2, `../context-management/context-metrics-and-evals.md` §2) — digest `../../sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` §3.6, §4.

## Why a separate eval

The long-session eval of s2 tests turn N+1 **within** a session after compaction. Memory fails **across** sessions: a fact said on Monday is not used on Thursday; a changed fact is still the old one; a forgotten fact comes back; one user's fact appears for another. These are outcome checks on the store and the prompt block, so they are code graders, not judges.

## The four minimum cases (one row each in `cases.jsonl`)

| Case | Setup (session 1 … N−1) | Check (session N) | Grader |
|---|---|---|---|
| **Recall** | user states a fact in session 1 ("I live in Lisbon"); N−2 unrelated sessions follow | a question that depends on it ("what's the weather where I live?") uses the fact — the tool call or the answer names Lisbon | `state_equals` on the tool argument, or `contains` on the output |
| **Update on contradiction** | session 1: "I live in Lisbon"; session 3: "I moved to Porto" | session N uses Porto and **not** Lisbon; the store has one active unit on the subject and the old one is `forgotten` with a trail | state check on the store + `contains` / negative `contains` |
| **Forgotten after retention** | an episodic unit with retention of N days, created N+1 days ago; the background job runs `expire(store, identity, N, now=clock)` with the injected clock | the fact is not used and `search(…, now=clock)` does not return it; the unit still exists with `status: forgotten` and a trail entry whose reason starts with "retention" | state check |
| **No leak across identities** | two identities with overlapping facts (both like coffee; different cities) | identity A's session N never receives B's city; the prompt block for A contains only A's units | state check on the prompt block (assertion 3) |

Add the product's own: a procedural memory applied ("always answer in Spanish" → the reply is Spanish); a secret said in session 1 never appears in any later prompt block (assertion 5); a user's "forget that" honoured in session N (assertion 4).

## Shape of a case (for `eval_harness.py`)

Each line is a task whose `input` is a script of sessions; `run_agent()` replays sessions 1…N−1 through the product (writing memory via the background path, clock advanced between sessions), then runs session N and records the prompt block, the tool calls and the final answer in `env["state"]`. Graders read `env["state"]`. Every trial starts from an **empty store** (clean environment, assertion 5 of the evals practice).

```json
{"id": "memory_update_on_contradiction", "input": "[{\"session\":1,\"user\":\"I live in Lisbon\"},{\"session\":3,\"user\":\"I moved to Porto\"},{\"session\":6,\"user\":\"what's the weather where I live?\"}]", "expected": {"weather_city": "Porto", "active_units_home_city": 1}, "assertions": [{"kind": "contains", "value": "Porto"}], "reference": "It is 21 °C in Porto today.", "parts": 2}
```

## One public benchmark (read before citing)

Alake names **LongMemEval, LoCoMo and MemBench**; Mem0 reports on **LOCOMO** (ten companion-style conversations; the paper's numbers are the vendor's). The s5 validation pass (`../../sources/scan-log.md` row 5) reads one of them in full before this file cites its task format; until then the product's own four cases are the eval, and a public benchmark is a sanity check on the store's retrieval, not a product metric.

## Cadence

In CI on every change to the extraction prompt, the consolidation prompt or model, the store schema, the retention policy or the prompt block template; `k = 5`; pass^k 1.0. A failed run is read in the viewer (`../evals/annotation-ui-brief.md`), not averaged away.
