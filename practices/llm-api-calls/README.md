---
title: "Practice — LLM API calls: one client module, a structured versioned prompt, a failure-mode checklist and a provider checklist for any product that calls a model"
type: practice
status: draft            # draft until principle 10 is confirmed against LIDR session 1
date: 2026-09-27
last-reviewed: 2026-09-30
tags: [llm-api, prompting, tokens, prompt-caching, providers, reliability]
kind: capability
applies-when: "llm_calls"
when: day-0   # day-0 | first-user | at-scale — when in a product's life this practice is installed (decision 0004 §5)
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
principle: principles/10-llm-api-fundamentals.md
sources:
  - sources/2026-09-27-s01-llm-setup-digest.md
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
  - https://docs.claude.com/en/docs/build-with-claude/prompt-caching
  - https://platform.openai.com/docs/guides/responses-vs-chat-completions
supersedes: null
superseded-by: null
---

# LLM API calls

## Solves
The product calls a language model at runtime and one of these symptoms appears: vendor SDK calls are scattered through handlers, each with its own model name, timeout and error handling; prompts are string literals edited in place, with no version, no record of what they were tested on, and variable content (date, user name) at the top, so the prompt cache never hits; the model is asked for facts, counts or arithmetic it cannot do reliably and the team "fixes" it by rewording; an irreversible action is guarded by a second model's opinion; the eval reports "92 % pass" while one scenario in ten fails for real users; the provider was chosen from a consumer plan comparison and switching would be a rewrite.

## Applies when
- The fact `llm_calls` holds (`../facts.md`): the product itself calls a model at runtime — an LLM SDK in the lockfile, model API keys in `.env.example`, prompt files or templates.
- One call or a hundred; a chat feature, a classifier, a scheduled generator, an agent loop — the client module and the prompt rules apply to all of them.

## Does not apply when
- The only model in the picture is the coding agent working on the repo (Claude Code, Cursor). That is `../agent-entry-file/`, `../hooks-and-guards/`, `../token-savings/`.
- The feature is an agent with tools and the question is workflow-vs-agent, tool design or transport — `../agent-patterns/` (this folder is the layer *under* it: the call itself and the prompt).
- Structured outputs, guardrails and output validation in depth — session-4 practice (pending). This folder only says *where* deterministic checks belong.
- Evals as a discipline (datasets, judges, regression tiers) — evals practice (pending, sessions 5/11/16). This folder gives the one rule: run each scenario N times and read the worst case.

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `llm_call_skeleton.py` | `<repo>/src/<package>/llm.py` (the *only* file that imports the vendor SDK) | ~90-line client module: model name, max tokens, timeout, retries, usage logging (incl. cached tokens), the typed item-list loop; Anthropic Messages API shown, OpenAI Responses adapter noted |
| `system-prompt-template.md` | `<repo>/prompts/<feature>/system.md` (one file per prompt, versioned) | The ten-part prompt structure, static-first for caching, with a header block and a 12-point checklist to run before shipping a prompt change |
| `failure-modes-and-mitigations.md` | read; copy the table rows that apply into the feature spec | What the model is structurally bad at and the tool, retrieval or deterministic check that covers each case |
| `provider-selection-checklist.md` | `<repo>/docs/llm-provider.md` (next to the model policy from `08-model-selection.md`) | Developer criteria for choosing and re-checking a provider; switching-cost estimate |
| `context-budget.md` | `<repo>/docs/llm-provider.md` §context, or the feature spec | How to size a request: what shares the window, where the caching boundary goes, when to start a new thread |
| `stack-notes/python.md`, `stack-notes/php-laravel.md` | (read) | Package family, retry defaults, differing names and runtime pitfalls per stack — fifteen lines, no code (decision 0005 §5) |

## Reference implementation

