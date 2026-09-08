# README / document by fixed index (one-shot template prompt)

You are an expert software architect. Prepare `<<docs/README.md>>` for this repository.

Rules: the output is Markdown, properly formatted and indented, and follows **exactly** this index — fill every section, add none, remove none. Every command you write must exist in the repo (package scripts, Makefile, compose, CI); if one is missing, write `MISSING — needs a script`. Mark inferred facts with "(inferred)". Link the detailed documents instead of repeating them.

```
# <<Project name>>
## 1. What this is (2 paragraphs)
## 2. Architecture (overview + link docs/architecture.md)
## 3. Technologies (table + link docs/stack.md)
## 4. Project structure (tree, one line per folder)
## 5. Setup and run (from zero; link docs/development-guide.md)
## 6. Testing (commands per layer; link docs/testing-standards.md)
## 7. Data model (quick view + link docs/data-model.md)
## 8. API (quick view + link docs/api-spec.yml)
## 9. How to contribute (workflow, branches, PRs; link docs/workflow.md)
## 10. Where to ask (owner, channel)
```

Output only the completed document.
