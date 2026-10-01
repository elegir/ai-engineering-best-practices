---
title: "Practice — structured outputs and guardrails: a typed object from every model call, validators with one bounded re-ask, decisions as classifications, a guardrail policy per checkpoint and tier, and generative UI through an allow-list"
type: practice
status: draft            # draft until principle 13 is confirmed against LIDR session 4 (2026-11-05) and a real repo passes Verify
date: 2026-10-01
last-reviewed: 2026-10-01
tags: [structured-outputs, json-schema, pydantic, validation, re-ask, guardrails, classifiers, generative-ui, s4]
kind: capability
applies-when: "llm_calls"
full-when: "llm_calls and (acts_on_world or personal_data or regulated or multi_tenant)"
when: day-0            # schema, client and validation files are day-0; the classifier tier is documented as first-user inside guardrail-policy.md
reference-status: untested   # decision 0005 §3; only a field report moves it
routed: false          # unrouted until the routing gate of decision 0004 §6 (the previous module's day-0 files must pass Verify in one real repo); no row in practices/README.md, absent from ROUTER.md
principle: principles/13-structured-outputs-and-guardrails.md
sources:
  - sources/2026-10-01-s04-structured-outputs-digest.md
  - https://platform.claude.com/docs/en/build-with-claude/structured-outputs
  - https://developers.openai.com/api/docs/guides/structured-outputs
  - https://python.useinstructor.com/
  - https://github.com/guardrails-ai/guardrails
  - https://openai.github.io/openai-agents-python/guardrails/
supersedes: null
superseded-by: null
---

# Structured outputs and guardrails

## Solves
The product calls a model and one of these symptoms appears: code runs `json.loads` or a regex over the model's text and a key that drifted (`user` → `username`) or a "here is the JSON" preamble breaks a handler; a validation library re-asks the model for schema errors on a provider that already guarantees the schema, and retries stack on retries; a refusal or a truncated output arrives as a JSON parse exception; a "rate this 1–10" number is compared to a threshold as if it were a probability and gates a send, a payment or a publish; an LLM judge is the only check on an irreversible action; guardrails exist as scattered `if` statements with no record of what each does on failure, whether it fails open or closed, or whether it runs before or beside the tool it guards; the model's output is inserted into a page as HTML; a schema is edited per request with no version and nobody notices the prompt cache broke.

## Applies when
- The fact `llm_calls` holds (`../facts.md`): the product itself calls a model at runtime and any of its outputs is consumed by code — parsed, stored, compared, dispatched, rendered.
- The **full** part (the guardrail fixture in CI, assertion 8; the classifier tier of `guardrail-tiers.md`) attaches when `acts_on_world or personal_data or regulated or multi_tenant` also holds — the same facts as the full part of `../security-baseline/`, because the risk the guardrails cover is the risk those facts name.

