# practices/ — applicable practices with ready-to-copy files

`principles/` says *what* the current best practice is and *why*. `practices/` is the **applicable** layer: one folder per practice, each with a README that tells an agent when it applies (and when it does not), the files to copy, how to adapt them to the target repo's stack, and how to verify the result. Everything is generic — no folder here is tied to any particular project.

## How an agent uses this folder

1. `../ROUTER.md` (generated, ≤ 2 KB) is the short form of the table below. `../scripts/applies.py --explain <facts…>` turns a repo's confirmed facts into the ordered list (`../playbooks/which-practices-apply.md` for an existing repo, ../`playbooks/bootstrap-new-repo.md` for a blank one).
2. The audit playbook (`../playbooks/audit-repo-against-kb.md`) produces a list of gaps in the target repo among the practices that apply.
3. For each gap, the agent implements the practice with `prompt-library/implement-practice.md`: the README's **Verify** is the contract (stack-neutral assertions), **Stack-sensitive points** and `stack-notes/<stack>.md` say where this stack's mechanism differs, **Reference implementation** is the Python example, **Adapt** lists the placeholders (`<<LIKE_THIS>>`). Every `when:` says at which stage of the product's life the practice is installed (day-0 | first-user | at-scale); `reference-status` says whether anyone has passed its Verify yet (`adoptions.md`).
4. The agent ends with a field report (`../templates/field-report.md`); the KB turns it into a variant and an adoptions row (`../playbooks/adopt-variant.md`).

Never copy blindly. Every README has an "Adapt" section listing what must change per repo.

## The practices

| Practice | Kind | Applies when | Solves | Principle | Difficulty |
|---|---|---|---|---|---|
| `verification/` | working-style | `always` | No deterministic way for the agent to prove the feature works end to end; when `acts_on_world`, no dry-run mode so senders/publishers/payments cannot be tested without doing the thing | `05-verification-loops.md` | M |
| `context-docs-skeleton/` | working-style | `always` | The agent infers conventions from random files because there are no standards documents | `01-context-engineering.md` | M (writing the content takes days; the skeleton takes an hour) |
| `agent-entry-file/` | working-style | `always` | `CLAUDE.md`/`AGENTS.md` is missing, bloated, or describes instead of pointing | `03-agent-instruction-files.md` | S |
| `hooks-and-guards/` | working-style | `always` | Rules exist only as prose; the agent can skip tests, edit `.env`, or silence linters | `02-harness-engineering.md`, `05-verification-loops.md` | S–M |
| `security-baseline/` | working-style | `always` (core); full part when `acts_on_world or personal_data or regulated or multi_tenant` | Agent can leak secrets, add unsafe dependencies, follow injected instructions, or reach prod through over-broad tools; products that act on the world, hold personal data, are regulated or multi-tenant also need the threat model, injection fixture and trust register | `02-harness-engineering.md`, `05-verification-loops.md` | S (core) – M (full); draft |
| `session-state/` | working-style | `long_tasks or parallel_sessions` | Every session starts from zero; long tasks lose their place; parallel agents don't know what's done | `02-harness-engineering.md` | S |
| `prompt-library/` | working-style | `always` | The same context-generating prompts get reinvented; quality depends on who prompts | `01-context-engineering.md`, `04-spec-driven-development.md` | S |
| `spec-driven/` | working-style | `always` | Work goes from a one-line request straight to code; no reviewable plan | `04-spec-driven-development.md` | S–M |
| `worktrees/` | working-style | `parallel_sessions` | Parallel sessions overwrite each other; shared DB/ports collide | `06-parallel-agents-and-worktrees.md` | S–M |
| `token-savings/` | working-style | `always` | Weekly token limits hit; tool output and repo exploration burn context | `07-token-economy.md` | S |
| `llm-api-calls/` | capability | `llm_calls` | Vendor SDK calls scattered through handlers; prompts as unversioned string literals with variable content first (cache never hits); the model asked for facts/counts/arithmetic it cannot do; an LLM's opinion guarding an irreversible action; evals reporting a mean while one scenario in ten fails | `10-llm-api-fundamentals.md` (draft) | S–M |
| `context-management/` | capability | `multi_turn or retrieval` | Answers degrade after many turns; the transcript is re-sent whole and the bill grows quadratically; history is summarised by an unconstrained prompt; tool results are dumped or lost; sub-agents get the whole history or return "see above"; a vector pipeline for a corpus that fits, or a changing corpus stuffed into the window; no trace, no long-session eval | `11-runtime-context-management.md` (draft) | M |
| `llm-gateway/` | capability | `llm_calls and production` | A provider's 429s or a slow reasoning model become an outage; retries stacked in two layers; a fallback model picked during the incident; one shared key for every route; model ids in twenty files; streams switched mid-way or parsed with regex; traces missing or leaking keys; a semantic cache serving another user's answer | `12-llm-gateway-layer.md` (draft) | M |
| `agent-patterns/` | capability | `tools or multi_agent or exposes_tools` | An LLM feature takes actions but nobody decided workflow vs agent; tools are one-per-endpoint and undocumented; the team tunes prompts instead of reading what the model saw; every integration is an MCP loaded at startup | `21-agent-design-and-tools.md` (draft) | S–M |

**Which of these apply to a given repo** is decided from the facts in `facts.md` — inferred with evidence on an existing repo (`../playbooks/which-practices-apply.md`), planned from intent on a blank one (`../playbooks/bootstrap-new-repo.md`) — and evaluated by `../scripts/applies.py`, which is the authority for the list and its order (`facts.md` §Ordering; decision 0004). The `Applies when` column uses only the vocabulary words; `always` means every repo an agent works in; "full part when …" after it names the facts (`full-when` in the practice's frontmatter) that attach a practice's conditional files. The audit playbook applies the script's order.

## Format of a practice (see `_template/`)

```
practices/<name>/
├── README.md        # Solves / Applies when / Does not apply when / Files / Reference implementation / Stack-sensitive points / Adapt / Verify / Sources / Change log (schema enforced by kb-check)
├── <files>          # the reference (Python) and the policy documents; placeholders marked <<LIKE_THIS>>
├── stack-notes/     # ≤ 15 lines per stack, no code, no version pins (decision 0005 §5)
└── variants/<stack>/ # field-tested copies born from a real repo's field report (decision 0005 §7)
```

## Adding or updating a practice

A practice changes when a source (`../sources/`) changes the recommendation. Follow `../playbooks/ingest-new-source.md`; update the practice's README "Sources" and "Change log", bump `last-reviewed` in its frontmatter, and add a line to `../INDEX.md`. Practices are living documents like principles: never delete, supersede.
