# Task E: Discovering New Misconceptions about AI Agents

> **Domain E Research Report**
> Researcher: Domain E Agent | Date: 2026-04-19
> For: FastCampus Harness Online Learning Curriculum (Part 1)

---

## Overview

This report identifies new misconceptions that have emerged in the AI agent practitioner community since mid-2025, complementing the 8 existing misconceptions already documented in the curriculum. These new false beliefs have arisen alongside the rapid adoption of coding agents, MCP (Model Context Protocol), vibe coding, and autonomous agentic workflows.

---

## Task E-1: "MCP/Tools Solve Everything" Misconception

### Misconception: "MCP만 연결하면 에이전트가 만능이 된다" (Connecting MCP makes the agent omnipotent)

**Why it's wrong:**

MCP (Model Context Protocol) has been widely adopted as the standard for connecting AI agents to external tools and data sources, but this adoption has bred a dangerous over-confidence in what the protocol actually provides. Three categories of evidence demonstrate the gap between perception and reality:

1. **Tool confusion at scale.** The MCP creators themselves acknowledge that when many MCP servers operate simultaneously, models struggle to select the correct tool. Overlapping tool descriptions increase error rates, and no universal maximum exists across models (Latent Space, MCP Podcast, 2025). The protocol provides a *connection mechanism*, not intelligent tool selection.

2. **Critical security vulnerabilities remain unsolved.** Invariant Labs demonstrated "tool poisoning attacks" where malicious instructions embedded in MCP tool descriptions manipulate AI models into performing unauthorized actions -- including data exfiltration of SSH keys and credentials -- while the user sees only benign-looking summaries. "Rug pull" attacks allow servers to change tool descriptions *after* initial client approval. These vulnerabilities affect Anthropic, OpenAI, Zapier, and Cursor platforms (Invariant Labs, 2025). The MCPSafetyScanner paper (arXiv:2504.03767) further confirmed that "industry-leading LLMs may be coerced into using MCP tools to compromise an AI developer's system."

3. **MCP is a protocol, not intelligence.** The official MCP documentation explicitly states: "MCP focuses solely on the protocol for context exchange -- it does not dictate how AI applications use LLMs or manage the provided context" (modelcontextprotocol.io). MCP provides the *plumbing*, not the reasoning about when, whether, or how to use tools.

**Real-world risk:** A development team connects 15 MCP servers to their coding agent, believing it now has comprehensive capabilities. The agent selects the wrong database tool due to overlapping descriptions, executes a destructive query on production data, and a compromised third-party MCP server simultaneously exfiltrates API keys through a tool poisoning attack that was invisible in the UI.

**Correction principle:** MCP is an interoperability standard, not a capability amplifier. Teach practitioners three rules: (1) Fewer, well-curated tools outperform many overlapping ones; (2) Every MCP server is an attack surface -- treat tool descriptions as untrusted input; (3) The agent's reasoning about *when not to use* a tool is more important than having the tool available.

**Sources:**
1. Latent Space Podcast, "MCP: The Model Context Protocol" (2025) -- MCP creators on tool confusion at scale
2. Invariant Labs, "MCP Security Notification: Tool Poisoning Attacks" (2025) -- tool poisoning, rug pulls, shadowing attacks
3. arXiv:2504.03767, "MCP Safety Audit" (ICSE 2025) -- MCPSafetyScanner and coercion of LLMs via MCP tools
4. Simon Willison, "MCP Prompt Injection" (April 2025) -- prompt injection via tool descriptions, fundamental unsolved problem
5. modelcontextprotocol.io/docs/concepts/architecture -- official scope statement

---

## Task E-2: "Agents Can Self-Correct" Misconception

### Misconception: "에이전트는 실수해도 스스로 교정할 수 있다" (Agents can self-correct their own mistakes)

**Why it's wrong:**

The belief that agentic loops with self-reflection reliably catch and fix their own errors is one of the most dangerous misconceptions in agent design. Multiple peer-reviewed studies provide strong evidence against it:

