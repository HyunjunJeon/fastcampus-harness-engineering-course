# Domain A: 2026 AI Agent 환경 조사 결과

Date: 2026-04-19

---

## A-1: Agent Framework SDK 현황

### Comparison Table

| Framework | Architecture Pattern | Key Differentiator | Maturity | License | Latest Version | Release Date |
|---|---|---|---|---|---|---|
| **OpenAI Agents SDK** | Multi-agent with handoffs, guardrails, tracing | Sandbox Agents with filesystem access; voice agent support (gpt-realtime-1.5); built-in MCP integration | Production-ready | MIT | v0.14.2 | 2026-04-18 |
| **Anthropic Claude Agent SDK** | Agentic loop with built-in tool execution | Same tools and context management as Claude Code; Python + TypeScript; subagent orchestration; hooks lifecycle | Production-ready | Commercial (Anthropic ToS) | v0.2.111+ | 2026-04 (ongoing) |
| **Google ADK** | Multi-agent with workflow agents (sequential, loop, parallel) | Native Vertex AI / Cloud Run / GKE deployment; 4-language support (Python, TS, Go, Java); deep Google Cloud integration | Production-ready | Apache 2.0 | ADK Go 1.0 / ADK Java 1.0 | 2026-Q1 |
| **LangGraph** | Graph-based orchestration (inspired by Pregel/Apache Beam) | Durable execution with failure recovery; human-in-the-loop; LangSmith observability; Deep Agents for planning | Production-ready | MIT | v1.1.8 | 2026-04-17 |
| **CrewAI** | Role-based Crews + event-driven Flows | Dual architecture (autonomous Crews + deterministic Flows); 100K+ certified developers; Crew Control Plane | Production-ready | MIT | Active (2,294 commits) | 2026-04 (ongoing) |
| **Microsoft AutoGen** | Layered (Core + AgentChat + Extensions) | Magentic-One multi-agent team; AutoGen Studio (no-code); cross-language (Python/.NET) | **Maintenance mode** | MIT | Stable (3,782 commits) | Maintenance only |
| **Microsoft Semantic Kernel** | Plugin-based model-agnostic SDK | Multi-agent orchestration; multi-modal; enterprise-ready with observability; Python/.NET/Java | Active development | MIT | Active (4,949 commits) | 2026-04 (ongoing) |

### Narrative Summary

The agent framework landscape in April 2026 has consolidated around several distinct architectural philosophies, each reflecting the priorities of their creators.

**OpenAI Agents SDK** (formerly Swarm) has matured significantly since its experimental origins, reaching v0.14.2 with 22.8K GitHub stars and 268 contributors. Its architecture centers on agents configured with instructions, tools, guardrails, and handoffs. The most notable addition is Sandbox Agents, which operate in isolated compute environments with filesystem access for long-running tasks. The SDK supports MCP tools natively, includes voice agent capabilities via gpt-realtime-1.5, and offers comprehensive tracing for debugging multi-agent workflows. Its MIT license and active release cadence (84 releases total) make it one of the most accessible frameworks.

**Anthropic's Claude Agent SDK** (renamed from Claude Code SDK) takes a fundamentally different approach: rather than building a framework from scratch, it exposes the same tools, agent loop, and context management that power Claude Code as a programmable library. This means developers get battle-tested file reading, code editing, bash execution, and web search out of the box. The SDK supports subagent spawning, lifecycle hooks (PreToolUse, PostToolUse, Stop, etc.), MCP server integration, session persistence with resume/fork, and permission controls. It operates under Anthropic's commercial terms rather than an open-source license, which distinguishes it from competitors.

**Google ADK** stands out for its breadth of language support (Python, TypeScript, Go, and Java as of ADK Go 1.0 and ADK Java 1.0) and deep integration with Google Cloud infrastructure. It supports LLM agents, workflow agents (sequential, loop, parallel), and custom agents. Its context management system includes automatic filtering, summarization, and lazy-loading. The evaluation framework with visual debugging and custom metrics reflects Google's emphasis on enterprise deployment. Native deployment targets include Vertex AI Agent Engine, Cloud Run, and GKE.

**LangGraph** remains the most architecturally distinctive framework with its graph-based orchestration inspired by Google's Pregel and Apache Beam. At v1.1.8 with ~38,000 dependent projects, it has the largest downstream adoption. Its durable execution model with automatic failure recovery is particularly valued in production environments. The recent addition of "Deep Agents" for planning and subagent coordination shows evolution toward more autonomous agent patterns. Integration with LangSmith provides comprehensive observability.

