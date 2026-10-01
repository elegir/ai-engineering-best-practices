# MCP / tool trust register — <<repo>>

Every server or tool an agent can call is a trust decision. One row each; review monthly with the MCP audit.

| Server / tool | Scope (user / project) | What it can read | What it can write / do | Credential (name only, never the value) | Blast radius if misused | Read-only? | Full description reviewed (not the summary) | Owner | Last reviewed |
|---|---|---|---|---|---|---|---|---|---|
| `<<postgres>>` | project | production DB, all tables | nothing (read-only role) | `PG_RO_URL` | data exfiltration | yes | YYYY-MM-DD, by <<who>> | Martin | YYYY-MM-DD |
| `<<playwright>>` | project | any URL the agent navigates | clicks/forms on those pages | none | actions on logged-in sites | no | | | |
| `<<github>>` | user | repos in the session's set | commits, PRs | app token | code changes | no | | | |

Rules: default to read-only roles; separate credentials per environment; no server may reach production write paths from an agent session without a human-run step; anything not in this table is removed from the agent's config. **Review the full tool descriptions, not the one-line summary the client shows**: the human approves a summary while the model reads the whole description, which can carry hidden instructions — the "iceberg effect" (Carpintero, 2026-04; `../../sources/2026-10-01-s04-structured-outputs-digest.md` §3.3); re-review when a server updates its tools.
