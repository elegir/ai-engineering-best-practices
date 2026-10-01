---
title: "Market scan — course session 5 'Advanced features: external context, conversational memory, permission-adaptive systems, testing and evaluation': which videos, podcasts and written sources were considered, selected and transcribed"
type: source
status: current
date: 2026-10-01
tags: [market-scan, evals, llm-as-judge, error-analysis, agent-memory, mem0, memgpt, letta, permissions, rbac, mcp, external-context, s5, lidr-ai-engineering]
sources:
  - sources/raw/2026-10-01-market-scan-s05-context-memory-permissions-evals/
  - sources/catalog-written-canon.md
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 5: external context, memory, permissions, evals

**What this file is.** The log of the scan (steps 1–2 of the four-step module cycle). The digest (step 3) is a separate entry.

## 1. Context

- **Topic map (LIDR session 5, 2026-11-12).** Integration of external context (files, web, databases) · conversational memory (short/long-term, summarisation, memory stores such as Mem0/LangMem/Letta) · permission-adaptive systems (RBAC in LLM apps, least-privilege tools, approvals) · testing and evaluation of LLM systems (evals, promptfoo, DeepEval, LLM-as-judge, error analysis).
- **Written canon** (step 1b, registered 2026-10-01 in `sources/catalog-written-canon.md` §Session 5, 21 items): Claude Files/PDF, web search/fetch/MCP connector docs, the MCP announcement, the memory tool, LangChain memory + LangMem, the Mem0 and MemGPT papers, Pinecone RAG with access control, OWASP LLM06/LLM02, the Agents guardrails & approvals guide, Hamel Husain *Your AI product needs evals*, Anthropic *Demystifying evals for AI agents* and the test-and-evaluate docs, Eugene Yan's two judge essays, the MT-Bench judge paper, promptfoo and DeepEval docs, and five courses.
- **Reuse (step 1a).** Read again for the digest, not re-transcribed: Lance Martin *Context engineering for agents* (s2 — write/select memory), the Manus context-engineering talk (s2 — file-system memory), Michel Tricot *Context poisoning* (s2 — memory hygiene), Barry Zhang *How we build effective agents* (s12 — tool permissions), Dave Ebbelaar agentic RAG (s12), the s1 Chain of Thought *Plausibility engines* episode (evals of plausibility). The s4 digest already covers judge calibration (≤ 5 classes, logprobs) and is cited rather than re-read.
- **Method.** `streamers/youtube-scraper` run `QYcP2x2e1o565uyg8` (8 queries × 15, last 12 months → 111 items) + canon run `Sblst55HtRmWsbYQ6` without the date filter (9 queries × 8 → 63 items) + a targeted run `CJYNj8VlhtzglNctN` for two podcast episodes' YouTube versions. `scripts/scan-filter.py`: 109 new in the dated run, 2 already decided (one s4 discard, the Stanford CME295 lecture parked by s4 and taken now? — no: it stays a candidate for s5's *validation* pass; see §4). Three reference feeds read directly: 10 + 21 + 1 titles matched the module's terms. Transcripts: `johnvc/YoutubeTranscripts` run `3r5kmiTQutzlfgo2Y`, dataset `hyPk7aUBdYkC1imrc`, 14 of 14 with captions, no Whisper. Cost: about US$0.50.
- **Queries.** "AI agent memory architecture long-term short-term Mem0 LangMem" · "LLM evals LLM-as-judge production evaluation" · "promptfoo DeepEval LLM evaluation CI pipeline" · "RAG access control permissions RBAC LLM application" · "AI agent permissions human approval tool authorization least privilege" · "LLM external context files API PDF web search tool" · "AI evals 2026" · "error analysis evals Hamel Husain Shreya Shankar"; canon run: Hamel Husain AIE talks, Lenny's evals episode, Mem0 reading group, Charles Packer/MemGPT, DoorDash evals, Chain of Thought memory episode, Eugene Yan judge talk, Anthropic demystifying evals, MCP permissions.
- **What the search taught.** The evals bullet has a real market with a visible canon: Hamel Husain's channel (nine videos in twelve months), AI Engineer 2026 (three talks), Lenny's. The memory bullet is covered by two primary sources (Letta/MemGPT lineage, Mem0) and one reference podcast; YouTube is otherwise tutorials. The permissions/RBAC bullet has **no conference talk** in the window — the market speaks about it inside MCP-deployment stories (Block) and zero-trust explainers (IBM); the written canon (Pinecone, OWASP, Agents SDK approvals) carries most of it. The external-context bullet is almost entirely MCP explainers (parked for s13) and "local LLM" noise (discarded).

## 2. Selection criteria

