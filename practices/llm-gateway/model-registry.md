# Model registry and the daily availability check

Copy to `<repo>/docs/models.md`; the check is a small scheduled job. The failure this prevents (API World, 2026-09): a model id hardcoded in ~22 places, a retirement the vendor had announced months earlier, no alert, a broken production button — "information is not control". Principle: `../../principles/12-llm-gateway-layer.md` §3.2.

## The registry (single source of truth)

| Route | Model id (exact provider string) | Provider | Class (chat / extract / reason / embed) | Introduced | Vendor deprecation date (if announced) | Replacement candidate | Last evaluated | Owner |
|---|---|---|---|---|---|---|---|---|
| chat | <<...>> | <<>> | chat | <<date>> | <<none announced>> | <<>> | <<date>> | <<>> |

Rules: no model id appears anywhere else in the repo (`grep -rn "<id>" src/ config/` finds the registry and the gateway config only); routes reference the registry; the prompt file header records the model it was tuned on (`../llm-api-calls/system-prompt-template.md`).

## The daily check (≈20 lines; run where your other daily jobs run)

1. For each provider in the registry, call its *list models* endpoint.
2. For each registered id: present → ok; missing → **alert** ("model <id> used by route <r> is no longer listed by <provider>"); if the provider publishes deprecation metadata, alert <<60>> days before the date.
3. If the check itself fails (network, auth) → **alert** too: a silent check is the same as no check.
4. Write the result to the registry's "last checked" line so a human can see the check ran.

## When a model is retired or replaced

1. Add the replacement to the registry as a candidate; run the route's evals against it (`fallback-approval.md` different-model block).
2. Switch the route in the gateway config, one route at a time; keep the old id in the registry marked *retired <<date>>* for the audit trail.
3. Re-audit older systems and side projects: the one that breaks is the one nobody migrated.
4. Quarterly, re-evaluate every route's model regardless of retirements: the market swings (frontier launch → surge → invoice → cheaper option months later — OpenRouter, 2026-09).
