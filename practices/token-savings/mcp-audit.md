# MCP / tool audit — <<repo>> — <<YYYY-MM-DD>>

| Server / tool | Scope (user / project) | What it gives | Used in last 14 days? | Tokens at load (from /context) | Decision |
|---|---|---|---|---|---|
| <<postgres>> | project | read-only DB queries | yes | | keep |
| <<playwright>> | project | browser verification | yes | | keep |
| <<context7>> | user | current library docs | | | keep if stack changes often |
| <<figma>> | user | designs | no | | remove from this repo |
| <<…>> | | | | | |

Rules: unused for 14 days → remove (it can come back). Overlapping servers → keep one. Anything a CLI already does well (git, gh, wp-cli) does not need an MCP. Re-run monthly.
