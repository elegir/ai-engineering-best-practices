@AGENTS.md

## Claude Code specifics

- This folder is documentation only. Do not run `/init`; do not create build tooling.
- When asked to ingest material, use plan mode first, show the proposed file list, then write.
- To ship: `/publish <slug> <message>` (runs `scripts/kb-check.sh` + `scripts/kb-publish.sh`). Do not run `git commit` on `main` directly.
