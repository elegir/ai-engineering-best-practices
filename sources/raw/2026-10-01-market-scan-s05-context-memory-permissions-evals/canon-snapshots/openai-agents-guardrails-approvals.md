# Written-source snapshot — https://developers.openai.com/api/docs/guides/agents/guardrails-approvals

Fetched 2026-10-01 by the main session (curl; tags stripped). Verbatim text for the s5 digest; see the registry entry for status.

Guardrails and human review | OpenAI API

For the complete documentation index, see llms.txt . Markdown versions of documentation pages are available by appending
 .md to the page URL.
 Search the API docs Search docs Suggested responses create reasoning_effort realtime prompt caching Primary navigation Search docs Suggested responses create reasoning_effort realtime prompt caching Overview Models Agents Tools Audio & voice Production API reference Overview Models Agents Tools Audio & voice Production API reference Docs Agents Home Get started Quickstart Using GPT-6 Key concepts Core concepts Responses API Conversation state Background mode Streaming WebSocket mode Mid-turn steering Multi-agent Webhooks File inputs Compaction Counting tokens SDKs and CLI OpenAI SDK OpenAI CLI Resources Changelog Deprecations Supported countries OpenAI Crawlers Terms and policies Legacy APIs Agent Builder Overview Migration guide Node reference Safety in building agents Evals Getting started Working with evals Prompt optimizer External models Best practices Graders Fine-tuning Optimization cycle Supervised fine-tuning Vision fine-tuning Direct preference optimization Reinforcement fine-tuning RFT use cases Best practices Assistants API Migration guide Model catalog Choose a model Pricing Model selection Text and code Text generation Code generation Structured output Prompting Overview Prompt engineering Citation formatting Migration guide Prompt generation Frontend prompting Reasoning Reasoning models Reasoning best practices Images Images and vision Image input cost calculator Image generation Overview Image prompting Realtime and audio Audio and speech Getting started Voice agents Specialized models Deep research Embeddings Moderation Overview Agents API Overview Quickstart Architecture Configuring Agents Sessions Run and continue sessions Events and items Manage sessions Webhooks Environments and sandboxes OpenAI-hosted sandboxes Self-hosted sandboxes Sandbox lifecycle Sandbox security Files and artifacts Tools and integrations Web search Computer use Functions MCP connections Plugins Vaults Multi-agent Observability and usage Tracing Errors and recovery API reference Bedrock Managed Agents Agents SDK Overview Quickstart Agent definitions Models and providers Running agents Sandbox agents Orchestration Guardrails Results and state Integrations and observability Evaluate agent workflows ChatKit Overview Customize Widgets Actions Advanced integrations Overview Function calling Search and retrieval Web search File search Retrieval Connect tools and data MCP servers Secure MCP Tunnel Build tool workflows Skills Tool search Programmatic tool calling Async tool calling Computer and code Shell Computer use Apply Patch Local shell Code interpreter Media Image generation Overview GPT-Live Getting started Prompting Managing sessions Delegation and tools Migrate to GPT-Live Partner integrations Realtime API Getting started Prompting Managing conversations Voice activity detection Tools and MCP Build with voice Voice agents Custom voices Cost optimization Connections WebRTC WebRTC with WARP WebSockets Telephony and SIP Server-side controls Audio processing File transcription Live transcription Live translation Text to speech Audio in Chat Completions Go live Production best practices Deployment checklist Performance and quality Fast mode Ultrafast mode Latency optimization Predicted Outputs Accuracy optimization Cost and throughput Cost optimization Prompt caching Prompt cache diagnostics Batch Flex processing Safety and governance Safety best practices Red teaming Daybreak Safety checks Safety classifiers Cybersecurity checks Misalignment monitoring Under-18 guidance CSAM guidance Content provenance Your data Private Safety Processing Permissions Infrastructure and access Terraform provider Overview Projects and access Service accounts Rate limits and spend Model, tool, and data controls Import and reconciliation Private Link IP allowlist Organization blocking Mutual TLS Workload identity federation Federation rules X.509 certificates Kubernetes AWS Microsoft Azure Google Cloud Oracle Cloud Infrastructure GitHub Actions SPIFFE IP egress ranges Amazon Bedrock Operations Rate limits Spend limits Admin APIs Error codes Overview Sign in with ChatGPT Plugins Workspace Agents Commerce Ads ChatGPT + Codex user docs Use cases Overview Sign in with ChatGPT Plugins Workspace Agents Commerce Ads ChatGPT + Codex user docs Use cases Docs Overview Home Quickstart Request a client ID Identity On your website In your ChatGPT plugin ChatGPT plan usage Overview UI/UX guidelines Registration and sign-in Accounts and sessions Models and inference Codex app-server Self-hosted VMs Token reference Errors and recovery Preview limitations Home Quickstart Core concepts Plugin architecture Skills MCP server Plan Brainstorm use cases Define tools Build Build an MCP server Add UI to your MCP server (optional) Add events to your MCP server (optional) Extensions Authenticate users Build skills Package your plugin Examples Test and publish Connect and test your plugin Submit and publish Submission error reference Conversion specs Restaurant reservation spec Get Quote spec Product checkout spec Guides UI guidelines Optimize Metadata Submit a Claude Code plugin Security & Privacy Troubleshooting Resources Changelog Plugin guidelines MCP server review requirements Plugin UI reference Checkout API reference Home Get started Trigger workspace agent runs Authenticate with Workspace Agent access tokens Home Guides Get started Best practices File Upload Overview Products API Overview Feeds Products Promotions Ads Overview Measurement Measurement Pixel Multiple Pixels (Advanced) Image Tag Conversions API Supported Events Advertiser API Overview API Partner Setup Campaign Management Bidding & Budgets Targeting Product Feeds Hotel Feeds (limited beta) Conversion Tracking Reporting Troubleshooting Account Management API Reference Authentication Ad Account Audit Logs Campaigns Ad Groups Ads Insights Files Conversion Setup Overview Features Configuration Developers Security Administration Use Cases Resources Overview Features Configuration Developers Security Administration Use Cases Resources Docs Overview Home Get started Quickstart Use ChatGPT Get started with Work Meet dots Import from another agent Foundations Prompting Model selection Personalize ChatGPT Skills & Plugins Permissions Explore What's new Models Pricing Glossary Available on ChatGPT desktop app Remote ChatGPT on the web Codex CLI Codex IDE extension Codex Cloud Releases Changelog Feature Maturity Open Source Overview Workflows Projects and chats Sites Build plugins Visualizations Scheduled tasks Long-running work Notifications Pets Codex Micro Capabilities Browser Computer use Voice Plugins Sign in with ChatGPT Web search Image generation Image inputs Appshots Browser extension Work with files dots Meet dots Getting started Messaging Tasks and memory Computers and apps Controls ChatGPT Space Overview Getting started Pages Work with agents Collaboration Reference Commands Slash commands Settings Troubleshooting Overview Customization Overview Memories Computer History Config file Config Basics Advanced Config Config Reference Environment Variables Sample Config Agent configuration AGENTS.md Subagents Speed Rules Extend ChatGPT and Codex Record & Replay MCP Linux Desktop app Windows Desktop app Windows sandbox WSL Overview Development workflows Code review Integrated terminal Extend and automate Build skills Site tools (WebMCP) Annotations Extensibility Hooks Environments Modes Local environments Git worktrees Codex Cloud Cloud environments Build with Codex Codex SDK App Server GitHub Action Non-interactive mode Third-party integrations GitHub GitLab (Beta) Slack Linear Reference CLI customization Developer commands Developer settings Overview Permissions Profiles Sandboxing Auto-review Agent approvals & security Codex Security Overview Codex Security plugin Quickstart Run a security scan Run a deep scan Review code changes Use the Security workbench Triage a backlog Fix findings Propose security hardening Write vulnerability reports Export and track findings Changelog Codex Security CLI Quickstart Run bulk scans Run scans in CI GitLab CI/CD Reference FAQ TypeScript SDK Codex Security Cloud Setup Security Review Improving the threat model FAQ Cyber safety Models & Trusted Access Recommended configuration Overview Getting started Admin rollout guide Admin plugin Feature setup Dots Space Teams and Team Tasks ChatGPT in Slack and Teams Workspace connections Local computer access for Work Cloud and dots Sites Identity and access Authentication overview Groups and provisioning User lifecycle management Roles and workspace permissions Personal access tokens Service accounts Deployment and configuration Windows app deployment Manage app updates Managed configuration Remote connections Workspace model availability Amazon Bedrock Connect to a gateway Deploy Codex through a gateway Gateway compatibility Bedrock through LiteLLM ChatGPT Work Overview Cloud security Local security Usage and cost Admin FAQ Collaboration and sharing GPTs and sharing Plugins and connections Plugin controls Plugin management Skill controls Migrate custom GPTs to plugins Usage and analytics Workspace analytics Usage Insights Analytics API Security and compliance Governance Agent security Prisma AIRS HIPAA configuration Compliance API and audit events Explore use cases Collections Home Videos Showcase OpenAI Academy Online trainings Community Codex Ambassadors Codex for Students Codex for Open Source Events Blog Company blog Developer blog Explore use cases Collections Home Videos Showcase OpenAI Academy Online trainings Community Codex Ambassadors Codex for Students Codex for Open Source Events Blog Company blog Developer blog Showcase Blog Cookbook Learn Community Showcase Blog Cookbook Learn Community Docs Select... All posts Recent Bringing my LED display to life with GPT-Live-1 and Codex Rethinking skills and prompts for GPT-6 Astra Architectural visualization with Astra Building games with Astra Meet Rosalind Workbench: Empowering every scientist to be their own research team Topics General API Apps SDK Audio Codex Life sciences Home Topics Sign-in with ChatGPT Agents Evals Multimodal Text Guardrails Optimization ChatGPT Codex gpt-oss Contribute Cookbook on GitHub Home OpenAI Developers plugin Docs MCP Categories Demo apps Videos Topics Agents Audio & Voice Computer Use Codex Evals gpt-oss Fine-tuning Image generation Scaling Tools Video generation Community Programs Codex Ambassadors Codex for Students Codex for Open Source OpenAI for Startups Spaces Events Developer Forum Discord Reddit X API Dashboard Try ChatGPT Copy Page Use guardrails for automatic checks and human review for approval decisions. Together, they define when a run should continue, pause, or stop. 

 Guardrails validate input, output, or tool behavior automatically. 
 Human review pauses the run so a person or policy can approve or reject a sensitive action. 

 Choose the right control 

 Use case 
 Start with 

 Block disallowed user requests before the main model runs 
 Input guardrails 

 Validate or redact the final output before it leaves the system 
 Output guardrails 

 Check arguments or results around a function tool call 
 Tool guardrails 

 Pause before side effects like cancellations, edits, shell commands, or sensitive MCP actions 
 Human-in-the-loop approvals 

 Add a blocking guardrail 
 Use input guardrails when you want a fast validation step to run before the expensive or side-effecting part of the workflow starts. 
 Block a request with an input guardrail JavaScript 1 
 2 
 3 
 4 
 5 
 6 
 7 
 8 
 9 
 10 
 11 
 12 
 13 
 14 
 15 
 16 
 17 
 18 
 19 
 20 
 21 
 22 
 23 
 24 
 25 
 26 
 27 
 28 
 29 
 30 
 31 
 32 
 33 
 34 
 35 
 36 
 37 import { Agent, InputGuardrailTripwireTriggered, run } from "@openai/agents" ; 
 import { z } from "zod" ; 

 const guardrailAgent = new Agent ({ 
 name: "Homework check" , 
 instructions: "Detect whether the user is asking for math homework help." , 
 outputType: z. object ({ 
 isMathHomework: z. boolean (), 
 reasoning: z. string (), 
 }), 
 }); 

 const agent = new Agent ({ 
 name: "Customer support" , 
 instructions: "Help customers with support questions." , 
 inputGuardrails: [ 
 { 
 name: "Math homework guardrail" , 
 runInParallel: false , 
 async execute ({ input , context }) { 
 const result = await run (guardrailAgent, input, { context }); 
 return { 
 outputInfo: result.finalOutput, 
 tripwireTriggered: result.finalOutput?.isMathHomework === true , 
 }; 
 }, 
 }, 
 ], 
 }); 

 try { 
 await run (agent, "Can you solve 2x + 3 = 11 for me?" ); 
 } catch (error) { 
 if (error instanceof InputGuardrailTripwireTriggered ) { 
 console. log ( "Guardrail blocked the request." ); 
 } 
 } 1 
 2 
 3 
 4 
 5 
 6 
 7 
 8 
 9 
 10 
 11 
 12 
 13 
 14 
 15 
 16 
 17 
 18 
 19 
 20 
 21 
 22 
 23 
 24 
 25 
 26 
 27 
 28 
 29 
 30 
 31 
 32 
 33 
 34 
 35 
 36 
 37 
 38 
 39 
 40 
 41 
 42 
 43 
 44 
 45 
 46 
 47 
 48 
 49 
 50 
 51 
 52 
 53 
 54 
 55 
 56 import asyncio 

 from pydantic import BaseModel 

 from agents import ( 
 Agent, 
 GuardrailFunctionOutput, 
 InputGuardrailTripwireTriggered, 
 RunContextWrapper, 
 Runner, 
 TResponseInputItem, 
 input_guardrail, 
 ) 

 class MathHomeworkOutput(BaseModel): 
 is_math_homework: bool 
 reasoning: str 

 guardrail_agent = Agent( 
 name="Homework check", 
 instructions="Detect whether the user is asking for math homework help.", 
 output_type=MathHomeworkOutput, 
 ) 

 @input_guardrail 
 async def math_guardrail( 
 ctx: RunContextWrapper[None], 
 agent: Agent, 
 input: str | list[TResponseInputItem], 
 ) -> GuardrailFunctionOutput: 
 result = await Runner.run(guardrail_agent, input, context=ctx.context) 
 return GuardrailFunctionOutput( 
 output_info=result.final_output, 
 tripwire_triggered=result.final_output.is_math_homework, 
 ) 

 agent = Agent( 
 name="Customer support", 
 instructions="Help customers with support questions.", 
 input_guardrails=[math_guardrail], 
 ) 

 async def main() -> None: 
 try: 
 await Runner.run(agent, "Can you solve 2x + 3 = 11 for me?") 
 except InputGuardrailTripwireTriggered: 
 print("Guardrail blocked the request.") 

 if __name__ == "__main__": 
 asyncio.run(main()) 
 Use blocking execution when the cost or risk of starting the main agent is too high. Use parallel guardrails when lower latency matters more than avoiding speculative work. 
 Pause for human review 
 Approvals are the human-in-the-loop path for tool calls. The model can still decide that an action is needed, but the run pauses until you approve or reject it. 
 Pause for approval before a sensitive action JavaScript 1 
 2 
 3 
 4 
 5 
 6 
 7 
 8 
 9 
 10 
 11 
 12 
 13 
 14 
 15 
 16 
 17 
 18 
 19 
 20 
 21 
 22 
 23 
 24 
 25 
 26 
 27 
 28 
 29 
 30 import { Agent, run, tool } from "@openai/agents" ; 
 import { z } from "zod" ; 

 const cancelOrder = tool ({ 
 name: "cancel_order" , 
 description: "Cancel a customer order." , 
 parameters: z. object ({ orderId: z. number () }), 
 needsApproval: true , 
 async execute ({ orderId }) { 
 return `Cancelled order ${ orderId }` ; 
 }, 
 }); 

 const agent = new Agent ({ 
 name: "Support agent" , 
 instructions: "Handle support requests and ask for approval when needed." , 
 tools: [cancelOrder], 
 }); 

 let result = await run (agent, "Cancel order 123." ); 

 if (result.interruptions?. length ) { 
 const state = result.state; 
 for ( const interruption of result.interruptions) { 
 state. approve (interruption); 
 } 
 result = await run (agent, state); 
 } 

 console. log (result.finalOutput); 1 
 2 
 3 
 4 
 5 
 6 
 7 
 8 
 9 
 10 
 11 
 12 
 13 
 14 
 15 
 16 
 17 
 18 
 19 
 20 
 21 
 22 
 23 
 24 
 25 
 26 
 27 
 28 
 29 
 30 
 31 import asyncio 

 from agents import Agent, Runner, function_tool 

 @function_tool(needs_approval=True) 
 async def cancel_order(order_id: int) -> str: 
 return f"Cancelled order {order_id}" 

 agent = Agent( 
 name="Support agent", 
 instructions="Handle support requests and ask for approval when needed.", 
 tools=[cancel_order], 
 ) 

 async def main() -> None: 
 result = await Runner.run(agent, "Cancel order 123.") 

 if result.interruptions: 
 state = result.to_state() 
 for interruption in result.interruptions: 
 state.approve(interruption) 
 result = await Runner.run(agent, state) 

 print(result.final_output) 

 if __name__ == "__main__": 
 asyncio.run(main()) 
 This same interruption pattern applies even when the approving tool lives deeper in the workflow, such as after a handoff or inside a nested agent.asTool() call. 
 Approval lifecycle 
 When a tool call needs review, the SDK follows the same pattern every time: 

 The run records an approval interruption instead of executing the tool. 
 The result returns interruptions plus a resumable state . 
 Your application approves or rejects the pending items. 
 You resume the same run from state instead of starting a new user turn. 

 If the review might take time, serialize state , store it, and resume later. That’s still the same run. 
 Workflow boundaries matter 
 Agent-level guardrails don’t run everywhere: 

 Input guardrails run only for the first agent in the chain. 
 Output guardrails run only for the agent that produces the final output. 
 Tool guardrails run on the function tools they’re attached to. 

 If you need checks around every custom tool call in a manager-style workflow, don’t rely only on agent-level input or output guardrails. Put validation next to the tool that creates the side effect. 
 Review cybersecurity actions before execution 
 For authorized cybersecurity workflows, evaluate each sensitive tool call