`llm_call_skeleton.py`: one client module implementing assertions 1, 3, 4, 6 for the Anthropic SDK. **Python idioms, not required:** the `Result` dataclass that returns errors instead of raising (Laravel's idiom is exceptions and the HTTP client's `throw()`; TypeScript's is a thrown error or a discriminated union — either satisfies the contract); the module-level singleton client. The five invariants in its docstring are now assertions 1, 3, 4, 5 and 6 above. See `stack-notes/` for other stacks.

## Stack-sensitive points

- **Retry ownership** depends on the SDK's default: Anthropic's and OpenAI's official Python/TS SDKs retry twice by default (set `max_retries=0` to own retries); community PHP packages differ — check before deciding who owns retries (assertion 4).
- **Request-scoped runtimes** (PHP-FPM): a per-request client is fine; a cooldown or circuit state must live in the cache store, not in a static variable.
- **Streaming** needs a long-lived response: trivial in Python/Node servers; in PHP it needs output buffering disabled and a web server configured for it, or a queued job with polling.
- **Prompt files**: Python/TS load them from disk at import; Laravel repos conventionally put them under `resources/prompts/`, WordPress plugins under the plugin folder — the location is free, the header block is not.

## Adapt
- `llm_call_skeleton.py`: set `<<MODEL>>`, `<<MAX_OUTPUT_TOKENS>>`, `<<TIMEOUT_S>>`; keep `call()` as the one entry point. If the product uses OpenAI, replace the SDK block per the comment (`client.responses.create(input=items, …)`; items and output items instead of messages and content blocks) — the loop shape does not change. If a framework (LangChain, Pydantic AI, Vercel AI SDK) is already in place, keep it, but route it through this module so model name, limits and usage logging still live in one file.
- `system-prompt-template.md`: delete the sections a prompt does not need (a classifier has no conversation history); never reorder static and dynamic parts. Fill the header (purpose, model, version, last evaluated on). Store under version control; the vendor's prompt dashboard (OpenAI prompt objects) is an alternative only if every change still lands in git.
- `failure-modes-and-mitigations.md`: keep the rows that apply; for each, name the concrete tool or check in *this* repo.
- `provider-selection-checklist.md`: fill it once per product; re-check the dated rows when a vendor ships a new generation.
- Stacks: Python shown; TypeScript is not a promised stack (decision 0005 §4) — implement from the contract with `../prompt-library/implement-practice.md` until a field-tested variant exists; PHP/Laravel: `stack-notes/php-laravel.md`.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. Exactly one module in the product imports or instantiates the model vendor's client; every other call site goes through it — observer: script — negative: a second import, or a handler that builds a request itself — framework: beats
2. Every runtime prompt is a versioned file with the header block (id, version, date, model, owner) filled, and its history is visible in version control — observer: script — negative: a prompt as a string literal, or a file without the header
3. When calls share a stable prefix longer than the vendor's minimum cacheable length (about 1,024 tokens for both major vendors; 2,048 for the smallest models), the second call that shares it reports cached tokens read above zero — observer: script — negative: zero cached tokens on that second call (variable content placed before the stable part); single-shot calls with short prompts are n.a. with that reason
4. Retries have a single owner: either the client or the vendor SDK retries, never both, and the retry count appears in the log — observer: script — negative: a 429 that produces more attempts than the single owner's cap — framework: beats
5. The model is never asked for facts, counts or arithmetic the code can compute, and no irreversible action is guarded by an LLM's opinion alone — observer: Martin — negative: a prompt that asks "how many…", or a send/pay/publish whose only gate is a model's yes
6. Per-call usage (input, output, cached tokens, latency, model id) is logged in a form that can be aggregated — observer: script — negative: a call with no usage record
7. The feature spec lists which rows of `failure-modes-and-mitigations.md` apply and what covers each — observer: Martin — negative: a row that applies with no mitigation named
8. The feature's eval runs each scenario at least five times and reports the worst case, not the mean — observer: script — negative: an eval that reports an average
9. `docs/llm-provider.md` exists, is dated, and states the switching cost — observer: Martin — negative: a provider chosen with no written reason

**Example commands (Python):** `grep -rln "import anthropic\|from anthropic\|import openai" src/ | wc -l` → `1`; `python3 llm_call_skeleton.py --demo` (after the three placeholders are replaced — the file does not parse before) prints the request shape (static system block with `cache_control`, dynamic content last) and the usage fields the log line carries, without calling the API.

## Sources
`sources/2026-09-27-s01-llm-setup-digest.md` §3.1–3.5 and impact table §6; primary texts listed in `principles/10-llm-api-fundamentals.md` §6. Vendor docs to re-check before promoting to `current`: Claude prompt engineering and prompt caching guides; OpenAI Responses API guide.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-27 — created from the session-1 market scan (draft).
- 2026-09-27 (s2) — checklist item 2 sharpened (cache breakers, positive rules); provider row 10 (cached-input price); `context-budget.md` rule 7 (cache limits). Source `sources/2026-09-27-s02-context-caching-digest.md`.
- 2026-09-30 (s3) — skeleton comment: one retry owner in production; provider row 8: gateway and provider policies both apply. Source `sources/2026-09-30-s03-wrappers-digest.md`.
