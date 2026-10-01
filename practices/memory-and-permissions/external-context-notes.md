# External context notes — files, web search and MCP servers as the provider offers them (dated 2026-10-01)

Copy the relevant rows into `<repo>/docs/architecture.md` §external context; delete the tools the product does not use; **re-read the vendor pages on adoption day and update the dates** — every fact below is a vendor fact read on 2026-10-01 from the canon snapshots (`../../sources/raw/2026-10-01-market-scan-s05-context-memory-permissions-evals/canon-snapshots/anthropic-files-api.md`, `anthropic-web-search-tool.md`) and from Angie Jones (Block, 2026-01). Principle: `../../principles/15-memory-external-context-and-permissions.md` §3.4 — digest §3.7.

## 1. Files API (Anthropic, read 2026-10-01)

**Mechanism.** Upload once, receive a `file_id`, reference it in a `document` (PDF, text), `image` or `container_upload` (datasets for code execution) content block; content is billed as input tokens on every call that references it; file operations themselves are free.

**The tenancy rule (the finding).** "Uploaded files are accessible to your entire workspace, not scoped to an end user, conversation, or session… **Never accept `file_id` values from end users**… create a separate workspace for each tenant. **The workspace is the isolation boundary**" (100 workspaces per organisation). Consequences in code:

- a `file_id` is a **server-side reference** the application looks up from its own `(tenant, user, upload) → file_id` table; a request body that carries a `file_id` is rejected (`../security-baseline/threat-model-agentic.md` T21);
- one **workspace per tenant** where tenants must not share uploads; the API key the application uses for a tenant's calls belongs to that workspace;
- uploads cannot be downloaded back (only files produced by skills or code execution can), so the application keeps its own copy if users may re-download;
- uploads, downloads and deletes appear in the Compliance API feed — the audit trail exists; wire it.

**Limits (2026-10-01):** 500 MB per file; 1 TB per organisation; about 500 requests per minute; optional `expires_in_seconds` from 1 hour to 90 days, set once at upload — expiry "is a lifecycle feature, not a guaranteed-deletion control" (an erasure path deletes explicitly).

## 2. Web search tool (Anthropic, read 2026-10-01)

**Mechanism.** A **server-side** tool: the model decides when to search and answers directly for stable knowledge; the application adds the tool and reads the result blocks. Three versions on 2026-10-01: `web_search_20250305`; `_20260209` adds **dynamic filtering**; `_20260318` adds `response_inclusion`.

**Controls:** `max_uses` caps searches per request ("simple factual queries typically use 1–3 searches; comparative… 10 or more"); `allowed_domains` **or** `blocked_domains` (both → 400); `user_location`; an organisation-level switch. Triggering is steerable by prompt and evaluated with a **balanced should-search / should-not-search set** (Anthropic's agents post, 2026-01 — the eval that stopped over- and under-triggering).

**Dynamic filtering = the provider doing *reduce*.** "Claude instead writes and runs code that filters the results first, so only relevant content reaches the context window" — inside code execution by default on the newer versions; `response_inclusion: "excluded"` drops consumed result blocks from the response. This is `../../principles/11-runtime-context-management.md` §3.2 *reduce* happening before the window.

**Client duties:**

- result blocks carry **`encrypted_content` that must be sent back unchanged on later turns** (400 otherwise) — never edit, trim or re-order search result blocks in the history;
- **citations must be included** when results are shown to end users;
- **errors arrive inside a 200** (`max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`, `unavailable`) — the client module (`../llm-api-calls/`) reads the error block, it does not wait for an exception;
- a long turn may return `stop_reason: "pause_turn"` — resume by resending;
- **price:** US$10 per 1,000 searches plus tokens; results count as input tokens on every later turn, so a long thread with early searches pays for them repeatedly (budget them in `../context-management/context-budget-and-triggers.md`).

Transport row: `../agent-patterns/tool-transport-decision-table.md` — provider server tools have no transport to run; the controls are the request parameters above.

## 3. MCP servers as the external-context transport (Block, 2026-01)

Jones's answer to "is MCP just fancy function calling": its value is **cross-system workflows** — an incident report that pages a human while a GitHub-connected agent opens a PR; an agent in Slack that reads a thread, proposes three fixes and implements the chosen one; tickets assigned to the agent in Jira. All narrow, hosted and permissioned — consistent with Notion's s12 position (CLIs for coding agents, MCP for narrow permissioned agents). The admission rules a regulated company used (Goose, ~12,000 employees):

- an **allow-list of MCP servers**, each admitted after a security review; most built in-house, "only a handful" from vendors;
- **tool annotations** marking a tool *destructive*, honoured by the client: non-destructive runs freely, destructive asks first (`permission-model.md` §4);
- **OAuth through the company identity provider** instead of API keys and scopes;
- client-side detection of malicious servers; a red team that found **invisible characters** in shareable bundles of prompt + servers (T15/T16).

Register: `../security-baseline/mcp-trust-register.md` — one row per server, with the new columns (identity and credential lifetime; admitted by review on <date>; destructive annotations honoured). MCP **sampling** (a server borrowing the user's model, as in the Council of Mind demo) is the primitive of `../../principles/21-agent-design-and-tools.md` §3.5; depth parked for session 13.