The authority test of the pilot (`sources/2026-09-24-market-scan-s12-intro-to-agents.md` §2). Reach floor 5k/500 unless primary. One exception recorded: the IBM zero-trust explainer (corporate education) is taken because the permissions bullet has no higher-authority video and the explainer has 203k views. Target met: 14 items, about 8 h 50 min, four podcast episodes.

## 3. Selected — transcribed (14)

| Title | Channel | Date | Length | Authority | Serves | Raw file |
|---|---|---|---|---|---|---|
| Why AI evals are the hottest new skill — Hamel Husain & Shreya Shankar | Lenny's Podcast | 2025-09 | 1 h 46 m | canon podcast | evals: error analysis, binary grading, judges | `podcast-BsWxPI9UM4c-…` |
| How to automate AI evals (correctly) | Hamel Husain | 2026-07 | 27 m | primary practitioner | evals automation | `yt-tqUDjc1HzO4-…` |
| How to build AI evals | Hamel Husain | 2026-07 | 34 m | primary practitioner | evals end to end | `yt-mF4CaijvJos-…` |
| Paired error analysis with AI agents | Hamel Husain | 2026-04 | 26 m | primary practitioner | error analysis for agents | `yt-FzO7NRe_7VA-…` |
| AI evals for cross-functional teams — DoorDash | AI Engineer | 2026-08 | 16 m | canon talk | eval platform, annotation, calibration | `yt-bMjlRrWjdT0-…` |
| Closed-loop evals for a multimodal agent at scale | AI Engineer | 2026-07 | 22 m | reference conference | evals in production | `yt-31GUkCBD-Uc-…` |
| "Evals, evals, evals" — 2026 state of AI engineering | AI Engineer | 2026-07 | 20 m | reference conference (survey) | evals: the market's own numbers | `yt-RGe6EjucbzI-…` |
| Eugene Yan on using LLMs as judges | Jason Liu | 2024-08 | 39 m | canon | LLM-as-judge | `yt-7EGF0Mc0_os-…` |
| Practical lessons for GenAI evals — Chip Huyen | Chain of Thought | 2024-12 | 50 m | reference podcast | evals | `podcast-mrYn6_6gJuY-…` |
| Agent memory: the last battleground — Richmond Alake | Chain of Thought | 2026-04 | 59 m | reference podcast | memory | `podcast-CDadnSE7Eww-…` |
| Mem0 paper reading group | AAIF Live | 2025-06 | 58 m | canon reading group | memory | `yt-cHQyugatz6M-…` |
| Letta: stateful agents, sleep-time compute | Arize AI × Letta | 2025-07 | 37 m | primary (MemGPT lineage) | memory | `yt-sgD-sw0RW78-…` |
| Securing AI agents with zero trust | IBM Technology | 2026-02 | 14 m | corporate explainer (exception) | permissions | `yt-d8d9EZHU7fw-…` |
| How Block deployed Goose to 12,000 employees with MCP — Angie Jones | Chain of Thought | 2026-01 | 50 m | reference podcast | external context + permissions at scale | `podcast-O7etCBod2IY-…` |

## 4. Considered — not transcribed (every item is in `sources/media-registry.json` with its reason)

- **Parked for other modules (16 incl. RSS):** Arize two-hour evals workshop → s16; LangChain observability & evals → s15; Hamel *Don't build agents, build environments* → s13; MIPRO/DSPy → s16; three MCP explainers (IBM ×2, codebasics), *The creators of MCP*, Notion's *Token Town* → s13; GraphRAG → s10; WisdomAI *context alone isn't enough* → s10; Andon Labs *Reality: the final eval* and Snorkel *evaluation gap* → s16; Chip Huyen on Lenny's → s1 validation. The Stanford CME295 evaluation lecture (parked by s4 for s5) stays a candidate for the s5 **validation** pass (academic lecture; the practitioner material above covers the session).
- **Discarded (144 + 2 RSS):** below the reach floor (most); "local LLM / LM Studio / Ollama" results of the external-context queries (off-topic); corporate-education and beginner explainers (Krish Naik, CampusX, Aakash Gupta ×3, Peter Yang ×2, ByteByteAI…); same-speaker duplicates (Hamel Husain's shorter cuts and tool comparisons, Charles Packer on three other channels, Eugene Yan elsewhere); vendor episodes on their own category (Galileo eval engineering, Braintrust).
- **Not found with captions:** none.

## 5. Still to do

Digest with the impact table; principle 14 (draft: evals) and possibly principle 15 (memory + external context + permissions) — the digest decides whether one principle or two; practice folders created **unrouted** (routing gate, decision 0004 §6); registry entries to `digested` → `applied`.

## 6. Raw notes

`sources/raw/2026-10-01-market-scan-s05-context-memory-permissions-evals/` — 14 transcripts, `youtube-search-results.json` (111), `youtube-search-results-canon.json` (63).
