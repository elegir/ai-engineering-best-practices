---
title: "Practice — agent patterns: decide workflow vs agent, build the minimal loop, design tools, pick the transport, add agentic RAG"
type: practice
status: draft            # draft until principle 21 is confirmed against LIDR session 12
date: 2026-09-24
last-reviewed: 2026-09-30
tags: [agents, tools, function-calling, mcp, agentic-rag, patterns]
kind: capability
applies-when: "tools or multi_agent or exposes_tools"
when: day-0   # day-0 | first-user | at-scale — when in a product's life this practice is installed (decision 0004 §5)
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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

- The product **exposes** tools to an external agent (an MCP server, a function-calling API): the loop is someone else's, but the tool names, descriptions, schemas, error strings and count are yours — `tool-definition-template.md` and the progressive-disclosure rules apply in full. (Added 2026-09-28, AI SDR test.)

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

## Reference implementation

`agent-loop-skeleton.py` (the minimal tool loop with a trace) and `agentic-rag-skeleton.py` (retrieval as a tool with citations). Python idioms that are **not** part of the contract: the `dict`-based tool registry and the `while` loop with a turn cap; a framework's own loop (LangGraph, Agents SDK, a Laravel job chain) satisfies the contract if assertions 2–3 hold.

## Stack-sensitive points

- A long-lived process (Python service, Node) can hold the loop and its trace in memory; a request-scoped runtime (PHP-FPM) must persist the trajectory per step (database or queue) or run the loop in a queued worker — the pattern changes, not just the syntax.
- Tool transport (`tool-transport-decision-table.md`): an MCP server is natural where the host already speaks MCP; in a PHP app a plain internal function registry is usually the right first step.
- Token budget for schemas: count it through the vendor's count-tokens endpoint (Anthropic) or a local tokenizer (OpenAI's tiktoken, Python/TS); in PHP estimate by characters ÷ 4 and record the estimate.

## Adapt
- `agent-loop-skeleton.py`: replace `<<MODEL>>`, the tool list and `MAX_ITERATIONS`; swap the SDK block if you use OpenAI / Gemini / a framework (the loop shape is the same: call → if tool_use, run tools, append results, repeat).
- `agentic-rag-skeleton.py`: set `<<NOTES_DIR>>`; if documents live in Postgres, replace the three functions' bodies and keep their signatures and docstrings; install `ripgrep` in the runtime image.
- `tool-definition-template.md`: the checklist is the deliverable; the docstring format follows your language (Python docstring, JSON schema `description`, TypeScript JSDoc).
- Delete `when-to-build-an-agent.md` sections that do not apply; keep the four answers.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. The feature's spec records the four decision answers (workflow or agent, which pattern, which tools, what the model sees) and the chosen shape, dated — observer: Martin — negative: an LLM feature with control flow and no written decision
2. Running the loop in its debug mode prints, for every tool call, the parameters the model chose and the result it received, so a reviewer can follow the trajectory without the code — observer: agent — negative: a tool call whose arguments or result do not appear in the trace
3. Every tool passes the twelve-point checklist in `tool-definition-template.md`: a description that says when *not* to use it, bounded reads, errors returned as data (never raised into the loop), no two tools with overlapping purpose — observer: agent — negative: a tool that raises, returns unbounded output, or whose description duplicates another's — framework: beats
4. The retrieval loop (when `retrieval`) returns answers with at least one citation that resolves to a real document and location — observer: script — negative: an answer with no citation, or a citation that points nowhere
5. Tool schemas occupy under a tenth of the context window at session start, and every MCP server or tool set loaded is used by the feature — observer: agent — negative: an unused server loaded at startup, or schemas above the budget
6. (Ongoing — not required for field-tested.) Three real trajectories have been reviewed with `../prompt-library/trajectory-review.md` and at least one tool description changed as a result, recorded in the change log — observer: Martin — negative: a tuning change made to a prompt without a trajectory read

**Example commands (Python):** `python3 agent-loop-skeleton.py --debug`; `python3 agentic-rag-skeleton.py "<question>"`; `/context` in Claude Code for the schema budget.

## Sources
`sources/2026-09-24-s12-agents-digest.md` §3.1–3.6 and the impact table §6; primary texts listed in `principles/21-agent-design-and-tools.md` §6.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).
- 2026-09-24 — created from the session-12 market scan (draft).
- 2026-09-27 (s2) — tool checklist item 13 (addressable results); sub-agent rules in `patterns-catalogue.md`; stable-tool-set note in `tool-transport-decision-table.md`. Source `sources/2026-09-27-s02-context-caching-digest.md`.
- 2026-09-28 — `applies-when` gains `exposes_tools`; a product that serves 100+ MCP tools needs the tool-design half of this practice even without an agent loop of its own (first real test, AI SDR).
