# MCP / tool trust register — <<repo>>

Every server or tool an agent can call is a trust decision. One row each; review monthly with the MCP audit.

| Server / tool | Scope (user / project) | What it can read | What it can write / do | Credential (name only, never the value) | Blast radius if misused | Read-only? | Owner | Last reviewed |
|---|---|---|---|---|---|---|---|---|
| `<<postgres>>` | project | production DB, all tables | nothing (read-only role) | `PG_RO_URL` | data exfiltration | yes | Martin | YYYY-MM-DD |
| `<<playwright>>` | project | any URL the agent navigates | clicks/forms on those pages | none | actions on logged-in sites | no | | |
| `<<github>>` | user | repos in the session's set | commits, PRs | app token | code changes | no | | |

Rules: default to read-only roles; separate credentials per environment; no server may reach production write paths from an agent session without a human-run step; anything not in this table is removed from the agent's config.
