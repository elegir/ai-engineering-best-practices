---
title: "Market scan — course session 1 'LLMs and environment setup': which videos and podcasts were considered, selected and transcribed"
type: source
status: current
date: 2026-09-27
tags: [market-scan, llm-api, prompting, tokens, context-window, providers, s1, lidr-ai-engineering]
sources:
  - sources/raw/2026-09-27-market-scan-s01-llm-setup/
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 1: LLMs and environment setup

**What this file is.** The log of the scan (steps 1–2 of the four-step module cycle): what was searched, what was found, what was selected by the authority test, what was discarded and why. The digest (step 3) and the KB changes (step 4) are in `sources/2026-09-27-s01-llm-setup-digest.md`.

## 1. Context

- **Topic map (LIDR session 1, 2026-10-15).** Communication with models and the structure of a call · managing prompts, tokens and responses · the provider ecosystem and selection criteria · analysis of real architectures and practical cases.
- **Written canon** catalogued 2026-09-24 in the Claude Project doc `curso-fuentes-sesiones-01-05.md` (Claude/OpenAI/Gemini platform docs, Karpathy, Chip Huyen, Lilian Weng, Applied LLMs, Anthropic Academy courses).
- **Method** (`playbooks/scan-market-for-module.md`): `streamers/youtube-scraper` run `BwTdh891dMcyydwAa`, 7 queries × 15, last 12 months, relevance → **105 videos**; `scripts/scan-filter.py` → **102 new, 1 parked candidate (s2), 2 already decided**. RSS of Latent Space, AI Engineering Podcast and Chain of Thought filtered for API / prompt / token / provider / model terms → 25 episodes read, 1 selected, 6 parked. Transcripts via `johnvc/YoutubeTranscripts` runs `SYCYYUrejAcI74HPy` and `LU2VQxyeEWUXZeYxi`: **13 items, ≈709,000 characters, ≈9 h 20 min**.
- **Queries.** "how LLM API calls work messages system prompt", "Claude API tutorial for developers", "OpenAI Responses API tutorial", "prompt engineering for developers 2026", "tokens context window explained developers", "choosing an LLM provider Anthropic OpenAI Gemini comparison for developers", "LLM application architecture production case study".
- **What the search taught.** The query "Claude API tutorial" returns mostly Claude *Code* tutorials (the coding agent), which are session-17 material; "choosing an LLM provider" returns consumer $20-plan comparisons, not developer criteria. Both are recorded as discard reasons so the next scan can phrase the queries better ("Claude Messages API", "LLM provider selection for developers latency price").

## 2. Selection criteria

The authority test of the pilot (`sources/2026-09-24-market-scan-s12-intro-to-agents.md` §2): primary source > academic or reference course > recognised practitioner or reference podcast > corporate explainer > trend signal. Discard by rule: consumer product comparisons, career/marketing content, coding-agent tutorials (off-topic for this session), re-uploads, low-reach re-explanations.

## 3. Selected — transcribed (13)

