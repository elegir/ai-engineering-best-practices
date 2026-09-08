---
title: "Playbook — make a repository consult this knowledge base"
type: playbook
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [adoption, claude-md, agents-md, windows]
sources:
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Adopt the knowledge base in a repository

**Goal.** After this playbook, an agent working inside `<repo>` knows the knowledge base exists, where it is, when to read it, and how to run the audit — without any file being copied.

**Assumptions.** The KB lives at `C:\Users\marti\Local Coding\ai-engineering-best-practices\` and the target repo is a sibling under `Local Coding\` (so the relative path is `../ai-engineering-best-practices/`). If the repo lives elsewhere, use the absolute path.

## Steps

1. **Open the repo's entry file.** If it has `AGENTS.md`, use that; if only `CLAUDE.md`, use that; if neither, create `AGENTS.md` and a `CLAUDE.md` containing `@AGENTS.md`.

2. **Add the pointer block** (verbatim; adjust the path if needed):

   ```markdown
   ## Shared engineering knowledge base
   Martin's AI-engineering best practices live in `../ai-engineering-best-practices/` (a sibling folder, not part of this repo).
   - Read `../ai-engineering-best-practices/AGENTS.md` before proposing changes to agent instructions, tooling, MCPs, testing strategy, specs, worktrees or workflow.
   - To evaluate this repo against those practices, run `../ai-engineering-best-practices/playbooks/audit-repo-against-kb.md` and present a plan before changing anything.
   - Do not copy files from the knowledge base into this repo; link to them.
   ```

   Keep it as prose. Do **not** use `@../ai-engineering-best-practices/AGENTS.md` by default: an import loads at every launch (costs context), triggers a one-time external-import approval, and is skipped in Cowork desktop sessions.

3. **(Optional) Make the skill global.** Copy `ai-engineering-best-practices/skills/apply-ai-engineering-kb/` to `C:\Users\marti\.claude\skills\apply-ai-engineering-kb\`. Claude Code (and other Agent-Skills clients that read that folder) will then offer the skill in every project by progressive disclosure. Do this once per machine, not per repo.

4. **(Optional, Claude Code only) Load the KB's memory files in a session** when you want the KB's `AGENTS.md` in context without editing anything:

   ```bash
   set CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
   claude --add-dir "C:\Users\marti\Local Coding\ai-engineering-best-practices"
   ```

5. **Verify.** Start a session in the repo and ask: *"Where do Martin's engineering best practices live and what should you do before changing our testing setup?"* The agent should cite the KB path and the audit playbook. If it does not, the pointer is in a file that did not load — run `/context` to see which memory files loaded.

6. **Run the audit** (`audit-repo-against-kb.md`) as the first real use.

## Notes for Windows

- No symlinks are needed anywhere in this flow. Claude Code's `@import` and plain prose pointers work without admin rights.
- Paths in Markdown use forward slashes; commands use backslashes.