1. **Intrinsic self-correction is largely ineffective.** Huang & Zhou (ICLR 2024, arXiv:2310.01798) demonstrated that "LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction." This is not a marginal finding -- performance actively *worsens* when models attempt autonomous self-critique on reasoning tasks.

2. **Apparent improvements are statistical artifacts.** A follow-up study (arXiv:2310.12397) showed that when iterative self-correction appears to work, it is "largely due to the correct solution being fortuitously present in the top-k completions of the prompt" -- meaning the model gets lucky by sampling multiple answers, not by genuinely improving a flawed answer. The study explicitly "calls into question claims about the self-critiquing capabilities of state of the art LLMs."

3. **Self-correction training suffers from distribution mismatch.** The SCoRe paper (arXiv:2409.12917) found that standard supervised fine-tuning for self-correction falls victim to "distribution mismatch" and "behavior collapse," where models learn correction patterns that look effective during training but fail in deployment. Even with specialized reinforcement learning training, improvements were modest (15.6% on MATH, 9.1% on HumanEval).

4. **Reliability degrades sharply with task length.** METR's longitudinal study (March 2025) found that the best current models (Claude 3.7 Sonnet) achieve 50% success probability at roughly one-hour task length and drop below 10% on tasks exceeding 4 hours. Each additional step in an agentic loop compounds the probability of unrecoverable error.

**Real-world risk:** A team deploys an autonomous coding agent with a "self-review" loop, trusting it to catch its own bugs. The agent introduces a subtle off-by-one error in a financial calculation, then during self-review, the same reasoning patterns that produced the error also fail to detect it -- or worse, the agent "fixes" correct code into incorrect code through sycophantic self-doubt. The bug reaches production because human review was deemed unnecessary.

**Correction principle:** Self-correction requires *external* feedback signals -- test results, type checkers, linters, human review, or a structurally different verification model. Teach practitioners the "prosecutor/defender" pattern: the correcting system must have different information, different prompting, or different architecture than the generating system. Never trust a model to reliably evaluate its own output.

**Sources:**
1. Huang & Zhou, "Large Language Models Cannot Self-Correct Reasoning Yet" (ICLR 2024, arXiv:2310.01798)
2. arXiv:2310.12397, "Self-correction in LLMs: Graph Coloring Study" -- improvements are sampling artifacts, not genuine self-critique
3. arXiv:2409.12917, "SCoRe: Training Self-Correction via RL" -- distribution mismatch and behavior collapse in self-correction training
4. METR, "Measuring AI Ability to Complete Long Tasks" (March 2025) -- reliability degrades sharply with task complexity
5. Anthropic, "Building Effective Agents" (2024) -- recommends simplicity and external validation over autonomous correction

---

## Task E-3: "If It Runs, It's Correct" Misconception

### Misconception: "실행되면 맞는 코드다" (If the code executes, it must be correct)

**Why it's wrong:**

The emergence of "vibe coding" -- generating code via AI without deeply understanding it -- has made this misconception acutely dangerous. Practitioners equate successful execution with correctness, but rigorous evidence shows a massive gap between the two:

1. **The ~45% Silent Failure Rate.** The study documented in arXiv:2604.12311 found that approximately 45% of successfully executed AI-generated scripts produce mathematically incorrect results. These are not crash failures -- the code compiles, runs without errors, and returns plausible-looking but wrong answers. GPT-4o-Mini performed worst, with ~56% of its functional code generating mathematically inaccurate outputs. The study coined the concept of "silent failures, wherein generated code compiles perfectly but executes flawed mathematical safety logic."

2. **High execution viability masks logic deficits.** The same study found ~85% "foundational execution viability" -- meaning most AI-generated code runs successfully. But this syntactic reliability "actively concealed logic deficits and insufficient defensive programming practices." The better AI gets at producing code that runs, the harder silent failures become to detect.

