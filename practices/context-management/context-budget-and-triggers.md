# Context budget and triggers — the numbers per feature

Copy to `<repo>/docs/context-policy.md`. One block per feature that keeps history or answers over documents. The numbers rot with every model generation: date them. Principle: `../../principles/11-runtime-context-management.md` §3.1–3.2. Sources: Manus (2025-10), LangChain (2025-11), AWS (2026-09), Horthy (2026-07), Google Cloud (2026-07) — `../../sources/2026-09-27-s02-context-caching-digest.md`.

## The context stack (what is in the window on every call)

Seven parts (Google Cloud's list, which matches Anthropic's). Mark each one static (cacheable prefix) or dynamic, and estimate its size:

| Part | Static / dynamic | Size (tokens) | Notes |
|---|---|---|---|
| 1. Instructions (system prompt, rules, output format rules) | static | <<n>> | No timestamps, user names, cwd. Positive examples over "don't" rules. |
| 2. Tool definitions | static | <<n>> | Fixed set per feature; do not add/remove per turn (cache + phantom tools). Aim for a small set (Manus: "not more than ~30") and reach the rest through a shell or code tool. |
| 3. Retrieved facts / documents | static per corpus, or dynamic per query | <<n>> | Bounded stable corpus → static, cached. Per-query retrieval → dynamic, after the prefix. |
| 4. Long-term memory (stable facts about the user/project, selected on demand) | dynamic | <<n>> | Selected, not dumped. |
| 5. Short-term notes (plan, what has been checked, where I left off) | dynamic | <<n>> | Lives in a file/scratchpad; the window holds the current version only. |
| 6. Conversation history (messages, tool calls, tool results) | dynamic, append-only | grows | Subject to compaction below. |
| 7. Current user input + reserved output (and thinking budget) | dynamic | <<n>> | Reserve output before you count what is left. |

## The budget

```
Feature: <<name>>                      Model: <<id>>            Filled: <<date>>
Window (per model docs):               <<n>> tokens
Static prefix (1+2+3 when static):     <<n>>   → must be byte-identical between turns
Reserved output + thinking:            <<n>>
Available for 4–7:                     <<window − prefix − reserved>>

Compaction trigger:                    <<60–85 % of the window, or the vendor's guidance; Manus compacts at ~128–200k on 1M models>>
Recency window kept verbatim:          <<last N turns or last T tokens; LangChain demo keeps ~1,000 tokens; AWS keeps the last 2 messages>>
Tool-result cap before offload:        <<e.g. 2,500 tokens → store, keep a 500-token preview + pointer>>
Summariser model:                      <<cheap tier>>
Cache TTL of the provider:             <<5 min / 1 h — a session idle longer pays a full write on resume>>
Minimum cacheable prefix:              <<~1,024 tokens on most providers>>
```

## Rules that go with the numbers

1. **Stay well below the window.** Quality falls before the limit ("context rot"); the trigger is a quality decision, not a capacity one.
2. **Static first, dynamic last, append-only.** The cache matches token by token from the start; the first change breaks it for everything after.
3. **New session on a new task.** Compact to continue the same task; clear to start another — the old trajectory biases the new work.
4. **Replace, do not append, when a requirement changes.** Stale instructions compete with current ones.
5. **Cap every tool result** before it enters the window; offload the rest with a pointer.
6. **Count the instructions**, not only the tokens: a prompt that has accumulated dozens of "don't" patches is over budget even when short.
7. **Measure** (`context-metrics-and-evals.md`) before changing any number here.