## Does not apply when
- The only model in the picture is the coding agent working on the repo — `../agent-entry-file/`, `../hooks-and-guards/`, `../security-baseline/` (its injection fixture is for the *agent*, this folder's is for the *product*).
- The model output is read only by a person and never by code (a draft the user edits by hand). The prompt rules of `../llm-api-calls/` still apply; nothing here does.
- The call itself — client module, prompt structure, caching, provider choice — is `../llm-api-calls/`; this folder sits on top of its client module and imports it.
- Routing, fallback, streaming transport and tracing are `../llm-gateway/`; guardrail *placement* rules there point here for *content*.
- Evals as a discipline (datasets, judges, regression tiers) — `../evals/` (draft, unrouted, 2026-10-01). This folder gives the per-class consistency rule and the fixture only.
- Protocol detail for generative UI (AG-UI, A2UI, MCP Apps) and the depth of code sandboxing — sessions 13 and 14 (`../../sources/scan-log.md`).

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `structured_call.py` | `<repo>/src/<package>/llm_structured.py` (imports the client module of `../llm-api-calls/`) | Python reference: Pydantic model → native structured output through `messages.create` + `output_config` (not the SDK's `parse`, which validates eagerly and would own the re-ask); typed `Result` with five branches `ok` / `refusal` / `truncated` / `invalid` / `error`; validators with messages; one re-ask carrying the message; schema version and attempt logged; `strict_tool()` helper; `--demo` prints the request shape without calling the API; the vendor client is imported from the `llm-api-calls` client module (`client()` accessor), never instantiated here |
| `schema-design-rules.md` | `<repo>/docs/llm-schemas.md` | Closed objects, all-required, nullable optionals, flat, no regex/min/max in the grammar, reasoning field first, enum with an out, the Maybe shape, naming as instruction; the dated vendor-limits table (2026-10-01) |
| `validation-and-reask.md` | `<repo>/docs/llm-schemas.md` §validation | What belongs in a validator (invariants, grounding, existence, membership), how to write the message, one owner and a cap of one, when to return `invalid` |
| `decision-vs-generation.md` | the feature spec, once per deciding output | Is this output a decision? Then enumerated options with an out, a probability not a written number, the threshold in code, a classifier or decision model; calibration rules for any score |
| `guardrail-policy.md` | `<repo>/docs/llm-guardrails.md` | One row per guardrail: checkpoint · tier · on-fail · fail-open/closed · budget · placement; side-effect guards blocking; the policy file versioned beside the prompts |
| `guardrail-tiers.md` | read | Grounding and rules → hosted classifier → self-hosted encoder (the ModernBERT recipe, numbers as the speaker's) → LLM judge; where each runs for a solo operator |
| `guardrail-fixture.md` | `<repo>/e2e/fixtures/guardrails/` | Known-bad inputs per class with the expected action, benign look-alikes, the CI stage (full part) |
| `generative-ui-decision.md` | `<repo>/docs/ui-generation.md` | Static / declarative / open-ended per screen; the renderer allow-list; the three untrusted-code questions and their controls |
| `stack-notes/python.md`, `stack-notes/php-laravel.md` | read | Schema generator, SDK native mode, validation idiom, re-ask ownership, streaming and classifier placement per stack — under twenty lines, no code (decision 0005 §5) |

## Reference implementation

`structured_call.py`: one module implementing assertions 1–5 and 10 for the Anthropic SDK with Pydantic, with an OpenAI Responses adapter sketched in a comment. It calls `messages.create` with `output_config.format` and runs the Pydantic validators itself, because the SDK's `messages.parse` validates eagerly inside the call — a validator failure, a truncation or a refusal would raise there, outside the loop that owns the one re-ask. It imports the vendor client from the `llm-api-calls` client module (`llm.py`'s `client()` accessor) so that exactly one module in the repo instantiates the SDK (`../llm-api-calls/README.md` assertion 1). **Python idioms, not required** (decision 0005 §3): Pydantic as the schema generator and validator (Zod, a hand-written JSON Schema or a DTO with a schema package satisfy the contract); the `Result` dataclass that returns branches instead of raising (typed exceptions caught at the handler are the Laravel idiom and also satisfy it); the module-level client; `Generic[T]` for the Maybe shape. The provider's constrained decoding is the mechanism in every stack — any language gets the guarantee by sending the schema. Other stacks: `stack-notes/<stack>.md` and, once a real repo passes Verify, `variants/<stack>/`.

## Stack-sensitive points

- **Schema generator and validation idiom** differ (Pydantic validators and exceptions; Zod `.strict()` and a result; a Laravel Form Request with custom rules); the *contract* — closed object, all required, nullable optionals, invariants in code, message names field and rule — does not.
- **Streaming partial objects** needs an incremental JSON parser or the SDK's helper: Python and TypeScript have one (Instructor's `partial`, the vendor SDKs' stream helpers); PHP generally does not — fall back to *iterable* mode (one complete object per event) or a non-streamed call.
- **The classifier tier is a separate process** in every stack; in a request-scoped runtime (PHP-FPM, serverless) it is an HTTP sidecar with a timeout and a fail-open/closed policy, never in-process.
- **Logprobs and prefill availability differ per provider and model** (prefill is incompatible with Anthropic JSON outputs, and the Messages API reference shows no logprobs field, as far as checked on 2026-10-01; OpenAI's Chat Completions exposes logprobs); the decision file records which the chosen model supports.
- **Where a rejected output is replaced** (the data-free placeholder) depends on who owns the session store — the application, the gateway or an agent framework; one of them must do it.

## Adapt
- `structured_call.py`: set `<<MODEL>>`, `<<MAX_OUTPUT_TOKENS>>` (large enough for the biggest object — truncation is not valid JSON); keep `from .llm import client` pointing at the one client module; replace the `Receipt` example with the product's schemas, each in its own module with its version string; keep `structured()` as the one entry point and `MAX_REASKS = 1` unless a written reason says otherwise. If Instructor or Pydantic AI is already in place, keep it and set its schema-level retries to zero, or make it the sole re-ask owner and delete the loop here — never both.
- `schema-design-rules.md`: keep the stack-neutral rules; re-read the vendor table against the provider's page on adoption day and date the copy.
- `validation-and-reask.md`, `decision-vs-generation.md`: fill the spec template per output; delete the sources' examples once the repo's own invariants are listed.
- `guardrail-policy.md`: delete the example rows; one row per real guardrail; the classifier tier starts as `rule` on day zero and is upgraded when the fixture shows misses (first-user).
- `guardrail-fixture.md`: start with the minimum set per class in the product's own language(s); grow from production triggers; the live run on merge to `main` is optional below the full part.
- `generative-ui-decision.md`: delete the tiers the product does not use; the catalogue list is the allow-list and is reviewed as code.
- Stacks: Python shown; PHP/Laravel in `stack-notes/php-laravel.md`; TypeScript is not a promised stack (decision 0005 §4) — implement from the contract with `../prompt-library/implement-practice.md` until a field-tested variant exists.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who judges it: `script` (a command's exit code), `agent` (observed in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's library; `bends` means the repo's idiom wins. Stack-specific commands live only under *Example commands (Python)*. Assertion 8 belongs to the full part.

1. Every model output that code consumes is produced through the provider's native schema-constrained mode where the chosen model supports it, and is parsed into a typed object before any other code reads it — observer: script — negative: a `json.loads`-style parse of free text, or a regex over the response, on a path that feeds a system — framework: beats
2. Every output schema is a closed object (no additional properties), lists every key as required with optionals expressed as nullable, and uses only features the provider's dialect accepts — observer: script — negative: a schema the provider rejects or that the SDK silently rewrites without a recorded reason
3. Every field carrying a business invariant (totals, ids, dates, quotes, URLs, membership) has a code validator, and a failure yields a message naming the field and the rule — observer: script — negative: a parsed object used while a known invariant is violated, or a bare "invalid"
4. Re-asks after a validation failure have one owner, carry the validator's message, are capped (default one) and are counted in the usage log; the library never re-asks for a schema violation the provider guarantees against — observer: script — negative: an unbounded re-ask loop, two layers re-asking, or a re-ask with no attempt count in the log — framework: beats
5. The three non-schema terminations — refusal, truncation at the output limit, provider error — reach the caller as typed results from named branches, never as a parse exception — observer: script — negative: a refusal or a truncated output that raises a JSON error
6. Where an output decides a branch (a label, a route, a gate, a score), the decision is an enumerated field with an explicit "none/unknown" option, any numeric score has at most five levels or is read as a probability, and the eval reports per-class consistency over at least five runs — observer: script — negative: a free-text label, a forced choice with no out, or a 1–10 score used as a probability
7. Every guardrail in the product has a row in the policy file with checkpoint, tier, on-fail action, fail-open/closed, time budget and placement, and guards on tools with side effects are placed blocking — observer: Martin — negative: a guardrail in code with no row, a row with no on-fail action, or a parallel guard on a send/pay/publish
8. (full) The known-bad fixture runs in CI against the input and output checkpoints and every item is caught by its stated action or recorded as a known gap — observer: script — negative: a fixture item that passes silently
9. Where the model drives the interface, it emits data (a schema or a declarative spec) that a renderer maps to components through an explicit allow-list which rejects unknown types, and any model-written code runs in an isolated runtime with outbound network denied by default — observer: agent — negative: model output inserted as HTML, an unknown component type rendered, or generated code with network access it was not granted
10. Each call logs the schema's version beside the prompt's version, and a schema change goes through the same header, eval and commit as a prompt change — observer: script — negative: a schema edited with no version bump or eval record

**Example commands (Python):** `grep -rn "json.loads(" src/ | grep -v llm_structured` → empty; `python3 -m <package>.llm_structured --demo` (after the two placeholders are replaced and `llm.py` sits beside it — the file does not parse before) prints the request with `output_config.format` and a `strict` tool, and names the five result branches; `pytest tests/test_guardrail_fixture.py`; `grep -rn "dangerouslySetInnerHTML\|innerHTML\|v-html" src/` → nothing on model output.

## Sources
`sources/2026-10-01-s04-structured-outputs-digest.md` §3.1–3.5 and impact table §6 (rows 1, 3, 5, 6, 8, 9, 11, 12, 14–17, 22–24); primary texts listed in `principles/13-structured-outputs-and-guardrails.md` §6. Vendor pages to re-read directly before promoting to `current`: the OpenAI structured-outputs guide (its limits came back through a summariser on 2026-10-01) and the Anthropic structured-outputs page.

## Change log

- 2026-10-01 (s6) — `guardrail-policy.md`: new checkpoint `ingestion` and row **G0** (PII, secrets or a wrong tenant in a document entering the index — checksum + regex, scrub or quarantine then log, closed, blocking, fixture §ingestion; `../data-ingestion/` Verify 6); G3 notes the reversible placeholder dictionary kept outside the index (Huyen 2024-07); G6 notes that on Postgres the ACL is an RLS policy, not an application filter (Supabase, read 2026-10-01); rule 2 "ingestion before the index" inserted, later rules renumbered (the `guardrail-tiers.md` pointer updated). Source: `../../sources/2026-10-01-s06-data-audit-cleaning-privacy-digest.md` §7.2.
- 2026-10-01 (s5) — `decision-vs-generation.md` rule 4: for a *grader*, binary per failure mode first, five classes only for a graded decision; `guardrail-policy.md` G4 (an approval is a paused run with serialised, resumable state) and G6 (authorisation pre-filter or post-filter chosen by hit rate → `../memory-and-permissions/permission-model.md`). Source `sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` rows 6, 36, 37.
- 2026-10-01 — created from the session-4 market scan digest (draft, **unrouted** per decision 0004 §6: no row in `practices/README.md`, absent from `ROUTER.md` until the previous module's day-0 files pass Verify in a real repo). Reference `structured_call.py` parses once placeholders are replaced and prints the request shape with `--demo`; no field report yet.
- 2026-10-01 (review) — `structured_call.py` moved from `messages.parse` to `messages.create` + `output_config` (the SDK's `parse` validates eagerly, which made the truncated branch and the re-ask loop unreachable), now imports the vendor client from the `llm-api-calls` module instead of instantiating its own (assertion 1 of that practice), and names five branches; tested with a stubbed `messages.create`: valid → ok, `max_tokens` → truncated, `refusal` → refusal, validator failure → one re-ask carrying the message then `invalid`, transport error → error. `schema-design-rules.md`: `pattern` is supported by Anthropic's API, stripped by the Python SDK helper; optionals "roughly double" state space, unions are "exponential". `guardrail-policy.md`: `run_in_parallel` is an input-guardrail option; the parallel allowance for text guards is Twilio's; the "Output withheld" placeholder applies to terminal tool outputs. `decision-vs-generation.md`: the smart if-statement is Type-Safe AI's guidance via Witteveen; Boundary's is the threshold example. Stack-notes gain package URLs (decision 0005 §5).
