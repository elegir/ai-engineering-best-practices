# Prompts to fill the docs/ skeletons

Use these in order. Each is a *guided investigation*: the agent reads the repo first, asks before assuming, and fills a fixed index (one-shot template) rather than inventing structure. Run with the top-tier model in plan mode where available. Review every output; the agent will be confidently wrong about at least one convention.

## 0. Before anything — ask the expert
```
You are a senior software architect joining this project. Read the repository (structure, package/dependency files, existing README and docs, tests, CI config, a sample of the code in each layer). Do not write any document yet.

List the questions you need answered to document accurately: the stack and versions, how the environment is started and tested, the architecture style and layer rules, the data model, the conventions per layer, security practices, the git workflow, and the real development process from request to production (who does what, what each phase delivers, what "done" means). Ask only what you cannot determine from the repo. Group the questions by document. Wait for my answers.
```

## 1. stack.md
```
You are an expert in this project's technologies. Fill docs/stack.md following its existing section structure exactly — do not add or remove sections. Read the dependency files and lockfiles to get exact versions. For each item write one plain-language sentence explaining what it is for in THIS project (cite the folder where it is used). Mark anything you inferred rather than found with "(inferred)". Output only the completed Markdown file.
```

## 2. development-guide.md
```
You are a developer-experience engineer. Fill docs/development-guide.md following its section structure exactly. Every command must be one you verified exists in package scripts, Makefile, compose files, or CI config; if a command is missing, write "MISSING — needs a script" instead of inventing one. Include the seed accounts you find in seed files or fixtures. In §5 describe how to run in a worktree with a distinct port and database name based on how this repo configures them. Output only the completed file.
```

## 3. backend-standards.md (the long one)
```
You are a panel of experts: an API designer, a database engineer, a security engineer, an observability engineer, and a git workflow lead. Fill docs/backend-standards.md following its section structure exactly. Be exhaustive: for every rule give WHY it exists, a GOOD example and a BAD example using real code patterns from this repository (cite file paths). Where the repo is inconsistent, state the dominant convention and list the deviations you found. Where the repo has no convention yet, propose one and mark it "PROPOSED — confirm". Do not shorten sections to save space; this document is expected to be long. Output only the completed file.
```
Repeat with the matching persona for `frontend-standards.md` (UI engineer + accessibility specialist), `testing-standards.md` (test architect), `documentation-standards.md` (technical writer).

## 4. architecture.md
```
You are a software architect. Fill docs/architecture.md following its structure. Determine the actual layers and import directions by reading imports across the codebase; produce the layer table from evidence and flag violations you found as a list at the end (do not fix them). Draw the overview and one key flow in Mermaid. Output only the completed file.
```

## 5. data-model.md
```
You are a database engineer and a technical writer. Read the schema (migrations, ORM models, or a schema dump). Fill docs/data-model.md: one section per entity in natural language — purpose, fields with meaning and validation, relationships, lifecycle, gotchas — followed by a Mermaid erDiagram. A non-technical reader must understand it; an engineer must be able to write correct queries from it. If there are more than <<15>> entities, document the core ones fully and list the rest in a table. Output only the completed file.
```

## 6. workflow.md
```
You are a delivery lead. Using my answers to the expert questions, fill docs/workflow.md following its structure. Describe the REAL process; if a phase has no owner or no gate, say so. Make the definition of done a checklist an agent can verify mechanically, and put the exact commands next to each item where possible. Output only the completed file.
```

## 7. api-spec.yml
```
You are an expert in API documentation with OpenAPI 3.1. Generate docs/api-spec.yml describing every route in this repository (read the route definitions and handlers). Include request/response schemas, auth requirements, and error responses using the error format in docs/backend-standards.md §4. Save it at docs/api-spec.yml. If the framework can generate this automatically, tell me the command instead and set it up.
```

## 8. Finish — README map and entry file
```
Update docs/README.md so its table lists every file now in docs/ with a "read it when…" phrase. Then propose (do not apply) the lines to add to CLAUDE.md/AGENTS.md pointing to docs/README.md and to the two or three documents an agent needs most often.
```