| # | Title | Channel | Date | Length | Authority | Session bullet | Raw file |
|---|---|---|---|---|---|---|---|
| 1 | Build Hour: Responses API | OpenAI (official) | 2025-10-14 | 51m | 1 — primary | call structure; responses; tools | `yt-hNr5EebepYs-…` |
| 2 | Building with MCP and the Claude API | Anthropic (official) | 2025-10-09 | 26m | 1 — primary | call structure; Claude Messages API | `yt-aZLr962R6Ag-…` |
| 3 | Prompting 101 (Code w/ Claude) | Anthropic (official) | 2025-05-22 | 25m | 1 — primary, canon (>12 months) | prompts | `yt-ysPbXH0LpIE-…` |
| 4 | AI prompt engineering: a deep dive | Anthropic (official) | 2024-09-04 | 1h17 | 1 — primary, canon | prompts | `yt-T9aRN5JkmL8-…` |
| 5 | AI Foundations: Tokens & Pricing | Cursor (official) | 2025-09-27 | 3m34 | 1 — vendor | tokens | `yt-Gauk0F6UBFo-…` |
| 6 | How to write better AI prompts as a software developer in 2026 | JetBrains (official) | 2026-02-02 | 4m | 1 — vendor | prompts | `yt---XpNP6NsqE-…` |
| 7 | Full AI Prompting Course with Andrew Ng | DeepLearning.AI | 2026-05-18 | 2h29 | 2/3 — reference course | prompts; tokens; responses | `yt-8ib4Qnh2HFE-…` |
| 8 | Intro to Large Language Models | Andrej Karpathy | 2023-11-22 | 1h | 3 — canon (>12 months) | what a model is; providers | `yt-zjkBMFhNj_g-…` |
| 9 | Deep Dive into LLMs like ChatGPT | Andrej Karpathy | 2025-02-05 | 3h31 | 3 — canon (>12 months) | tokens; training → why parameters matter | `yt-7xTGNNLPyMI-…` |
| 10 | Most devs don't understand how context windows work | Matt Pocock | 2025-10-22 | 9m | 3 — practitioner | tokens; context | `yt--uW5-TaVXu4-…` |
| 11 | Open Responses — the new standard API for open models | Sam Witteveen | 2026-01-20 | 16m | 3 — practitioner | provider ecosystem; API standards | `yt-b-BzeHF6WLA-…` |
| 12 | What is an AI stack? | IBM Technology | 2025-11-03 | 9m | 4 — corporate explainer | real architectures | `yt-RRKwmeyIc24-…` |
| 13 | Why LLMs are plausibility engines, not truth engines — Dan Klein | Chain of Thought (podcast, YouTube version) | 2026-04-08 | 1h18 | 3 — reference podcast | what a model is; responses | `podcast-2HwtyPE6JuQ-…` |

Items 3, 4, 8, 9 are older than 12 months and were added from the written canon.

## 4. Considered — not transcribed

94 YouTube items discarded, all registered with a reason in `sources/media-registry.json`. Grouped:

