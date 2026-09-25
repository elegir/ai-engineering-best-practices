# Patterns catalogue — composable shapes for LLM systems

Names follow Anthropic's *Building Effective Agents* (2024-12); Andrew Ng's four design patterns (2024-03) and Google ADK's agent shapes (2026) are mapped onto them. Each entry: what it is, when to use it, the minimal implementation. Digest: `sources/2026-09-24-s12-agents-digest.md` §3.1.

## Workflows (code decides the path)

| Pattern | What | Use when | Minimal shape |
|---|---|---|---|
| **Prompt chaining** | Fixed sequence of narrow prompts, optional code checks between steps | The task decomposes into stable steps and each step is easier than the whole | `out1 = llm(p1, x); assert check(out1); out2 = llm(p2, out1)` |
| **Routing** | A classifier prompt sends the input to one of several specialised prompts/flows | Distinct categories need different handling; one prompt for all degrades each | `route = llm(classify, x); handlers[route](x)` |
| **Parallelisation** | Same task on N sections (*sectioning*) or N attempts on the same input (*voting*) | Independent subtasks; or confidence from majority | `results = await gather(llm(p, s) for s in sections)` |
| **Orchestrator–workers** | A model breaks the task into subtasks it did not know in advance, delegates, synthesises | Subtasks cannot be predicted (e.g. which files to edit) | Orchestrator prompt returns a list of subtasks → each run as a worker call → synthesis prompt |
| **Evaluator–optimiser** | Generator produces, evaluator critiques with a verdict, loop until pass or cap | Clear evaluation criteria exist and iteration measurably helps | ADK shape: `LoopAgent([generator, checker], max_iterations=3)`; checker answers only `OK` or `retry: <reasons>`; shared state key passes the artefact |

Ng's **reflection** = evaluator–optimiser with the same model in two roles (coder + reviewer). Ng's **planning** = orchestrator–workers where the first step is an explicit plan. ADK's **sequential agent** = prompt chaining; **planning agent** = orchestrator.

## Agents (the model decides the path)

| Pattern | What | Use when | Minimal shape |
|---|---|---|---|
| **Single agent (ReAct loop)** | Model + tools + system prompt, called in a loop until no tool call | Ambiguous, valuable, verifiable task; errors cheap to discover | `agent-loop-skeleton.py` |
| **Workflow of agents** | A fixed pipeline whose each step is a small closed loop | You know the stages but each stage needs self-correction (write SQL → run → fix → hand off) | Chain of single-agent loops with a hard cap each |
| **Agentic RAG** | Single agent whose tools are list / search / read over a corpus, output with citations | Retrieval must recover from a miss; latency budget allows several tool calls | `agentic-rag-skeleton.py` |
| **Tool router / tool search** | A first cheap step picks the relevant tools from a large catalogue, then only those schemas are loaded | > ~30 tools, or tools owned by many teams | A `search_tools(query)` tool, or name-plus-one-line list → select → load schemas |
| **Subagent as tool** *(parked → session 14)* | A tool whose implementation is another agent with its own context | Isolate a large exploration from the main context; parallel independent work | Tool `run_subagent(brief)`; write the brief like a first-time manager should not: full context, output format, boundaries |

## Rules that apply to all of them
1. Start with the simplest shape that could work; add a layer only when an eval shows the simpler one fails.
2. Every loop has a cap (iterations, tokens, seconds) and a signal that ends it (test, checker, eval).
3. Read what the model sees before changing what the model does (`../prompt-library/trajectory-review.md`).
4. Optimise (cache the prefix, parallelise tool calls, show progress) only after behaviour is right.
