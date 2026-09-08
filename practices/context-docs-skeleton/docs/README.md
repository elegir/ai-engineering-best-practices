# docs/ — technical context for humans and agents

This folder is the single source of truth for how this project is built. Agents read these files instead of inferring conventions from code. **If you change behavior, update the matching document in the same change** (see `documentation-standards.md` and the definition of done in `workflow.md`).

| Document | Read it when… |
|---|---|
| `stack.md` | choosing a library, checking a version, wondering what a dependency is for |
| `development-guide.md` | setting up, running anything (app, DB, seeds, tests, lint), working in a worktree |
| `architecture.md` | adding a module, deciding where a file goes, importing across layers |
| `data-model.md` | touching the database, writing a query, adding a field |
| `backend-standards.md` | writing any server-side code, API endpoint, migration, log line, error |
| `frontend-standards.md` | writing any UI code |
| `testing-standards.md` | writing or changing tests; before every commit |
| `documentation-standards.md` | finishing a task (what to update), writing comments or docs |
| `workflow.md` | starting a task (phases, definition of done), choosing a model, opening a PR |
| `api-spec.yml` | (generated) the API contract — regenerate, don't hand-edit |
| `generated/` | schema dumps and other machine-produced references |