**CrewAI** has carved out a niche with its dual architecture: autonomous role-based Crews for collaborative multi-agent work and deterministic event-driven Flows for precise control. With 100,000+ certified developers through learn.crewai.com, it has built the largest dedicated educational community among agent frameworks. The Crew Control Plane adds enterprise observability.

**Microsoft's landscape** is notable for its transition: AutoGen has entered maintenance mode with no new features planned, and Microsoft officially recommends the Microsoft Agent Framework for new production applications. Meanwhile, Semantic Kernel continues active development as a model-agnostic SDK supporting agents, plugins, and multi-agent orchestration across Python, .NET, and Java.

The overall trend shows convergence on several shared capabilities: MCP integration, multi-agent orchestration, human-in-the-loop support, and session/memory persistence. The key differentiators are now architectural philosophy (graph vs. role vs. loop), deployment targets (cloud-native vs. local-first), and licensing models.

**Sources:**
- [1] OpenAI Agents SDK GitHub: https://github.com/openai/openai-agents-python (accessed 2026-04-19)
- [2] Claude Agent SDK documentation: https://code.claude.com/docs/en/agent-sdk/overview (accessed 2026-04-19)
- [3] Google ADK documentation: https://adk.dev/ (accessed 2026-04-19)
- [4] LangGraph GitHub: https://github.com/langchain-ai/langgraph (accessed 2026-04-19)
- [5] CrewAI GitHub: https://github.com/crewAIInc/crewAI (accessed 2026-04-19)
- [6] AutoGen GitHub: https://github.com/microsoft/autogen (accessed 2026-04-19)
- [7] Semantic Kernel GitHub: https://github.com/microsoft/semantic-kernel (accessed 2026-04-19)

---

## A-2: MCP/A2A 프로토콜 현황

### Protocol Comparison Table

| Aspect | MCP (Model Context Protocol) | A2A (Agent-to-Agent Protocol) |
|---|---|---|
| **Maintained by** | Anthropic (open-source) | Google (open-source) |
| **Spec version** | 2025-06-18 (latest protocol version) | v1.0.0 (released 2026-03-12) |
| **Primary focus** | Connecting AI apps to external tools, data sources, and workflows | Enabling agent-to-agent communication and collaboration |
| **Architecture** | Client-server (Host -> Client -> Server) | Client-remote agent (peer-to-peer capable) |
| **Transport** | Stdio (local) + Streamable HTTP (remote) | HTTP(S) with JSON-RPC 2.0, SSE, async push notifications |
| **Protocol base** | JSON-RPC 2.0 | JSON-RPC 2.0 |
| **Core primitives** | Tools, Resources, Prompts (server); Sampling, Elicitation (client) | Agent Cards, Tasks, Messages, Artifacts |
| **Discovery** | tools/list, resources/list, prompts/list | Agent Cards (JSON capability declarations) |
| **Task model** | Synchronous tool calls (Tasks primitive is experimental) | Full lifecycle: immediate, long-running, async |
| **SDKs** | Python, TypeScript, Java, Kotlin, C#, Go, Swift, Rust | Python, Go, JavaScript, Java, .NET |
| **Ecosystem size** | 85.1K GitHub stars on awesome-mcp-servers; 40+ categories; hundreds of server implementations | 50+ technology partners; 10 releases |
| **Key adopters** | Claude, ChatGPT, VS Code, Cursor, Windsurf, JetBrains | Atlassian, Salesforce, SAP, ServiceNow, Workday, PayPal |
| **License** | Open-source | Open-source |
| **Maturity** | Established standard; broad adoption | v1.0 released; growing adoption |

### MCP Server Ecosystem

The MCP server ecosystem has grown substantially, with the curated awesome-mcp-servers repository reaching 85.1K GitHub stars with 5,913 commits and 747 open pull requests. Servers span 40+ categories including:
- Cloud Platforms (AWS, GCP, Azure)
- Databases (PostgreSQL, MongoDB, Redis)
- Developer Tools (GitHub, GitLab, Jira)
- Search & Data Extraction
- Finance & Fintech
- Home Automation
- Security
- Aerospace & Astrodynamics

Major client support includes: Claude (Desktop, Code, Web), ChatGPT, VS Code (Copilot), Cursor, Windsurf, MCPJam, JetBrains IDEs, and many more.

