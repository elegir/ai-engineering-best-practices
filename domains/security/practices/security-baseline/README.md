---
title: "Practice — security baseline for agent-driven repos"
type: practice
status: draft
date: 2026-09-09
last-reviewed: 2026-09-09
domains: [security]
tags: [security, secrets, dependencies, mcp, threat-model]
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

**Status: draft.** The files below are a first cut from the two sources already in the KB; the open questions in `domains/security/README.md` must be answered (and a dedicated security source ingested) before this becomes `current`.

## Applies when

- Any repo where an agent can run commands or reach external systems (that is, every repo in practice).

## Does not apply when

- Never fully. Scale down: at minimum secret scanning + protected `.env`.

## Files in this folder

| File | Copy to | Purpose |
|---|---|---|
| `lefthook.security.yml` | merge into `<repo>/lefthook.yml` | Pre-commit secret scan (gitleaks) + dependency audit on push |
| `mcp-trust-register.md` | `<repo>/docs/mcp-trust-register.md` | One row per MCP server/tool: scope, credentials, read/write, blast radius, owner |
| `threat-model-agentic.md` | `<repo>/docs/threat-model.md` | Checklist of agent-specific threats and the control that covers each |
| `dependency-policy.md` | paste into `docs/backend-standards.md` §8 | How new dependencies are proposed, verified and approved |
| `injection-fixture.md` | `<repo>/e2e/fixtures/injection.md` + an eval | A page with hidden instructions the agent must ignore (for `practices/verification/harness-evals.md`) |

## Adapt

- Extend `hooks-and-guards/dot-claude/hooks/block-dangerous-bash.sh` with the repo's production hosts and cloud CLIs.
- Register every MCP server in `mcp-trust-register.md`; prefer read-only variants; remove what is unused (`practices/token-savings/mcp-audit.md`).
- Install gitleaks (`winget install gitleaks` / `brew install gitleaks`) or rely on GitHub push protection if the repo is on GitHub — but keep a local check, because the agent commits locally first.

## Verify

1. Commit a fake secret (`AKIA...` pattern) → pre-commit blocks it.
2. `npm audit` / `pip-audit` / `composer audit` runs on push and fails on high severity.
3. The injection fixture eval passes: the agent reports the hidden instruction instead of executing it.
4. Every server in `.mcp.json` has a row in the trust register.

## Sources

- Practitioner guide §2 (safety gates, protected configs, security linters, AI code anti-patterns) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md`.
- LIDR: Snyk MCP for vulnerability scans, security-by-design conventions — `sources/2026-09-08-lidr-workshop-harness-engineering.md`.

## Change log

- 2026-09-09 — created (draft).
