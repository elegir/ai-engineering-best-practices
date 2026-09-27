---
title: "Market scan — course session 2 'CAG: context, parameters and costs': which videos and podcasts were considered, selected and transcribed"
type: source
status: current
date: 2026-09-27
tags: [market-scan, context-engineering, prompt-caching, context-window, cag, long-context, s2, lidr-ai-engineering]
sources:
  - sources/raw/2026-09-27-market-scan-s02-context-caching/
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 2: CAG architecture — context, parameters and costs

**What this file is.** The log of the scan (steps 1–2 of the four-step module cycle): what was searched, what was found, what was selected by the authority test, what was discarded and why. The digest (step 3) and the KB changes (step 4) are in `sources/2026-09-27-s02-context-caching-digest.md`.

## 1. Context

- **Topic map (LIDR session 2, 2026-10-22).** Fundamentals of Cache-/Context-Augmented Generation · context management, parameters and costs · conversational architecture · consumption best practices and optimisation (prompt caching, context windows, long context vs RAG).
- **Written canon** catalogued 2026-09-24 in the Claude Project doc `curso-fuentes-sesiones-01-05.md` §2: the CAG paper (Chan et al., arXiv 2412.15605), the prompt-caching docs of Anthropic, OpenAI and Gemini, Anthropic *Effective context engineering for AI agents* (2025-09-29), Anthropic context-windows / compaction docs, *Lost in the Middle* (Liu et al., 2023), Chroma *Context Rot* (2025-07), Simon Willison *Context engineering* (2025-06), Lance Martin *Context Engineering for Agents* (2025-06), Redis prompt vs semantic caching.
- **Method** (`playbooks/scan-market-for-module.md`): `streamers/youtube-scraper` run `g94g5fGuyWOaPepTR`, 7 queries × 15, last 12 months, relevance → **105 videos**; `scripts/scan-filter.py` → **97 new, 1 parked candidate (IBM "Is RAG still needed?", taken), 7 already decided**. RSS of Latent Space, AI Engineering Podcast and Chain of Thought filtered for cache / context / token / cost / compaction / memory terms → 9 matching episodes, 1 taken from each of Latent Space (canon) and Chain of Thought (parked by s12, taken now); title search for the Chain of Thought episode: run `HS9jcEHSgRTrLBYNj`. Transcripts via `johnvc/YoutubeTranscripts` runs `SlaESbO0FHebseABa`, `vRIALHstW817bPdoM`, `FojiOGHzTR6oE2cTs`: **16 items, ≈491,000 characters, ≈7 h 35 min**.
- **Queries.** "prompt caching explained LLM API cost", "context engineering for AI agents", "cache augmented generation vs RAG", "long context vs RAG when to use", "LLM context window management compaction summarization", "LLM API cost optimization tokens 2026", "conversational AI architecture context management".
- **What the search taught.** "Context engineering" is now the market's term for this whole module; it returns the strongest material (vendor developer-relations, AI Engineer conference, LangChain, Manus, Dex Horthy). "Cache augmented generation" as a query returns almost only tiny re-explanations of one paper — the CAG term has not been adopted by practitioners; the authoritative treatment comes from IBM's explainers and from the long-context-vs-RAG debate. "LLM API cost optimization" returns cost-guide content below the reach floor; the useful cost material sits inside the context-engineering talks (AWS "Quit tokenmaxxing", Hugging Face on caching). "Compaction" returns Claude-Code-specific tutorials (s17 territory) plus one official Claude short (taken).

## 2. Selection criteria

The authority test of the pilot (`sources/2026-09-24-market-scan-s12-intro-to-agents.md` §2): primary source > academic or reference conference > recognised practitioner or reference podcast > corporate explainer > trend signal. Discard by rule: re-explanations below the reach floor, coding-agent tutorials (s17), vendor panels with no original contribution, interview-prep content.

## 3. Selected — transcribed (16)

