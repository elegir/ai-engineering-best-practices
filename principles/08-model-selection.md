---
title: "Model selection — match reasoning depth to the task, not brand to habit"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-24
tags: [models, opus, sonnet, codex, gemini, routing]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Model selection

## 1. The question this answers

Which model (or tier) should be used for which phase of development, given that the vendors' top models are roughly at parity and the real variable is reasoning depth versus cost?

## 2. Short answer

Use the **top tier (Opus / Gemini HIGH / Codex) to plan**: technical design, architecture, specs, complex or cross-module implementation, deep debugging and security, DevOps/terminal work. Use the **mid tier (Sonnet / Gemini LOW-MED) to execute**: discovery, PRDs and user stories, routine implementation, shallow review, production maintenance. LIDR's rule for SDD: *Opus writes the exhaustive spec and atomized tasks; Sonnet executes them.* Re-check this table whenever a vendor ships a new generation — model names rot fastest of anything in this KB.

## 3. Long explanation

The workshop's table (2026-09-08) is reproduced in the source entry. The durable pattern behind it:

- **Tier, not brand.** Anthropic separates tiers by name (Sonnet vs Opus); Google by thinking level inside one model (LOW ≈ Sonnet, HIGH ≈ Opus); OpenAI's Codex is a single "high" model by design. Choose the *level of reasoning* the phase needs.
- **Plan high, execute mid.** Planning errors are expensive and compound; execution of an atomized task is cheap to verify and redo. Spend reasoning where mistakes are costly.
- **Terminal/DevOps leans Codex** on the cited Terminal-Bench numbers (77.3% vs 65.4% Opus, as cited by LIDR; verify version).
- **Dissenting data point:** Boris Cherny uses the top model with thinking *for everything*, arguing it needs less steering and is usually faster overall. The two positions reconcile as: if you have strong context and a good plan, the mid tier executes fine; if you are steering by hand, the top tier is cheaper in wall-clock time.
- **Auto routing** (Cursor/Copilot "Auto", OpenRouter/LiteLLM) is acceptable for cost control when the task is routine; the speaker "barely notices differences" on daily work. Turn it off for planning.
- **Privacy mode on, memories on** regardless of model.

Vendor preference stated in the workshop: Anthropic (latest Opus for planning, Sonnet 4.6 for execution as of 2026-09-08), with Codex (if already paying ChatGPT) and Gemini Pro as fully valid alternatives; Cursor's Composer 2 for speed.

## 4. How to apply it in a repo

1. Write the model policy into `docs/workflow.md`: which phase uses which tier.
2. In Claude Code: plan mode + top model for the spec; switch to the mid model for `/develop-ticket`-style execution.
3. Log which model produced each spec/PR for a month; compare rework rate.

## 5. Anti-patterns

- Choosing by brand loyalty or habit.
- Top tier for formatting-level tasks; mid tier for architecture.
- Treating this table as stable — set a reminder to re-review quarterly.

## 6. Evidence & sources

- LIDR hub §2 model table and video C — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.9.

## 7. Change log

- 2026-09-08 — created. Model names reflect 2026-09-08.
- 2026-09-24 — reviewed against `sources/2026-09-24-s12-agents-digest.md`; confirms "start with the most capable model to learn the headroom, then optimise cost/latency" (Stanford CME295, Barry Zhang) and adds one datum: Notion prices custom agents by usage and nudges users away from the top tier for routine automations ("most tasks aren't Opus-level"). Do not fine-tune on your own tools (they change daily). No change to the table.
