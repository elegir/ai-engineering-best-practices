---
title: "Practice — LLM API calls: one client module, a structured versioned prompt, a failure-mode checklist and a provider checklist for any product that calls a model"
type: practice
status: draft            # draft until principle 10 is confirmed against LIDR session 1
date: 2026-09-27
last-reviewed: 2026-09-27
tags: [llm-api, prompting, tokens, prompt-caching, providers, reliability]
kind: capability
applies-when: "llm_calls"
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

## Adapt
- `llm_call_skeleton.py`: set `<<MODEL>>`, `<<MAX_OUTPUT_TOKENS>>`, `<<TIMEOUT_S>>`; keep `call()` as the one entry point. If the product uses OpenAI, replace the SDK block per the comment (`client.responses.create(input=items, …)`; items and output items instead of messages and content blocks) — the loop shape does not change. If a framework (LangChain, Pydantic AI, Vercel AI SDK) is already in place, keep it, but route it through this module so model name, limits and usage logging still live in one file.
- `system-prompt-template.md`: delete the sections a prompt does not need (a classifier has no conversation history); never reorder static and dynamic parts. Fill the header (purpose, model, version, last evaluated on). Store under version control; the vendor's prompt dashboard (OpenAI prompt objects) is an alternative only if every change still lands in git.
- `failure-modes-and-mitigations.md`: keep the rows that apply; for each, name the concrete tool or check in *this* repo.
- `provider-selection-checklist.md`: fill it once per product; re-check the dated rows when a vendor ships a new generation.
- Stack variants: Python shown; TypeScript is a direct port (`@anthropic-ai/sdk`, `openai`); keep the same module boundary.

## Verify
- `grep -rn "anthropic\|openai" src/ | grep import` returns exactly one file.
- Every runtime prompt is a file with the header block filled; `git log` on it shows the versions.
- Logging one multi-turn conversation shows `cache_read_input_tokens > 0` from the second call on; if it is 0, the static/dynamic order is wrong.
- The feature spec lists which rows of `failure-modes-and-mitigations.md` apply and what covers each.
- The eval for the feature runs each scenario at least 5× and reports the worst case, not the mean.
- `docs/llm-provider.md` exists, dated, with the switching-cost line filled in.

## Sources
`sources/2026-09-27-s01-llm-setup-digest.md` §3.1–3.5 and impact table §6; primary texts listed in `principles/10-llm-api-fundamentals.md` §6. Vendor docs to re-check before promoting to `current`: Claude prompt engineering and prompt caching guides; OpenAI Responses API guide.

## Change log
- 2026-09-27 — created from the session-1 market scan (draft).
