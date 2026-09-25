---
title: "Practice — agent patterns: decide workflow vs agent, build the minimal loop, design tools, pick the transport, add agentic RAG"
type: practice
status: draft            # draft until principle 21 is confirmed against LIDR session 12
date: 2026-09-24
last-reviewed: 2026-09-24
tags: [agents, tools, function-calling, mcp, agentic-rag, patterns]
principle: principles/21-agent-design-and-tools.md
sources:
  - sources/2026-09-24-s12-agents-digest.md
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://www.anthropic.com/engineering/writing-tools-for-agents
supersedes: null
superseded-by: null
---

# Agent patterns

## Solves
A repo is about to add (or already has) a feature where a language model takes actions — calls APIs, searches documents, edits data — and one of these symptoms appears: nobody wrote down why it is an agent rather than a pipeline; the agent loop is entangled with a framework nobody fully understands; tools are one-per-endpoint with one-line descriptions; the agent "does weird things" and the team tunes the prompt instead of reading what the model actually saw; every integration is an MCP server loaded at startup; retrieval is a single embedding search with no way to recover from a miss.

## Applies when
- A feature lets a model decide *what to do next* (tool calls, multi-step tasks, search-and-answer over private data).
- The team is choosing between a fixed pipeline and an autonomous loop and wants the decision recorded.
- Tools are being written for a model (function calling, MCP server, CLI wrapper).
- A RAG feature needs to self-correct when the first retrieval misses.

## Does not apply when
- The feature is one LLM call with a fixed prompt (classification, summarisation, extraction) — use structured outputs instead (session-4 practice, pending).
- The "agent" is Claude Code / Cursor working on the repo itself — that is covered by `practices/agent-entry-file/`, `hooks-and-guards/`, `session-state/`.
- Multi-agent delegation, human-in-the-loop approvals or sandboxing are the problem — session-14 practice (pending); this folder stops at one loop.

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `when-to-build-an-agent.md` | `<repo>/docs/features/<feature>/agent-decision.md` (or the feature spec) | The four-question checklist, filled per feature; records workflow / agent / workflow-of-agents |
| `patterns-catalogue.md` | read; copy the relevant pattern paragraph into the feature design | The composable patterns with when-to-use and the minimal shape of each |
| `agent-loop-skeleton.py` | `<repo>/src/<feature>/agent_loop.py` | ~100-line file; the loop itself is ~35 lines (Anthropic Messages API shown); tools as plain functions; bounded iterations; errors returned as text |
| `tool-definition-template.md` | one copy per tool, next to the tool's code (docstring) | Template + 12-point checklist for a tool description and behaviour |
| `tool-transport-decision-table.md` | `<repo>/docs/architecture.md` §tools | CLI vs MCP vs skill vs RAG vs memory, and the auth-ladder rung per tool |
| `agentic-rag-skeleton.py` | `<repo>/src/<feature>/agentic_rag.py` | list / grep (ripgrep) / read tools over a folder of markdown, bounded, with cited structured output |
| `../prompt-library/trajectory-review.md` | run as a prompt | "Think like your agent": ask the model to critique the raw context and a trajectory |

## Adapt
- `agent-loop-skeleton.py`: replace `<<MODEL>>`, the tool list and `MAX_ITERATIONS`; swap the SDK block if you use OpenAI / Gemini / a framework (the loop shape is the same: call → if tool_use, run tools, append results, repeat).
- `agentic-rag-skeleton.py`: set `<<NOTES_DIR>>`; if documents live in Postgres, replace the three functions' bodies and keep their signatures and docstrings; install `ripgrep` in the runtime image.
- `tool-definition-template.md`: the checklist is the deliverable; the docstring format follows your language (Python docstring, JSON schema `description`, TypeScript JSDoc).
- Delete `when-to-build-an-agent.md` sections that do not apply; keep the four answers.

## Verify
- The feature spec contains the four answers and the chosen shape.
- Running the loop with `debug=True` prints, for every tool call, the *parameters the model chose* and the *result it got back*; a reviewer can follow the trajectory without the code.
- Every tool passes the 12-point checklist; no tool raises inside its body; every read is bounded.
- `python3 agentic-rag-skeleton.py "<question>"` returns an answer with at least one citation pointing to a real file and line.
- `/context` (Claude Code) or the equivalent shows tool schemas below ~10 % of the window; unused MCP servers are disabled.
- Three real trajectories were reviewed with `trajectory-review.md` and at least one tool description changed as a result.

## Sources
`sources/2026-09-24-s12-agents-digest.md` §3.1–3.6 and the impact table §6; primary texts listed in `principles/21-agent-design-and-tools.md` §6.

## Change log
- 2026-09-24 — created from the session-12 market scan (draft).
