---
title: "Market scan — course session 12 'Introduction to AI agents': which videos and podcasts were considered, selected and transcribed"
type: source
status: current
date: 2026-09-24
tags: [market-scan, agents, tool-use, function-calling, mcp, agentic-rag, react, s12, lidr-ai-engineering]
sources:
  - sources/raw/2026-09-24-market-scan-s12-agents/
  - https://apify.com/streamers/youtube-scraper
  - https://apify.com/automation-lab/podcast-scraper
  - https://apify.com/johnvc/YoutubeTranscripts
supersedes: null
superseded-by: null
---

# Market scan — session 12: Introduction to AI agents

**What this file is.** A *log*, not yet a digest. It records which YouTube videos and podcast episodes were found, which were selected as maximum-authority material for this topic, which were discarded and why, and where the verbatim transcripts live. The digest of the selected material (what was said, what it means, what to copy into `principles/` and `practices/`) is a separate step and is tracked in `sources/scan-log.md`. This is the pilot run of `playbooks/scan-market-for-module.md`; the same procedure is meant to be repeated for every module of any course Martin follows.

## 1. Context

- **Trigger.** Martin is enrolled in the LIDR "Máster AI Engineering" (Oct 2026 – Feb 2027). Its syllabus is used only as a *map of topics*; the goal of each scan is to find what the market's most authoritative voices are currently saying about that topic, independently of what the course teaches.
- **Topic map for this session (LIDR session 12, 2027-01-14).** Anatomy of an agent · reasoning and planning patterns (ReAct, plan-and-execute, reflection) · tools and function calling (OpenAI, Anthropic, Google ADK, MCP as tool transport) · integration with RAG (agentic RAG).
- **Written canon** (docs, papers, engineering blogs) for this session was catalogued separately on 2026-09-24 in the Claude Project doc `curso-fuentes-sesiones-12-14.md`; this scan covers *spoken* material (video, podcast) only.
- **Method.** Apify, from Claude via the Apify MCP server:
  1. `streamers/youtube-scraper` (official Apify actor), run `2SuBQh2X1xhP67Sgn`: 7 search queries × 15 results, filter "uploaded in the last year", sorted by relevance, regular videos only → **105 videos**. Raw results: `sources/raw/2026-09-24-market-scan-s12-agents/youtube-search-results.json`.
  2. `automation-lab/podcast-scraper`, run `6wTby4sxl4JBYGKih`: Apple Podcasts search, 3 queries → **30 shows**. Raw: `…/apple-podcasts-search-results.json`. Then the RSS feeds of the three shows with real authority were read directly and filtered for episodes about agents/tools/MCP in the last 12 months.
  3. Selection by hand (criteria in §2).
  4. `johnvc/YoutubeTranscripts`, runs `GTmS0fKOJ6S6P9B5j` and `iDx7HZZJypI5VKRid`: captions for the 15 selected items (14 videos + the YouTube version of 1 podcast episode) → one file each under `sources/raw/2026-09-24-market-scan-s12-agents/`. Total ≈ 407,000 characters (~7.5 hours of audio).
- **Cost.** Search ≈ 0.05 compute units + ~$0.30 per-video fees; transcripts ≈ $0.01. Negligible.
- **Queries used.** "building effective AI agents", "AI agent tool use function calling", "ReAct agent reasoning planning LLM", "agentic RAG", "Model Context Protocol agents tools", "how to build AI agents 2026", "anatomy of an AI agent".

## 2. Selection criteria (authority test)

An item is **selected** if it passes at least one of these, in this order of weight:

1. **Primary source**: published by the organisation that builds the thing (Anthropic, Google, OpenAI, Cursor, the MCP project) or by the people who wrote the reference text (e.g. Barry Zhang for *Building Effective Agents*).
2. **Academic**: a university lecture (Stanford Online) or a talk at the field's reference conference (AI Engineer World's Fair / Summit).
3. **Recognised practitioner**: a person whose written work is already in the written canon for this topic (Andrew Ng, Lance Martin, Simon Willison…), or a podcast that the AI-engineering community treats as the record (Latent Space).
4. **Corporate education channel with editorial standards** (IBM Technology, Google Cloud Tech): accepted for *explainers*, weighted lower than 1–3.
5. **Trend signal**: a community video with unusually high reach on a term that is new in the market (e.g. "agent harness") — kept to record *what the market is talking about*, not as a source of truth.

