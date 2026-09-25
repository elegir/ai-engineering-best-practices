---
title: "Scan log — every course module or topic scanned for market best practices, and how far each one got"
type: source
status: current
date: 2026-09-24
tags: [scan-log, market-scan, courses, tracking]
sources:
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Scan log

One row per module of every course Martin follows (or any topic he decides to scan). The course syllabus is only a **map of topics**; each scan looks for what the market's most authoritative voices are saying about that topic right now. Procedure: `playbooks/scan-market-for-module.md`. Update the row at every stage change; this is the "tick it off" view.

Stages: `mapped` (topic listed, nothing done) → `catalogued` (written canon listed) → `scanned` (video/podcast search done, selection logged) → `transcribed` (raw transcripts in `sources/raw/`) → `digested` (source entry has a full digest) → `principled` (principle + practice exist, status draft) → `validated` (compared against the course session itself; principle `current`).

## LIDR — Máster AI Engineering (Oct 2026 – Feb 2027)

Written canon for all 17 sessions was catalogued on 2026-09-24 (Claude Project docs `curso-fuentes-sesiones-*.md`; to be moved into this repo as sources/catalog.md (pending)).

| S | Date | Topic | Stage | Scan entry | Principle / practice | Notes |
|---|---|---|---|---|---|---|
| 1 | 2026-10-15 | LLMs and environment setup | catalogued | — | — | |
| 2 | 2026-10-22 | CAG: context, parameters, costs | catalogued | — | — | Candidate video from S12 scan: IBM "Is RAG still needed?" (1.0M views) |
| 3 | 2026-10-29 | Wrappers and layered architecture | catalogued | — | — | |
| 4 | 2026-11-05 | Advanced AI products (structured outputs, guardrails) | catalogued | — | — | |
| 5 | 2026-11-12 | External context, memory, permissions, testing | catalogued | — | — | Candidate podcast: Chain of Thought "Agent memory: the last battleground" |
| 6 | 2026-11-19 | Data-driven AI: audit, cleaning, privacy | catalogued | — | — | |
| 7 | 2026-11-26 | Embeddings and vector representation | catalogued | — | — | |
| 8 | 2026-12-03 | Vector databases | catalogued | — | — | |
| 9 | 2026-12-10 | RAG fundamentals | catalogued | — | — | Candidate video: Stanford CS230 L8 "Agents, prompts and RAG" |
| 10 | 2026-12-17 | Advanced retrieval | catalogued | — | — | |
| 11 | 2027-01-07 | Advanced RAG: generation and quality | catalogued | — | — | |
| 12 | 2027-01-14 | Introduction to AI agents | **principled** (draft) | `sources/2026-09-24-market-scan-s12-intro-to-agents.md` → digest `sources/2026-09-24-s12-agents-digest.md` | `principles/21-agent-design-and-tools.md` (draft), `practices/agent-patterns/`, `practices/prompt-library/trajectory-review.md`; refined 00, 02, 05, 07, 08, `mcp-audit.md` | Pilot. 15 transcripts, ~7.5 h. Parked from the digest: Notion's 3 eval tiers → S5/11/16; tool-auth ladder, multi-agent, sandboxing → S14. Becomes `validated` after LIDR session 12 |
| 13 | 2027-01-21 | Agent orchestration | catalogued | — | — | Candidate podcasts: Latent Space "Age of async agents"; AI Eng. Podcast "Pydantic AI" |
| 14 | 2027-01-28 | Advanced multi-agent: HITL, security, sandboxing | catalogued | — | — | Candidates: Latent Space "Giving agents computers"; AI Eng. Podcast "MCP as the API… security"; Chain of Thought "You can't secure an agent with software" |
| 15 | 2027-02-04 | Production and LLMOps I | catalogued | — | — | Candidates: Latent Space Modal / Railway episodes |
| 16 | 2027-02-11 | Production and LLMOps II | catalogued | — | — | Candidate: Chain of Thought "Every agent has an evaluation gap" |
| 17 | 2027-02-18 | Lab 10x: SDD, agents, MCP, skills, code review | catalogued (principles 02–05 already exist) | — | refine principles 02, 04, 05 | Candidates: Latent Space "Extreme harness engineering" (OpenAI), "GitHub's plan for agents"; AI Eng. Podcast "Harness engineering for governed agents" (2026-09-19) |

## Earlier sources (before the scan procedure existed)

| Date | Topic | Stage | Entry |
|---|---|---|---|
| 2026-09-08 | LIDR workshop: Harness Engineering | validated | `sources/2026-09-08-lidr-workshop-harness-engineering.md` → principles 00–09 |
| 2026-09-08 | How teams structure agent knowledge (web survey) | validated | `sources/2026-09-08-how-teams-structure-agent-knowledge.md` → principle 09 |
