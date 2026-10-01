---
title: "Practice — memory and permissions: a memory store the application owns (extract → consolidate, identity-scoped reads, forgetting with a trail), the provider's files, web search and memory tool used within their tenancy rules, and permissions carried from identity through retrieval to the tool boundary"
type: practice
status: draft            # draft until principle 15 is confirmed against LIDR session 5 (2026-11-12) and a real repo passes Verify
date: 2026-10-01
last-reviewed: 2026-10-01
tags: [memory, long-term-memory, mem0, memory-tool, consolidation, forgetting, files-api, web-search, permissions, rebac, approvals, nhi, s5]
kind: capability
applies-when: "multi_turn"
full-when: "multi_turn and (multi_tenant or personal_data or regulated or acts_on_world)"
when: first-user       # memory is not a day-0 artifact: a single loop passes its eval before memory is added (s2 rule); the Files and web-search notes are read whenever those provider tools are used
reference-status: untested   # decision 0005 §3; only a field report moves it
routed: false          # unrouted until the routing gate of decision 0004 §6 (the previous module's day-0 files must pass Verify in one real repo); no row in practices/README.md, absent from ROUTER.md
principle: principles/15-memory-external-context-and-permissions.md
sources:
  - sources/2026-10-01-s05-context-memory-permissions-evals-digest.md
  - https://docs.langchain.com/oss/python/concepts/memory
  - https://arxiv.org/abs/2504.19413
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
  - https://platform.claude.com/docs/en/build-with-claude/files
  - https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/web-search-tool
  - https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
  - https://www.pinecone.io/learn/rag-access-control/
supersedes: null
superseded-by: null
---

# Memory and permissions

## Solves
The product keeps history across turns or sessions and one of these symptoms appears: the assistant forgets a preference the next day, or repeats a stale one after the user changed it; a user profile that contradicts itself ("lives in Lisbon" and "lives in Porto", both active); every reply waits for a memory write, so latency grows with the store; one user's facts surface in another user's conversation, or a tenant's memory is readable by another tenant; a secret, a card number or an excluded field was saved as a memory; a `file_id` from a request is passed to the provider and reads another user's upload; web-search result blocks are edited before being sent back and the next turn fails; every agent and sub-agent shares one static API key; an MCP server was installed without review; a destructive tool runs with no approval, or an approval "approves" when nobody answers.

## Applies when
- The fact `multi_turn` holds (`../facts.md`): the product passes history back into the model. This folder answers what, if anything, should outlive the session and how it is written, read, scoped and forgotten; the session-only case is excluded below.
- The **full** part (assertion 10: identity per tool, approvals as resumable state, the retrieval filter placement; the erasure path of assertion 4) attaches when `multi_tenant or personal_data or regulated or acts_on_world` also holds — the safety facts of `../security-baseline/`, because the permissions this folder maps are the controls those facts demand.
- The notes on the provider's files, web search and memory tool (`external-context-notes.md`, `memory-tool-handler-notes.md`) are read whenever those tools are used, whatever the facts.