3. **Prompt informality compounds the problem.** The study found a "highly significant relationship between user persona and data hallucination" -- less formal, more casual prompts (characteristic of vibe coding) drastically increase the AI's tendency to invent missing safety variables, creating compounding risk factors that are invisible at the execution level.

4. **Tests are insufficient safeguards.** AI-generated tests often share the same flawed assumptions as the AI-generated code they test. When both the implementation and the test suite emerge from the same model context, they can be "consistently wrong together" -- the tests pass precisely because they encode the same misunderstanding as the code.

**Real-world risk:** A developer uses vibe coding to build a construction safety calculation module. The code runs perfectly, all AI-generated tests pass, and the output looks reasonable. But the underlying formula contains a subtle sign error that underestimates load-bearing requirements by 15%. The error is undetectable without domain expertise because the code's behavior is internally consistent -- it just doesn't match physical reality.

**Correction principle:** Execution is a necessary but radically insufficient condition for correctness. Teach the "three-gate validation" approach: (1) Does it run? (syntax gate); (2) Does it produce correct results on known inputs with known outputs? (semantic gate -- requires human-authored test cases with independently verified expected values); (3) Does it handle edge cases, adversarial inputs, and domain constraints? (robustness gate). Gate 1 alone catches less than half of all defects.

**Sources:**
1. arXiv:2604.12311, "Silent Failures in AI-Generated Code" (2025) -- ~45% silent failure rate, ~56% for GPT-4o-Mini, execution viability masking logic deficits
2. Anthropic, "Building Effective Agents" (2024) -- emphasis on sandboxed testing and tool validation
3. HuggingFace smolagents documentation (2025) -- open models placing final_answer() prematurely, execution succeeds but behavior is wrong
4. METR, "Measuring AI Ability to Complete Long Tasks" (March 2025) -- success rates below 10% for complex tasks despite apparent execution

---

## Task E-4: Open-Ended Survey of Emerging Misconceptions

### Misconception 1: "바이브 코딩이면 프로덕션도 가능하다" (Vibe coding is sufficient for production systems)

**Why it's wrong:** Vibe coding -- Andrej Karpathy's term for generating code by describing intent to AI without understanding the output -- works remarkably well for prototypes and personal tools but fails catastrophically at production scale. The arXiv:2604.12311 study's ~45% silent failure rate applies directly: code that "works" in a demo context harbors undetected logic errors. Production systems require understanding of concurrency, error handling, security boundaries, and failure modes that vibe coding systematically omits because they are not visible in the happy-path description.

**Real-world risk:** A startup ships a vibe-coded payment processing system. It works perfectly in testing with small amounts. In production, a race condition in the transaction logic (never specified in the natural language prompt) causes double-charges under concurrent load.

**Correction principle:** Vibe coding is a legitimate prototyping technique, not a production methodology. Every line of AI-generated code destined for production must be read, understood, and validated by a human who can explain *why* it works -- not just observe *that* it works.

**Sources:**
1. arXiv:2604.12311 -- silent failure rates in AI-generated code
2. Anthropic, "Building Effective Agents" -- start simple, add complexity only when needed

---

### Misconception 2: "컨텍스트 윈도우가 길수록 좋다" (Longer context window = better results)

**Why it's wrong:** The "Lost in the Middle" study (Liu et al., 2023, arXiv:2307.03172) demonstrated that language models significantly underperform when relevant information is positioned in the middle of long contexts. Performance is "often highest when relevant information occurs at the beginning or end" with substantial degradation for mid-context retrieval. This holds true even for models specifically designed for long contexts. Simply feeding an agent a massive codebase or long document does not ensure it will use all the information -- it creates a false sense of comprehensiveness while critical details in the middle are effectively invisible.

**Real-world risk:** A developer dumps an entire 50,000-line codebase into an agent's context window, believing the agent now "understands" the full system. The agent confidently generates code that contradicts a critical constraint defined in the middle of the codebase, because it effectively never processed that section.

**Correction principle:** Context management is an engineering discipline, not a scaling problem. Teach practitioners to use structured retrieval (RAG), strategic context placement (important information at the beginning and end), and hierarchical summarization rather than relying on raw context length.

