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
when: day-0   # day-0 | first-user | at-scale — when in a product's life this practice is installed (decision 0004 §5)
full-when-stage: day-0   # the threat model and trust register are cheapest on day zero
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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
| `stack-notes/php-laravel.md` | (read) | Secrets paths, `composer audit` semantics, per-tenant keys, `tinker` as a destructive command |

Pending files for the full part (from the s3 scan, see "Notes from later scans"): per-route and per-tenant model keys with spend caps; trace redaction rules. They land when the security module (session 14) is ingested or when a consumer needs them first.

## Reference implementation

`lefthook.security.yml` (core gates) and the three documents of the full part. No code file: the secret scanner (gitleaks) and the audit tools are external and the same on every stack.

## Stack-sensitive points

- **Dependency audit semantics differ**: `npm audit --audit-level=high` and `pip-audit` fail on a threshold; `composer audit` fails on **any** advisory by default; since Composer 2.8 (2024-10) `--ignore-severity=low --ignore-severity=medium` approximates a high/critical threshold — state which in the policy.
- **Where secrets live**: `.env` in Python/Node/Laravel; `wp-config.php` on WordPress (protect it like `.env`); Laravel `config:cache` copies them into `bootstrap/cache/` (protect that path too).
- **Multi-tenant keys** (assertion 8) assume the product owns the model calls; a WordPress plugin calling a vendor API uses the site owner's key and the assertion reduces to "one key per site, in the options table only if encrypted".

## Adapt

- Add the repo's production hosts and cloud CLIs to `deny_commands` in `hooks-and-guards/dot-claude/hooks.json`.
- Register every MCP server in `mcp-trust-register.md`; prefer read-only variants; remove what is unused (`practices/token-savings/mcp-audit.md`).
- Install gitleaks (`winget install gitleaks` / `brew install gitleaks`) or rely on GitHub push protection if the repo is on GitHub — but keep a local check, because the agent commits locally first.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

Core (`always`):

1. A staged commit containing a secret-shaped string is refused before it is created, with a message naming the pattern — observer: script — negative: the commit lands
2. A staged `.env`-family file is refused — observer: script — negative: `.env` in the commit
3. The dependency audit runs before push and fails on a vulnerability the audit tool classifies as high or critical; where the tool has no severity threshold, the policy document states what is checked instead — observer: script — negative: a known high-severity dependency pushed without a failure — framework: bends
4. A new dependency is added only through the steps of `dependency-policy.md` (reason, maintenance check, pinned by lockfile) — observer: Martin — negative: a dependency in the lockfile with no entry in the policy's log

Full (`acts_on_world or personal_data or regulated or multi_tenant`, in addition):

5. The injection fixture eval passes: given content with hidden instructions, the agent reports them and does not execute them — observer: agent — negative: the agent follows an instruction found in fetched content
6. Every MCP server or external tool the agent can reach has a row in the trust register (scope, credentials, read/write, blast radius, owner) — observer: Martin — negative: a server in the agent's configuration with no row
7. `docs/threat-model.md` has no row with an empty status: each threat has a control in this repo or an explicit `GAP` with an owner — observer: Martin — negative: an empty cell
8. When `llm_calls`: model API keys are per route and, when `multi_tenant`, per tenant, with a spend cap and an alert — observer: Martin — negative: one key shared by every route and tenant
9. Traces and logs contain no API key and no raw personal data — observer: script — negative: a key or an email address found in the trace store

**Example commands (Python / Node / PHP):** stage `AKIA` + sixteen characters → `gitleaks protect --staged` blocks; `pip-audit` / `npm audit --audit-level=high` / `composer audit`; the injection eval in `../verification/harness-evals.md`.

## Sources

- Practitioner guide §2 (safety gates, protected configs, security linters, AI code anti-patterns) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md`.
- LIDR: Snyk MCP for vulnerability scans, security-by-design conventions — `sources/2026-09-08-lidr-workshop-harness-engineering.md`.

## Notes from later scans

- 2026-09-30 (s3): two rows to add to the trust/threat files when this practice is revised — **model API keys per route and per tenant with spend caps and anomaly alerts** (one shared key lets a noisy tenant or a runaway agent exhaust everyone's quota; a gateway is a fraud target — Twilio, OpenRouter) and **tracing decorators capture function arguments by default** (an API key in a traced call lands in the trace store — PyCon DE). Detail: `../llm-gateway/routing-policy.md` §keys, `../llm-gateway/tracing-otel.md` §rules.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-09 — created (draft).
- 2026-09-30 — split into a **core** part (`applies-when: always`) and a **full** part (`full-when: acts_on_world or personal_data or regulated or multi_tenant`), per `decisions/0004-day-one-for-blank-and-existing-repos.md` §7 after the day-one debate (`sources/2026-09-30-day-one-debate.md` attack 2: the safety facts selected no practice). Files regrouped; Verify split; still draft until a real repo passes Verify.
- 2026-09-28 — merged into `main` from the 2026-09-09 local commits (they had never been pushed); added `kind` and `applies-when` per decision 0003. Still draft; the open questions above stand. Relates to the session-14 (security) scan, pending.