### Common Misconceptions

1. **"MCP and A2A are competitors"** -- They are complementary. MCP connects agents to tools and data sources (vertical integration), while A2A enables agents to communicate with each other (horizontal integration). Google explicitly states A2A "complements Anthropic's Model Context Protocol."

2. **"MCP requires a specific LLM"** -- MCP is model-agnostic. The specification defines a protocol for context exchange and "does not dictate how AI applications use LLMs or manage the provided context." OpenAI, Google, and many other providers support MCP.

3. **"MCP servers must run locally"** -- MCP supports both Stdio transport (local, process-to-process) and Streamable HTTP transport (remote, over the network). Remote MCP servers can serve many clients simultaneously.

4. **"A2A replaces the need for MCP"** -- A2A handles inter-agent orchestration but relies on something like MCP for each agent's tool access. They operate at different layers: MCP is infrastructure plumbing, A2A is agent coordination.

5. **"MCP is just function calling with extra steps"** -- MCP provides dynamic tool discovery (tools can change at runtime via notifications), resources for contextual data, prompts for interaction templates, session lifecycle management, and capability negotiation. This is fundamentally more than static function definitions.

6. **"A2A is only for Google's ecosystem"** -- A2A v1.0 has SDKs in 5 languages and 50+ technology partners. It builds on standard HTTP/SSE/JSON-RPC, requiring no Google-specific infrastructure.

### Assessment (400 words)

The protocol landscape for AI agents in April 2026 has stabilized around two complementary standards that address different dimensions of the agent interoperability challenge.

**MCP** has achieved dominant adoption as the standard for connecting AI applications to external tools and data. With the protocol version at 2025-06-18, its architecture follows a clean client-server model where hosts (like Claude Code or VS Code) create dedicated MCP clients for each server connection. The three core server primitives -- Tools (executable functions), Resources (contextual data), and Prompts (interaction templates) -- cover the fundamental ways agents need to interact with external systems. The addition of client-side primitives (Sampling and Elicitation) allows servers to request LLM completions or user input, creating bidirectional capability. The experimental Tasks primitive for durable execution suggests MCP is evolving toward supporting longer-running operations.

The ecosystem growth has been remarkable: the curated awesome-mcp-servers repository has 85.1K stars with hundreds of implementations across every major software domain. Every major AI coding IDE and assistant now supports MCP natively, creating a genuine network effect. The Streamable HTTP transport, which replaced the earlier SSE transport, enables production-grade remote server deployments with standard HTTP authentication.

**A2A** reached v1.0.0 in March 2026, marking its transition from proposal to production-ready specification. Its Agent Card discovery mechanism, where agents advertise capabilities via JSON documents, provides an elegant solution for multi-vendor agent collaboration. The protocol supports synchronous request/response, streaming via SSE, and asynchronous push notifications, covering the full spectrum of interaction patterns needed for enterprise workflows. The partnership with DeepLearning.AI for educational content signals Google's intent to drive broad adoption.

The relationship between MCP and A2A is best understood through a layered model: MCP operates at the tool/resource layer (connecting an agent to databases, APIs, and file systems), while A2A operates at the coordination layer (enabling agents to discover, communicate, and delegate to each other). A production system might use A2A for an orchestrator agent to discover and delegate tasks to specialist agents, each of which uses MCP to access their specific tools and data sources.

The key challenge remaining is practical integration. While both protocols are well-specified, the tooling for composing MCP+A2A systems is still maturing. Most current deployments use one or the other, not both together. The next phase of adoption will likely focus on reference architectures showing how to build systems that leverage both protocols effectively.

**Sources:**
- [8] MCP specification and architecture: https://modelcontextprotocol.io/docs/learn/architecture (accessed 2026-04-19)
- [9] MCP homepage: https://modelcontextprotocol.io/ (accessed 2026-04-19)
- [10] Google A2A announcement: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ (accessed 2026-04-19)
- [11] A2A GitHub: https://github.com/google/A2A (accessed 2026-04-19)
- [12] awesome-mcp-servers: https://github.com/punkpeye/awesome-mcp-servers (accessed 2026-04-19)

---

## A-3: 코딩 에이전트 벤치마크

### SWE-bench Verified Leaderboard (as of 2026-04-19)