**Sources:**
1. Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (2023, arXiv:2307.03172)

---

### Misconception 3: "벤치마크 점수가 높으면 실무에서도 잘한다" (High benchmark scores predict real-world performance)

**Why it's wrong:** METR's longitudinal study (March 2025) provides the most direct evidence of the benchmark-reality gap. While frontier models achieve near-perfect scores on tasks requiring under 4 minutes of human effort (the scale of most benchmarks), they drop below 10% success on tasks exceeding 4 hours (the scale of real work). SWE-bench scores, which have become the de facto measure of coding agent capability, test isolated bug fixes in well-structured open-source repositories -- a far cry from navigating ambiguous requirements, legacy codebases, and organizational constraints that characterize real software engineering.

**Real-world risk:** A team selects an agent based on its 49% SWE-bench Verified score, expecting it to handle half their engineering tickets autonomously. In practice, their tickets involve multi-file refactors, unclear specifications, and integration with proprietary systems -- none of which SWE-bench tests. Actual autonomous completion rate is under 5%.

**Correction principle:** Evaluate agents on *your* tasks, not on public benchmarks. Build internal evaluation sets from representative past tickets. Benchmark scores indicate potential, not performance -- treat them as necessary but insufficient signals.

**Sources:**
1. METR, "Measuring AI Ability to Complete Long Tasks" (March 2025) -- success drops below 10% for 4+ hour tasks
2. Anthropic, "Building Effective Agents" (2024) -- emphasis on task-specific evaluation over general benchmarks

---

### Misconception 4: "AI가 작성한 코드는 내 책임이 아니다" (AI-generated code is not my responsibility)

**Why it's wrong:** A class-action lawsuit against GitHub Copilot, Microsoft, and OpenAI highlights the unresolved legal landscape: generated code lacks provenance documentation, making license compliance impossible to verify automatically (IEEE Spectrum, 2024). More practically, when AI-generated code causes a production incident, the deployment team -- not the AI vendor -- bears operational, legal, and ethical responsibility. The developer who commits the code is the author of record regardless of how it was generated.

**Real-world risk:** A developer accepts AI-generated code that inadvertently copies a GPL-licensed implementation. The company ships it in a proprietary product. The license violation is discovered, requiring either open-sourcing the entire module or rewriting it from scratch under legal pressure.

**Correction principle:** AI is a tool, not an author. The human who commits code is responsible for its correctness, security, licensing compliance, and operational behavior. Teach the "sign-off rule": never commit code you cannot explain and defend in a code review.

**Sources:**
1. IEEE Spectrum, "AI Code Generation Ownership" (2024) -- Copilot lawsuit, attribution failures, licensing violations
2. arXiv:2604.12311 -- ~45% silent failure rate underscores the danger of unreviewed AI code

---

### Misconception 5: "멀티 스텝 에이전트는 단계가 많을수록 정확해진다" (More agentic steps = more accurate results)

**Why it's wrong:** Error propagation in multi-step agent workflows follows compound probability. If each step has a 90% success rate, a 10-step chain has only a 35% chance of being entirely correct (0.9^10 = 0.349). METR's data confirms this: the best models achieve 50% success at one-hour task length (roughly 10-20 agentic steps) and collapse below 10% at four hours. The HuggingFace smolagents documentation reports that open models sometimes place `final_answer()` calls prematurely mid-script, halting execution before all steps complete -- demonstrating that more steps introduce more failure modes, not more accuracy.

**Real-world risk:** A team builds a 15-step autonomous pipeline: gather requirements, design schema, generate code, write tests, run tests, fix failures, deploy. Each step appears to work in isolation, but errors compound silently -- a slightly wrong schema leads to subtly wrong code, which is "fixed" by tests that encode the same wrong assumption, and the deployment succeeds with a fundamentally flawed system.

**Correction principle:** Minimize agentic chain length. Each step should have an independent verification gate (test, type check, human approval). Design for "checkpoint-and-verify" rather than "chain-and-hope." Anthropic's guidance: "start with the simplest solution possible, and only increase complexity when needed."

