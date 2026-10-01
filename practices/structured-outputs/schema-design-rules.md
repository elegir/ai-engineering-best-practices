# Schema design rules — what an output schema must look like, and the vendor limits as of 2026-10-01

Copy to `<repo>/docs/llm-schemas.md` and apply to every schema that goes to a model as an output format or a strict tool. Principle: `../../principles/13-structured-outputs-and-guardrails.md` §3.1. Sources: Michelle Pokrass, OpenAI (Latent Space, 2024-09); Jason Liu (AI Engineer, 2023-11 and 2024-09); the OpenAI structured-outputs guide and the Anthropic structured-outputs page, both read 2026-10-01 — digest `../../sources/2026-10-01-s04-structured-outputs-digest.md` §3.1. Every rule below says who said it; the vendor-limits table is dated and will rot.

## The stack-neutral rules

1. **Closed object.** Every object sets `additionalProperties: false`. JSON Schema's default is `true`, which Pokrass calls "the opposite of what developers want"; both providers require the closed form rather than redefining the standard. In Pydantic: `model_config = ConfigDict(extra="forbid")`; in Zod: `.strict()`; by hand: write the key.
2. **Every key required.** In JSON Schema every property is optional by default — "you'd be very surprised if you passed in a bunch of keys and you didn't get some of them back" (Pokrass). List every key in `required`. A schema generator that drops keys with defaults from `required` (Pydantic does, when a field has a default) is working against you: give optional fields no default.
3. **Optional means nullable, not absent.** An optional value is a union with `null` (`"type": ["string", "null"]` or `anyOf`), still listed in `required` (Pokrass; both vendor pages). The model then has to *say* "nothing", instead of silently omitting the key.
4. **Flat where possible, few optionals, few unions.** On Anthropic's compiler "each optional parameter roughly doubles a portion of the grammar's state space", and union-typed parameters (`anyOf`, type arrays) "are especially expensive because they create exponential compilation cost" (page read 2026-10-01); the limits in the table below are on exactly these. Nested objects are fine; deep recursion and many optionals are expensive and slow the first call.
5. **No min/max in the grammar; treat a regex as a validator too.** `minimum`, `maximum`, `minLength`, `maxLength` are unsupported by Anthropic's API and the SDK helper moves them into the field *description*; `pattern` (regex) *is* supported by the API (page read 2026-10-01), but the Python SDK helper (`transform_schema`, 1.11.0) moves it into the description as well — so on any provider a range or a format is a **business invariant** that belongs in a code validator with a message (`validation-and-reask.md`), and a `pattern` left in the schema is a hint, never the check. The schema constrains the shape; the validator constrains the meaning.
6. **Reasoning field before the answer field.** Generation is sequential; the model reads what it already wrote. Liu puts an optional `chain_of_thought` first in reusable sub-models and switches it off in production; Pokrass's launch example is a `steps` array before `final_answer`; Witten (Anthropic, 2024-06) puts the grader's reasoning before the grade. Order the properties accordingly — Anthropic emits required properties in schema order.
7. **Every enum has an out.** A `Literal["a", "b", "c"]` with no `"none"` / `"unknown"` / `"other"` forces a choice the model will make even when nothing fits (`../llm-api-calls/failure-modes-and-mitigations.md` row 7). Add the out and test that it is used on edge inputs.
8. **Model failure as data — the Maybe shape.** Instead of "return I DON'T KNOW in all caps" and a substring check, the schema is `{result: T | null, error: bool, error_message: string | null}` (Liu 2023, `MaybeUser`). The provider's refusal (`stop_reason: refusal`) is the same idea one level down; `structured_call.py` returns both as typed branches.
9. **The schema is a prompt — name and describe accordingly.** Three places, three jobs (Pokrass): the **system message** says *when* to produce this shape or call this tool; the **field or function description** says *how* ("year-month-day, not day-month-year"; "verbatim, as printed"); and a descriptive **key name** helps (`merchant_as_printed`, not `m`) — though the key-name trick is swyx's habit, not officially endorsed by Pokrass. Docstrings and `Field(description=…)` travel into the schema the model sees (Liu 2023); the rules in `../agent-patterns/tool-definition-template.md` apply to output schemas unchanged.
10. **Enum values are compared case-insensitively in code.** Anthropic does not guarantee the capitalisation of string enum and const values (page read 2026-10-01). Normalise before comparing.
11. **Version the schema beside the prompt.** A schema change is a behaviour change: it carries a version string (`receipt-v3`) that is logged on every call next to the prompt version, goes through the same eval and commit as a prompt change — and on Anthropic **invalidates the prompt cache** for the thread (`../../principles/11-runtime-context-management.md` §3.3). Do not iterate a schema per request.
12. **No personal or regulated data in the schema definition.** Anthropic caches compiled schemas server-side for 24 hours and says "PHI must not be included in JSON schema definitions" (page read 2026-10-01). Field names, descriptions and enum values are definitions; keep patient names, account numbers and the like in the *input*, never in the schema.
13. **One schema per purpose; a decision is a decision.** If the output decides a branch (a label, a route, a gate, a score), apply `decision-vs-generation.md`: enumerated options, a probability not a written number, the threshold in code. Do not bury a decision inside a generation schema as a `score: int` field.