| Rank | Model / Agent | Score (%) | Avg. Instance Calls | Cost per Instance | Data Collection Date |
|---|---|---|---|---|---|
| 1 | Claude 4.5 Opus (high reasoning) | 76.8% | 32.9 | $0.754 | 2026-02-17 |
| 2 | Gemini 3 Flash (high reasoning) | 75.8% | 56.1 | $0.356 | 2026-02-17 |
| 3 | MiniMax M2.5 (high reasoning) | ~75-77% | 60.5 | $0.073 | 2026-02-17 |
| -- | OpenHands (best config) | 77.6% | N/A | N/A | 2026 |

*Note: SWE-bench Verified results use mini-SWE-agent v2.0.0 with unified attempt parameters across diverse Python repositories (Django, Astropy, PyData, SymPy).*

### Other Benchmark Results

| Benchmark | Description | Key Result | Significance |
|---|---|---|---|
| **SWE-bench Verified** | 500 human-reviewed real GitHub issues from Python repos | Top scores clustered at 75-77% | Benchmark approaching saturation for leading models |
| **SWE-Lancer** | 1,400+ real Upwork freelance tasks ($1M total value) | Frontier models unable to solve majority of tasks | Maps model performance to monetary value; includes managerial decisions |
| **SWE-Lancer Diamond** | Public evaluation split of SWE-Lancer | Open for community evaluation | Docker-based reproducible evaluation |
| **SWE-smith** | Synthetic task generation (50K+ tasks, 128 repos) | SWE-agent-LM-32B achieves 40% on SWE-bench Verified | Demonstrates viability of training specialized coding agents on synthetic data |
| **WebArena** | Autonomous web navigation across real websites | Claude achieves SoTA among single-agent systems | Tests computer use / browser agent capabilities |

### Historical Progression of SWE-bench Verified Scores

| Period | Best Score | Notable Agent |
|---|---|---|
| Early 2024 | ~1.96% | Devin (first autonomous coding agent) |
| Mid 2024 | ~33% | Various |
| Late 2024 (Claude 3.5 Sonnet) | 49% | Anthropic minimal scaffold |
| Early 2025 | ~55-60% | Multiple agents |
| Early 2026 | 76.8% | Claude 4.5 Opus |
| Early 2026 (OpenHands) | 77.6% | OpenHands open-source agent |

### Analysis: The Benchmark-Reality Gap (400 words)

The coding agent benchmark landscape in 2026 reveals both impressive progress and important caveats about translating benchmark performance to real-world productivity.

**Benchmark Saturation.** SWE-bench Verified scores have clustered at 75-77% for top models, suggesting the benchmark is approaching its useful ceiling. When the gap between first and third place is less than 2 percentage points (76.8% vs. ~75%), and different models excel at different problem domains, the benchmark becomes less useful for distinguishing capabilities. This is a natural maturation pattern -- just as ImageNet scores eventually converged, coding benchmarks are reaching a plateau where incremental improvements require disproportionate effort.

**Cost-Performance Tradeoffs.** The SWE-bench data reveals a striking cost spectrum: Claude 4.5 Opus achieves the highest accuracy at $0.754/instance with 32.9 calls, while MiniMax M2.5 reaches comparable scores at just $0.073/instance with 60.5 calls. This 10x cost difference for similar accuracy makes clear that in production, model selection is as much an economic decision as a capability one.

**The SWE-Lancer Reality Check.** SWE-Lancer provides perhaps the most sobering perspective on the benchmark-reality gap. By sourcing 1,400+ real freelancing tasks from Upwork valued at $1M USD total, it maps model performance directly to economic value. The finding that "frontier models are still unable to solve the majority of tasks" -- including tasks ranging from $50 bug fixes to $32,000 feature implementations -- demonstrates that real-world software engineering involves complexities (ambiguous requirements, system-level understanding, stakeholder communication, architectural decisions) that benchmarks like SWE-bench do not capture.

**METR's Productivity Paradox.** METR conducted a randomized controlled trial measuring whether AI coding tools help experienced open-source developers. The surprising finding -- that AI tools did not reliably increase task completion speed, and in some configurations appeared to slow developers down -- highlighted the gap between tool capability and practical productivity. Developers reported perceiving the tools as helpful despite objective measurements showing otherwise, suggesting confirmation bias in self-reported productivity gains. This study has been widely discussed and remains an important counterpoint to vendor claims about developer productivity multiples.

