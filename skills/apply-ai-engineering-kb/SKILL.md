---
name: apply-ai-engineering-kb
description: Consult Martin's local AI-engineering knowledge base (harness engineering, context engineering, agent instruction files, spec-driven development, verification loops, worktrees, token economy, model selection) and apply it to the current repository. Use when asked about best practices for working with coding agents, when auditing or improving a repo's CLAUDE.md/AGENTS.md, hooks, tests, specs or workflow, or when Martin says "apply the knowledge base", "check this against the KB", or mentions the harness workshop.
---

# Apply the AI Engineering Knowledge Base

The knowledge base is a folder of Markdown, not a library. Default location on Martin's machine: `C:\Users\marti\Local Coding\ai-engineering-best-practices\` (from a sibling repo: `../ai-engineering-best-practices/`). If it is not there, ask Martin for the path; do not guess.

## Procedure

1. Read `<kb>/AGENTS.md` (short). Then `<kb>/INDEX.md` to see what exists.
2. Identify the question type:
   - **Consult** ("what's the best practice for X?") → read the matching `principles/NN-*.md`; answer from it; cite the file; if the principle's `status` is not `current`, say so. Go to `sources/` only if the reasoning or original wording is needed.
   - **Apply/audit** ("check this repo", "improve our setup") → follow `<kb>/playbooks/audit-repo-against-kb.md` literally: inventory (read-only) → score → findings → plan → **stop and wait for approval**. Then implement one item per prompt by copying from `<kb>/practices/<name>/` (read its README: Applies when / Adapt / Verify; pick the stack variant; replace every `<<PLACEHOLDER>>`; run Verify).
   - **Install a specific practice** ("add hooks", "set up worktrees", "give me the docs skeleton") → go straight to `<kb>/practices/<name>/README.md` and follow it.
   - **Ingest** ("add this workshop/article/lesson to the KB") → follow `<kb>/playbooks/ingest-new-source.md`.
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
| prompts (meta, ask-expert, audit, lesson→rule, commit) | — | `practices/prompt-library/` |
| how the KB itself is designed | `principles/09-knowledge-base-design.md` | `practices/README.md` |
