# Fallback approval — "available is not approved"

One block per fallback target, kept in `<repo>/docs/llm-gateway.md`. A fallback nobody approved is chosen during the incident, under pressure, against data you did not check — that is how a different model becomes a different product (API World, 2026-09; ManyChat; Twilio; TensorZero — `../../sources/2026-09-30-s03-wrappers-digest.md` §3.2). Principle: `../../principles/12-llm-gateway-layer.md` §3.2.

```
Route:               <<chat>>
Primary:             <<azure/deployment-reserved — model X>>
Fallback target:     <<provider-b/model X>>                       Kind: [ ] same model, other capacity   [ ] different model
Trigger:             <<429 / 5xx / timeout before first token>>   Automatic: [ ] yes (same model)  [ ] only after human switch (different model)

Checks (all required for a DIFFERENT model; the first two for the same model elsewhere):
[ ] Data sensitivity — the target's data policy (retention, training, region) is equal or stricter than the primary's; personal_data/regulated facts considered
[ ] Capacity — quota and rate limits at PEAK primary volume verified; load-tested on <<date>>
[ ] Capability — tool-calling schema, JSON mode, max tokens, stop reasons, context window compared; differences handled in the normalisation layer
[ ] Consequence — what this route does with the answer (acts_on_world? irreversible?) and whether a quality drop is acceptable for the outage window
[ ] Evals — the route's eval set run against the target on <<date>>: <<result vs primary>>; the preserve-list / schema checks pass
[ ] Cost — price per class at the target; spend cap adjusted
[ ] Prompt — same prompt file version works, or a target-specific variant exists and is versioned

Approved by: <<name>>   Date: <<>>   Re-check: <<quarterly / on model generation change>>
```

Rules: the same-model-elsewhere block can be approved once per provider pair; a different-model block is per route; "we'll pick something if it goes down" is not a fallback, it is an outage with extra steps.
