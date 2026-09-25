# How to expose a capability to an agent — decision table

Source: `sources/2026-09-24-s12-agents-digest.md` §3.4 (Notion on Latent Space 2026-04; Claude "MCP in Claude Code" 2026-05; IBM 2026-08/09; MCP spec 2026-07-28). Principle: `principles/21-agent-design-and-tools.md` §3.5.

## First: what kind of thing is it?

| The thing you want the agent to have | Mechanism | Why |
|---|---|---|
| Knowledge someone **wrote down** (docs, runbooks, tickets) | **RAG** — retrieval tools over the corpus (`agentic-rag-skeleton.py`) | It is data; the agent should fetch only the relevant part when needed |
| Knowledge the agent **learned from experience** (what fixed it last time) | **Memory** — a file/page/table the agent (and a human) can read and write | It is not written anywhere else; simplest durable store wins (Notion: "memory is just pages") |
| A **procedure** to follow, with judgment about when to stop or escalate | **Skill** (`SKILL.md` + scripts/references) | Loads only when relevant (progressive disclosure); can bundle a CLI's usage |
| An **action or lookup in another system** | **Tool** — via CLI, MCP or in-process function (next table) | It needs code to run |

## Second: for a tool, which transport?

| Criterion | In-process function | CLI (agent has a shell) | MCP server |
|---|---|---|---|
| Agent type | Your own loop (`agent-loop-skeleton.py`) | Coding agents (Claude Code, Codex, Cursor…) or any agent with a sandboxed terminal | Any MCP client; narrow/lightweight agents without a runtime; desktop apps |
| Context cost | Only the tools you register | Near zero until used (`--help` is progressive disclosure) | Every tool schema loaded at startup unless the client has tool search |
| Self-repair | You fix the code | The agent can read `--help`, retry flags, even patch a wrapper in the same environment | If the transport breaks, the agent has nothing |
| Permission model | Whatever you enforce | Murky: the shell can reach tokens, files, network | Strong by construction: "all you can do is call the tools"; OAuth on the server side |
| Determinism / cost | Deterministic | Deterministic call; no model tokens spent renegotiating the integration | The model re-decides the call each time; fine for the long tail, wasteful for hot paths |
| Sharing with others | No | If the CLI exists (`gh`, `aws`, `wp-cli`, `psql`) | Yes — one server, every client; the right way to publish a capability |
| **Default** | Your own product loop | **Coding agents, when a CLI exists** | **Narrow permissioned agents; capabilities you publish; the long tail** |

Operational rules (Claude Code, 2026-05): MCP tool definitions occupy context even when unused — run `/mcp` and disable what you do not use; scope shared servers with a project `.mcp.json`; prefer the CLI when one exists and package its usage as a skill; if MCP tools exceed ~10 % of the context window the client switches to tool search, which works but is weaker than having the right few tools in context. Audit monthly: `practices/token-savings/mcp-audit.md`.

Keep an internal abstraction (`tool`, `agent`, `completion`, `integration`) so that MCP is one integration type among others; expect to rebuild it.

## Third: which rung of the auth ladder? (detail in the session-14 practice, pending)

| Rung | Pattern | The tool knows… | Risk |
|---|---|---|---|
| 5 | Agent uses its own service credentials | nothing about the user | no per-user authorisation — only for public/company-wide data |
| 4 | OAuth: the tool authenticates the user, the agent stores the token | the user (impersonated) | long-lived tokens on disk (GitHub: up to 90 days); tool cannot see the agent |
| 3 | Same, through an MCP server | the user | same, but the agent only needs to know MCP |
| 2 | Token exchange: agent authenticates itself and acts *on behalf of* the user | user **and** agent, with delegation | needs an identity provider that supports exchange |
| 1 | Rung 2 + a vault holds long-lived tokens and issues short-lived credentials to the MCP layer | user and agent | the target: only short-lived credentials ever reach the agent |

Record the rung per tool in the tool's checklist item 9. Anything at rung 4–5 that touches private data needs a written reason and an expiry.
