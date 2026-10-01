---
title: "Practice — security baseline for agent-driven repos"
type: practice
status: draft
date: 2026-09-09
last-reviewed: 2026-09-30
tags: [security, secrets, dependencies, mcp, threat-model]
kind: working-style
applies-when: "always"
full-when: "acts_on_world or personal_data or regulated or multi_tenant"
principle: principles/02-harness-engineering.md
sources:
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Security baseline

## Solves

Agents with shell, file, git and MCP access can leak secrets, add unsafe dependencies, follow instructions hidden in fetched content, or run destructive commands — and none of that shows up in a unit test. This practice adds the minimum mechanical defenses on top of `practices/hooks-and-guards/` and a written trust policy for tools.

**Status: draft.** The files below are a first cut from the two sources already in the KB. Open questions before this becomes `current`: which secret scanner to standardize on (gitleaks vs trufflehog vs GitHub push protection) and where it runs; a concrete prompt-injection eval; an MCP trust policy (read-only by default, documented blast radius); a mechanical rule for adding dependencies; what a security review of an agent-written PR checks. A dedicated security source must be ingested first.

## Applies when

This practice has two parts, routed separately (decision `decisions/0004-day-one-for-blank-and-existing-repos.md` §7):

- **Core — `always`.** Any repo where an agent can run commands or reach external systems, that is every repo in practice: secret scan before commit, `.env` never committed, a dependency policy, and the dangerous-command guard from `practices/hooks-and-guards/`.
- **Full — `acts_on_world or personal_data or regulated or multi_tenant`.** The product sends, publishes or pays on its own; or stores data about people; or falls under a legal regime; or serves several customers whose data must not mix. Then the threat model, the injection fixture, the MCP trust register and the key/trace rules from the s3 scan are mandatory, not optional. `scripts/applies.py` prints `security-baseline (full)` when the line holds and `security-baseline (core)` otherwise.

## Does not apply when

- Never fully. The core applies to a static marketing site with no users; the full part is skipped there with the reason "no `acts_on_world`, `personal_data`, `regulated` or `multi_tenant`: <evidence>".

## Files in this folder

**Core (`always`):**

| File | Copy to | Purpose |
|---|---|---|
| `lefthook.security.yml` | merge into `<repo>/lefthook.yml` | Pre-commit secret scan (gitleaks) + `.env` refusal + dependency audit on push |
| `dependency-policy.md` | paste into `docs/backend-standards.md` §8 | How new dependencies are proposed, verified and approved |

**Full (`acts_on_world or personal_data or regulated or multi_tenant`):**

| File | Copy to | Purpose |
|---|---|---|
| `threat-model-agentic.md` | `<repo>/docs/threat-model.md` | Checklist of agent-specific threats and the control that covers each |
| `mcp-trust-register.md` | `<repo>/docs/mcp-trust-register.md` | One row per MCP server/tool: scope, credentials, read/write, blast radius, owner (also useful in core repos that load MCPs; mandatory here) |
| `injection-fixture.md` | `<repo>/e2e/fixtures/injection.md` + an eval | A page with hidden instructions the agent must ignore (for `practices/verification/harness-evals.md`) |

Pending files for the full part (from the s3 scan, see "Notes from later scans"): per-route and per-tenant model keys with spend caps; trace redaction rules. They land when the security module (session 14) is ingested or when a consumer needs them first.

## Adapt

- Extend `hooks-and-guards/dot-claude/hooks/block-dangerous-bash.sh` with the repo's production hosts and cloud CLIs.
- Register every MCP server in `mcp-trust-register.md`; prefer read-only variants; remove what is unused (`practices/token-savings/mcp-audit.md`).
- Install gitleaks (`winget install gitleaks` / `brew install gitleaks`) or rely on GitHub push protection if the repo is on GitHub — but keep a local check, because the agent commits locally first.

## Verify

Core:

1. Commit a fake secret (`AKIA...` pattern) → pre-commit blocks it.
2. `npm audit` / `pip-audit` / `composer audit` runs on push and fails on high severity.

Full (in addition):

3. The injection fixture eval passes: the agent reports the hidden instruction instead of executing it.
4. Every server in `.mcp.json` has a row in the trust register.
5. `docs/threat-model.md` has no row whose status is empty: each is a control in this repo or an explicit `GAP` with an owner.

## Sources

- Practitioner guide §2 (safety gates, protected configs, security linters, AI code anti-patterns) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md`.
- LIDR: Snyk MCP for vulnerability scans, security-by-design conventions — `sources/2026-09-08-lidr-workshop-harness-engineering.md`.

## Notes from later scans

- 2026-09-30 (s3): two rows to add to the trust/threat files when this practice is revised — **model API keys per route and per tenant with spend caps and anomaly alerts** (one shared key lets a noisy tenant or a runaway agent exhaust everyone's quota; a gateway is a fraud target — Twilio, OpenRouter) and **tracing decorators capture function arguments by default** (an API key in a traced call lands in the trace store — PyCon DE). Detail: `../llm-gateway/routing-policy.md` §keys, `../llm-gateway/tracing-otel.md` §rules.

## Change log

- 2026-09-09 — created (draft).
- 2026-09-30 — split into a **core** part (`applies-when: always`) and a **full** part (`full-when: acts_on_world or personal_data or regulated or multi_tenant`), per `decisions/0004-day-one-for-blank-and-existing-repos.md` §7 after the day-one debate (`sources/2026-09-30-day-one-debate.md` attack 2: the safety facts selected no practice). Files regrouped; Verify split; still draft until a real repo passes Verify.
- 2026-09-28 — merged into `main` from the 2026-09-09 local commits (they had never been pushed); added `kind` and `applies-when` per decision 0003. Still draft; the open questions above stand. Relates to the session-14 (security) scan, pending.