**Sources:**
1. METR, "Measuring AI Ability to Complete Long Tasks" (March 2025) -- reliability degrades with task complexity
2. HuggingFace smolagents documentation (2025) -- premature termination in multi-step agent execution
3. Anthropic, "Building Effective Agents" (2024) -- start simple, add complexity only when warranted

---

### Misconception 6: "프레임워크를 쓰면 에이전트 개발이 쉬워진다" (Frameworks make agent development easier)

**Why it's wrong:** Anthropic's "Building Effective Agents" guide (2024) explicitly warns that frameworks "create extra layers of abstraction that can obscure underlying prompts and responses, making debugging harder and encouraging unnecessary complexity." The most successful agent implementations use "simple, composable patterns rather than complex frameworks." Many teams adopt heavy frameworks (LangChain, CrewAI, AutoGen) before understanding the underlying LLM API behavior, then struggle to debug failures hidden behind abstraction layers.

**Real-world risk:** A team adopts a multi-agent framework for a customer service bot. When the bot produces incorrect responses, they cannot determine whether the error originates in the prompt, the routing logic, the tool selection, or the framework's internal state management. Debugging takes 5x longer than it would with direct API calls.

**Correction principle:** Start with direct LLM API calls -- "many patterns can be implemented in a few lines of code" (Anthropic). Only adopt frameworks when you have outgrown direct implementation and can articulate specifically which framework features you need. Understand the abstraction before depending on it.

**Sources:**
1. Anthropic, "Building Effective Agents" (2024) -- frameworks obscure debugging, encourage unnecessary complexity
2. HuggingFace smolagents (2025) -- advocates simple code-based agents over framework-heavy approaches

---

### Misconception 7: "도구 설명서만 잘 쓰면 에이전트가 도구를 올바르게 쓴다" (Good tool descriptions guarantee correct tool use)

**Why it's wrong:** Even with well-documented tools, AI agents face fundamental challenges in tool selection and use. The MCP ecosystem demonstrates this clearly: with many connected servers, models struggle to select the correct tool when descriptions overlap. Anthropic's SWE-bench agent team reported spending "more time optimizing tools than the overall prompt" and found that tool design requires equal engineering attention as prompt engineering -- including "poka-yoke" principles (designing tools so incorrect usage is harder), example usage patterns, and explicit edge case documentation. Tool descriptions are necessary but insufficient; the tool's API surface itself must be designed for AI consumption.

**Real-world risk:** A team provides detailed descriptions for 30 database tools. The agent consistently selects `query_table` (read-only) when it should use `update_table` (write) because the descriptions are semantically similar. A subtle bug persists for weeks because the agent's tool selection appears reasonable at first glance.

**Correction principle:** Design tools for AI consumption using the "Agent-Computer Interface (ACI)" concept: minimize the number of tools, make tool names unambiguous, include usage examples in descriptions, design input schemas that prevent misuse, and test tool selection empirically with representative queries.

**Sources:**
1. Anthropic, "Building Effective Agents" (2024) -- ACI design, poka-yoke for tools, tool optimization > prompt optimization
2. MCP creators interview (Latent Space, 2025) -- tool confusion at scale with overlapping descriptions
3. Invariant Labs (2025) -- tool descriptions as attack surfaces, not just documentation

---

### Misconception 8: "에이전트에게 자율성을 많이 줄수록 더 유능해진다" (More autonomy = more capable agent)

**Why it's wrong:** This is a new variant of the existing "full autonomy = efficiency" misconception, but specifically applied to coding agents and agentic workflows. HuggingFace's smolagents documentation defines agency as a spectrum and advises: "For the sake of simplicity and robustness, it's advised to regularize towards not using any agentic behaviour." The METR study shows that agent success probability drops below 10% for tasks requiring more than 4 hours of autonomous operation. Anthropic's recommendation is unambiguous: "start with the simplest solution possible." Autonomous multi-step agents should be the exception, not the default.

