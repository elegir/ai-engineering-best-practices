# Validation and the re-ask — what belongs in a validator, how to write its message, who owns the second call

Copy to `<repo>/docs/llm-schemas.md` §validation. Principle: `../../principles/13-structured-outputs-and-guardrails.md` §3.2. Sources: Jason Liu (AI Engineer, 2023-11 and 2024-09); Instructor front page (read 2026-10-01); Shreya Rajpal (AI Engineer, 2023-11); Michelle Pokrass (Latent Space, 2024-09) — digest `../../sources/2026-10-01-s04-structured-outputs-digest.md` §3.1, §3.3. Reference code: `structured_call.py`.

## The division of labour

The provider's constrained decoding guarantees the **shape**: the object parses, every key is there, every type is right (`schema-design-rules.md`). It guarantees nothing about the **meaning** — "the guarantees is that they fit the schema but the schema itself may be too broad… you might give me zero, give me 12" (Pokrass). The meaning is checked by **validators in code** attached to the parsed object, and a failed validator is the *only* reason to ask the model again. A library that re-asks for a schema violation on a provider that already guarantees the schema is paying twice (swyx's one-pipeline measurement of −55 % API cost after removing library retries, relayed by Pokrass; the number is anecdotal, the mechanism is not).

## What belongs in a validator

The sources' own examples, each an invariant a grammar cannot express:

| Invariant | Check in code | Source |
|---|---|---|
| Arithmetic consistency | `sum(quantity × unit_price) == total` within a cent | Liu 2023 (receipts) |
| Grounding — the quote exists | every `quote` string is a literal substring of the source chunk; a fact whose quote is not found is dropped or re-asked | Liu 2023 ("not by asking it to not hallucinate but actually trying to figure out… what the quotes were"); Rajpal's *provenance* validator (embedding similarity / NLI / self-check) is the softer form |
| Existence — the reference resolves | every URL returns 200; every id exists in the system of record; a label is in the allowed set | Liu 2024 ("if it's not real just throw it out next time, don't try too hard") |
| Membership | `owner ∈ participants`; `assignee ∈ team` | Liu 2024 (meeting notes) |
| Range and format | `0 < total`; a date parses; a phone number matches the locale | `minimum`/`maximum`/length are unsupported by Anthropic's API and a `pattern` is stripped by the Python SDK helper — so these live here, in code |
| Policy | no competitor name; no blocked phrase; no PII in a field that must not carry it | Guardrails AI validators (README read 2026-10-01); `guardrail-policy.md` decides where the check runs |

Not a validator: anything the schema already guarantees (type, presence, enum membership); anything that needs a second model's opinion (that is a guardrail with its own tier and budget — `guardrail-policy.md`).

## How to write the message

The validator's message **is the re-ask prompt**: "really all you care about is having good, well-written, informative error messages" (Liu 2024). Rules:

1. Name the **field** and the **rule**: `items sum to 6.00 but total is 7.00`.
2. Say **what to do**: `fix the quantities, unit prices or the total so they agree` — not `invalid`.
3. Quote the **offending value**, not the whole object.
4. Keep it one line per failed rule; `structured_call.py`'s `_message()` joins them with `; `.
5. Never leak into the message what the model must not see (another tenant's data, a secret, the full source document twice).

## Who owns the re-ask, and how many

- **One owner.** The re-ask is a deliberate second call made by one module (`structured_call.py`, `MAX_REASKS`), the same way `../llm-gateway/routing-policy.md` rule 2 has one owner of transport retries. If a library (Instructor `max_retries`, Pydantic AI `retries`, Guardrails `reask`) is in the stack, set its re-asks to zero *or* make it the sole owner — never two layers, which is how ManyChat reached 16 attempts per call for transport retries (s3) and would reach it again for re-asks.
- **Cap of one by default.** "Often one retry for models like OpenAI and Anthropic are basically enough" (Liu 2024). A second re-ask on the same message is almost always the same wrong answer; it is cheaper to return `invalid` and let the caller decide (fallback, human, skip).
- **The re-ask carries the message and nothing else.** The model's own output goes back as the assistant turn, the validator's message as the next user turn ("it is the error message that is part of the prompt but conditionally added" — Liu). The system prompt and the earlier items are untouched, so the cache still hits.
- **Counted.** The usage log records `attempt` per call (1 = first, 2 = after the re-ask) beside the schema version and the prompt version. An eval that shows a rising re-ask rate is telling you the schema or the prompt moved, not that the model got worse.
- **Refusal and truncation are not re-asked.** A refusal is a decision; a truncation is a `max_tokens` problem — raise the limit for that schema. Both reach the caller as their own branch (`structured_call.py`).

## When to give up — the `invalid` result

After the capped re-ask fails, `structured()` returns `Result(branch="invalid", message=<the validator's message>)`. The caller chooses, per feature and written in the spec: a deterministic fallback (a default, a queue for a human, the Maybe shape's `error_message` shown to the user), **never** a silent use of the object that failed and never an exception thrown from a handler. For an action with side effects the `invalid` branch is a hard stop (`../verification/dry-run-and-approval.md`).

## Why the reference uses `messages.create`, not the SDK's `parse`

Anthropic's `client.messages.parse(output_format=Model)` transforms the schema, sends it, validates the response and returns `parsed_output` — convenient, but the validation happens *inside* the SDK call: a validator failure, a truncated object or a refusal with text raises there, before the caller can check `stop_reason` or run its own re-ask. `structured_call.py` therefore calls `messages.create` with `output_config.format`, checks the stop reason first (refusal, max_tokens), and runs `Model.model_validate_json(raw)` inside the one `try/except ValidationError` that owns the re-ask. The trade-off: `create` sends the schema exactly as Pydantic emits it (no SDK transform), so every model must carry `extra="forbid"` and the unsupported constraints must not be in the schema at all (`schema-design-rules.md`).

## Testing the loop without a model

Unit-test the validators with hand-built objects (the `items_add_up` example in `structured_call.py` is one line to assert). Unit-test the *loop* with a mock model that returns a typed object — Pydantic AI's `TestModel` / `FunctionModel` are the named mechanism (Colvin, 2025-02); any stack can stub the one function that calls the provider. Run a live smoke test on real inputs separately and on every commit to `main`, because "all of the models fail more often than you might expect" (Colvin).