**Synthetic Training Data.** SWE-smith's approach of generating 50,000+ synthetic task instances across 128 repositories and using them to train SWE-agent-LM-32B (achieving 40% on SWE-bench Verified) demonstrates that specialized smaller models trained on targeted synthetic data can approach the performance of much larger general-purpose models. This has implications for deployment cost and latency in production coding agents.

**The Bottom Line.** Benchmarks remain essential for tracking progress and comparing approaches, but they should not be confused with production readiness. The factors that matter most in real deployments -- handling ambiguity, integrating with existing workflows, managing cost at scale, and reliably producing correct code across diverse codebases -- are only partially captured by current benchmarks.

**Sources:**
- [13] SWE-bench leaderboard: https://www.swebench.com/ (accessed 2026-04-19)
- [14] Anthropic SWE-bench research: https://www.anthropic.com/research/swe-bench-sonnet (accessed 2026-04-19)
- [15] SWE-Lancer: https://arxiv.org/abs/2502.12115 and https://www.swelancer.com/ (accessed 2026-04-19)
- [16] SWE-smith: https://swesmith.com/ (accessed 2026-04-19)
- [17] OpenHands: https://github.com/All-Hands-AI/OpenHands (accessed 2026-04-19)

---

## A-4: 에이전트 신규 패러다임

### Taxonomy of 2026 Agent Paradigms

| Paradigm | Description | Key Examples | Production Readiness |
|---|---|---|---|
| **Computer Use / Browser Use Agents** | Agents that interact with desktop/web GUIs via screenshots, mouse, keyboard | Anthropic Computer Use (beta), OpenAI Operator, Devin browser agent | **Beta** -- latency issues, prompt injection risks, coordinate accuracy challenges |
| **Code Execution Sandboxes** | Isolated environments where agents execute code with filesystem access | OpenAI Sandbox Agents, Devin sandboxed environment, OpenHands Docker containers, Claude Code web sessions | **Production-ready** -- standard Docker/VM isolation; cost management is main concern |
| **Agentic RAG** | Agents that dynamically retrieve, reason over, and synthesize information from multiple sources | Claude Code with MCP data sources, LangGraph + retrieval, Google ADK with Vertex AI Search | **Production-ready** -- mature retrieval stacks; quality depends on data preparation |
| **Memory-Augmented Agents** | Agents with persistent memory across sessions (short-term context + long-term learned patterns) | Claude Code auto-memory + CLAUDE.md, Cursor Memories, Windsurf Cascade Memories, LangGraph persistent memory | **Production-ready** -- file-based memory is simple; vector-based memory requires tuning |
| **Spec-Driven Development** | Agents that work from specifications, PRDs, or design documents to implement features | Claude Code skills + CLAUDE.md, Cursor Composer, Devin with task specs | **Early production** -- works well for well-defined specs; struggles with ambiguous requirements |
| **Multi-Modal Coding Agents** | Agents that process images, designs, voice alongside code | Claude Code + Figma MCP, Cursor with image input, Windsurf drag-and-drop image-to-code | **Early production** -- image-to-code improving rapidly; voice still nascent |
| **Autonomous Multi-Agent Teams** | Multiple specialized agents collaborating on complex tasks | Claude Code subagents, OpenAI multi-agent handoffs, CrewAI Crews, LangGraph Deep Agents, AutoGen Magentic-One | **Early production** -- coordination overhead remains high; debugging is challenging |
| **Cloud/Background Agents** | Agents that run independently in cloud environments, accessible asynchronously | Claude Code Web/Routines, Cursor Cloud Agents, Devin background tasks, OpenAI Codex | **Production-ready** -- mature cloud infrastructure; requires trust boundaries |
| **IDE-Integrated Agents** | AI deeply embedded in the development environment with real-time context | Cursor (Composer 2), Windsurf (Cascade), Claude Code VS Code/JetBrains, GitHub Copilot | **Production-ready** -- dominant paradigm; Tab completion + chat + agent in one |

### Detailed Paradigm Analysis

#### 1. Computer Use / Browser Use Agents

Anthropic's Computer Use tool enables Claude to interact with desktop environments through screenshot capture, mouse control, and keyboard input. The latest version (computer_20251124) supports Claude Opus 4.7, Opus 4.6, Sonnet 4.6, and Opus 4.5, adding a zoom action for inspecting specific screen regions at full resolution. The tool requires a sandboxed computing environment (Docker container recommended) with a virtual X11 display, desktop environment, and pre-installed applications.

