---
title: "Prompt — trajectory review: think like your agent"
type: template
status: current
date: 2026-09-24
tags: [prompt, agents, debugging, tools]
sources:
  - sources/2026-09-24-s12-agents-digest.md
---

# Trajectory review — "think like your agent"

Use before changing a prompt or adding orchestration. Source: Barry Zhang and Erik Schluntz (Anthropic), 2025; `principles/21-agent-design-and-tools.md` §3.3.

**Step 0 — get the raw material.** Dump exactly what the model received on a failing run: the system prompt, every tool schema (name, description, parameters), and the full sequence of tool calls with the *parameters the model chose* and the *results it got back*. Read it once yourself with nothing else open. Note what you, knowing only this, would not have known.

**Step 1 — ask the model to review its context** (paste the system prompt and tool schemas):

```
You are reviewing the context an agent receives before it acts. Below are its system prompt and its tool definitions.
1. List every instruction that is ambiguous or that two reasonable readers would apply differently.
2. For each tool: could you use it correctly from its description alone? What is missing (when to use it, when not, the return format, error cases, limits)? Would you want more or fewer parameters?
3. What information about the environment would you need to complete the task that is not here (state, formats, ids, conventions)?
4. Rewrite the three weakest tool descriptions.
Answer as a numbered list; be concrete; do not praise.
```

**Step 2 — ask the model to explain a trajectory** (paste the full trajectory):

```
Below is the complete trajectory of an agent run that ended badly: every tool call with its parameters and result, and the final answer.
For each step where the decision looks wrong, say: what the agent believed at that point (based only on what was in its context), why the decision followed from that, and what single piece of context or tool change would have led to a better decision.
Then answer: was the failure caused by (a) missing context, (b) a tool's return value or description, (c) the prompt, or (d) the model's reasoning? Give the most likely cause first.
```

**Step 3 — act on the answer in this order:** fix the tool (return value, description, bounds) → add the missing context → adjust the prompt → only then consider a different model or more orchestration. Record what changed in the harness changelog (`principles/02-harness-engineering.md` §4.6).
