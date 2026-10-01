---
name: apply-ai-engineering-kb
description: Consult Martin's local AI-engineering knowledge base (harness engineering, context engineering, agent instruction files, spec-driven development, verification loops, worktrees, token economy, model selection) and apply it to the current repository. Use when asked about best practices for working with coding agents, when auditing or improving a repo's CLAUDE.md/AGENTS.md, hooks, tests, specs or workflow, or when Martin says "apply the knowledge base", "check this against the KB", or mentions the harness workshop.
---

# Apply the AI Engineering Knowledge Base

The knowledge base is a folder of Markdown, not a library. Default location on Martin's machine: `C:\Users\marti\Local Coding\ai-engineering-best-practices\` (from a sibling repo: `../ai-engineering-best-practices/`). If it is not there, ask Martin for the path; do not guess.

## Procedure

0. Run `bash <kb>/scripts/kb-sync.sh --pull` (the guide must be current; stop only if it reports `ahead` or uncommitted changes).
1. Read `<kb>/ROUTER.md` (under 2 KB, generated): every routed practice with its `applies-when`, `when` and reference status. Read `<kb>/AGENTS.md` only if the task is about the KB itself.
2. Identify the question type:
   - **Which practices apply here** (day one of a repo, or before an audit) → existing repo: `<kb>/playbooks/which-practices-apply.md` (infer the facts with evidence, confirm in one screen, then `python3 <kb>/scripts/applies.py --explain <facts…>` is the list and the order); blank repo: <kb>/`playbooks/bootstrap-new-repo.md` (plan the facts from intent; planned facts attach only day-0 practices).
   - **Consult** ("what's the best practice for X?") → read the matching `principles/NN-*.md`; answer from it; cite the file; if the principle's `status` is not `current`, say so. Go to `sources/` only if the reasoning or original wording is needed.
   - **Apply/audit** ("check this repo", "improve our setup") → after the selection above, follow `<kb>/playbooks/audit-repo-against-kb.md` literally on the practices that apply: inventory (read-only) → score → findings → plan → **stop and wait for approval**.
   - **Implement one practice** ("add hooks", "set up worktrees", "install the LLM client") → `<kb>/practices/prompt-library/implement-practice.md` with the practice name: its `## Verify` is the contract, `## Stack-sensitive points` and `stack-notes/<stack>.md` say where this stack differs, `## Reference implementation` is an example (Python), not a port to copy; end with the field report (`<kb>/templates/field-report.md`), which is how the KB learns.
   - **Ingest** ("add this workshop/article/lesson to the KB") → follow `<kb>/playbooks/ingest-new-source.md`; a field report from a repo → `<kb>/playbooks/adopt-variant.md`.
3. Respect the KB's rules: English inside the KB; long-form explicit prose; date everything; cite sources; never edit an existing `sources/` entry; never delete — supersede; update `INDEX.md` in the same change.
4. When talking to Martin: Spanish, plain language, one step at a time, explain what a step does before proposing to run it, and prefer mechanical fixes (hooks, linters, tests) to more prose.

## Quick topic map

| Need | Why | How (copyable) |
|---|---|---|
| vocabulary | `principles/00-glossary.md` | — |
| project context docs | `principles/01-context-engineering.md` | `practices/context-docs-skeleton/` |
| harness (tools, env, state, feedback) | `principles/02-harness-engineering.md` | `practices/hooks-and-guards/`, `practices/session-state/` |
| CLAUDE.md / AGENTS.md | `principles/03-agent-instruction-files.md` | `practices/agent-entry-file/` |
| specs, OpenSpec/Spec-Kit/Superpowers/Spec-Boot | `principles/04-spec-driven-development.md` | `practices/spec-driven/`, `templates/open-spec-user-story.md` |
| tests, hooks, e2e, definition of done | `principles/05-verification-loops.md` | `practices/verification/` |
| worktrees, parallel agents | `principles/06-parallel-agents-and-worktrees.md` | `practices/worktrees/` |
| tokens | `principles/07-token-economy.md` | `practices/token-savings/` |
| models | `principles/08-model-selection.md` | workflow.md §3 in the docs skeleton |
| prompts (meta, ask-expert, audit, lesson→rule, commit, implement-practice) | — | `practices/prompt-library/` |
| LLM calls, context management, gateway, agent patterns (capability practices; routed by facts) | `principles/10-llm-api-fundamentals.md`, `principles/11-runtime-context-management.md`, `principles/12-llm-gateway-layer.md`, `principles/21-agent-design-and-tools.md` (drafts) | `practices/llm-api-calls/`, `practices/context-management/`, `practices/llm-gateway/`, `practices/agent-patterns/` |
| how the KB itself is designed | `principles/09-knowledge-base-design.md` | `practices/README.md` |
