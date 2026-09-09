# skills/ — agent-loadable procedures (Agent Skills open standard)

A **skill** is a folder with a `SKILL.md` (frontmatter `name` + `description`, then instructions) that compatible agents (Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode…) load by progressive disclosure: only the description at startup, the full file when the task matches. Skills are how *procedures* from this knowledge base travel into other repos or into `~/.claude/skills/` for global use.

## What lives here vs. in practices/

- `practices/<name>/` holds the *material* (files to copy, variants, verification).
- `skills/<name>/SKILL.md` holds a *procedure an agent runs*. Some practices ship their own skill inside the practice folder (e.g. `practices/prompt-library/commit-skill/SKILL.md`); this folder holds the KB-level ones.

| Skill | Purpose | Install |
|---|---|---|
| `apply-ai-engineering-kb/` | Consult this KB, apply a practice, or ingest new material from any repo | copy to `~/.claude/skills/` (global) or `<repo>/.claude/skills/` |

## Rules

- Every practice that is procedural (a sequence an agent executes, not just files) gets a `SKILL.md` — either inside the practice or here — and is listed in `INDEX.md`.
- Skill descriptions are the trigger: write them as "use when…" sentences with the phrases Martin actually says.
- Skills are versioned like everything else: `last-reviewed` in the practice README that owns them; superseded skills are kept with a pointer.
- Skills never contain secrets, absolute paths to other people's machines, or project-specific commands — those are placeholders `<<LIKE_THIS>>`.