An item is **discarded** if it is: no-code/automation-platform marketing (n8n, "build & sell agents", "automate 99 % of your life"); a low-reach re-explanation of a paper (< 5k subscribers, no original contribution); off-topic for this session (voice agents, SAP/Copilot product demos); or not in English/Spanish.

## 3. Selected — transcribed (15)

| # | Title | Channel / show | Date | Length | Authority | Session bullet it serves | Raw file |
|---|---|---|---|---|---|---|---|
| 1 | Building more effective AI agents | Anthropic (official) | 2025-10-17 | 18m 51s | 1 — primary | anatomy; patterns; tools | `yt-uhJJgc-0iTQ-…` |
| 2 | Tips for building AI agents (Schluntz, Zhang) | Anthropic (official) | 2025-02 | 18m 16s | 1 — primary | workflows vs agents; when to build | `yt-LP5OCa20Zpg-…` |
| 3 | How We Build Effective Agents — Barry Zhang | AI Engineer (Summit NYC) | 2025-03 | 15m 10s | 1/2 — author + conference | patterns; "think like your agent" | `yt-D7_ipDqhtwk-…` |
| 4 | Building Agents with MCP — full workshop, Mahesh Murag | AI Engineer | 2025-03 | 1h 44m | 1/2 — MCP product lead | MCP as tool transport | `yt-kQmXtrmQ5Zg-…` |
| 5 | MCP in Claude Code | Claude (official) | 2026-05-09 | 3m 32s | 1 — primary | MCP in practice | `yt-kkBFmwkDzdo-…` |
| 6 | How Model Context Protocol (MCP) actually works | Google Cloud Tech | 2026-06-24 | 7m 43s | 1/4 — vendor | MCP architecture | `yt-cGuyrANVi4A-…` |
| 7 | AI agents explained: build your first agent in 8 minutes (ADK) | Google Cloud Tech | 2026-06-10 | 8m 14s | 1/4 — vendor | anatomy; ADK tools | `yt-Zqno_vux6d8-…` |
| 8 | AI Foundations: Tool Calling | Cursor (official) | 2025-09-27 | 5m 58s | 1 — vendor | function calling loop | `yt-byR5YVesMeg-…` |
| 9 | Stanford CME295 Autumn 2025 — Lecture 7: Agentic LLMs | Stanford Online | 2025-11-18 | 1h 49m | 2 — academic | anatomy; ReAct; planning; tool use | `yt-h-7S6HNq0Vg-…` |
| 10 | What's next for AI agentic workflows — Andrew Ng | Sequoia Capital | 2024-03-26 | 13m 41s | 3 — practitioner (canon) | four agentic patterns (reflection, tool use, planning, multi-agent) | `yt-sal78ACtGTc-…` |
| 11 | 5 Ways to Connect AI Agents to Tools: From APIs to MCP | IBM Technology | 2026-08-16 | 11m 17s | 4 — corporate explainer | tool integration options | `yt-BHGTA6ZEls4-…` |
| 12 | Skills vs MCP vs RAG vs Memory: What AI Agents Need to Know | IBM Technology | 2026-09-03 | 8m 58s | 4 — corporate explainer | how the four capability mechanisms relate (2026 framing) | `yt-X4FVEEegCbk-…` |
| 13 | Building Agentic RAG From Scratch in Pure Python | Dave Ebbelaar | 2026-05-10 | 27m 30s | 3 — practitioner (295k subs, code-first) | agentic RAG integration | `yt-RxwjoegpI98-…` |
| 14 | Agent Harness explained in 8 min | Caleb Writes Code | 2026-05-22 | 8m 21s | 5 — trend signal (579k views) | "harness" entering mainstream vocabulary; links this session to `principles/02-harness-engineering.md` | `yt-1a1VXDdIyrk-…` |
| 15 | Notion's Sarah Sachs & Simon Last on custom agents, evals, 100+ tools, MCP vs CLIs | Latent Space (podcast; YouTube version) | 2026-04-15 | 1h 25m | 3 — reference podcast | tool design at scale; MCP vs CLI as tool transport; evals for agents | `podcast-ATt7QJgt-2k-…` |

