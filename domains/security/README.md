---
title: "Domain — security of agent-driven development"
type: domain
status: draft
date: 2026-09-09
last-reviewed: 2026-09-09
domains: [security]
tags: [security, secrets, dependencies, prompt-injection, mcp, permissions]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Security of agent-driven development

## What is different here

An agent is a program that reads untrusted text (web pages, tool output, issue comments, files it did not write) and then *acts* with real permissions (shell, files, git, MCP servers with database or browser access). That combination creates threats classic AppSec does not cover: instructions hidden in a fetched page that the agent follows; a leaked `.env` because the agent "helpfully" read and echoed it; a dependency added because a hallucinated package name resolved to a typosquat; a destructive command run because it was the fastest way to make a test pass. The agnostic practices already contain the mechanical defenses (protected files, blocked commands, permission allow-lists, tests as sensors); this domain organizes them as a security posture and adds what is missing.

## How the agnostic layer applies

| Agnostic practice | In security terms | Extra constraint |
|---|---|---|
| `practices/hooks-and-guards/` | PreToolUse gates are the agent's firewall: `.env*`, lock files, CI, linter configs, destructive commands, `--no-verify` | Add production hosts, cloud CLIs (`aws`, `gcloud`, `wp` against prod) and secret stores to the deny list |
| `practices/verification/` | Security checks are sensors too: dependency scan, secret scan, SAST run before "done" | They run in the Stop hook / pre-commit, not only in CI |
| `practices/context-docs-skeleton/` (`backend-standards.md` §8) | Secure-by-design conventions written down so the agent applies them: parameterized queries, input validation at the edge, output encoding, CORS, CSRF, rate limits, no PII in logs | Every rule has a GOOD/BAD example from the repo |
| `practices/agent-entry-file/` | Prohibitions must name their enforcement; "never commit secrets" without a hook is a wish | `permissions.allow` lists only known-safe commands |
| `practices/token-savings/mcp-audit.md` | Fewer tools = smaller attack surface; every MCP server is a trust decision (what can it read/write, on whose behalf) | Remove unused servers; prefer read-only variants (as Martin does with Postgres MCPs) |
| `practices/spec-driven/constitution.md` | Security rules are constitutional: a spec cannot override them | |

## Vertical-specific practices

- `domains/security/practices/security-baseline/` — the minimum set: secret scanning (pre-commit), dependency scanning, protected paths, permission scopes, a threat-model checklist for agent workflows, and an incident note template. **Status: draft** — files to be added after the first dedicated source is ingested.

## Open questions this domain must answer before becoming `current`

- Which secret scanner to standardize on for Windows/Git Bash + Linux CI (gitleaks vs trufflehog vs GitHub push protection) and where it runs.
- A concrete prompt-injection test the harness evals can run (a fixture page with hidden instructions; the agent must not follow them).
- MCP trust policy: how to document each server's scope, credentials and blast radius; read-only by default.
- Supply chain: rule for adding dependencies (agent proposes, human approves; verify package provenance) and how to enforce it mechanically.
- What "security review" means for an agent-written PR: checklist and which items are automatable.

## Sources

- LIDR workshop: Snyk and Sentry MCPs; security-by-design list (XSS, CORS, SQL injection, secrets not in `.env` committed) — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.9 (videos C, D).
- Practitioner guide: PreToolUse safety gates, protected configs, security linters mandatory (gosec, Ruff `S`, eslint-plugin-security), AI-generated code anti-patterns — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.

## Change log

- 2026-09-09 — created (draft) at Martin's request to give the KB an explicit cybersecurity vertical.
