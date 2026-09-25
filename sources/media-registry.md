---
title: "Media registry — every video and podcast episode ever considered by this KB, with its status (transcribed / applied / candidate / discarded) and reason"
type: source
status: current
date: 2026-09-24
tags: [media-registry, market-scan, youtube, podcasts, tracking]
sources:
  - sources/media-registry.json
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Media registry (human view)

**Machine source of truth:** `sources/media-registry.json`. This file is a generated, readable view; regenerate it after every change to the JSON (the snippet is in `playbooks/scan-market-for-module.md`, step "Track"). Filter new scans with `python3 scripts/scan-filter.py <scan.json>` so that items already decided here are never re-examined.

Statuses: **transcribed** — verbatim text in `sources/raw/`, digest pending · **digested** — a source entry has a full digest · **applied** — the knowledge reached `principles/` / `practices/` · **candidate** — parked on purpose for a named module · **discarded** — do not re-consider unless the reason no longer holds (e.g. the channel later publishes primary-source material).

Updated: 2026-09-24. Totals: applied 5, candidate 17, discarded 92, transcribed 15.


## applied (5)

| Title | Channel | Published | Module | Reason / note | Decided | Link |
|---|---|---|---|---|---|---|
| Harness Engineering: Las 5 áreas clave para controlar y guiar a tus Agentes IA | LIDR - Carreras potenciadas por IA | 2026-09 | workshop-2026-09-08 | LIDR harness workshop; digested into principles 00-09 | 2026-09-08 | https://www.youtube.com/watch?v=fCkTax4WfRA |
| How to Use MCP Servers in Cursor | LIDR - Carreras potenciadas por IA | 2026-09 | workshop-2026-09-08 | LIDR harness workshop; digested into principles 00-09 | 2026-09-08 | https://www.youtube.com/watch?v=5s-lvoJpMTY |
| Programa como un Senior con IA usando Context Engineering | LIDR - Carreras potenciadas por IA | 2026-09 | workshop-2026-09-08 | LIDR harness workshop; digested into principles 00-09 | 2026-09-08 | https://www.youtube.com/watch?v=okYRbetLh7M |
| Spec-Driven Development: Cómo escalar tu productividad con IA y Contexto (prompts & settings) | LIDR - Carreras potenciadas por IA | 2026-09 | workshop-2026-09-08 | LIDR harness workshop; digested into principles 00-09 | 2026-09-08 | https://www.youtube.com/watch?v=eca3lWJgRmA |
| ¿Qué es un Agentic Engineer? El rol de software más demandado hoy | LIDR - Carreras potenciadas por IA | 2026-09 | workshop-2026-09-08 | LIDR harness workshop; digested into principles 00-09 | 2026-09-08 | https://www.youtube.com/watch?v=rdrtQyGhjYE |

## transcribed (15)

| Title | Channel | Published | Module | Reason / note | Decided | Link |
|---|---|---|---|---|---|---|
| 5 Ways to Connect AI Agents to Tools: From APIs to MCP | IBM Technology | 2026-08-16 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=BHGTA6ZEls4 |
| AI Foundations: Tool Calling | Cursor | 2025-09-27 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=byR5YVesMeg |
| AI agents explained: Build your first agent in 8 minutes | Google Cloud Tech | 2026-06-10 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=Zqno_vux6d8 |
| Agent Harness explained in 8min | Caleb Writes Code | 2026-05-22 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=1a1VXDdIyrk |
| Building Agentic RAG From Scratch in Pure Python | Dave Ebbelaar | 2026-05-10 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=RxwjoegpI98 |
| Building Agents with Model Context Protocol — Full Workshop with Mahesh Murag | AI Engineer | 2025-03-01 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=kQmXtrmQ5Zg |
| Building more effective AI agents | Anthropic | 2025-10-17 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=uhJJgc-0iTQ |
| How Model Context Protocol (MCP) actually works | Google Cloud Tech | 2026-06-24 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=cGuyrANVi4A |
| How We Build Effective Agents: Barry Zhang, Anthropic | AI Engineer | 2025-03-01 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=D7_ipDqhtwk |
| MCP in Claude Code | Claude | 2026-05-09 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=kkBFmwkDzdo |
| Notion's Sarah Sachs & Simon Last on Custom Agents, Evals, and the Future of Work (Latent Space podcast) | Latent Space | 2026-04-15 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=ATt7QJgt-2k |
| Skills vs MCP vs RAG vs Memory: What AI Agents Need to Know | IBM Technology | 2026-09-03 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=X4FVEEegCbk |
| Stanford CME295 Autumn 2025 — Lecture 7: Agentic LLMs | Stanford Online | 2025-11-18 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=h-7S6HNq0Vg |
| Tips for building AI agents | Anthropic | 2025-02-01 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=LP5OCa20Zpg |
| What's next for AI agentic workflows ft. Andrew Ng | Sequoia Capital | 2024-03-26 | s12 | selected by authority test | 2026-09-24 | https://www.youtube.com/watch?v=sal78ACtGTc |

