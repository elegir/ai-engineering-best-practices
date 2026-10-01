# Decision or generation? — when a model output is a classification, treat it as one

Copy the questions into the feature spec, once per model output that decides something. Principle: `../../principles/13-structured-outputs-and-guardrails.md` §3.4. Sources: Michelle Pokrass (Latent Space, 2024-09); Zack Witten (Anthropic, AI Engineer World's Fair, 2024-06); Shreya Rajpal (AI Engineer, 2023-11); Diego Carpintero (AI Engineer, 2026-04); Boundary's *Jev Explained* stream and Sam Witteveen's Jev test (both 2026-09) — digest `../../sources/2026-10-01-s04-structured-outputs-digest.md` §3.4.

## The question

**Is this output a decision?** A decision is a label, a route, a gate (yes/no, send/hold), a priority, a score that a threshold will act on. A generation is text a person reads or arguments a tool needs. The sources agree that most decisions inside software are classifications and that a generative model is the wrong tool for them: Pokrass recommends log-probabilities over options instead of a sampled number; Witten warns a 1–5 grade is "not very well calibrated"; Rajpal and Carpintero use encoder classifiers for guardrails because "you don't need a jackhammer to crack open a walnut"; Jev's premise is that "software doesn't want a paragraph, it wants a value" (Witteveen).

If the answer is yes, the rules below apply. If no — the output is prose, a document, a plan with free text, tool arguments — `schema-design-rules.md` applies and this file does not.

## Rules for a decision output

1. **Enumerate the options, with an out.** The decision is a field with a fixed set of values and an explicit `none` / `unknown` / `other` (`../llm-api-calls/failure-modes-and-mitigations.md` row 7). A free-text label is not a decision; a forced choice with no out is a wrong decision waiting to happen.
2. **A written number is not a probability.** When a generative model outputs `0.9` or `7/10`, that is a token it predicted, not its confidence: "a non-calibrated model might always pick seven" (Pokrass); "the number that you're getting back there is just generated text" (Witteveen on Jev's contrast with LLMs). Never feed a written score into a threshold as if it were a probability.
3. **Where a probability is needed, read one.** In order of preference for a solo operator (opinion, stated as such): (a) a **hosted moderation or classification endpoint** that returns scores for the classes you need; (b) **log-probabilities over enumerated options** — ask for one of `A / B / C / D` and read the logprobs of those tokens (Pokrass: "rather than sampling two tokens for yellow you can just do ABCD and get the log probs"); (c) a **probability-returning decision model** (Jev's *choice* / *score* / *nul* questions, 2026-09 — a dated trend, re-evaluate after 2026-12 with an eval); (d) a **fine-tuned encoder classifier** you host (`guardrail-tiers.md`). Record in the spec which the chosen model and provider actually support — logprobs after a chain of thought need prefill and logprobs in one API, "which few models offer" (Witten).
4. **Coarse scales only.** If a score must be generated, "limit the granularity to maybe five different classes" (Witten) — `very_low / low / medium / high / very_high`, or 1–5 — never 1–10 or 0–100. Five levels can be checked for consistency; a hundred cannot.
5. **Reason first, decide last.** When the model generates the decision (options b and 4 above), put a short reasoning field *before* the decision field in the schema (Witten; Liu; Pokrass's `steps`); generation is sequential and the model reads what it already wrote.
6. **The threshold lives in code, not in the prompt.** "If the email feels urgent with confidence 80 % do this; 50–80 % maybe; otherwise normal" (Boundary's example in the *Jev Explained* stream): the model returns the probability, the code holds the number, and changing the policy is a code change with a test — not a prompt edit.
7. **Decompose compound judgements — the "smart if-statement".** "Rate this pitch" becomes four small questions (is the market named? is there a number? is the ask clear? is the tone professional?), each a separate decision, run in parallel, combined in code — Type-Safe AI's guidance as relayed by Witteveen; Boundary's triage class (an enum, a score and booleans as independent calls) is the same idiom in BAML. Small questions are more consistent and easier to eval than one big rating.
8. **A decision model does not produce arguments.** Jev "is just telling us which tool to use as opposed to getting the right arguments out" (Witteveen); Horthy's attempt to run a coding agent as a state machine over choice questions was "an abuse of Jev". Route with the decision model; generate the arguments with the generative model and a strict tool schema.
9. **Eval per class, over runs.** The eval reports per-class consistency over at least five runs of every case (`../../principles/05-verification-loops.md`): a decision that flips on the same input is not a decision. Measure the miss rate of the decision model on *your* hard cases, as `failure-modes-and-mitigations.md` row 11 asks of a judge.
10. **A decision model can be wrong without hallucinating.** "Cannot hallucinate" means it cannot leave the option set; it can still pick the wrong option. "You're going to have to build code to deal with the fact that it might be completely wrong" (Vaibhav Gupta, Boundary). Every decision that gates a side effect keeps the dry-run and approval rules of `../verification/dry-run-and-approval.md` — including rule 2b, the confidence-gated approval window.

## Model tier for a decision

A decision task is its own tier **below the cheapest chat model** (`../../principles/08-model-selection.md`, change log 2026-10-01): a classifier, a moderation endpoint or a probability-returning model answers in tens of milliseconds for a fraction of a cent (Carpintero's ModernBERT at 35–40 ms; Witteveen's Jev at 70–500 ms and free output tokens — both speakers' own measurements). Reach for a reasoning model only when the decision needs the argument written down for a human, and then still extract the decision as an enumerated field after the reasoning.

## Spec template

```
Output: <<name>>                      Decision? <<yes/no>>
Options: <<a | b | c | none>>         Probability source: <<moderation endpoint | logprobs | decision model | classifier | generated 5-level>>
Threshold(s) in code: <<file:line>>   Side effect gated: <<none | send | pay | publish>> → approval rule 2b window: <<n hours>>
Eval: <<cases>> × 5 runs, per-class consistency ≥ <<n/5>>, miss rate on hard cases: <<%>>
```