## Does not apply when
- Memory is the **session alone** — the message history that `../context-management/` budgets, compacts and offloads. Thread-scoped state (LangChain's short-term memory) is principle 11's problem; this folder starts where a fact must survive the session. "Does memory outlive the session?" is answered in `memory-design.md`, not by routing.
- The only memory is the **coding agent's** (`CLAUDE.md`, a progress file) — `../session-state/`, `../agent-entry-file/`.
- The product is a **retrieval pipeline over documents** with no per-user state — `../context-management/context-store-decision.md` and the RAG sessions; only the retrieval-authorisation rule of `permission-model.md` applies there.
- Runtime guardrail *content* (what a check looks for) is `../structured-outputs/guardrail-policy.md`; dry-run and the approval window are `../verification/dry-run-and-approval.md`; the register of tools and servers is `../security-baseline/mcp-trust-register.md`. This folder's `permission-model.md` is the **map** that points at them and adds the identity, retrieval and approval-state rules they lacked.
- Zero-trust infrastructure in full (vault, NHI lifecycle, AI gateway), authorisation as a service (SpiceDB), sandboxing — session 14; memory graphs and chunk-level permission metadata — sessions 10/11 (`../../sources/scan-log.md`).

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `memory_store.py` | `<repo>/src/<package>/memory.py` | Python reference: `MemoryUnit` (id, owner scope, type, text, timestamps, source pointer, status `active|forgotten`, importance, trail); `extract(exchange, summary, recent)` with include/exclude; `consolidate(candidate, neighbours) -> ADD|UPDATE|FORGET|NOOP` by a reasoning-model call; `search(store, identity, query, k, max_chars, owner=None, now=None)` with the identity filter applied **before** ranking (the requested `owner` validated against the identity on the read path itself), reads bounded by k and characters, an injectable clock; recency × relevance × importance scoring with `touch()` raising importance on a neighbour hit and on an UPDATE; `forget()` as a status change with a trail, `expire()` as retention (forgets units older than the window with the reason "retention"), `erase()` as the hard path; namespace validation on `search`, `forget` and `erase`; an in-memory backend behind a five-method store interface; `--demo` runs the two-identity isolation, contradiction, forget-vs-erase and exclusion cases offline |
| `memory-design.md` | `<repo>/docs/memory.md` | Per feature: types kept, profile vs collection, hot path vs background, what is never written, retention and forgetting, erasure path, substrate, the eval case that proves it |
| `memory-tool-handler-notes.md` | read; `memory_tool.py` if the provider tool is used | Client-side duties for Anthropic's memory tool: path validation, size caps, sensitive-data stripping, expiry, the multisession progress pattern — restated for a home-made store |
| `permission-model.md` | `<repo>/docs/permissions.md` | Identity per agent and sub-agent (NHI), credential source and lifetime, least privilege and just-in-time; the read path (retrieval authorisation pre/post, memory namespaces); the write path (destructive annotations → approval; pointers to 2b and G4); the register row each tool needs; kill switch, throttle, canary |
| `external-context-notes.md` | `<repo>/docs/architecture.md` §external context | Files API tenancy and limits, web search controls and echo-back rules, MCP server admission — dated vendor facts (2026-10-01) |
| `memory-eval.md` | `<repo>/evals/memory/` | Cross-session cases (recall after N sessions; update on contradiction; forget after retention; no leak across identities) and one public memory benchmark, run through `../evals/eval_harness.py` |
| `stack-notes/python.md`, `stack-notes/php-laravel.md` | read | Python: the skeleton, or a framework store (LangGraph store, Mem0 OSS) configured to the same rules; Laravel: memory units as an Eloquent model with a tenant scope, consolidation in a queued job, pgvector or a text index, the identity filter as a global scope — under twenty lines, no code (decision 0005 §5) |

## Reference implementation

`memory_store.py`: one module implementing assertions 1–7 for Python with an in-memory store, the extraction and consolidation models left as callables (`ExtractionModel`, `ConsolidationModel`) that the repo wires to its one LLM client (`../llm-api-calls/`), and `--demo` standing in for both with rules. The mechanism it fixes is the write path — a candidate fact meets its *s* nearest active units of the same owner and a reasoning model returns `{reasoning, action, target, new_text}`; the module applies the decision and writes the trail — and the read path: `store.for_owner(identity)` is the filter, ranking happens after it, and the result is bounded by `k` and characters and rendered as a block labelled by type. **Python idioms, not required** (decision 0005 §3): dataclasses, the dict store, token overlap as similarity, pydantic for the decision. Any stack satisfies the contract with a table that has an owner column and a status column, a queued consolidation step that calls a reasoning model, a query whose first predicate is the identity, and a forget that updates status while erase deletes. Other stacks: `stack-notes/<stack>.md` and, once a real repo passes Verify, `variants/<stack>/`.

## Stack-sensitive points

- **Consolidation needs a reasoning-capable model and runs off the response path**: after responding in a long-lived process (an async task), queued in a request-scoped runtime (a job after the response is sent). Mem0's finding — a small reasoning model beat a small chat model at the update decision — makes the model tier a stack-neutral rule; where it runs is the stack's.
- **The identity filter is a query predicate everywhere**: a global scope on the model in Laravel, a mandatory argument with no default in Python, a `WHERE owner = ?` that the ORM cannot drop; it is never a filter on a ranked list.
- **Vector neighbour search is optional on day one**: a text index or token overlap finds the five neighbours of a candidate at small scale; `pgvector` or a vector store comes when the per-owner store is large.
- **Anthropic's memory tool has SDK helpers in Python, TypeScript, C#, Java; Go and Ruby run the loop by hand; PHP wraps a handler in the generic runnable-tool helper** (docs read 2026-10-01) — the handler duties (path validation, size caps, stripping, expiry) are identical in every one.
- **An authorisation service is a sidecar in every stack** (SpiceDB-style `LookupResources` / `CheckPermission`); a per-user `owner_id` column with the filter above is the day-one equivalent and is enough until data is shared across users.
- **Approval state must be serialisable** in whatever runtime holds it: a row with the paused tool call, its arguments, the calling identity and the resumable run state, so a restart does not lose a pending approval.

## Adapt
- `memory_store.py`: set `<<CONSOLIDATION_MODEL>>` (reasoning tier) and `<<EXTRACTION_MODEL>>`; replace `InMemoryStore` with the repo's table behind the same five methods; wire `_real_*` callables through the LLM client module; keep `EXCLUDED_FIELDS` and `SECRET_SHAPES` as the product's include/exclude lists (Mem0's per-use-case prompt asks for exactly these); keep `search()`'s signature — identity is never optional.
- `memory-design.md`: one copy per feature that keeps memory; delete the types the feature does not keep; the "never written" list is mandatory.
- `memory-tool-handler-notes.md`: if the provider's tool is used, implement the handler as `memory_tool.py` against the same store; otherwise read it for the duties and delete.
- `permission-model.md`: fill the identity table from the trust register; the retrieval placement row is a decision (pre- or post-filter by hit rate); the approval rows point at the repo's `dry-run-and-approval.md` copy.
- `external-context-notes.md`: keep only the tools the product uses; re-read the vendor pages on adoption day and update the dates.
- `memory-eval.md`: the four cases are the minimum; add the product's own; run through the evals harness with `k = 5`.
- Stacks: Python shown; PHP/Laravel in `stack-notes/php-laravel.md`; TypeScript is not a promised stack (decision 0005 §4) — implement from the contract with `../prompt-library/implement-practice.md` until a field-tested variant exists.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who judges it: `script` (a command's exit code), `agent` (observed in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's library. Stack-specific commands live only under *Example commands (Python)*. Assertion 10 and the erasure path of assertion 4 belong to the full part.

1. Every memory write passes through extract and consolidate: a new fact is compared with its nearest existing units and one of add / update / forget / noop is recorded with the reason, never an unconditional append — observer: script — negative: two active units stating contradictory facts for one owner, or a duplicate
2. Every memory unit carries an owner scope, a type, a timestamp, a source pointer and a status — observer: script — negative: a unit with no owner or no source
3. A read returns only units whose owner scope matches the requesting identity, proven by a test with two identities and overlapping facts — observer: script — negative: a unit of one identity returned to the other — framework: beats
4. Forgetting is a status change with a trail and the forgotten unit is excluded from reads; where `personal_data` or `regulated` holds, an erasure path removes the unit and its trail on request — observer: script — negative: a forgotten unit still retrieved, or no erasure path where the fact holds
5. A conversation containing a secret-shaped string or an excluded field produces no memory unit containing it — observer: script — negative: the string found in the store
6. Memory paths or namespaces are validated: no read or write outside the identity's namespace, no traversal — observer: script — negative: a crafted path or namespace that reaches another store
7. Consolidation runs off the response path and reads are bounded by k and size, so response latency does not grow with the store — observer: script — negative: a reply that waits for consolidation, or a read that returns the whole store
8. What enters the window from memory is labelled by type with its purpose and stays within the context budget — observer: agent — negative: unlabelled memory text in the prompt, or memory that pushes the window past the compaction trigger
9. The cross-session eval passes five runs out of five: a fact from session 1 is used in session N, a contradicted fact is updated, a retention-expired fact is not used — observer: script — negative: one failed run
10. (full) Every tool the agent can call runs under a named identity with a credential source and lifetime in the trust register; destructive tools require an approval that is a paused, resumable state and fails closed on timeout; retrieval over scoped data applies the identity filter before or after the vector query and the placement is written down — observer: Martin — negative: a shared static key, a destructive tool with no approval, or a retriever with no filter

**Example commands (Python):** `python3 memory_store.py --demo` (two-identity isolation and contradiction update, printing the consolidation decisions; offline, no placeholders needed); `pytest tests/test_memory.py`; `../evals/eval_harness.py --tasks evals/memory/cases.jsonl --trials 5`.

## Sources
`sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` §3.6–3.8 and impact table §6 (rows 24–39); primary texts listed in `principles/15-memory-external-context-and-permissions.md` §6. Vendor pages to re-read directly before promoting to `current`: Anthropic's memory tool, Files API and web search tool pages (limits, versions and prices dated 2026-10-01), the OpenAI Agents approvals page.

## Change log

- 2026-10-01 (s6) — `permission-model.md` §3 gains a third placement row, **RLS in the store**: the policy reads the request identity (`auth.uid()`, a session variable, a JWT claim), is preferred over a `WHERE` in application code, and reaches permissions held elsewhere through a foreign data wrapper (Supabase, read 2026-10-01); the day-one owner column is written at ingestion (`../data-ingestion/` Verify 2). Source: `../../sources/2026-10-01-s06-data-audit-cleaning-privacy-digest.md` §7.2.
- 2026-10-01 — created from the session-5 market scan digest (draft, **unrouted** per decision 0004 §6: no row in `practices/README.md`, absent from `ROUTER.md` until the previous module's day-0 files pass Verify in a real repo). Reference `memory_store.py` run with `--demo` (offline, rule-based stand-ins for the extraction and consolidation models, no network) on 2026-10-01: two identities with overlapping facts → each read returns only its owner's units (Lisbon never appears for Bob, Madrid never for Alice); ADD on new facts; NOOP on an identical duplicate; UPDATE on "I moved to Porto" → the Lisbon unit becomes `forgotten` with a trail entry `superseded by <new id>`; FORGET on "I don't drink coffee anymore" → status change, excluded from reads, still in the store; `erase()` → unit and trail gone with an audit line; a secret-shaped string (`sk-…`) and an excluded field (`ssn`) dropped at extraction; crafted namespaces (`bob`, `../bob`, `alice%2F..`, `alice/bob`) refused, and Alice forgetting Bob's unit refused; a bounded read returns 3 units / 927 characters from a 23-unit store at `k=5, max 1000`; a fresh unit outranks a 200-day-old one of equal relevance; an unparseable consolidator answer → NOOP, nothing appended. No field report yet.
- 2026-10-01 (review) — clean-context review: `search`, `forget` and `erase` take an explicit `owner` (default: the identity's own) validated by `validate_namespace` on the real path; `expire()` implements retention as a `forget()` with the reason "retention" (`memory-design.md` §5, `memory-eval.md` case 3); the clock is injectable (`now` on `search`, `score`, `forget`, `expire`); `touch()` raises importance on a neighbour hit and on an UPDATE, the successor inheriting it; the card-number shape requires separators so a 13–19-digit order id is kept; excluded fields match the candidate's subject or a whole word, not a substring. IBM's NHI statement kept to its words, the per-sub-agent identity marked as the KB's extension; the handler notes mark "the provider holds no copy" and "reject symlinks" as the KB's additions. `--demo` re-run 2026-10-01 after the changes: all earlier branches, plus `search(owner="bob")` as Alice refused, `erase(owner="alice")` as Bob refused, `forget` refused with and without an explicit owner, order id `4111222233334444` kept while `4111 2222 3333 4444` is dropped, `expire()` at day 0 forgets nothing and at day 31 forgets the one episodic unit (reason "retention: older than 30 days") leaving semantic units active, the superseded Lisbon unit at importance 1.2 with its successor inheriting it, and equal scores for equal clock distance.