**Real-world risk:** A team gives a coding agent full autonomy to refactor a legacy module: read code, plan changes, implement, test, and deploy. The agent makes an architecturally reasonable but organizationally inappropriate change (renaming a public API used by 3 other teams), causing a cascade of downstream failures that take days to untangle.

**Correction principle:** Autonomy should be earned through demonstrated reliability at each level, not granted upfront. Use the "graduated autonomy" model: start with human-in-the-loop approval at every step, then selectively remove gates only for steps where the agent has proven reliable. The goal is the *minimum viable autonomy* for the task.

**Sources:**
1. HuggingFace smolagents (2025) -- "regularize towards not using agentic behaviour"
2. METR (March 2025) -- success rates collapse with extended autonomous operation
3. Anthropic, "Building Effective Agents" (2024) -- start simple, graduated complexity

---

## Summary Table

| # | Misconception (Korean) | Misconception (English) | Key Evidence |
|---|----------------------|------------------------|-------------|
| E-1 | MCP만 연결하면 만능 | MCP/Tools solve everything | Tool poisoning attacks; tool confusion at scale; MCP is plumbing, not intelligence |
| E-2 | 에이전트가 스스로 교정 | Agents can self-correct | ICLR 2024: performance degrades after self-correction; improvements are sampling artifacts |
| E-3 | 실행되면 맞는 코드 | If it runs, it's correct | ~45% silent failure rate (arXiv:2604.12311); execution viability masks logic deficits |
| E-4a | 바이브 코딩 = 프로덕션 | Vibe coding = production-ready | Silent failures + missing non-functional requirements |
| E-4b | 컨텍스트 길수록 좋다 | Longer context = better | Lost in the Middle (arXiv:2307.03172): mid-context information effectively invisible |
| E-4c | 벤치마크 = 실무 성능 | Benchmarks = real performance | METR: <10% success on 4+ hour tasks despite high benchmark scores |
| E-4d | AI 코드 내 책임 아님 | AI code isn't my responsibility | Copilot lawsuit; developer remains legally and operationally responsible |
| E-4e | 단계 많을수록 정확 | More steps = more accurate | Compound probability: 10 steps at 90% each = 35% overall; METR confirms |
| E-4f | 프레임워크 = 쉬운 개발 | Frameworks make it easy | Anthropic: frameworks obscure debugging, encourage unnecessary complexity |
| E-4g | 도구 설명 = 올바른 사용 | Good docs = correct tool use | Tool selection failures at scale; ACI design required, not just documentation |
| E-4h | 자율성 = 유능함 | More autonomy = more capable | METR: <10% at 4hr tasks; smolagents: regularize *against* agency |

---

## Cross-References to Existing Curriculum Misconceptions

These new misconceptions extend and complement the existing 8:

- **E-1** extends Misconception #3 (prompt-only control) -- MCP adds tools but doesn't solve the control problem
- **E-2** extends Misconception #7 (full autonomy = efficiency) -- self-correction is a specific failure mode of autonomous agents
- **E-3** extends Misconception #5 (demo = production) -- running code is the new "demo that works"
- **E-4a** is a specific instantiation of Misconception #5 for the vibe coding era
- **E-4b** is entirely new -- emerged with the 1M+ context window race
- **E-4c** is entirely new -- emerged with SWE-bench-driven marketing
- **E-4d** is entirely new -- emerged with widespread AI code generation adoption
- **E-4e** extends Misconception #2 (multi-agent is better) -- applies to step count, not just agent count
- **E-4f** is entirely new -- emerged with the proliferation of agent frameworks
- **E-4g** extends Misconception #8 (NL generates correct schemas) -- applies to tool interfaces, not just data schemas

---

*Report compiled from 15+ sources including peer-reviewed papers (ICLR 2024, ICSE 2025), official documentation (Anthropic, MCP), security research (Invariant Labs), and longitudinal studies (METR). All claims are evidence-backed with specific citations.*
