# System prompt template — ten parts, static first, versioned

Copy to `<repo>/prompts/<feature>/system.md`. One file per runtime prompt, under version control. The order is Anthropic's *Prompting 101* (2025-05) structure; it is also the order that makes **prompt caching** work: everything above the `--- dynamic ---` line must be byte-identical between calls, everything that varies goes below it or into the first user message. Delete parts the prompt does not need; never move a dynamic part above the line.

Principle: `principles/10-llm-api-fundamentals.md` §3.3–3.4.

```
<!-- prompt header (not sent to the model; strip before rendering or keep as a comment your renderer drops)
purpose:        <<what this prompt does, one line>>
model:          <<model id this was tuned on>>       tier policy: docs/workflow.md §models
version:        <<v3 — 2026-09-27>>
last-evaluated: <<date; N real inputs, M edge cases, K runs each; worst-case result>>
changelog:      <<v3: added "give an out" rule after empty-input failures; v2: …>>
-->

# 1. Task context and role
You are <<a support assistant for ACME's order system>>. You work for <<who>> and your job is <<what>>.
(Write it as a briefing for a competent temp who has never heard of your company. No theatrical
role-play the task does not need; "you are a helpful assistant" adds nothing.)

# 2. Tone
<<Plain, concise, no marketing language. Address the customer by first name. Never apologise more than once.>>

# 3. Background data and documents
<document name="<<policy.md>>">
<<Paste the actual policy / spec / reference text. Give the model the paper, not your summary of it.>>
</document>

# 4. Rules
Numbered, one behaviour each. Prohibitions as well as obligations.
1. <<Answer only from the documents above and the tool results; if the answer is not there, say so.>>
2. <<Never quote a price, date or order id from memory; call the tool.>>
3. <<If none of the categories apply, output "none" — do not force a match.>>   ← the "out"
4. <<Do not agree with a premise just because the user states it; check it.>>   ← sycophancy guard
5. <<What you are, your cutoff and what you can't do: "<<model/product name>>, cannot access X">>  ← identity is prompted, not known

# 5. Examples
<example type="illustrative">   ← shows the SHAPE; the model should not copy the content
<<input → ideal output>>
</example>
<example type="edge">           ← at least one that covers the RANGE: empty, off-topic, malformed
<<input → ideal output>>
</example>

--- dynamic (everything below may change per request) ---

# 6. Conversation history
<<injected by the client as items; nothing here for single-shot prompts>>

# 7. The immediate task
<<"Classify the message below into one of: …" / "Answer the customer's question using the tools.">>
Today is <<date>>. The user is <<name / plan / locale>>.

# 8. Thinking
Reasoning model: leave this empty and set the thinking/effort budget in the API call.
Other models: "Before answering, work through <<the steps>> inside <thinking> tags; then give the answer."
Never: "reply with just the number" on a multi-step problem.

# 9. Output format
<<Return JSON matching this schema: … / Markdown with these headings: … >>
Repeat the two rules that matter most here; the end of the prompt is remembered best.

# 10. Prefill (Anthropic: first assistant tokens; OpenAI: omit)
<<"{" to force JSON / "## Summary" to force the structure>>
```

## Checklist before shipping a prompt change

1. The header is filled: purpose, model, version, last-evaluated, changelog line.
2. Everything above `--- dynamic ---` is identical between calls (diff two rendered prompts).
3. The rules are numbered, one behaviour each, and include an **out** ("if none apply, say so").
4. Every fact, number, id or date the answer may need is in §3 or reachable by a tool — none is expected from memory.
5. Examples: at least one illustrative, at least one edge case; none that the model could copy verbatim into a real answer.
6. §8 matches the model: thinking budget for a reasoning model, explicit "show your work" otherwise; no bare-answer demand on multi-step tasks.
7. Output format stated once in §9, and validated in code (schema / parser) — the prompt is not the guarantee.
8. Sycophancy test: the same question phrased leading ("don't you think X?") and neutral ("is X true?") gives the same answer.
9. Ten real inputs and five edge cases (empty, off-topic, malformed, hostile, very long) were run **at least 5× each**; the worst case is recorded in the header, not the mean.
10. You read the outputs. All of them.
11. The model was asked "what in this prompt is ambiguous or missing?" and its answer was acted on (`../prompt-library/trajectory-review.md`).
12. The change is a commit on this file, not an edit in a dashboard nobody diffs.
