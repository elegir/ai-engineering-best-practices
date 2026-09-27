# Context budget — sizing a request

Copy into `<repo>/docs/llm-provider.md` §context or into the feature spec. Fill the numbers for the model you actually use; they rot. Principle: `../../principles/10-llm-api-fundamentals.md` §3.4; sources: Pocock (2025-10), Ng (2026-05), Karpathy (2025-02), Cursor (2025-09).

## What shares the window

Everything below is added up on **every call**, and re-sent on every turn of a conversation:

| Part | Typical size | Static (cacheable) or dynamic |
|---|---|---|
| System prompt (§1–5 of `system-prompt-template.md`) | <<n>> tokens | static |
| Tool definitions (names, descriptions, schemas) | <<n>> tokens — audit them; 20 tools with long schemas can be thousands | static |
| Reference documents pasted into the prompt | <<n>> tokens | static per feature |
| Few-shot examples | <<n>> tokens | static |
| Conversation history (all previous items, incl. tool results) | grows every turn | dynamic |
| Current input (user message, attached file, retrieved chunks) | <<n>> tokens | dynamic |
| Thinking budget (reasoning models) + output | <<n>> tokens, reserved | dynamic |

Rule of thumb from the same sources: a token ≈ ¾ of an English word; a page of prose ≈ 500 tokens; a tool result you did not truncate can be larger than your whole prompt.

## The budget

```
Model: <<id>>            Window: <<n>> tokens (look it up; per model)       Max output: <<n>>
Static prefix (cached after first call):  <<n>>  = system + tools + docs + examples
Reserved for output + thinking:           <<n>>
Left for history + current input:         <<window − static − reserved>>
Truncation policy for history:            <<keep last N turns / summarise older / new thread per task>>
Truncation policy for tool results:       <<max chars per result; e.g. 8,000>>
```

## Rules

1. **Static first, dynamic last**, always — that is where the caching boundary goes. Verify with the usage log: `cache_read > 0` from the second call on.
2. **Quality drops before the limit.** "Lost in the middle": material in the middle of a long context is recalled worse than the start and the end. Put the rules at the start, repeat the critical ones at the end, and keep the middle short.
3. **New thread on topic change.** Stale context contaminates answers and you cannot tell afterwards which answer was contaminated (Ng). For chat products, start a new conversation per task; for coding agents, `/clear` rather than `/compact` between unrelated tasks (Pocock).
4. **Truncate every tool result** before it enters the context; one un-truncated log dump ends the conversation's usefulness.
5. **Audit tool and MCP schemas**: they load every turn. Anything not used by this feature is removed from *this* call, not just from the repo (`../token-savings/mcp-audit.md`).
6. **Put the document in, do not describe it.** Even for texts the model has "read", pasting the chapter beats asking from memory (Karpathy's *Pride and Prejudice* demonstration). The window is the working memory; the weights are a vague recollection.
7. **Know the cache's limits.** Minimum cacheable prefix ≈ 1,024 tokens on most providers; TTL 5 minutes to 1 hour depending on provider and setting — a session idle over lunch pays a full cache write on resume; compaction resets the cache from the compaction point (expected). Multi-turn policy: `../context-management/`.
8. **Measure.** Log input / output / cached tokens per call (`llm_call_skeleton.py` does); compute cost per feature per week; decide changes from the numbers, not from the vendor's pricing page.