| # | Reason | Examples |
|---|---|---|
| 33 | below reach/authority floor (<5k subs or <500 views), re-explanation | OpenAI featured my app. Here's how I use Responses API. (meremortaldev) · Ep 06 | Structured Outputs: Stop Regexing LLM Responses (JSON Schema + (@TechLifeWithAI) · OpenAI API Quickstart with JavaScript: Your First API Call in Node.js (Build with Joon) · Ep 04 | Calling LLM APIs the Right Way: Messages, System Prompts, Temp (@TechLifeWithAI) · Ep 02 | LLM Costs Explained: Tokens, Context Windows, and Caching for  (@TechLifeWithAI) · How Large Language Models LLMs Work Explained | Tokens, Context Window (AI Hints) · … (+27 more in the registry) |
| 26 | education/opinion channel; no original contribution beyond the primary sources selected | 🛠️ OpenAI Responses API in Python | Switching from Chat Completions fo (Super Data Science) · Claude API Crash Course #1 - Introduction & Setup (Net Ninja) · Agent AI System Design Explained in 27 Minutes (Aishwarya Srinivasan) · Demo to Production. Architect a Real Agentic AI System (Step by Step) (Applied with AI - Sanjay Kumar) · OpenAI API Tutorial: Handling Chat Completions & Markdown in Python (Super Data Science) · The Ultimate Beginner’s Guide to Claude AI (Metics Media) · … (+20 more in the registry) |
| 9 | consumer plan/product comparison, not provider selection for developers | ChatGPT vs Claude vs Gemini: Which $20 AI Plan Is Worth It? (Parker Prompts) · ChatGPT, Claude, and Gemini: how to choose the right AI tool for real  (Leaders insights) · ChatGPT Plus vs Claude Pro vs Gemini Pro: The Best $20 AI Plan (Paul J Lipsky) · ChatGPT vs Claude vs Gemini  | Which AI Tool Wins? (Vishal Nagpal - TechIntel AI) · Claude vs ChatGPT vs Gemini: I Tested All 3 (2025 Results) (EKSATech) · LLM Tier List for Recruiters: Claude vs ChatGPT vs Gemini | HR Built W (The Talent Supply Chain) · … (+3 more in the registry) |
| 8 | off-topic for s1: Claude Code (coding agent) tutorial, not the API — belongs to s17 territory and is education content | 🚀 Audit Your Context Window Like a Pro | Track Every Claude Code Token (Technical Rajni) · Claude Code - Full Tutorial for Beginners (Tech With Tim) · Claude Code Crash Course For Developers (Traversy Media) · Learn 80% of Claude Code in 10 Minutes (2026 Tutorial) (Sajjaad Khader) · CLAUDE CODE FULL COURSE 4 HOURS: Build & Sell (2026) (Nick Saraev) · 1h Claude Code Crash Course For App Developers (Beginner Level) (Philipp Lackner) · … (+2 more in the registry) |
| 6 | off-topic: no-code platform, other platform, or interview prep | LLM Interview Prep: How to Explain Context Windows & Tokens Perfectly (Peetha Academy ) · Responses API - OpenAI node in n8n. How to use build-in node without h (Tech with Ilia) · How to Add OpenAI API Key for AI Agent || Enable AI-Powered Responses  (BotPenguin Customer Support) · ChatDatabricks Full Tutorial: Call LLMs on Databricks using LangChain (datageekrj) · Real-Time AI Responses in Bubble.io: OpenAI Streaming API Connector Se (Build With Lucas) · User Messages In LLM Apis Explained: A Simple Guide in Telugu (KKPBT Online Training by Vicky) |
| 4 | career/marketing content | How to Become a $300K AI Engineer in 2026 (Complete Roadmap) (Sajjaad Khader) · Is Software Engineering Dying in 2026? (What the Data Actually Says) (Tech With Tim) · I Have Spent 500+ Hours Programming With AI. This Is what I learned (The Coding Sloth) · You SUCK at Prompting AI (Here's the secret) (NetworkChuck) |
| 3 | not selected in s1 authority pass: overlaps a selected primary source | How an LLM Request Works? (lustoykov) · How LLM Tokens Work (Attention) (lustoykov) · Claude AI Tutorial for Beginners (Step-by-Step) (Kevin Stratvert) |
| 2 | official but a 1–2 minute product announcement; the Build Hour (selected) is the substantive source | GPT-Live-1 is now in the API (OpenAI) · Introducing the Agents API (OpenAI) |
| 2 | corporate explainer; one representative IBM video selected (AI stack); this one belongs to s13 (frameworks) or repeats | How to Use Agentic AI: LLMs, AI Agents & Prompt Engineering in Action (IBM Technology) · Agentic AI Frameworks Explained: Workflows, Multi-Agent, & Production (IBM Technology) |
| 1 | re-upload of a Stanford/Andrew Ng talk on an unofficial channel; use the official DeepLearning.AI course instead | Prompting Is Dead in 6 Months. Andrew Ng, Stanford (philia) |
Podcast episodes considered and parked (registered as `candidate`): Latent Space "The Inference Engineering Masterclass" (Baseten, 2026-08) → s15; "Why the Frontier Ecosystem must be Open" (Databricks, 2026-06) → s15; "Shopify's AI Phase Transition" (2026-04) → s16; AI Engineering Podcast "Operationalizing LLM Apps with OpenLit" (2026-02) → s15; "TensorZero LLM Gateway" (2025-01) → s3; Chain of Thought "Stop Token Maxxing" (2026-06) → s16. The parked s2 candidate that resurfaced (IBM "Is RAG still needed?") stays parked for s2.

## 5. Still to do for this module

- [x] Digest (step 3) → `sources/2026-09-27-s01-llm-setup-digest.md`.
- [x] KB changes (step 4) as the digest's impact table says.
- [ ] After LIDR session 1 (2026-10-15): ingest LIDR material, compare, promote the principle.

## 6. Raw notes

`sources/raw/2026-09-27-market-scan-s01-llm-setup/` — 13 transcripts + `youtube-search-results.json`.