Key limitations remain: latency for real-time human-AI interaction, computer vision accuracy for coordinates, tool selection reliability with niche applications, and vulnerability to prompt injection via on-screen content. Anthropic has added automatic classifiers that flag potential prompt injections in screenshots and steer the model to request confirmation.

Claude achieves state-of-the-art results on WebArena among single-agent systems. OpenAI's Operator provides similar browser automation capabilities. Devin v1.6 includes browser-based interaction within its sandboxed environment.

#### 2. Code Execution Sandboxes

The sandbox paradigm has become standard across all major coding agents. OpenAI's Sandbox Agents operate in isolated compute environments with filesystem access for long-duration tasks. Devin runs in a sandboxed environment with shell, code editor, and browser. OpenHands uses Docker containers for its agent environment. Claude Code's web sessions run in Anthropic-managed infrastructure.

The key innovation is treating the sandbox not just as a security boundary but as a persistent development environment where agents can install dependencies, run tests, start servers, and iterate on code.

#### 3. Memory-Augmented Agents

Memory has become a first-class concern. Claude Code implements a dual memory system: CLAUDE.md files for explicit project instructions and auto-memory that saves learnings (build commands, debugging insights) across sessions without manual configuration. Cursor's Memories system remembers important codebase details and workflow patterns. Windsurf's Cascade tracks user actions to maintain context. LangGraph provides both short-term (within-session) and persistent (across-session) memory systems.

The trend is toward memory that is both automatic (the agent learns from experience) and explicit (developers can codify instructions), with file-based formats preferred over opaque vector stores for transparency.

#### 4. IDE-Integrated Agents vs. Standalone Agents

The market has bifurcated between IDE-integrated agents (Cursor, Windsurf, Claude Code VS Code extension, GitHub Copilot) and standalone agents (Devin, OpenHands, Claude Code CLI). IDE-integrated agents dominate daily developer workflows with features like tab autocomplete, inline diffs, and contextual chat. Cursor reports being "trusted by over half of the Fortune 500" and Windsurf claims 1M+ users with 94% of code generated by AI.

Standalone agents are finding their niche in asynchronous, long-running tasks: CI/CD pipelines, overnight refactoring, batch operations, and scenarios where developers want to delegate entire tasks rather than pair-program.

#### 5. Cloud/Background Agents and Routines

A significant 2026 development is the shift toward agents that run independently in the cloud. Claude Code's Routines run on Anthropic-managed infrastructure on schedules or triggers (API calls, GitHub events), continuing even when the developer's computer is off. Cursor's Cloud Agents "use their own computing resources to build, test, and demo features end-to-end." Devin can manage and schedule other Devin instances.

This paradigm enables new workflows: overnight PR reviews, continuous dependency audits, automated issue triage, and post-merge documentation updates -- all without human presence.

### Analysis: The State of Agent Paradigms (400 words)

The agent paradigm landscape in April 2026 reflects a maturing field that has moved from "can AI write code?" to "how should AI integrate into the software development lifecycle?"

**Convergence on the Agentic Loop.** Every major framework has converged on some variant of the agentic loop: the agent receives a task, plans its approach, executes actions (read files, run commands, edit code), observes results, and iterates. The differences lie in how much control the developer retains (Anthropic's philosophy of giving "as much control as possible to the language model itself" vs. LangGraph's deterministic graph-based workflows) and where the loop runs (local terminal vs. cloud).

**The IDE as Operating System.** The most significant paradigm shift is the IDE evolving from a text editor with plugins into an agent operating system. Cursor's Composer 2 and Windsurf's Cascade represent IDEs where the AI is not an add-on but the primary interface through which developers interact with their codebase. Tab completion, chat, and autonomous agent execution exist on a spectrum within the same tool. Claude Code's approach of being available across terminal, IDE, desktop app, web, and even Slack represents the most surface-agnostic strategy.

**Memory as Competitive Moat.** As model capabilities converge (SWE-bench scores cluster at 75-77% across top models), the differentiation shifts to context and memory. Agents that understand your specific codebase, remember your preferences, know your team's conventions, and learn from past sessions provide compounding value. This is why every major tool now invests heavily in memory systems, from Claude Code's CLAUDE.md to Cursor's Memories to Windsurf's Cascade memory.