## Vendor limits and behaviour — as read on 2026-10-01 (dated; re-check before relying on a number)

| Fact | Anthropic (structured-outputs page) | OpenAI (structured-outputs guide, via summariser; Pokrass 2024-09 for the design) |
|---|---|---|
| Request parameter | `output_config.format` = `{type: "json_schema", schema: …}` on `messages.create`; SDK `client.messages.parse(output_format=Model)` → `parsed_output` | `text.format` / `response_format` with `strict: true`; SDK `responses.parse(text_format=Model)` → `output_parsed` |
| Strict tool arguments | `strict: true` per tool; combinable with JSON outputs in one request | function schemas with `strict: true` |
| Closed object, all required, nullable optionals | required | required |
| Unsupported constraints | `minimum`, `maximum`, `minLength`, `maxLength` unsupported by the API, moved to descriptions by the SDK helper; `pattern` supported by the API but moved to the description by the Python SDK helper (1.11.0) | a documented subset of JSON Schema; the summary did not return the list |
| Size limits | 20 strict tools per request; 24 optional parameters across strict schemas; 16 union-typed parameters; compile timeout 180 s; `400 "Schema is too complex for compilation"` beyond | the summary omitted the limits — read the page directly before promoting this practice |
| Grammar cache | compiled on first use; cached 24 h from last use; **no PHI in schema definitions** | one-time compile per new schema; pre-registration considered and rejected (Pokrass) |
| Prompt cache | changing the output schema invalidates the prompt cache for that thread | not stated in the summary |
| Non-schema terminations | `stop_reason: "refusal"` (HTTP 200, billed); `stop_reason: "max_tokens"` (truncated — raise the limit); enum casing not guaranteed | refusal as a field in the response (a design choice: "there's kind of like the model's fault, and there's no error code for that" — Pokrass); incomplete at the output limit |
| Incompatibilities | message prefill; citations | parallel function calling excluded at launch (compile latency) — Pokrass |
| Ordering | required properties emitted first, in schema order | — |
| Streaming | "like normal responses" | supported; Instructor's *partial* and *iterable* modes on top |

The two rows marked "summary" are the digest's caveat (§1, §4): the OpenAI page came back through a summariser on 2026-10-01 and the limits it omitted are not invented here.

## Checklist before a schema ships

- [ ] closed object; every key in `required`; optionals nullable with no default
- [ ] no `minimum` / `maximum` / length constraints (unsupported); any `pattern` is also checked by a validator (the SDK helper strips it)
- [ ] reasoning field first, answer last; every enum has an out
- [ ] descriptions say *how*, the system prompt says *when*; key names are descriptive (a habit, not a guarantee)
- [ ] a version string, logged per call; an eval record for this version
- [ ] no personal or regulated data in names, descriptions or enum values
- [ ] `python3 structured_call.py --demo` (or the stack's equivalent) prints it and the provider accepts it on a first call