| # | Title | Channel | Date | Length | Authority | Session bullet | Raw file |
|---|---|---|---|---|---|---|---|
| 1 | Context Management in Claude Code | Claude (official) | 2026-05-18 | 3m26 | 1 — primary | context management; compaction | `yt-eW3oTyfeWZ0-…` |
| 2 | Context engineering explained: what every AI developer should know | Google Cloud Tech (official) | 2026-07-15 | 9m50 | 1 — vendor | context management | `yt-BBPQYtR7oUk-…` |
| 3 | Quit Tokenmaxxing: 4 context engineering techniques for AI agents | AWS Developers (official) | 2026-09-14 | 21m34 | 1 — vendor | costs; context optimisation | `yt--q_u6nrVdgo-…` |
| 4 | Managing agent context with LangChain: summarization middleware | LangChain (official) | 2025-11-25 | 8m30 | 1 — vendor | conversational architecture; summarisation | `yt-A1t53E4vtGo-…` |
| 5 | Context engineering for AI agents with LangChain and Manus | LangChain (official; Lance Martin + Manus) | 2025-10-14 | 1h01 | 1/3 — vendor + practitioner | context management; KV-cache | `yt-6_BcCthVvb8-…` |
| 6 | How we solved context management in agents — Sally-Ann DeLucia (Arize) | AI Engineer (conference) | 2026-05-10 | 16m16 | 2 — reference conference | conversational architecture | `yt-esY99nYXxR4-…` |
| 7 | Building the document context layer for AI agents — Jerry Liu (LlamaIndex) | AI Engineer (conference) | 2026-09-23 | 20m47 | 2 — reference conference | context; long context vs retrieval | `yt-RQi7x-navxU-…` |
| 8 | Context engineering our way to long-horizon agents — Harrison Chase | Sequoia Capital | 2026-01-21 | 39m18 | 3 — recognised practitioner | context management; architecture | `yt-vtugjs2chdA-…` |
| 9 | Context engineering with Dex Horthy | The Pragmatic Engineer | 2026-07-15 | 1h33 | 3 — recognised practitioner (12-Factor Agents) | context management; costs | `yt-Usufn8IQJgw-…` |
| 10 | Effective context engineering for AI agents (why agents still fail) | Dave Ebbelaar | 2025-12-19 | 25m03 | 3 — practitioner | context management | `yt-nkJXADeI62c-…` |
| 11 | Prompt caching explained: stop overpaying for AI agents | Hugging Face | 2026-08-10 | 17m14 | 3 — practitioner / vendor | prompt caching; costs | `yt-SkM4k4SKvCM-…` |
| 12 | What is prompt caching? | IBM Technology | 2026-02-07 | 9m00 | 4 — corporate explainer | prompt caching | `yt-u57EnkQaUTY-…` |
| 13 | CAG vs long context | IBM Technology | 2026-05-21 | 10m46 | 4 — corporate explainer | CAG fundamentals | `yt-B_RrXwDupIg-…` |
| 14 | Is RAG still needed? Choosing the best approach for LLMs | IBM Technology | 2026-03-09 | 11m03 | 4 — corporate explainer (parked by s12, 1.0M views) | long context vs RAG | `yt-UabBYexBD4k-…` |
| 15 | Context Engineering for Agents — Lance Martin | Latent Space (podcast, YouTube version) | 2025-09-11 | 1h03 | 3 — reference podcast, canon (>12 months) | context management (write/select/compress/isolate) | `podcast-_IlTcWciEC4-…` |
| 16 | Context poisoning is killing your AI agents — Michel Tricot (Airbyte) | Chain of Thought (podcast, YouTube version) | 2026-03-25 | 44m10 | 3 — reference podcast (parked by s12) | context quality; data layer | `podcast-tYJmgpIEd-Y-…` |

Item 15 is older than 12 months and was added from the written canon. Items 14 and 16 were parked for this session by the session-12 scan and taken now.

## 4. Considered — not transcribed

84 YouTube items discarded, all registered with a reason in `sources/media-registry.json`. Grouped:

