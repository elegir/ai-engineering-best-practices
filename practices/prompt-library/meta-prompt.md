---
description: Expand a one-line request into a precise, structured prompt (do not execute it). Usage: /meta <request>
---

You are an expert in prompt engineering for coding agents working in THIS repository.

Given the request below, rewrite it as a complete prompt using this structure, filling each section with specifics you find in the repo (stack from `docs/stack.md`, conventions from `docs/*-standards.md`, the files involved, the tests that exist). Stick strictly to the requested objective; do not add scope.

# ROLE
# CONTEXT (stack, architecture, the exact files and functions involved, current behavior)
# OBJECTIVE
# SPECIFIC REQUIREMENTS (numbered; include success cases, error cases, edge cases where relevant)
# CONSTRAINTS (standards to follow, files not to touch, out of scope)
# RESPONSE FORMAT (files to produce, tests, report)
# QUALITY STANDARDS (coverage, lint, docs, verification commands)

Output only the rewritten prompt, ready to run. Do not perform the task.

Request: $ARGUMENTS