Items 2, 3, 4 and 10 are older than 12 months and did **not** surface in the "last year" search; they were added from the written canon because they are the reference talks for this topic. The scan finds *trend*; the canon supplies *foundation*. Both belong in the log.

## 4. Considered — not transcribed, with reason

From the 105 YouTube results (full list in the JSON):

| Item | Channel | Reason not selected |
|---|---|---|
| Stanford CS230 Autumn 2025 — Lecture 8: Agents, Prompts, and RAG (499k views) | Stanford Online | Academic and good, but broader than this session (prompts + RAG); CME295 L7 is the agent-specific lecture. Candidate for session 9 (RAG fundamentals). |
| How AI Agents Actually Work (every piece explained & built) · How to Build AI Agents in Python – 3 ways · Build a local AI agent in 10 minutes | Tech With Tim (2.09M subs) | Education channel, competent, but no original contribution beyond the primary sources already selected. Optional for beginners. |
| Don't learn AI Agents without learning these fundamentals (1.24M views) | KodeKloud | Same as above; DevOps-education channel. |
| RAG's Evolution: From Simple Retrieval to Agentic AI · RAG vs Agentic AI · Is RAG still needed? · Anatomy of AI Agents · What is OpenClaw? · MCP vs gRPC · MCP vs RAG · 5 Best Practices for Building AI Agent Skills · The 7 Skills You Need · What AI Agent Skills Are | IBM Technology | Kept two IBM explainers (#11, #12) as representative; the rest repeat the same framing. "Is RAG still needed?" (1.0M views) is a candidate for session 2 (CAG vs RAG). |
| RAG & MCP Fundamentals – hands-on crash course (1h40) · Intro to MCP Servers with Python (1h12) | freeCodeCamp.org | Long tutorials; useful for a learner, not needed for the KB because the Mahesh Murag workshop (#4) is the primary source. |
| MCP In 26 Minutes | Tina Huang (1.32M subs) | Popular explainer; superseded by #4 and #6. |
| MCP is Dead – why no one uses MCP · Tool Calling vs MCP | Piyush Garg | Opinion content; the "MCP vs CLIs/skills" debate is captured with more rigour in #15 (Notion) and #12. |
| Anthropic killed Tool calling (209k views) | AI Jason | Reacts to Anthropic's *Advanced tool use* post (2025-11-24); read the post (in the written canon) instead. |
| Agentic RAG tutorial (Oxylabs) · The missing piece that makes RAG agentic · Agentic RAG with MCP (Edward Donner) · Agentic RAG with LangGraph (Krish Naik, AI Bites) · The complete agentic RAG build (The AI Automators, 2h14) | various | Tutorials on one framework each; #13 chosen as the framework-free reference. LangGraph agentic-RAG is already covered by LangChain's official docs page in the written canon. |
| ReAct explainers (Micro Learning, BioinfQuests, Tech With Mala, DATA JARVIS, CodeCraft Academy, datarekha, What's AI, SH AI Academy…) | small channels | Re-explanations of the ReAct paper (in the written canon); no original contribution. "ReAct vs Plan-and-Execute" (What's AI, 74k subs) is the best of them if a short explainer is ever needed. |
| How do thinking and reasoning models work? | Google for Developers | Good, but about reasoning models, not agents; candidate for session 1. |
| AI Agents + LLM Reasoning (IBM) | IBM Technology | Overlaps #11/#12. |
| Give your voice AI agent real abilities (tool calling) · LiveKit async function tools · AgenticXLab voice course | Google Cloud Tech, LiveKit, others | Voice-agent specific; out of scope. |
| How to build & sell AI agents in 2026 · AI agents masterclass 4 hours · n8n tutorial · How I built an AI agent in 14 minutes as a beginner · 4 AI agents to automate 99 % of your life · You're not behind (yet) · STOP building AI agents · AI agents full course 2026 (Nick Saraev) · Building AI agents that actually work (Greg Isenberg) · Copilot Agent Builder · SAP Joule Studio | Liam Ottley, Michele Torti, Youri van Hofwegen, Mikey No Code, Sandeep Swadia, Dan Martell, Futurepedia, Zubair Trabzada, Nick Saraev, Greg Isenberg, Collaboration Simplified, SAP | No-code / automation-platform / "sell agents" marketing, or product demos. Discarded by rule. |
| 工业级实战：从传统RAG到Agentic RAG的进阶优化 | 白白说大模型 | Not in English/Spanish. |
| ~25 videos with < 5k subscribers and < 500 views | various | Below the reach/authority floor. |

Podcast shows found on Apple Podcasts (30) — kept as **authoritative feeds** for future scans: *Latent Space* (Swyx & Alessio; the AI-engineering record), *AI Engineering Podcast* (Tobias Macey), *Chain of Thought* (Galileo). Discarded shows: marketing/"AI for small business" podcasts, one-episode shows, a German-language show.

Podcast **episodes** considered (last 12 months, titles matching agent/tool/MCP/harness) and where they belong:

| Episode | Show | Date | Decision |
|---|---|---|---|
| Notion's Token Town: 5 rebuilds, 100+ tools, MCP vs CLIs | Latent Space | 2026-04-15 | **Selected (#15)** — tool design and MCP-vs-CLI debate are session-12 material. |
| Extreme Harness Engineering for Token Billionaires — Ryan Lopopolo, OpenAI | Latent Space | 2026-04-07 | Candidate for `principles/02-harness-engineering.md` / session 17, not this session. |
| The Age of Async Agents — Cognition & OpenInspect | Latent Space | 2026-05-28 | Candidate for session 13/14 (orchestration, long-running agents). |
| Giving Agents Computers — Daytona · Railway: the agent-native cloud · Why AI infra must evolve for agent experience — Modal | Latent Space | 2026-05/07 | Candidates for session 14 (sandboxing) and 15 (LLMOps). |
| GitHub's plan for agents — Kyle Daigle | Latent Space | 2026-06-02 | Candidate for session 17 (coding agents, code review). |
| Harness Engineering for Reliable, Governed AI Agents | AI Engineering Podcast | 2026-09-19 | Candidate for session 14/17. Very recent; flag for the next harness-engineering review. |
| MCP as the API for AI-native systems: security, orchestration, scale · Designing scalable AI systems with FastMCP | AI Engineering Podcast | 2025-12-16 · 2025-08-26 | Candidates for session 14 (MCP security) and 17. |
| Building production-ready AI agents with Pydantic AI | AI Engineering Podcast | 2025-10-07 | Candidate for session 13 (frameworks). |
| Agent Memory: the last battleground · Context poisoning is killing your agents · Every AI agent has an evaluation gap · You can't secure an AI agent with software | Chain of Thought | 2026-03/07 | Candidates for sessions 5 (memory), 2 (context), 11/16 (evals), 14 (security). |

## 5. What is still to do for this module

- [ ] **Digest** the 15 transcripts into this file's successor sections (one-paragraph summary; detailed digest; claims worth checking; contested points; implications per repo; actions), following `CONVENTIONS.md` §3.
- [ ] Create principles/21-agent-design-and-tools.md (pending) (status `draft`) from the digest + the written canon.
- [ ] Create practices/agent-patterns/ (pending) with the copyable assets identified in the written catalogue: pattern catalogue with "when to use", tool-definition template, tool_use/tool_result loop, agentic-RAG skeleton, "when to build an agent" checklist.
- [ ] After LIDR session 12 (2027-01-14): ingest the LIDR material as its own source, compare, promote the principle to `current`.
- [ ] Mark the row in `sources/scan-log.md`.

## 6. Raw notes

All verbatim material: `sources/raw/2026-09-24-market-scan-s12-agents/` (15 transcript files + 2 search-result JSON files). File names carry the YouTube id so the source is always recoverable: `yt-<id>-<slug>.md`, `podcast-<id>-<slug>.md`.