before it executes. Use tool guardrails and approval interruptions to enforce
the written engagement scope at the boundary where side effects occur: 

 Check the proposed target, action, tool arguments, calling identity, and
engagement window against the approved scope. 
 Give a separate policy component or reviewer the exact proposed action and
only the context needed to evaluate it. 
 Deny out-of-scope hosts, credential theft, persistence, data exfiltration,
destructive changes, production access, and attempts to bypass policy. 
 Pause ambiguous or high-risk actions for explicit human approval before the
tool runs. 
 Enforce independent filesystem, network, identity, and project boundaries,
record decisions and execution outcomes, and fail closed if review times out
or becomes unavailable. 

 Responses API and Agents SDK applications don’t automatically inherit
 Codex Auto-review . Add review and enforcement
to your own harness. The
 open-source Codex reviewer policy 
illustrates one approach. Review Models and Trusted Access 
for approved model access and Recommended configuration 
for safe engagement setup. 
 Streaming and delayed review use the same state model 
 Streaming doesn’t create a separate approval system. If a streamed run pauses, wait for it to settle, inspect interruptions , resolve the approvals, and resume from the same state . If the review happens later, store the serialized state and continue the same run when the decision arrives. 
 Next steps 
 Once the control boundaries are clear, continue with the guide that covers the runtime or tool surface around them. 
 Running agents See how interruptions and resumptions fit into the runtime loop. Results and state Learn which result surfaces paused runs return to your application. Using tools Decide which tool surfaces need validation or approval before side effects
happen. Ask AI 
Loading docs agent...
