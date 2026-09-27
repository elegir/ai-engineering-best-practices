# Provider selection checklist — for developers, not for plan shoppers

Copy to `<repo>/docs/llm-provider.md`, fill it once per product, date it, and re-check the rows marked *(dated)* whenever a vendor ships a new generation. Which *model tier* to use for which phase is a different question, answered by `../../principles/08-model-selection.md`; this file is about the **API and the account** you build on. Principle: `../../principles/10-llm-api-fundamentals.md` §3.5.

The labs' top models are near parity and rotate quarterly; the durable differences are in the rows below. Consumer "which $20 plan" comparisons answer none of them.

```
Product: <<name>>        Filled: <<date>>        Owner: <<who>>
Candidates: <<Anthropic / OpenAI / Google / open-weight via <host> >>
```

| # | Criterion | Why it matters | Candidate A | Candidate B |
|---|---|---|---|---|
| 1 | **API shape** the client must speak (Messages / Responses / Chat-Completions-compatible / Open Responses) | Decides the adapter in `llm.py`; each lab owns its shape; third-party servers copy one of them *(dated)* | | |
| 2 | **Model tiers** available: fast/cheap, mid, top; is there a **reasoning tier** with a thinking/effort budget? | Routing by phase (`08`) and by verifiability (`10` §3.1) needs both a fast and a thinking tier | | |
| 3 | **Prompt caching**: automatic or explicit breakpoints; minimum prefix; TTL; price of cached vs fresh input | The cheapest token lever; the prompt's static/dynamic order depends on the rules | | |
| 4 | **Structured outputs**: JSON-schema enforcement, or JSON mode only, or prefill only | Decides how much output validation you write yourself (session-4 practice, pending) | | |
| 5 | **Tool calling**: parallel calls; strict schemas; **hosted tools** (web search, code execution, file search, computer use) | Hosted tools are less to run and more lock-in; write down which you take | | |
| 6 | **MCP**: can the API call remote MCP servers directly (`allowed_tools`, approval gates)? | Same trade: convenience vs coupling to one vendor's connector | | |
| 7 | **State**: must I resend the item list, or can the server chain (`previous_response_id`, conversations)? Encrypted reasoning for stateless use? | Portability and auditability vs less code; zero-data-retention needs the stateless path | | |
| 8 | **Data handling**: retention default, ZDR availability, training-on-your-data policy, region/residency options | `personal_data` / `regulated` facts (`../facts.md`) may decide this row alone | | |
| 9 | **Limits**: rate limits per tier, max context window per model, max output tokens, batch API | A feature that needs 200k-token inputs or 10k requests/min is decided here, not by benchmarks | | |
| 10 | **Price** per million tokens: input / output / cached / batch, by tier *(dated)* | Fill with today's numbers and the date; recompute cost per feature from your usage log | | |
| 11 | **Streaming**: typed events (item/tool-call/text deltas) or text deltas only | Typed events make robust clients; text-only means regex | | |
| 12 | **SDK and docs quality** in your language; prompt versioning tooling (dashboard prompt objects) | Days of friction; but every prompt change must still land in git | | |
| 13 | **Switching cost**: if we moved to Candidate B tomorrow — files touched, prompts to re-evaluate, features lost (hosted tools, MCP, server state) | If the answer is "a rewrite", the client module is not thin enough | | |

## Decision

```
Chosen: <<provider>> because <<rows that decided it>>.
Lock-in accepted: <<hosted tools / server state / MCP connector — or none>>.
Switching cost today: <<"llm.py adapter + re-evaluate 4 prompts (~2 days)">>.
Re-check on: <<date, or "next model generation">>.
```
