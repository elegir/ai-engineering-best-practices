# MCP / tool audit — <<repo>> — <<YYYY-MM-DD>>

| Server / tool | Scope (user / project) | What it gives | Used in last 14 days? | Tokens at load (from /context) | Decision |
|---|---|---|---|---|---|
| <<postgres>> | project | read-only DB queries | yes | | keep |
| <<playwright>> | project | browser verification | yes | | keep |
| <<context7>> | user | current library docs | | | keep if stack changes often |
| <<figma>> | user | designs | no | | remove from this repo |
| <<…>> | | | | | |

Rules: unused for 14 days → remove (it can come back). Overlapping servers → keep one. Anything a CLI already does well (git, gh, wp-cli) does not need an MCP — package the CLI's usage as a skill instead. Keep MCP where the permission boundary matters (the agent must only be able to call these tools) or where no CLI exists. If tool schemas exceed ~10 % of the context window, bucket them or rely on tool search, but know that tool search is weaker than having the right few tools in context (Claude, 2026-05). Re-run monthly. Rationale: `practices/agent-patterns/tool-transport-decision-table.md`.
