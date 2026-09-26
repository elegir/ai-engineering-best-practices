# practices/ — applicable practices with ready-to-copy files

`principles/` says *what* the current best practice is and *why*. `practices/` is the **applicable** layer: one folder per practice, each with a README that tells an agent when it applies (and when it does not), the files to copy, how to adapt them to the target repo's stack, and how to verify the result. Everything is generic — no folder here is tied to any particular project.

## How an agent uses this folder

1. The audit playbook (`../playbooks/audit-repo-against-kb.md`) produces a list of gaps in the target repo, each mapped to a practice below.
2. For each gap, the agent reads the practice's `README.md`, checks the **Applies when / Does not apply when** section against the target repo, picks the right **variant** for the stack, copies the files, adapts the marked placeholders (`<<LIKE_THIS>>`), and runs the **Verify** steps.
3. The agent reports what it copied and adapted, and records the practice name in the repo's harness changelog.

Never copy blindly. Every README has an "Adapt" section listing what must change per repo.

## The practices

| Practice | Kind | Applies when | Solves | Principle | Difficulty |
|---|---|---|---|---|---|
| `context-docs-skeleton/` | working-style | `always` | The agent infers conventions from random files because there are no standards documents | `01-context-engineering.md` | M (writing the content takes days; the skeleton takes an hour) |
| `agent-entry-file/` | working-style | `always` | `CLAUDE.md`/`AGENTS.md` is missing, bloated, or describes instead of pointing | `03-agent-instruction-files.md` | S |
| `hooks-and-guards/` | working-style | `always` | Rules exist only as prose; the agent can skip tests, edit `.env`, or silence linters | `02-harness-engineering.md`, `05-verification-loops.md` | S–M |
| `session-state/` | working-style | `long_tasks or parallel_sessions` | Every session starts from zero; long tasks lose their place; parallel agents don't know what's done | `02-harness-engineering.md` | S |
| `worktrees/` | working-style | `parallel_sessions` | Parallel sessions overwrite each other; shared DB/ports collide | `06-parallel-agents-and-worktrees.md` | S–M |
| `verification/` | working-style | `always` | No deterministic way for the agent to prove the feature works end to end | `05-verification-loops.md` | M |
| `spec-driven/` | working-style | `always` | Work goes from a one-line request straight to code; no reviewable plan | `04-spec-driven-development.md` | S–M |
| `prompt-library/` | working-style | `always` | The same context-generating prompts get reinvented; quality depends on who prompts | `01-context-engineering.md`, `04-spec-driven-development.md` | S |
| `token-savings/` | working-style | `always` | Weekly token limits hit; tool output and repo exploration burn context | `07-token-economy.md` | S |
| `agent-patterns/` | capability | `tools or multi_agent` | An LLM feature takes actions but nobody decided workflow vs agent; tools are one-per-endpoint and undocumented; the team tunes prompts instead of reading what the model saw; every integration is an MCP loaded at startup | `21-agent-design-and-tools.md` (draft) | S–M |

**Which of these apply to a given repo** is decided by `../playbooks/which-practices-apply.md` from the facts in `facts.md` (the `Applies when` column above uses only those words; `always` means every repo an agent works in). Recommended order for a repo with nothing: `verification` (can the agent even run tests?) → `context-docs-skeleton` → `agent-entry-file` → `hooks-and-guards` → `session-state` → `prompt-library` → `spec-driven` → `worktrees` → `token-savings`. The audit playbook applies this order.

## Format of a practice (see `_template/`)

```
practices/<name>/
├── README.md        # Solves / Applies when / Does not apply when / Files / Adapt / Verify / Sources
└── <files>          # ready to copy; placeholders marked <<LIKE_THIS>>; variants in variants/ or per-stack subfolders
```

## Adding or updating a practice

A practice changes when a source (`../sources/`) changes the recommendation. Follow `../playbooks/ingest-new-source.md`; update the practice's README "Sources" and "Change log", bump `last-reviewed` in its frontmatter, and add a line to `../INDEX.md`. Practices are living documents like principles: never delete, supersede.