| # | Reason | Examples |
|---|---|---|
| 51 | below reach/authority floor (<5k subs or <500 views), re-explanation | RAG Is Dying : Long Context + Grep Just Won (The Weights) · RAG vs Long Context: The Future of AI Systems Explained (Poniak Labs) · RAG Is Dead? Everyone's Wrong About This (Holy Shifted - Software & AI Engineering) · RAG vs Long Context: When "Just Paste It All In" Quietly Fails (Skill MD) · Agentic Context Management: The Five Primitives of Agent Memory (Research Paper Review) · … (+46 more in the registry) |
| 9 | education/opinion or framework-vendor channel; no original contribution beyond the primary sources selected | Prompt Caching Reduced My Agent Costs by 90% (Mastra) · Caching Strategies to Slash Your LLM Bill | Prompt & Semantic Caching  (MadeForCloud) · Prompt Caching Explained Visually — Cut Your LLM API Bill (2026) (Balaji Chippada) · You Don't Own Your AI. The Harness Does. (Manolo Remiddi) · How AI Agents Work: Prompt, Context, Harness & Loop Explained (JetBrains) · … (+4 more in the registry) |
| 7 | off-topic for s2: coding-agent or specific-tool usage; s17 territory or product tutorial | Master Context in Claude Code in 5 Minutes (GritAI Studio) · OpenClaw Lossless Context: How It Works (Ray Fernando) · Context Window Management in Claude Code | CampusX (CampusX) · The Hidden Cost of Claude Code (Prompt Caching Explained) (Cathy Cranberry) · 10. Headroom CacheAligner Explained | Boost LLM Cache Hit Rates & Redu (Micro Learning) · … (+2 more in the registry) |
| 7 | vendor event or panel; no original contribution beyond the primary sources selected | The Context Layer: Building Context-Aware AI with Collate, Graphwise,  (Data Science Connect) · Context Engineering for Reliable AI Agents on Databricks (Databricks Events) · The Context Layer : The Missing Architecture Tier in Enterprise AI (IEEE AI Native & Networking Technical Group ) · NODES AI 2026 - Build Intelligent AI Agents With Context Engineering (Neo4j) · From Context Engineering to AI Agent Harnesses: The New Software Disci (Delphina) · … (+2 more in the registry) |
| 6 | corporate explainer; three representative IBM videos selected for s2 (prompt caching, CAG vs long context, is RAG still needed) | How RAG, GraphRAG, and Context Engineering Improve AI Performance (IBM Technology) · RAG vs Direct Context: Choosing the Right LLM Strategy in Practice (IBM Developer) · How Context Engineering Improves AI Coding Agents (IBM Developer) · How to Pass Context in an Agentic AI Flow (IBM Technology) · What Is Context Engineering? Why It Matters for AI Agents (IBM Technology) · … (+1 more in the registry) |
| 4 | interview-prep / lecture-series re-explanation; no original contribution | Lecture-14: Architecting Context & Memory in Conversational AI Systems (SkillBakery Studio) · Ep 9: Conversational AI Platform Design | Agentic AI Interview Prep (Agentic AI World) · Ep 142: Long Context vs RAG - Which One Actually Wins | LLM Mastery Po (carlos Hernandez) · AI Cost Optimization | Episode_05 | Reduce Output Tokens- Max_Tokens (Human Mimics AI) |

Podcast episodes matched by the RSS pass and **not** taken: Latent Space "[State of Post-Training] … Token Efficiency — Josh McGrath, OpenAI" (2025-12) → parked s16; "Cline: the open source coding agent that doesn't cut costs" (2025-07) → parked s17; "Shopify's AI Phase Transition" (2026-04), "Notion's Token Town" (2026-04, already applied in s12), "Extreme Harness Engineering for Token Billionaires" (2026-04, harness → already covered by principle 02 sources), "Agent Memory: The Last Battleground" (2026-04, parked s5), "Stop Token Maxxing" (2026-06, parked s16). AI Engineering Podcast: no matching episode in the window.

## 5. Still to do for this module

- [x] Digest (step 3) → `sources/2026-09-27-s02-context-caching-digest.md`.
- [x] KB changes (step 4) as the digest's impact table says.
- [ ] After LIDR session 2 (2026-10-22): ingest LIDR material, compare, promote the principle.

## 6. Raw notes

`sources/raw/2026-09-27-market-scan-s02-context-caching/` — 16 transcripts + `youtube-search-results.json`.