## candidate (17)

| Title | Channel | Published | Module | Reason / note | Decided | Link |
|---|---|---|---|---|---|---|
| How do thinking and reasoning models work? | Google for Developers | 2025-12-03 | s1 | parked for module s1 | 2026-09-24 | https://www.youtube.com/watch?v=xCRvOUykOX0 |
| Building Production-Ready AI Agents with Pydantic AI | AI Engineering Podcast | 2025-10-07 | s13 | parked for module s13 | 2026-09-24 | https://www.aiengineeringpodcast.com/pydantic-ai-type-safe-agent-framework-episode-63 |
| The Age of Async Agents — Cognition & OpenInspect | Latent Space | 2026-05-28 | s13 | parked for module s13 | 2026-09-24 | https://www.latent.space/p/cognition |
| Giving Agents Computers — Daytona | Latent Space | 2026-05-21 | s14 | parked for module s14 | 2026-09-24 | https://www.latent.space/p/daytona |
| Harness Engineering for Reliable, Governed AI Agents | AI Engineering Podcast | 2026-09-19 | s14 | parked for module s14 | 2026-09-24 | https://www.aiengineeringpodcast.com/trueforge-ai-agent-harness-engineering-episode-79 |
| MCP as the API for AI-Native Systems: Security, Orchestration, and Scale | AI Engineering Podcast | 2025-12-16 | s14 | parked for module s14 | 2026-09-24 | https://www.aiengineeringpodcast.com/stacklok-toolhive-mcp-curation-episode-71 |
| You Can't Secure an AI Agent with Software | Chain of Thought | 2026-07-01 | s14 | parked for module s14 | 2026-09-24 | https://share.transistor.fm/s/bbbcbe24 |
| Railway: The Agent-Native Cloud | Latent Space | 2026-05-20 | s15 | parked for module s15 | 2026-09-24 | https://www.latent.space/p/railway |
| Why AI Infrastructure must evolve for Agent Experience — Modal | Latent Space | 2026-07-08 | s15 | parked for module s15 | 2026-09-24 | https://www.latent.space/p/modal2026 |
| Every AI Agent Has an Evaluation Gap — Alex Ratner | Chain of Thought | 2026-04-29 | s16 | parked for module s16 | 2026-09-24 | https://share.transistor.fm/s/18593a4c |
| Designing Scalable AI Systems with FastMCP | AI Engineering Podcast | 2025-08-26 | s17 | parked for module s17 | 2026-09-24 | https://www.aiengineeringpodcast.com/fastmcp-ai-tools-integration-episode-58 |
| Extreme Harness Engineering for Token Billionaires — Ryan Lopopolo, OpenAI | Latent Space | 2026-04-07 | s17 | parked for module s17 | 2026-09-24 | https://www.latent.space/p/harness-eng |
| GitHub's plan for Agents — Kyle Daigle | Latent Space | 2026-06-02 | s17 | parked for module s17 | 2026-09-24 | https://www.latent.space/p/github |
| Context Poisoning is Killing Your AI Agents | Chain of Thought | 2026-03-25 | s2 | parked for module s2 | 2026-09-24 | https://share.transistor.fm/s/e9df3b6f |
| Is RAG Still Needed? Choosing the Best Approach for LLMs | IBM Technology | 2026-03-09 | s2 | parked for module s2 | 2026-09-24 | https://www.youtube.com/watch?v=UabBYexBD4k |
| Agent Memory: The Last Battleground in the AI Stack — Richmond Alake | Chain of Thought | 2026-04-02 | s5 | parked for module s5 | 2026-09-24 | https://share.transistor.fm/s/964292e1 |
| Stanford CS230 / Autumn 2025 / Lecture 8: Agents, Prompts, and RAG | Stanford Online | 2025-11-21 | s9 | parked for module s9 | 2026-09-24 | https://www.youtube.com/watch?v=k1njvbBmfsw |

