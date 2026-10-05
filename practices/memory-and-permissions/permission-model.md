# Permission model — <<product>>

Copy to `<repo>/docs/permissions.md`; one per product; reviewed as code with the trust register. This file is the **map**: identity, the read path and the write path, each pointing at the practice that already holds the control. Principle: `../../principles/15-memory-external-context-and-permissions.md` §3.5. Sources: IBM *Securing AI agents with zero trust* (2026-02); Angie Jones, Block (2026-01); OpenAI Agents *Guardrails and human review* (read 2026-10-01); Pinecone/AuthZed *RAG with access control* (2026-01-08); Zhang (s12, reused) — digest `../../sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` §3.8. Session 14 carries the depth (vault, NHI lifecycle, gateway inspection, SpiceDB).

## 1. Vocabulary (IBM, 2026-02)

**Verify, then trust** (no implicit trust by network position); **just-in-time, not just-in-case** (access "only when they're needed, and not for longer than they're needed"); **pervasive controls** (not "the hard crunchy outside and the soft, chewy center"); **assume breach**. For agents: agents spawn agents and use many **non-human identities (NHIs)**, all controlled "with the same level of control and visibility that we had for the human users" (IBM's statement). **KB extension (opinion):** one narrower identity per spawned sub-agent, never the parent's credential — IBM does not say this; the rows below assume it. **No static credentials** — a vault issues dynamic, short-lived ones; a **tool registry** of vetted tools; an **AI gateway** inspecting inputs and outputs; **immutable logs**; and a human with a **kill switch**, **throttles** and **canary deployments**.

## 2. Identity — one row per agent and sub-agent

| Agent / sub-agent | Identity (NHI) | Credential source | Lifetime | Scope (least privilege) | Kill switch | Throttle |
|---|---|---|---|---|---|---|
| `<<support-agent>>` | `<<svc-support-agent>>` | `<<vault role / OAuth client via the IdP>>` | `<<1 h token>>` | `<<read tickets, write replies in draft>>` | `<<feature flag SUPPORT_AGENT_ENABLED>>` | `<<50 tool calls / min; 200 emails / day>>` |
| `<<research sub-agent>>` | `<<svc-support-research>>` | same vault, own role | `<<15 min>>` | `<<read-only web + docs>>` | inherits | `<<20 searches / task>>` |

Rules: a sub-agent never inherits the parent's credential — it gets its own, narrower one; a credential is never in the prompt or in a tool result; the register (`../security-baseline/mcp-trust-register.md`, columns "identity the tool runs as" and "credential lifetime") is the source of truth for the tool side of this table. Block's choice for MCP: **OAuth against the company identity provider**, not API keys and scopes (Jones).

## 3. The read path — authorisation at retrieval, namespaces for memory

"If different users have different levels of access to data… your RAG pipeline must enforce those access boundaries"; **embeddings retain the permissions of their source** (Pinecone/AuthZed, 2026-01). Two placements, chosen by **hit rate**:

| Placement | How | Choose when |
|---|---|---|
| **Pre-filter** | ask the authorisation layer for the ids the subject may see (`LookupResources`), then query the vector store with `filter: {doc_id: {$in: authorised}}` | large corpus, low authorised rate (most results would be dropped) |
| **Post-filter** | query top-k, then check each result (`CheckPermission` / `CheckBulkPermissions`) before building the context | most retrieved documents are authorised; the check is cheap |
| **RLS in the store** (added 2026-10-01, s6) | a Row Level Security policy on the elements table reads the request identity (`auth.uid()`, a session variable, a JWT claim) and filters every query, the similarity query included — "RLS is always applied even as new queries and application logic is introduced in the future" (Supabase, read 2026-10-01); the table and policy shape, the foreign-data-wrapper variant and the owner column written at ingestion are in `../data-ingestion/privacy-compliance-checklist.md` §4 | the store is Postgres (pgvector): preferred over a `WHERE` in application code, which "will work" today and is forgotten by the next query; pre/post-filter remain the mechanism when authorisation lives outside the store; **with an iterative scan or a partition for recall** (added 2026-10-05, s8: a policy on an approximate index is applied after the scan — `../vector-store/tenant-isolation-in-the-store.md`) |
| **In-graph (filter-aware) filtering and the planner** (added 2026-10-05, s8) | the store keeps the graph connected under a filter — extra edges per payload value (Qdrant, 2019-11-24 and 2023) or the ACORN variant (Weaviate, 2025-02-21) — and a cardinality planner switches to the payload index or a scan when the filter is narrow; pgvector 0.8.0 iterates the scan until *k* results pass (`../vector-store/tuning-and-capacity.md` §3) | the filter is selective or correlated with similarity — the hit-rate rule above assumes a connected graph and silently returns fewer than *k* when it is not (`../../principles/18-vector-stores.md` §3.4); the strategy per filter class is recorded in the store manifest (`../vector-store/` Verify 5) |

Decision for `<<corpus>>`: <<pre-filter, because a tenant sees < 5 % of the corpus>>. Day-one form without an authorisation service: an `owner_id` / `tenant_id` column on every chunk, written at ingestion by the ingestion identity (`../data-ingestion/` Verify 2), and — on Postgres — an RLS policy over it, elsewhere a mandatory filter in the query (`../context-management/context-store-decision.md` question 5); `../structured-outputs/guardrail-policy.md` G6 records the row. **Memory** is the same mechanism with a namespace per owner: `memory_store.py`'s `search()` filters by identity before ranking (assertion 3) — always pre-filter, since a memory store is one namespace per owner. A revoked permission must drop the result on the next query, not on the next re-index.

## 4. The write path — the tool boundary

"Don't rely only on agent-level input or output guardrails. **Put validation next to the tool that creates the side effect**" (OpenAI Agents guide, read 2026-10-01). The decision table: block disallowed requests → input guardrail; validate the final output → output guardrail; check arguments and results around a function → tool guardrail; "pause before side effects like cancellations, edits, shell commands, or sensitive MCP actions" → **approval**.

- **Destructive annotations → mandatory approval.** Block marks MCP tools *destructive* and the client runs non-destructive tools freely while a destructive one must "ask my permission first, like give me some insight into what this is" (Jones). Every tool in the register carries the annotation; `guardrail-policy.md` G4 is the blocking row.
- **An approval is a paused run with serialised, resumable state** (Agents SDK): the tool is declared as needing approval; the run records an interruption instead of executing, returns the interruptions plus a resumable state; the application stores it, a human decides later, the run resumes *from that state* — "that's still the same run". `../verification/dry-run-and-approval.md` rule 2b holds the threshold and the window; its serialised-state rule (added 2026-10-01) is this.
- **Fail closed.** "Fail closed if review times out or becomes unavailable"; an expired approval does not send (2b's inverted default). Reviewer sees "only the context needed": proposed target, action, arguments, calling identity, window — compared against the approved scope.
- **Allow-list of servers and tools.** Block admits an MCP server only after a security review — "if it's not on that allow list… the agent will say nope, can't install it"; most built in-house, "only a handful" from vendors; their red team found **invisible characters** in shared prompt bundles — `../security-baseline/threat-model-agentic.md` T15/T16; the register column "admitted by review on <date>".
- **Limits beside approvals:** per-agent, per-day, per-amount, per-tenant caps (G4, Bhardwaj s4); throttles and canaries (IBM).

## 5. Why scope limits are scale limits (Zhang, s12)

"If your errors are going to be high stake and very hard to discover… you can have read only access, you can have more human in the loop, but this will also limit how well you're able to scale your agent." The survey (Amplify 2026-07, self-report) shows the market going the other way — 89 % of agents can write data, controls "the same toolkit you'd use to manage an intern". The position here: read-only and approvals are the default for `acts_on_world`; the way to scale is a golden set and graders that earn each tool its autonomy (`../evals/eval-policy.md` §5), never removing the approval first.

## 6. The register row each tool needs

Every tool the agent can call has a row in `../security-baseline/mcp-trust-register.md` with: identity it runs as (NHI) and credential lifetime; read-only?; destructive annotation honoured?; admitted by review on <date>; full description reviewed; blast radius; owner. A tool with no row is removed from the agent's config.

Last reviewed: <<date>> by <<owner>>.
