# Context metrics, the long-session eval, and the isolation rules

Copy into `<repo>/docs/context-policy.md` §metrics and `<repo>/evals/`. Principle: `../../principles/11-runtime-context-management.md` §3.2 (isolate), §3.3 (cache), §3.5 (traces and evals). Sources: Arize (2026-05), Hugging Face (2026-08), Harrison Chase (2026-01), Manus (2025-10), Ebbelaar (2025-12) — `../../sources/2026-09-27-s02-context-caching-digest.md` §3.2–3.5.

## 1. What to log

Per call (the client module already emits these — `../llm-api-calls/llm_call_skeleton.py`):

| Field | Why |
|---|---|
| `input`, `output`, `cache_read`, `cache_write` tokens | Cost; and `cache_read == 0` after turn 1 means the prefix is not static |
| `context_size` = input + cache_read | Utilisation vs the window; drives the compaction trigger |
| `turn_index`, `session_id` | Long-session analysis |
| `compaction_event` (step 1 / step 2 / none, tokens before → after) | To see how often and how much you compact |
| `tool_calls[]` with input params and result size | To find the tool that floods the window |

Per session: cache hit rate (`Σ cache_read / Σ (input + cache_read)`), cost, number of compactions, final context size, whether the user's goal was reached. A dashboard with these five columns is the whole observability requirement for this practice. Use the OpenTelemetry GenAI attributes or your tracing tool (Langfuse, LangSmith); the fields matter, the tool does not.

**Read one full trace per week.** "You don't actually know what the context at step 14 will be, because there's 13 steps before that that could pull arbitrary things in" (Chase). Bugs that never appear in a five-turn dev test appear at turn 10–20 in production and are obvious in a full trace (Ebbelaar). Name what you see with `context-failure-modes.md`.

## 2. The long-session eval (Arize's pattern)

Context failures are reported by users because dev testing is short. Make them reproducible:

1. Collect **10 real sessions** of ≥10 turns from production (or synthesise them from real inputs).
2. For each, freeze turns 1–N as the fixture (after your compaction policy has run on them, exactly as in production).
3. Define the **turn N+1** check: a follow-up that depends on something said early (turn 1–3) — an id, a constraint, a preference — and its expected answer or expected tool call.
4. Run each case **at least 5×**; report the worst case per scenario, not the mean (`../llm-api-calls/failure-modes-and-mitigations.md` row 12).
5. Run it in CI on every change to the compaction policy, the system prompt, the tool set or the model.

Extend with: a case where the user reverses a requirement at turn 5 (checks *replace, don't append*); a case with a duplicated tool result (checks dedupe); a case that crosses the compaction trigger between N and N+1 (checks that the summary preserved the `must_preserve` list).

## 3. Isolation rules for sub-agents

| Rule | Why | Source |
|---|---|---|
| The sub-agent's **final message is self-contained**: conclusions, values, pointers restated; never "see above" | Only the final message crosses the boundary; the orchestrator never saw "above" | Chase |
| Default to **communicate** (short brief in, structured result out), not **share memory** (whole history in) | Shared history forfeits the cache (different prefix) and costs the full prefill per sub-agent | Manus |
| **Fan out only read-only, independent gathering**; converge for anything that must cohere (final report, integrated code) | Inter-agent compression is lossy and decisions conflict; Anthropic's researcher works because sub-agents only read | Cognition vs Anthropic, via Martin |
| Constrain sub-agent output with a **schema** defined at spawn time (a `submit_result` tool) | Many parallel results must aggregate without parsing prose | Manus |
| **No role-based agents** mimicking an org chart; an executor, a planner, a memory agent at most | Every extra agent multiplies communication | Manus |
| Put **noisy work** (log parsing, wide searches, long reads) in the sub-agent and only the digest in the parent | Keeps the orchestrator's context light and cache-friendly across many turns | AWS, Arize, Claude |

Test for rule 1: hand the sub-agent's final message to a fresh model with no history and ask for the conclusion; if it cannot answer, the message is not self-contained.
