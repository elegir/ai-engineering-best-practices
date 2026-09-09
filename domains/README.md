# domains/ — vertical-specific knowledge

`principles/` and `practices/` are agnostic: they apply to any repo. Some knowledge only makes sense inside a vertical — what a *spec* means for product management, what *verification* means for a payments system, what *the harness* must block in a WordPress fleet. That knowledge lives here, one folder per vertical, and it **extends** the agnostic layer instead of duplicating it.

## Rules

- A domain folder never restates a principle or practice; it says *how it applies here*, *what is different here*, and *what extra practice this vertical needs*. Link, don't copy.
- Same frontmatter and gate as everything else (`CONVENTIONS.md`, `playbooks/evaluate-new-material.md`). Domain entries carry `domains: [<vertical>]` in frontmatter; agnostic files carry `domains: [all]` or omit the field.
- A domain starts as `status: draft` with a README that lists the questions it must answer; it becomes `current` when at least one dated source backs it.
- Vertical-specific *practices* live under `domains/<vertical>/practices/<name>/` with the same structure as the agnostic ones (README with Solves / Applies when / Files / Adapt / Verify / Sources).

## Verticals

| Folder | Status | Scope | Seeded from |
|---|---|---|---|
| `security/` | draft | Security of agent-driven development: secrets, dependency and code scanning, agent-specific threats (prompt injection through tool output, MCP trust, permission scopes), secure-by-design conventions | LIDR (Snyk/Sentry MCPs, security-by-design list); practitioner guide (PreToolUse safety gates, protected configs) |
| `product/` | draft | Product-management side of spec-driven work: PRDs and user stories that agents can execute, discovery with agents, definition of done from the product side, functional documentation for non-technical readers | LIDR (workflow deliverables, Confluence-style functional docs, model table for PRD/user stories) |
| `web-wordpress/` | planned | WordPress sites and fleets: plugin/theme conventions, WP-CLI as the sensor, staging-first verification, multi-site isolation | — |
| `data-pipelines/` | planned | ETL, scrapers, senders, schedulers: dry-run modes as sensors, idempotency, seeded batches, observability | — |
| `gtm-sales-automation/` | planned | Outbound/GTM systems (sequences, enrichment, deliverability): compliance gates, sandbox senders, evals on generated copy | — |
| `fintech-payments/` | planned | Payments and regulated flows: audit trails, reversible migrations, PCI-style secret handling, spec-kit-grade traceability | — |
| `mobile/` | planned | Mobile apps: simulator-based verification, store-release gates | — |

To add a vertical: copy `_template/`, fill the README questions, add a row here and a line in `../INDEX.md`, publish.