**The Multi-Agent Question.** Multi-agent architectures are the most hyped but least mature paradigm. While frameworks like CrewAI, LangGraph Deep Agents, and Claude Code subagents enable agent teams, practical deployments still struggle with coordination overhead, error propagation, and debugging complexity. The most successful multi-agent patterns are simple: one orchestrator delegating to 2-3 specialists, rather than large teams of collaborating agents.

**Production Readiness Varies Dramatically.** Code execution sandboxes, IDE integration, and memory systems are genuinely production-ready. Computer use is promising but still beta. Multi-modal coding (especially image-to-code from Figma designs) works well for UI components but struggles with complex application logic. Autonomous multi-agent teams work for well-structured tasks but require significant guardrails for open-ended work.

The overall trajectory points toward a future where AI coding agents are not standalone tools but infrastructure -- embedded in IDEs, CI/CD pipelines, cloud platforms, and team communication tools, continuously operating on codebases with varying degrees of autonomy.

**Sources:**
- [18] Claude Computer Use documentation: https://platform.claude.com/docs/en/docs/agents-and-tools/computer-use (accessed 2026-04-19)
- [19] Anthropic Building Effective Agents: https://www.anthropic.com/research/building-effective-agents (accessed 2026-04-19)
- [20] Claude Code overview: https://code.claude.com/docs (accessed 2026-04-19)
- [21] Cursor: https://www.cursor.com/ (accessed 2026-04-19)
- [22] Windsurf: https://windsurf.com/ (accessed 2026-04-19)
- [23] OpenHands: https://github.com/All-Hands-AI/OpenHands (accessed 2026-04-19)
- [24] Devin / Cognition: https://www.cognition.ai/ (accessed 2026-04-19)
- [25] Devin introduction: https://www.cognition.ai/blog/introducing-devin (accessed 2026-04-19)

---

## 출처

1. OpenAI Agents SDK GitHub repository - https://github.com/openai/openai-agents-python (accessed 2026-04-19)
2. Claude Agent SDK documentation - https://code.claude.com/docs/en/agent-sdk/overview (accessed 2026-04-19)
3. Google ADK documentation - https://adk.dev/ (accessed 2026-04-19)
4. LangGraph GitHub repository - https://github.com/langchain-ai/langgraph (accessed 2026-04-19)
5. CrewAI GitHub repository - https://github.com/crewAIInc/crewAI (accessed 2026-04-19)
6. Microsoft AutoGen GitHub repository - https://github.com/microsoft/autogen (accessed 2026-04-19)
7. Microsoft Semantic Kernel GitHub repository - https://github.com/microsoft/semantic-kernel (accessed 2026-04-19)
8. MCP specification and architecture - https://modelcontextprotocol.io/docs/learn/architecture (accessed 2026-04-19)
9. MCP homepage - https://modelcontextprotocol.io/ (accessed 2026-04-19)
10. Google A2A announcement blog - https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ (accessed 2026-04-19)
11. A2A GitHub repository - https://github.com/google/A2A (accessed 2026-04-19)
12. awesome-mcp-servers repository - https://github.com/punkpeye/awesome-mcp-servers (accessed 2026-04-19)
13. SWE-bench leaderboard - https://www.swebench.com/ (accessed 2026-04-19)
14. Anthropic SWE-bench research - https://www.anthropic.com/research/swe-bench-sonnet (accessed 2026-04-19)
15. SWE-Lancer paper and website - https://arxiv.org/abs/2502.12115 / https://www.swelancer.com/ (accessed 2026-04-19)
16. SWE-smith - https://swesmith.com/ (accessed 2026-04-19)
17. OpenHands GitHub repository - https://github.com/All-Hands-AI/OpenHands (accessed 2026-04-19)
18. Claude Computer Use documentation - https://platform.claude.com/docs/en/docs/agents-and-tools/computer-use (accessed 2026-04-19)
19. Anthropic Building Effective Agents - https://www.anthropic.com/research/building-effective-agents (accessed 2026-04-19)
20. Claude Code overview and documentation - https://code.claude.com/docs (accessed 2026-04-19)
21. Cursor IDE - https://www.cursor.com/ (accessed 2026-04-19)
22. Windsurf IDE - https://windsurf.com/ (accessed 2026-04-19)
23. OpenHands (formerly OpenDevin) - https://github.com/All-Hands-AI/OpenHands (accessed 2026-04-19)
24. Cognition / Devin AI - https://www.cognition.ai/ (accessed 2026-04-19)
25. Devin introduction - https://www.cognition.ai/blog/introducing-devin (accessed 2026-04-19)
