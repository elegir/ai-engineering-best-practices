---
title: "Market scan — course session 3 'Model wrappers and layered architecture': which videos, podcasts and written sources were considered, selected and transcribed"
type: source
status: current
date: 2026-09-30
tags: [market-scan, llm-gateway, routing, fallback, observability, streaming, semantic-cache, s3, lidr-ai-engineering]
sources:
  - sources/raw/2026-09-30-market-scan-s03-wrappers/
  - sources/catalog-written-canon.md
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 3: model wrappers and layered architecture

**What this file is.** The log of the scan (steps 1–2 of the four-step module cycle): what was searched, what was reused from earlier modules, what was found, what was selected by the authority test, what was discarded and why. The digest (step 3) and the KB changes (step 4) are in `sources/2026-09-30-s03-wrappers-digest.md`.

## 1. Context

- **Topic map (LIDR session 3, 2026-10-29).** Conversational interfaces (Streamlit and alternatives) · abstraction and automatic fallback between models (LiteLLM, OpenRouter, provider-agnostic SDKs) · intelligent caching, streaming and traceability · design patterns for scalable LLM systems.
- **Written canon** (step 1, registered 2026-09-30 in `sources/catalog-written-canon.md` §Session 3, 16 items): Streamlit and Gradio chat docs, LiteLLM Router and proxy-reliability docs, OpenRouter provider-routing and failover docs, Vercel AI SDK, Anthropic streaming and reduce-latency docs, OpenTelemetry GenAI semantic conventions, Langfuse docs, RedisVL semantic cache and the GPT Semantic Cache paper, 12-Factor Agents, DeepLearning.AI Streamlit course. Read for the digest: the OTel GenAI span spec (now in the `semantic-conventions-genai` repository; status *Development*), the LiteLLM Router page.
- **Reuse (step 1a, first module to apply it).** Transcripts from earlier modules that touch this one and were read again, not re-transcribed: Sam Witteveen *Open Responses* (s1 — API shapes and compatibility), OpenAI *Build Hour: Responses API* (s1 — typed streaming events), Dave Ebbelaar *Effective context engineering* (s2 — Langfuse tracing in practice), Lance Martin on Latent Space (s2 — provider caching behaviour), Notion on Latent Space (s12 — harness rebuilt five times, tool ownership). Their registry entries gain `s3` in `modules`.
- **Method** (`playbooks/scan-market-for-module.md`): `streamers/youtube-scraper` run `TUEUWfeOnH8zqeoAE`, 8 queries × 15, last 12 months, relevance → **118 videos**; `scripts/scan-filter.py` → **110 new, 1 parked candidate (Twilio gateway talk, taken), 7 already decided**. Title searches for two podcast episodes: run `uZvJMSBgZ7ovFMLbh`. RSS of Latent Space, AI Engineering Podcast and Chain of Thought filtered for gateway / routing / fallback / observability / caching / streaming terms → 9 matching episodes, 2 taken. Transcripts: `johnvc/YoutubeTranscripts` run `0ur5pjl6NEJw5Pd3s` (11 of 12 succeeded); `memo23/video-audio-transcriber` run `AeDomtuVdcZXbw9XD` (Whisper, 81 min of audio, the first use of the audio fallback: the Latent Space OpenRouter episode has no YouTube version). **13 items, ≈7 h 20 min.**
- **Queries.** "LLM gateway architecture fallback routing production", "LiteLLM vs OpenRouter model fallback", "provider-agnostic LLM SDK abstraction layer", "LLM observability tracing OpenTelemetry Langfuse", "semantic caching LLM responses", "streaming LLM responses architecture server-sent events", "Streamlit chat app LLM tutorial 2026", "layered architecture for LLM applications design patterns".
- **What the search taught.** This module's YouTube market is thin: the strongest material is conference talks (AI Engineer, EuroPython, PyCon DE, CNCF, Scala Days, API World) and founder panels, not channels. "LiteLLM vs OpenRouter" returns only small comparison channels — the vendors' docs and the OpenRouter founders on Latent Space are the authority. "Streamlit chat app" returns tutorials; the Streamlit docs are the canon and no video was selected for that bullet. "Layered architecture" returns generic software-architecture courses (Uplatz) — the useful layering material came from the gateway talks and 12-Factor Agents. One selected talk (NDC, Microsoft.Extensions.AI) had no extractable captions and is recorded as such.

## 2. Selection criteria