## discarded (92)

| Title | Channel | Published | Module | Reason / note | Decided | Link |
|---|---|---|---|---|---|---|
| #11 ReAct Framework Explained 🤖 / How AI Agents Reason & Act | Tech With Mala | 2026-01-30 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=QczejEN_LsA |
| 4 AI Agents To Automate 99% Of Your Life | Sandeep Swadia | 2026-07-30 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=TL8V41Ea6oM |
| 5 Best Practices for Building AI Agent Skills | IBM Technology | 2026-08-10 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=qYNs80FKIVc |
| 5-Getting Started With Agentic RAG With Detailed Implementation Using LangGraph | Krish Naik | 2025-10-14 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=Chl-cRcwVpA |
| 9. ReAct Prompting Explained: The Foundation of AI Agents & Tool Calling (2026) | Micro Learning | 2026-07-11 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=X4to5jRLEDE |
| AI AGENTS MASTERCLASS 4 HOURS: Build & Sell (2026) | Michele Torti | 2026-07-28 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=0C6xYvQhjwQ |
| AI Agent Full Tutorial for Beginners 2026: How to Build AI Agents in Minutes | Mikey No Code | 2026-03-23 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=C05XDMGaAn8 |
| AI Agent Tool Use — Routing Is the Real Bottleneck | Multi-Agent Academy | 2026-07-13 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=OIPIEiBTyyg |
| AI Agentic Design Patterns: ReAct Explained / Reasoning + Acting in AI Agents | CodeCraft Academy | 2026-02-26 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=WBgI9ce_7wM |
| AI Agents + LLM Reasoning: Transforming Autonomous Workflows | IBM Technology | 2025-10-23 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=2ihEirLXeas |
| AI Agents Explained - What Is an AI Agent and how to build one? (Real Examples, Not Hype) | Tech With Tim | 2026-07-16 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=ZvDkJsKE80k |
| AI Agents Explained for Beginners (And How to Build One) | Roboverse | 2026-08-26 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=HTNz4L2XM58 |
| AI Agents Explained: Build Your First One in 2026 | Roboverse | 2026-07-07 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=-Zhntlk0v80 |
| AI Agents Explained: How to Create and Use AI Agents in 2026 | AI Master | 2026-05-13 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=4TvH-OZhwxI |
| AI Agents Full Course 2026: Master Agentic AI (2 Hours) | Nick Saraev | 2026-03-08 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=EsTrWCV0Ph4 |
| AI Voice Agent Course / #12 Tool Calling & Function Access (Voice Agent Actions) | AgenticXLab | 2026-04-24 | s12 | off-topic: voice agents | 2026-09-24 | https://www.youtube.com/watch?v=zEreig4ny7U |
| Agentic RAG Tutorial: RAG That Fixes Its Own Answers | Oxylabs | 2026-09-09 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=tbkU0EvGPGU |
| Agentic RAG with MCP - building an Expert Agent in 12 minutes | Edward Donner | 2026-05-13 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=KdKqMfs-8gs |
| Anatomy of AI Agents: Inside LLMs, RAG Systems, & Generative AI | IBM Technology | 2025-12-11 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=CAKGKkWf0tI |
| Anatomy of an AI Agent | That AI Agent | 2025-11-22 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=uXI7cv8xs40 |
| Anatomy of an AI Agent | Close Win | 2025-10-27 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=UHWu3FlnLRI |
| Anatomy of an AI Agent | Load Lobrau | 2026-03-12 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=OAf2etjxNOM |
| Anatomy of an AI Agent: Sensors, Actuators & Environments Explained | Agentic Minds | 2026-08-03 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=B1kFPFCBsi8 |
| Anthropic killed Tool calling | AI Jason | 2026-02-22 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=3wglqgskzjQ |
| Beginners Guide To Build & Sell AI Agents in 2026 | Zack Kirk | 2026-02-23 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=OqKBOLplDZ8 |
| Build AI Agents in Joule Studio / SAP Sapphire Madrid 2026 | SAP | 2026-05-21 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=i4bqqTehbhM |
| Build a 100% Local Tool-Calling AI Agent with Python & Ollama (No API Keys) | Codernex | 2026-08-27 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=z9FZABTeeBs |
| Build a Local AI Agent in 10 Minutes using Python | Tech With Tim | 2026-09-11 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=ByWCsa8DbF8 |
| Build a Multi Tool AI Agent in Python  Function Calling & Tool Calling Explained | Dhaarani – The Practical AI Dev | 2026-07-03 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=cUfjql072N8 |
| Build a ReAct Agent in Python Step by Step / LLM + Tools Explained | DATA JARVIS | 2026-05-11 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=XQEXdZOMj4Q |
| Build an Agentic RAG Pipeline with LangGraph + ChromaDB (Step-by-Step Tutorial) | AI Bites | 2025-12-10 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=oo4OeE3yVBI |
| Building AI Agents that actually work (Full Course) | Greg Isenberg | 2026-03-17 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=eA9Zf2-qYYM |
| Building Agents LLM Autonomy / AI Agents + LLM Reasoning: Transforming Autonomous Workflows | S3CloudHub | 2025-12-01 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=v_mw4aSLKGY |
| Building an AI Agent That Uses Real Tools (Function Calling) | Xavier Fok | 2026-07-15 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=42JPAX9MUAk |
| Day 31 - Anatomy of an AI Agent: How Autonomous Systems Learn to Think and Act | Festive Tech Calendar | 2025-12-31 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=JmPBcLcwFHQ |
| Don't learn AI Agents without Learning these Fundamentals | KodeKloud | 2025-10-21 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=ZaPbP9DwBOE |
| Fix Voice Agent Tool Call Latency With Async Function Tools | LiveKit | 2026-07-07 | s12 | off-topic: voice agents | 2026-09-24 | https://www.youtube.com/watch?v=AQZOIr3511U |
| Give your voice AI agent real abilities (tool calling) | Google Cloud Tech | 2026-09-23 | s12 | off-topic: voice agents | 2026-09-24 | https://www.youtube.com/watch?v=Sdrpso7IKtU |
| Giving AI Hands: Function Calling & Tool Execution Masterclass / Ep 02 | Insight Ops | 2026-09-22 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=kMyN5LF1BrE |
| How AI Agents Actually Work (Every Piece Explained & Built) | Tech With Tim | 2026-09-03 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=HzGOWq5UyjY |
| How AI Thinks: Mastering Planning & Reasoning in Agentic AI (CoT & ReAct) | SH AI Academy | 2025-12-18 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=PIv5NV9iDXQ |
| How I Built an AI Agent in 14 minutes as A Beginner (2026) | Mikey No Code | 2026-07-27 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=UyoVmQLekBc |
| How to Build & Sell AI Agents in 2026: Ultimate Beginner’s Guide | Liam Ottley | 2026-03-22 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=AYQtRqW1xX4 |
| How to Build AI Agents in Python - 3 Ways | Tech With Tim | 2026-09-23 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=-RTgK6qX6A8 |
| How to Build an AI Agent with Claude Code (Claude AI Agent Tutorial) | AI Master | 2026-06-30 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=bcM9dP_uXJU |
| How to Set Up AI Agents in 2026 (Use this FREE AI Tool) | Youri van Hofwegen | 2026-09-05 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=qfXxWLxNGuM |
| How to Set Up your First AI Agent in 2026 (Step by Step) | Youri van Hofwegen | 2026-04-13 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=vJTEyamAxFk |
| How to Use the Call n8n Workflow Tool Inside the AI Agent | Ryan & Matt Data Science | 2025-11-20 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=sHQQloMG-Fc |
| How to build an AI Agent and MCP Server (step-by-step) | Google Cloud Tech | 2026-06-18 | s12 | not selected in s12 authority pass | 2026-09-24 | https://www.youtube.com/watch?v=wBnnA8aIxUs |
| Hugging Face Agents Course / Thought: Internal Reasoning and the ReAct Approach Part 2 🧠⚙️ | codeManS | 2026-05-27 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=Az4ORALeoVo |
| Intro to MCP Servers – Model Context Protocol with Python Course | freeCodeCamp.org | 2025-10-15 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=DosHnyq78xY |
| Lesson 02 AI Agent Tool Use Function Calls | Stephen Blum | 2026-09-15 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=5HgVRv37E_U |
| MCP Complete Explanation | Aishwarya Srinivasan | 2026-07-25 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=_fzpnqt39jQ |
| MCP In 26 Minutes (Model Context Protocol) | Tina Huang | 2025-10-15 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=kOhLoixrJXo |
| MCP is Dead - Why no one uses Model Context Protocol! | Piyush Garg | 2026-04-26 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=sPtTDDXsew0 |
| MCP vs Function Calling explainer | AlgoFox | 2026-09-24 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=Nci--nlB8CM |
| MCP vs Skills: Which Is Right for Your AI Agent and LLMs? | IBM Technology | 2026-07-07 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=goU9VIXA8II |
| MCP vs gRPC: How AI Agents & LLMs Connect to Tools & Data | IBM Technology | 2025-10-13 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=23PzNxw11jc |
| MCP vs. RAG: How AI Agents & LLMs Connect to Data | IBM Technology | 2025-11-17 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=X95MFcYH1_s |
| Model Context Protocol (MCP) Explained: Give Your AI Access to Tools 🚀 | The Setup Academy | 2026-09-24 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=SGsoonwLI6c |
| Module 2: How Agent Tool Calling Works | TechForge | 2026-09-06 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=roCnw07Drlc |
| Planning Agents — ReAct, Plan-and-Execute and When Each Wins / datarekha | datarekha | 2026-07-06 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=JKz-O-OaRJk |
| RAG & MCP Fundamentals – A Hands-On Crash Course | freeCodeCamp.org | 2026-01-22 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=I7_WXKhyGms |
| RAG vs Agentic AI: How LLMs Connect Data for Smarter AI | IBM Technology | 2025-12-08 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=fB2JQXEH_94 |
| RAG's Evolution: From Simple Retrieval to Agentic AI | IBM Technology | 2026-05-05 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=JB2P5Gk23VI |
| ReAct Prompting: Synergizing Reasoning and Acting in LLMs | AI Explained in 5 Minutes | 2026-04-06 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=7LsMd9icgVU |
| ReAct vs Plan-and-Execute for AI Agents | What's AI by Louis-François Bouchard | 2026-03-02 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=Y-VCZ_KTuzo |
| ReAct vs ReWOO: Choosing the Right LLM Agent Reasoning Pattern / Agentic AI & Cloud Advisory | Agentic AI & Cloud Advisory | 2026-08-23 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=LLUCyGbyCXA |
| STOP Building AI Agents. Do THIS Instead. | Zubair Trabzada | AI Workshop | 2026-03-05 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=wqH1hTkA6qg |
| Stop Using AI Wrong — Agentic AI vs RAG Explained | Nana Janashia | 2026-06-23 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=PmpFmclctuM |
| The 7 Skills You Need to Build AI Agents | IBM Technology | 2026-04-14 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=mtiOK2QG9Q0 |
| The Anatomy of AI Agents | Student O.S (One Stop) | 2026-08-01 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=HxxoqKV6_WQ |
| The Anatomy of an AI Agent | Voxel51 | 2026-04-22 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=4_JGRGX2zxo |
| The Anatomy of an AI Agent | Benn253 | 2026-05-26 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=yHwi1jq-oqE |
| The Anatomy of an AI Agent in 2026 | Ram Vegiraju | 2026-04-16 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=CyB7jpMt144 |
| The Anatomy of an [Enterprise] AI Agent | SAS Software | 2026-05-14 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=IgbXfSdeV4c |
| The Complete Agentic RAG Build: 8 Modules, 2+ Hours, Full Stack | The AI Automators | 2026-01-28 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=xgPWCuqLoek |
| The Complete Guide to AI Agents in 2026 (And How to Actually Use Them) | Tech With Tim | 2026-05-21 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=LNkAW4SSgdY |
| The EASIEST Way to Build a Copilot Agent (NEW Agent Builder Tutorial) | Collaboration Simplified | 2026-02-28 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=9_Dw9qcjLgA |
| The Missing Piece That Makes RAG "Agentic" | Edward Donner | 2026-04-15 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=K6wpRkJrcpM |
| The Secret Anatomy of AI Agents Explained | cholakovit | 2026-04-06 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=gHVUMvx_VCc |
| Tool Based Agents & Function Calling / AI Agent Patterns #2 | Lightboarding Tech | 2026-08-14 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=JU8tQ8AyU-A |
| Tool Calling VS MCP in AI Agents / Model Context Protocol Explained | Piyush Garg | 2025-09-25 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=TlIOk8VuEBU |
| Waypoint-1 Explained: Agent Foundation Model for LLM Reasoning Planning and Tool Use | CosmoX | 2026-01-28 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=81i076H5hDE |
| What AI Agent Skills Are and How They Work | IBM Technology | 2026-04-20 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=Lg-meK5IU8Q |
| What is OpenClaw? Inside AI Agents, LLMs and the Agentic Loop | IBM Technology | 2026-04-27 | s12 | corporate explainer; two representative IBM videos already selected | 2026-09-24 | https://www.youtube.com/watch?v=L7FF8Zgab3M |
| Why I switched my RAG decisions to Jev... | The AI Automators | 2026-09-24 | s12 | education/opinion channel; no original contribution beyond primary sources selected | 2026-09-24 | https://www.youtube.com/watch?v=olIve0D8pJQ |
| You’re Not Behind (Yet): How to Build AI Agents in 2026 (no coding) | Futurepedia | 2026-02-21 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=ibFJ--CH3cQ |
| You’re Not Behind (Yet): How to Build Your First AI Agent (Full Guide) | Dan Martell | 2026-07-15 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=Bm84BAtOfQw |
| n8n Tutorial for Beginners 2026: How to Build AI Agents | Youri van Hofwegen | 2025-12-04 | s12 | no-code / marketing / product demo | 2026-09-24 | https://www.youtube.com/watch?v=TKnaDGpN7Ns |
| 工业级实战：从传统RAG到Agentic RAG的进阶优化！ | 白白说大模型 | 2026-01-09 | s12 | not English/Spanish | 2026-09-24 | https://www.youtube.com/watch?v=UZs_yOKcw7A |
| 🤖 ReAct Design Pattern for AI Agents (Reason–Act–Observe) | BioinfQuests | 2026-01-13 | s12 | below reach/authority floor (<5k subs or <500 views), re-explanation | 2026-09-24 | https://www.youtube.com/watch?v=2sEFIziDba4 |
