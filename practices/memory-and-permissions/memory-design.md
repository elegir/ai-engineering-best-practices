# Memory design — <<feature>>

Copy to `<repo>/docs/memory.md`; one copy per feature that keeps anything beyond the session; date it. Principle: `../../principles/15-memory-external-context-and-permissions.md` §3.1–3.3. Sources: LangChain memory concepts (read 2026-10-01); Mem0 paper (2025-04) and the AAIF reading group (2025-06); Letta (2025-07); Alake (2026-04); Anthropic memory tool page (read 2026-10-01); Manus (s2, reused) — digest `../../sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` §3.6.

## 0. Does memory outlive the session at all?

Thread-scoped state — the message history, per-conversation variables, a checkpointer — is `../context-management/`. Answer this first: **what must the product know next week that the user said today?** If the answer is "nothing" (a one-shot tool, a stateless API), stop here and write "no long-term memory" with the date. The s2 rule holds: a single loop passes its eval before memory is added.

```
Feature: <<name>>                                   Date: <<>>
Outlives the session: <<yes / no>>                  Because: <<the user expects X to be remembered / regulatory retention / nothing>>
```

## 1. Types kept (CoALA via LangChain; Alake)

| Type | Means | Kept here? | Example | Runtime home |
|---|---|---|---|---|
| **Semantic** | facts about the user or the domain | <<yes>> | "prefers window seats"; "tenant uses EUR" | the knowledge base / profile |
| **Episodic** | past events and actions, timestamped | <<yes / no>> | "asked for a refund on 2026-09-30" | anything with a timestamp; few-shot examples for the model |
| **Procedural** | instructions the agent follows for this user or tenant | <<yes / no>> | "always answer in Spanish"; a learned workflow step | the system prompt's dynamic part; skills |

## 2. Profile or collection (LangChain)

- **Profile** — one JSON document per owner, regenerated or patched; simple, easy to show the user; "error-prone as it grows"; keep the schema strict (constrained decoding, `../structured-outputs/`).
- **Collection** — many small units; higher recall; the model (or the consolidator) must delete or update existing items, and "some models default to over-inserting, others to over-updating" — which is why the reference uses a *reasoning* model for the decision.

Decision: <<profile for the five fixed fields (language, timezone, plan), collection for everything else>>.

## 3. Hot path or background (LangChain; Mem0; Letta)

| | Hot path (during the turn) | Background (after the reply) |
|---|---|---|
| Latency | adds a model call per turn | none on the reply |
| Transparency | the user can see "saved to memory" (ChatGPT's `save_memories`; Manus's "would you like to accept it or reject it?") | needs a trigger policy and, where it matters, a later confirmation |
| Fits | agents working across sessions on their own tasks (a tool-triggered write — MemGPT/Letta, Anthropic's memory tool) | user-facing products where latency and quiet matter (Mem0: `add` async, `search` sync; Letta's sleep-time consolidation) |

Decision: <<background, queued after the response; user-confirmed for procedural memory>>. Mem0's numbers: three model calls per exchange (summary, extraction, update), one off the critical path; the graph variant roughly doubles tokens and is "not recommended to all users" — relational cases only (parked, sessions 10/11).

## 4. What is never written (include / exclude)

Mem0's platform asks for a use case, a memory style and **include/exclude lists** — order ids kept, SSNs not. Write the lists here; they are the `EXCLUDED_FIELDS` and `SECRET_SHAPES` of `memory_store.py` and the stripping duty of the memory-tool handler.

- Never: <<secrets and tokens; card numbers; government ids; health data unless the feature is for it; other users' names from a shared thread; anything the user asked not to remember>>
- Always: <<the fields the feature exists for>>
- Only with confirmation: <<procedural instructions ("always do X")>>

## 5. Retention, forgetting, erasure

- **Forgetting is a status with a trail**, not a delete (Alake: "you don't delete information in memory engineering. You forget"); a unit leaves recall by status (`forgotten`, with why and when) or by decay — recency × relevance × importance (Generative Agents 2023 via Alake; verify the paper's exact form before tuning) — and stays for audit.
- **Retention:** <<episodic units expire after N days; semantic units never expire but decay>>; implemented as `expire(store, identity, retention_days, now)` in `memory_store.py` — a `forget()` with the reason "retention", run from the same background job as consolidation, so an expired unit keeps its trail; expiry is a lifecycle feature, "not a guaranteed-deletion control" (Anthropic's Files page says the same of its expiry) — the erasure path below is the deletion control.
- **Erasure path** (where `personal_data` or `regulated` holds): <<a DSAR endpoint calls `erase()` for every unit of the owner; the request reference is logged outside the store; the vector index entry is removed in the same job>>. Forgetting serves audit; erasure serves the law; a product with both facts needs both.

## 6. Substrate and interface

The model's **interface** may be files or file-like commands (Claude Code's files, Manus's sandbox, Anthropic's memory tool over any store); the **substrate** behind a multi-user handler is a namespaced store with concurrency and audit (Alake's "ACID transactions… auditability", stripped of the one-database preference). Decision: <<a `memories` table with `owner_id`, `type`, `status`, `importance`, `source`, timestamps; a text index first, `pgvector` when the per-owner store exceeds N units>>. A single-user agent may keep real files.

## 7. Boundary with context engineering

Storage side — retrieval strategy, indexing, data model, the forget logic — is **memory engineering**; inside the window — budget, just-in-time retrieval, composition — is **context engineering** (Alake). A summary written back into the window is context engineering; the original moved to a store with an id and a description is memory engineering (Manus's compaction-vs-summarisation split). What this feature puts in the window: a block labelled by type with its purpose, ≤ <<n>> units / <<n>> characters, inside the budget of `../context-management/context-budget-and-triggers.md`.

## 8. The eval that proves it

`memory-eval.md` cases, run through `../evals/eval_harness.py` with `k = 5`: recall after N sessions; update on contradiction; forgotten after retention; no leak across identities. Pass^k floor: 1.0. Last run: <<date, result>>.