The authority test (`sources/2026-09-24-market-scan-s12-intro-to-agents.md` §2): primary source > academic or reference conference > recognised practitioner or reference podcast > corporate explainer > trend signal. One exception recorded: the API World talk is on a personal channel below the reach floor, but it is a conference talk on exactly this topic with a first-person production failure; taken as "conference" with the exception noted.

## 3. Selected — transcribed (13)

| # | Title | Channel | Date | Length | Authority | Session bullet | Raw file |
|---|---|---|---|---|---|---|---|
| 1 | Productionizing LLM Gateways: architecture, trade-offs and hard lessons — Kanish Manuja (Twilio) | AI Engineer (conference) | 2026-06 | 16m23 | 2 — reference conference | fallback; streaming; guardrail placement | `yt-zrZ1amZBSPw-…` |
| 2 | 12-Factor Agents: patterns of reliable LLM applications — Dex Horthy | AI Engineer (conference) | 2025-06-17 | 17m02 | 2/3 — conference + recognised practitioner (canon) | layered design; own prompts/context/control flow | `yt-8kMaTybvDUw-…` |
| 3 | Optimize your AI applications automatically with the TensorZero LLM gateway — Viraj Mehta | AI Engineering Podcast (Tobias Macey; YouTube version) | 2025-01-22 | 1h03 | 3 — reference podcast (parked by s1) | gateway responsibilities; typed LLM functions | `podcast-dVl5aQSQuhM-…` |
| 4 | OpenRouter: from Seed to Stripe — Alex Atallah & Anjney Midha | Latent Space (podcast; Whisper from RSS audio) | 2026-09-25 | 1h21 | 3 — reference podcast | routing across providers; fallback economics | `podcast-latent-space-openrouter-…` |
| 5 | Surviving LLM traffic spikes: routing, rate limits and failover in Python — Sergi Porta (ManyChat) | EuroPython (conference) | 2026-08-19 | 23m24 | 2 — conference, first-person case | LiteLLM router in production; tiers; retry multiplication | `yt-jwblSAaFnNc-…` |
| 6 | Designing an API layer for AI providers that won't stay put — Isadora Martin-Dye | API World (conference; personal channel) | 2026-09-07 | 26m20 | 2 — conference (reach-floor exception) | model retirement; routing by sensitivity; visibility | `yt-W48Oj-YCzrs-…` |
| 7 | Observability in AI, explained — Marc Klingen (Langfuse) & Jason Lopatecki (Arize) | Mastra (vendor event) | 2025-12-08 | 28m47 | 3 — founders of the two reference tools | traceability; evals online/offline | `yt-FnH9jmoUuss-…` |
| 8 | What is OTEL, and why does Langfuse speak it? | Langfuse (official) | 2026-07-23 | 3m54 | 1 — vendor | traceability; OTel model | `yt-joRiZICf_LM-…` |
| 9 | Langfuse, OpenLIT and Phoenix: observability for the GenAI era — Emanuel Fabani | PyCon DE (conference) | 2025-10-05 | 30m37 | 2 — conference, neutral practitioner | tracing in code; secrets in traces; gateway tracing | `yt-EE3xRZYRyyQ-…` |
| 10 | Panel: AI's real-time engine — gRPC, WebSockets or SSE? | CNCF (conference) | 2026-02-05 | 35m24 | 2 — conference panel | streaming transports | `yt-RJapRLPxqcg-…` |
| 11 | LLMs in the wild: streaming, RAG and real-time GenAI at scale — Muayad Sayed Ali (Writer) | Scala Days (conference) | 2025-11-26 | 43m05 | 2 — conference, vendor speaker | streaming through a gateway; mid-stream fallback | `yt-ZbcruZB7Irk-…` |
| 12 | Semantic caching with Valkey and Redis: reducing LLM cost and latency — Martin Visser | Percona (vendor) | 2026-01-23 | 26m20 | 4 — vendor explainer with demo | semantic cache mechanics and risks | `yt-7vdFUJgGOSs-…` |
| 13 | (reused) Open Responses; Build Hour Responses API; Ebbelaar; Lance Martin; Notion | s1 / s2 / s12 raw folders | — | — | — | API shapes; typed streaming events; tracing; provider caching; rebuilt harnesses | see §1 Reuse |

Items 2 and 3 are older than 12 months and were taken from the written canon / parked list.

## 4. Considered — not transcribed

98 YouTube items discarded, all registered with a reason in `sources/media-registry.json`. Grouped:

| # | Reason | Examples |
|---|---|---|
| 57 | below reach/authority floor (<5k subs or <500 views), re-explanation | Orchestrating Intelligence: Multi-Agentic Design Patterns for Producti (Developer Summit) · LLM and Agent Foundations Part 5: Patterns, Architecture, HLD & MVP (Core Concept Learning) · LLMOps Architecture Deep Dive | How Production LLM Systems Are Designe (StackOps AI) · Enterprise AI Architecture: The 3-Layer Framework That Stops Shadow AI (JanisExplains Architecture) · … (+53 more in the registry) |
| 15 | Streamlit/chatbot tutorial; the Streamlit docs and the DeepLearning.AI course (written canon) are the authority | 06 Add Chat Memory to a Local AI Assistant with Streamlit (EasyHarshMods) · Build a Local AI Chatbot with Streamlit & Ollama (Offline LLM) (DataNomus) · Build Your Own ChatGPT for FREE | TinyLlama + Streamlit Tutorial | No  (thecodeQ) · Build Your First AI Chatbot in 15 Minutes | Gemini API + Streamlit (St (AgentStax) · … (+11 more in the registry) |
| 11 | off-topic stack/format or language-specific course; no original contribution | S7 | Layered Architecture Pattern | SDA Best Practices | Uplatz (Uplatz) · Layered Design in Ruby on Rails: Scalable Architecture Patterns | Upla (Uplatz) · AI Architect Enterprise Complete | Full Course for Production AI Syste (Coding Fever • 1M) · Why Your HPC Integration Logic Is Broken (And How to Fix It) (FINOS) · … (+7 more in the registry) |
| 8 | tool-vs-tool comparison on a small channel; the vendors' own routing docs (written canon) and the Latent Space OpenRouter episode are the authority | OpenRouter vs LiteLLM: The $60,000 Routing Trap (Jono Finds) · OpenRouter vs LiteLLM Comparison 2026: API Features Overview and Perfo (Mariselle Hartwell) · Openrouter vs Litellm: Which Network Routing Software is BETTER in 202 (houdztech) · OpenRouter vs LiteLLM (2026) – Which AI Model Router Is Better for Dev (QuickTweak) · … (+4 more in the registry) |
| 5 | education/opinion channel; no original contribution beyond the primary sources selected | React Native AI: Bringing On-Device LLMs With AI SDK by Szymon Rybczak (Callstack) · OpenRouter Tutorial 2026: Connect to 400+ AI Models with One API Key (Ai Titan) · LLM Gateway: Build Production-Ready AI Apps 🔥 (DSwithBappy) · Stop Paying for the Same LLM Call Twice | Semantic Caching with Better (Applied with AI - Sanjay Kumar) · … (+1 more in the registry) |
| 1 | selected (NDC, Microsoft.Extensions.AI abstraction layer) but no transcript could be extracted (captions unavailable); re-try in a later scan | Easily Add GenAI to .NET Apps using Microsoft.Extensions.AI - Brandon  (NDC Conferences) |
| 1 | third-party 3-minute summary of a podcast episode; the episode itself was transcribed | Latent Space in 3 minutes: OpenRouter: from Seed to Stripe (The Daily  (The Daily FM) |

Parked for other modules from this scan (registered as `candidate`): Google Cloud Tech "AI agent design patterns" and IBM "Orchestrating complex AI workflows" → S13; "Mem0: long-term memory" → S5; two Claude Code / OpenClaw cost videos → S17. Podcast episodes matched and not taken: Latent Space "Why AI infrastructure must evolve for agent experience" (Modal, 2026-07) and "NVIDIA's AI engineers: agent inference at planetary scale" (2026-03) → parked S15; "DevDay 2025" → covered by s1; Chain of Thought "The critical infrastructure behind the AI boom" (Cisco) and "AI infrastructure & the evolution of RAG" (Weaviate, 2025-01) → not on topic (hardware; RAG → S9).

## 5. Still to do for this module

- [x] Digest (step 3) → `sources/2026-09-30-s03-wrappers-digest.md`.
- [x] KB changes (step 4) as the digest's impact table says.
- [ ] After LIDR session 3 (2026-10-29): ingest LIDR material, compare, promote the principle.

## 6. Raw notes

`sources/raw/2026-09-30-market-scan-s03-wrappers/` — 12 transcripts + `youtube-search-results.json`; the five reused transcripts stay in their original folders.
