# OpenSpec quickstart (state as of 2026-09-08 — verify the CLI before relying on this)

OpenSpec (Fission-AI) is the lightest SDD engine: **delta specs** describe only what a change ADDS/MODIFIES/REMOVES versus the current spec, which suits brownfield repos.

```bash
npm install -g @fission-ai/openspec
cd <repo>
openspec init            # creates openspec/ with project spec + changes/ folder; installs slash commands for supported agents
```

Flow and how it maps to this practice's manual commands:

| OpenSpec | Manual equivalent here | Notes |
|---|---|---|
| `/opsx:explore` | the ask-the-expert step of `/plan-ticket` | optional thinking out loud |
| `/opsx:propose` | `/plan-ticket` output: proposal + spec delta + design + tasks | review this before applying |
| `/opsx:apply` | `/develop-task` for each task | keep TDD and the Stop hook; OpenSpec does not enforce tests by itself |
| `/opsx:archive` | move spec to `implemented`/`archive` | merges the delta into the permanent spec |

Delta spec example:

```markdown
## ADDED Requirements
### Requirement: Two-factor authentication
The system MUST support TOTP-based 2FA.
```

Keep the user-story format from `templates/open-spec-user-story.md` inside the delta's requirements so acceptance criteria stay testable.

Known limits (per the workshop): multi-repo "Stores" feature is early beta; treat cross-repo specs as unstable. For solo/single-repo use it is fine.

When to consider the others: **Spec-Kit** if audit trails/compliance are required (heavier, sequential); **Superpowers** if planning is fine but the agent skips tests (behavioral skills, forced TDD, native worktrees, no shareable spec doc); **Spec-Boot** (LIDR) as a ready-made `docs/` context kit under any of them.
