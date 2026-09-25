# Tool definition — <<tool_name>>

The description is part of the prompt. Write it for a new engineer who has never seen your system and cannot ask questions. Source: `principles/21-agent-design-and-tools.md` §3.4; Anthropic *Writing effective tools for agents* (2025-09-11).

## Template (put this in the docstring / schema `description`)

```
<<verb_noun>>(<<param_1>>, <<param_2>>) -> <<what comes back, in one line>>

What it does: <<one or two sentences in the user's terms, not the API's>>.
Use it when: <<the situations in which the model should reach for it — and one in which it should not>>.
Returns: <<the shape, e.g. "markdown with sections: Status, Items, Shipping, Last messages">>.
Errors: returned as text starting with "error:" — <<the cases: not found, no permission, too many results>>.
Limits: <<max results / max lines / rate>>.
Example: <<param values → what the model will see, three lines>>.
```

Parameter descriptions: one line each, with the format and an example value (`order_id: the 8-digit id shown in the customer's email, e.g. "10482233"`).

## Checklist (all twelve before the tool ships)

1. [ ] **UI-shaped, not API-shaped.** One call returns what a person would see on the screen for this question, with the surrounding context. Not three endpoints the model must stitch.
2. [ ] **Named for the intent** (`get_order`, `search_runbooks`), unique across every server/tool set the agent loads. No collisions, no `a`/`b` parameters.
3. [ ] **Description says when to use it and when not.** Includes domain hints the model cannot know.
4. [ ] **Returns a format the model already knows** — markdown, plain text, JSON with obvious keys, SQL results as a table. No internal XML/DSL.
5. [ ] **Errors are returned, never raised.** Every failure path yields a human-readable `error: …` the model can act on.
6. [ ] **Bounded.** Max results, max lines/characters, timeouts; paths confined to an allowed root; no unbounded reads.
7. [ ] **Idempotent or explicitly marked as a write.** Reads and writes are separate tools; writes say so in the name and description (and carry a read/write annotation if the transport supports it).
8. [ ] **Token-efficient.** Relative paths not absolute; ids resolved to names before returning; no repeated boilerplate.
9. [ ] **Auth rung recorded.** Which of: agent's own credentials / OAuth impersonation / token exchange on behalf of the user / vault-issued short-lived credential. Anything below token exchange needs a written reason.
10. [ ] **Probed from the model's side.** You asked the model: "Is this description clear? Would you need more or fewer parameters?" and ran ≥ 5 requests with `debug=True`, reading the parameters it chose.
11. [ ] **Has an eval.** ≥ 5 (request → expected tool call + parameters) pairs, run in CI, owned by the team that owns the tool.
12. [ ] **Counted.** The agent's total tool count is known; above ~30, tools are bucketed or behind a tool-search step; unused ones are removed.
