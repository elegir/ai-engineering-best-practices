# Agent decision — <<FEATURE>> — <<YYYY-MM-DD>>

Fill this in before writing code. Source of the four questions: Barry Zhang (Anthropic), "How we build effective agents", 2025-03; `principles/21-agent-design-and-tools.md` §3.1.

## The task in one sentence
<<What the model must accomplish, from whose request, producing what.>>

## 1. Complexity — can we draw the decision tree?
- [ ] Yes, on one page → **workflow**. Sketch it below and optimise each node.
- [ ] No — the inputs or the path vary in ways we cannot enumerate → candidate for an **agent**.

<<sketch or "not drawable because …">>

## 2. Value — what is the budget per task?
- Budget per task: <<$>> ≈ <<tokens>> tokens at <<model>> prices.
- [ ] Cents → workflow for the common cases; agent only for the long tail, if at all.
- [ ] Dollars, and the task is worth it → agent affordable.

## 3. Critical capabilities — what must the model already do well?
List the 2–3 capabilities the trajectory depends on and how we checked them (a 10-example probe is enough):

| Capability | Probe | Result |
|---|---|---|
| <<e.g. write a correct SQL query for our schema>> | <<10 hand-written requests>> | <<8/10>> |

If any is weak: reduce scope and re-probe before scaffolding around it.

## 4. Cost of error and of error discovery
- Worst plausible error: <<…>>
- How would we notice? <<test / checker / human review / never>>
- [ ] Cheap to discover → autonomy acceptable.
- [ ] Expensive or hard to discover → limit: read-only tools / approval before write actions / human in the loop. (Note: this also limits scale.)

## Decision
- [ ] **Workflow** (fixed pipeline of narrow prompts)
- [ ] **Workflow of agents** (fixed pipeline, each step a small closed loop with its own check)
- [ ] **Agent** (open-ended loop with tools)

Why, in two sentences: <<…>>

## The minimal shape (if agent or workflow of agents)
- Environment: <<what system it acts in>>
- Tools (≤ 10 to start): <<names>>
- System prompt: <<one paragraph: goal, constraints, ideal behaviour>>
- Signal that closes the loop: <<test / checker / eval>>
- Stop conditions: max <<N>> iterations, max <<tokens>>, max <<seconds>>
