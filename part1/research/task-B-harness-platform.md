# Domain B: Harness Platform and Framework 2026

Date: 2026-04-19

---

## B-1: Harness AIDA and AI Agent Updates

### Feature Inventory

| Feature | Release/Update Period | Status | Description |
|---|---|---|---|
| AI-Powered Pipeline Generation | GA (current) | Production | Natural language descriptions generate full CI/CD pipelines automatically |
| AI-Powered Verification and Rollback | March 2026 | Production | Automatically identifies relevant observability signals and determines in real-time whether rollouts should proceed, pause, or reverse |
| AI Error Analysis | GA (current) | Production | Sifts through deployment error logs, summarizes errors, and recommends fixes |
| AI SRE Capabilities | Late 2025/Early 2026 | Production | AI-powered site reliability engineering for diagnosis and remediation |
| GitOps AI Diagnostics | 2025-2026 | Production | AI support for diagnosing and remediating setup errors in GitOps applications and manifests |
| Release Orchestration | March 2026 | Production | Automates multi-team release coordination with unified controls and sequencing |
| Database DevOps (Snowflake Support) | March 2026 | Production | Integrates schema changes alongside application code in the same pipeline with synchronized rollbacks |
| FME Pipeline Support | March 2026 | Production | Progressive feature deployment and measurement against technical and business metrics |
| Warehouse-Native FME | March 2026 | Production | Tests and measures business impact directly within data warehouses (Snowflake, Redshift) |
| MCP Server Integration | October 2025 | Production | Model Context Protocol server for AI-powered IDEs (Claude Code, Cursor, Windsurf) to interact with feature flags |
| Agentic AI Architecture (C-P-A Model) | March 2026 | Strategic/Roadmap | Perception-Memory-Reasoning-Tooling model for autonomous DevOps agents |
| Service Account Token Notifications | 2025-2026 | Production | Configurable notifications for token creation, rotation, and expiration events |
| Vault Integration for IaC | 2025-2026 | Production | HashiCorp Vault natively manages and pulls secrets for infrastructure workflows |

### Three-Horizon Agent Adoption Roadmap

Harness has published a three-horizon model for AI agent adoption in DevOps:

| Horizon | Timeframe | Model | Description |
|---|---|---|---|
| Horizon 1 | Present | Augmented Operator | AI assists human engineers with triage, diagnosis, and generation |
| Horizon 2 | 1-2 years | Agent Swarms / Human-on-the-Loop | Task autonomy for agents; humans monitor rather than direct |
| Horizon 3 | 3-5 years | Autonomous SRE / Human-out-of-the-Loop | Proactive remediation without human intervention |

### Summary (400 words)

Harness has made substantial AI investments since late 2025, culminating in a major capability release on March 31, 2026 that explicitly frames its value proposition around the "AI Delivery Gap"---the disconnect between how fast AI can generate code and how safely organizations can release it. Harness's own data claims that teams with high AI adoption achieve daily-or-better release velocity but face a 22% remediation rate and 7.6-hour mean time to recovery, which motivated the five-capability release.

The most significant AI feature is AI-Powered Verification and Rollback, which moves beyond simple metric threshold alerts. The system automatically identifies which observability signals are relevant to a given deployment context and makes real-time proceed/pause/reverse decisions. Ancestry.com, cited as a reference customer, reported a 50% reduction in overall production outages using this capability. This represents a shift from rule-based canary analysis toward ML-driven deployment verification where the system learns which signals matter.

Pipeline generation via natural language has moved from novelty to production feature. Users describe their desired pipeline in plain language, and Harness generates the configuration. While this was available earlier, its integration with the broader AI stack---error analysis, GitOps diagnostics, and verification---creates a more cohesive AI-assisted deployment surface than competitors typically offer.

The MCP Server integration (October 2025) is strategically important because it positions Harness as a tool-provider for coding agents rather than just a deployment platform. By exposing feature flag management through the Model Context Protocol, developers using Claude Code, Cursor, or Windsurf can query and manage feature flags conversationally. The four initial tools (list workspaces, list environments, list flags, get flag definitions) are read-oriented, suggesting a cautious start with plans to expand to write operations.

Harness's published agentic AI architecture (the C-P-A model) describes agents with perception (ingesting logs, metrics, traces as embeddings), memory (RAG over runbooks and incident history), reasoning (ReAct and Chain-of-Thought patterns), and tool use (CLI execution with verification). This is an architectural vision statement rather than a shipped product, but it signals where the platform is headed: toward agents that can autonomously diagnose incidents, execute remediation runbooks, and verify their own fixes.

The safety model for these agents emphasizes Policy-as-Code engines, contextual permission boundaries, and comprehensive audit logging of agent reasoning and actions. This governance-first framing distinguishes Harness's approach from more permissive agent architectures and aligns with the broader industry trend toward controlled autonomy rather than unbounded agent freedom.

---

## B-2: Harness Governance Model Updates

### Governance Capability Matrix

| Capability | Current State | Key Details |
|---|---|---|
| **OPA Policy-as-Code** | GA, OPA v0.62.0 | Rego-based policies; enforced via Policy Sets at account/org/project scope; triggers on Save, Run, Step Start; severity levels: Error+Exit or Warn+Continue |
| **Policy Scope Hierarchy** | GA | Account-level policies cascade to all orgs/projects; org-level to projects within; project-level local only |
| **Supported Policy Entities** | GA | Pipelines (Save/Run/Step), Templates (Save), Feature Flags (save/create/toggle), Repositories, Services (behind feature flag), Custom entities |
| **User Metadata in Policy Evaluation** | GA | Every OPA evaluation payload automatically includes user roles, groups, and attributes for ABAC-style decisions |
| **RBAC Core Model** | GA | Principals (users, user groups, service accounts) + Resource Groups + Roles; three-tier scope (Account/Org/Project); additive permission model |
| **RBAC Split Permissions** | Recent update | Granular separation: Pipeline create vs. edit; Secret create/edit vs. view/access; User Group "manage" split into 8 specific actions |
| **ABAC Extension** | GA | Attribute-Based Access Control for connectors and environments based on attribute combinations |
| **SEI RBAC** | Recent addition | Role-Based Access Control extended to Software Engineering Insights module |
| **Audit Trail** | GA | Up to 2 years retention; immutable records; tracks 20+ module categories; CREATE/UPDATE/DELETE/RESTORE/MOVE plus specialized actions |
| **Audit Log Streaming** | GA | Export to external systems for long-term retention beyond 2 years |
| **Pipeline Execution Auditing** | GA (opt-in) | Separate setting required to capture pipeline start/end events |
| **Secrets Management** | GA | Built-in KMS (Google Cloud KMS default, AWS KMS); third-party: HashiCorp Vault, Azure Key Vault, Google Secret Manager, AWS Secrets Manager, CyberArk Conjur |
| **Ephemeral Credentials** | GA | AWS STS, Vault dynamic secrets that auto-expire after job completion |
| **Delegate-Based Secret Isolation** | GA | Secrets resolved at runtime inside customer VPC; never bulk-injected as environment variables |
| **Environment-Scoped Delegates** | GA | Dev credentials cannot reach production; different vaults, delegates, and network segments per environment |
| **Egress Filtering (Airlock)** | GA | Outbound-only HTTPS/WSS; allowlist-based network controls |
| **SOC 2** | Certified | Current |
| **ISO 27001/27017/27018** | Certified | Current |
| **GDPR** | Compliant | Current |
| **CCPA** | Compliant | Current |
| **Service Account Token Lifecycle** | Recent addition | Configurable notifications for creation, rotation, and upcoming expiration |
| **Sensitive Value Masking** | Recent fix | Fixed security issue where sensitive values were visible in logs during secret manager connection tests |

### Gap Analysis (300 words)

Harness has built a comprehensive governance stack, but several gaps and limitations merit attention for organizations evaluating it against enterprise and AI-era requirements.

**OPA Policy Enforcement Gaps.** The most significant architectural limitation is that On Save policies enforced through Git Experience or Terraform do not prevent synchronization. Violations appear only as UI warnings, meaning teams relying on GitOps workflows could bypass policy enforcement unless they also implement On Run policies. This is a real-world governance gap: the policy engine can be circumvented by the infrastructure-as-code path that many mature organizations prefer.

**Missing Compliance Certifications.** Harness holds SOC 2, ISO 27001/27017/27018, GDPR, and CCPA certifications. However, HIPAA and FedRAMP certifications are not documented on their public security page. For healthcare and US federal government customers, this represents a significant adoption barrier. Organizations in regulated industries should verify current certification status directly through the Harness Trust Center (trust.harness.io).

**Secrets Management Constraints.** KMS key rotation is not supported---removing older key versions risks access loss. Secrets cannot be migrated from the random-key store used in Community and Self-Managed editions, creating lock-in risks for organizations upgrading from open-source to enterprise tiers. The 30-minute secret cache TTL can cause stale metadata issues in fast-rotating credential scenarios.

**AI Agent Governance.** While Harness's strategic documentation describes Policy-as-Code engines, contextual permission boundaries, and audit logging for autonomous agents, the current shipped product does not yet include purpose-built governance controls for AI agent actions within pipelines. The three-horizon roadmap acknowledges this gap implicitly: Horizon 1 (current) is "augmented operator" where humans retain authority, precisely because the agent-specific governance layer is not yet mature.

**Audit Trail Limitations.** Pipeline execution events require opt-in enablement, which means organizations that do not explicitly configure this setting have a blind spot in their compliance record. Audit events may take several minutes to appear, which is acceptable for compliance but insufficient for real-time security monitoring.

---

## B-3: Harness Engineering Framework Evolution

### Framework Evolution Timeline

| Date | Event | Source | Significance |
|---|---|---|---|
| 2024 | GitClear reports copy/paste exceeds refactoring for first time | GitClear 2025 Report | Copy/paste rose to 12.3% while moved/refactored code fell to 9.5%; empirical evidence of AI-driven code quality shifts |
| Nov 2025 | ThoughtWorks Tech Radar Vol 33: AGENTS.md files at Trial | ThoughtWorks Radar | First formal recognition of shared instruction files as an engineering practice |
| Nov 2025 | ThoughtWorks Tech Radar Vol 33: Curated shared instructions at Adopt | ThoughtWorks Radar | Embedding AI guidance as collaborative engineering assets reaches top recommendation level |
| Feb 17, 2026 | Bockeler publishes initial memo on harness engineering | martinfowler.com | First articulation of the harness concept for coding agents |
| March 31, 2026 | Harness ships AI-Powered Verification and Rollback | harness.io | Commercial platform operationalizes verification/rollback cycle aligned with harness engineering principles |
| Apr 2, 2026 | Bockeler publishes full harness engineering article | martinfowler.com | Expands memo into complete Guide/Sensor framework with three regulation categories, harnessability concept, and harness templates |
| Apr 15, 2026 | ThoughtWorks Tech Radar Vol 34 published | ThoughtWorks Radar | Massive AI-coding-agent focus: 40+ entries directly address agent controls, harness concepts, and code quality |
| Apr 15, 2026 | Feedback Sensors for Coding Agents at Trial | ThoughtWorks Radar | Direct operationalization of Bockeler's "sensor" concept; wiring deterministic quality gates into agentic workflows |
| Apr 15, 2026 | Context Engineering at Adopt | ThoughtWorks Radar | Treating the context window as a design surface; underpins the "guide" half of harness engineering |
| Apr 15, 2026 | Agent Skills at Trial | ThoughtWorks Radar | Modularized instructions loaded just-in-time; reduces context bloat while maintaining harness quality |
| Apr 15, 2026 | Codebase Cognitive Debt at Caution | ThoughtWorks Radar | Warning that AI-accelerated development creates understanding gaps; direct motivation for harness engineering |
| Apr 15, 2026 | Feedback Flywheel at Assess | ThoughtWorks Radar | Meta-technique for continuously improving coding agent harnesses through captured successes and failures |
| Apr 15, 2026 | Measuring Collaboration Quality at Assess | ThoughtWorks Radar | Shift from throughput metrics to first-pass acceptance rate, iteration cycles, post-merge rework |
| Apr 15, 2026 | Coding Agent Swarms at Caution | ThoughtWorks Radar | Warning that multi-agent approaches are premature; reinforces need for controlled single-agent harnesses first |
| Apr 15, 2026 | Agent Instruction Bloat at Caution | ThoughtWorks Radar | Warning that AGENTS.md files accumulate conflicting rules; argues for minimal, selective instructions |
| Apr 15, 2026 | Coding Throughput as Productivity Metric at Caution | ThoughtWorks Radar | Explicitly warns against lines-of-code metrics; recommends first-pass acceptance rate and DORA metrics instead |
| Apr 15, 2026 | Claude Code at Adopt | ThoughtWorks Radar | Terminal-based agentic coding tool recommended for production use; features skills, subagents, team workflows |
| Apr 15, 2026 | Cursor at Adopt | ThoughtWorks Radar | IDE-based coding agent at Adopt; plan mode, hooks, subagents |
| Apr 15, 2026 | CodeScene at Assess | ThoughtWorks Radar | Behavioral code analysis with CodeHealth metric that flags areas too complex for LLMs |
| Apr 15, 2026 | Git AI at Assess | ThoughtWorks Radar | Open-source Git extension tracking AI-generated code linked to agent, model, and prompts |
| Apr 15, 2026 | Entire CLI at Assess | ThoughtWorks Radar | Captures AI coding agent sessions as searchable metadata; Git-native audit trail |

### Updated Code Quality Statistics

| Metric | Value | Period | Source |
|---|---|---|---|
| Moved/refactored code share | 24.8% to 9.5% | 2021-2024 | GitClear 2025 Report |
| Copy/pasted code share | 8.4% to 12.3% | 2021-2024 | GitClear 2025 Report |
| First year copy/paste exceeded refactoring | 2024 | Annual | GitClear 2025 Report |
| Changed lines analyzed | 211 million | Through 2024 | GitClear 2025 Report |
| Teams with high AI adoption: remediation rate | 22% | 2026 | Harness |
| Teams with high AI adoption: MTTR | 7.6 hours | 2026 | Harness |
| Silent Failure Rate in vibe-coded scripts | ~45% | 2026 | arXiv 2604.12311 |
| GPT-4o-Mini mathematical inaccuracy in functional code | ~56% | 2026 | arXiv 2604.12311 |
| Developers distrusting AI output accuracy | 46% | 2025 | Stack Overflow 2025 Survey |
| Developers who highly trust AI accuracy | 3.1% | 2025 | Stack Overflow 2025 Survey |

### ThoughtWorks Tech Radar Vol 34: Harness Engineering Alignment

The April 2026 Tech Radar (Vol 34) represents the strongest institutional validation of harness engineering to date. Here is how the Radar entries map to Bockeler's Guide/Sensor framework:

**Guide-aligned entries (feedforward controls):**

| Radar Entry | Ring | Harness Engineering Mapping |
|---|---|---|
| Context Engineering | Adopt | Systematic design of information provided to agents before generation |
| Curated Shared Instructions for Software Teams | Adopt | Inferential guides: team-level instructions (CLAUDE.md, AGENTS.md) embedded in templates |
| Agent Skills | Trial | Modular inferential guides loaded just-in-time to reduce context bloat |
| Progressive Context Disclosure | Trial | Guide optimization: lightweight discovery before full context loading |
| Sandboxed Execution for Coding Agents | Trial | Computational guide: constraining agent execution environment |
| Code Intelligence as Agentic Tooling | Assess | Computational guide: LSP-based AST-aware tools for agents |
| Context Graph | Assess | Inferential guide: modeling institutional decisions as queryable nodes |

**Sensor-aligned entries (feedback controls):**

| Radar Entry | Ring | Harness Engineering Mapping |
|---|---|---|
| DORA Metrics | Adopt | Organizational-level feedback sensors for delivery performance |
| Feedback Sensors for Coding Agents | Trial | Direct implementation of Bockeler's sensor concept with deterministic quality gates |
| Mutation Testing | Trial | Behavior harness sensor: verifying AI-generated test quality |
| Browser-Based Component Testing | Trial | Computational sensor: real-browser validation |
| Architecture Drift Reduction with LLMs | Assess | Architecture fitness sensor: detecting structural and semantic violations |
| Feedback Flywheel | Assess | Meta-sensor: continuous improvement of the entire harness based on accumulated feedback |
| Measuring Collaboration Quality | Assess | Process sensor: first-pass acceptance rate, iteration cycles, post-merge rework |
| CodeScene | Assess (Tool) | Computational sensor: CodeHealth metric flags areas too complex for LLMs |

**Caution-aligned entries (anti-patterns the harness should prevent):**

| Radar Entry | Ring | Harness Engineering Mapping |
|---|---|---|
| Agent Instruction Bloat | Caution | Guide failure: context files accumulate conflicting rules |
| Codebase Cognitive Debt | Caution | Sensor gap: AI-accelerated development outpaces team understanding |
| Coding Agent Swarms | Caution | Premature autonomy without adequate harness maturity |
| Coding Throughput as Productivity | Caution | Measurement failure: wrong metrics encourage wrong agent behaviors |
| AI-Accelerated Shadow IT | Caution | Governance gap: non-developers building uncontrolled systems |
| MCP by Default | Caution | Over-engineering: adding protocol overhead when CLIs suffice |

### Assessment (400 words)

The harness engineering framework has evolved from a single-author memo in February 2026 to a broadly validated industry concept within just two months. The April 15, 2026 ThoughtWorks Technology Radar (Vol 34) is the most significant external validation: of the approximately 40 new AI-related entries, at least 20 directly map to components of Bockeler's Guide/Sensor framework. The Radar does not merely cite harness engineering---it operationalizes it across Adopt, Trial, Assess, and Caution rings, creating a maturity model that organizations can use to assess their own agent governance posture.

The most important conceptual advance is the recognition that harness engineering is not a one-time setup but a continuous improvement process. The Feedback Flywheel (Assess ring) describes a meta-technique where teams capture successes and failures from coding agent sessions to refine their harness controls over time. This extends Bockeler's static Guide/Sensor model into a dynamic learning loop: spec, plan, implement, feedback, improvement. ThoughtWorks explicitly warns that harness effectiveness varies across model versions, meaning the harness itself must be treated as a living engineering artifact subject to regular re-evaluation.

The code quality evidence has not substantially changed since the GitClear 2025 report, but new framing from the Tech Radar adds urgency. The "Codebase Cognitive Debt" entry (Caution ring) names a specific risk that the original harness engineering article only implied: rapid AI code generation creates understanding gaps that compound traditional technical debt. When multiple contributors or agent swarms modify code faster than teams can review and internalize changes, the system becomes harder to reason about, debug, and evolve. This is the demand-side argument for harness engineering---not just "AI makes mistakes" but "AI makes changes faster than humans can track."

The emergence of new tooling categories reinforces the practical trajectory. Git AI (Assess) tracks AI-generated code linked to specific agents, models, and prompts. Entire CLI (Assess) captures full agent sessions as searchable metadata with Git-native audit trails. CodeScene provides a CodeHealth metric that explicitly flags code areas "too complex for LLMs." These tools operationalize the sensor half of harness engineering with purpose-built infrastructure rather than repurposed traditional developer tools.

The article itself has not been revised since April 2, 2026. Bockeler explicitly noted that the full article updates and supersedes the February 17 memo, and the original memo URL now redirects to the full article. No additional corrections, addenda, or revisions have been published. The conceptual framework---guides (feedforward), sensors (feedback), three regulation categories (maintainability, architecture fitness, behavior), harnessability, and harness templates---remains stable and has been reinforced rather than challenged by subsequent industry commentary and the Tech Radar's independent analysis.

Community adoption signals are strong. ThoughtWorks placing "Curated Shared Instructions for Software Teams" at Adopt and "Feedback Sensors for Coding Agents" at Trial means they are recommending these practices for production use across client engagements. Claude Code and Cursor both reached the Adopt ring, indicating that the terminal-based and IDE-based agent categories that harness engineering targets are now considered mainstream tools rather than experimental.

---

## Source List

1. Harness blog, "Harness Ships Five Capabilities to Power Confident Releases at AI Speed" (March 31, 2026)
   https://www.harness.io/blog/how-to-release-confidently-at-ai-speed

2. Harness blog, "Agentic AI in DevOps: The Architect's Guide to Autonomous Infrastructure" (March 2026)
   https://www.harness.io/blog/agentic-ai-in-devops-the-architects-guide-to-autonomous-infrastructure

3. Harness blog, "It's Time to Rethink Untrusted Code in Your Pipeline" (March 30, 2026)
   https://www.harness.io/blog/teampcp-trivy-open-vs-governed-execution-pipelines

4. Harness blog, "AI-Powered Feature Management with Harness MCP Server and Claude Code" (October 31, 2025)
   https://www.harness.io/blog/ai-powered-feature-management-with-harness-mcp-server-and-claude-code

5. Harness Developer Docs, "Harness Policy As Code Overview"
   https://developer.harness.io/docs/platform/governance/policy-as-code/harness-governance-overview

6. Harness Developer Docs, "RBAC in Harness"
   https://developer.harness.io/docs/platform/role-based-access-control/rbac-in-harness

7. Harness Developer Docs, "Secrets Management Overview"
   https://developer.harness.io/docs/platform/secrets/secrets-management/harness-secret-manager-overview

8. Harness Developer Docs, "Audit Trail"
   https://developer.harness.io/docs/platform/governance/audit-trail

9. Harness Developer Docs, "Release Notes"
   https://developer.harness.io/release-notes

10. Harness Security Page
    https://www.harness.io/security

11. Harness Continuous Delivery Product Page
    https://www.harness.io/products/continuous-delivery

12. Birgitta Bockeler / Martin Fowler, "Harness Engineering for Coding Agent Users" (April 2, 2026; initial memo February 17, 2026)
    https://martinfowler.com/articles/harness-engineering.html

13. ThoughtWorks Technology Radar Vol 34 (April 2026)
    https://www.thoughtworks.com/radar

14. ThoughtWorks Technology Radar, "Feedback Sensors for Coding Agents" (April 15, 2026)
    https://www.thoughtworks.com/radar/techniques/feedback-sensors-for-coding-agents

15. ThoughtWorks Technology Radar, "Context Engineering" (April 15, 2026)
    https://www.thoughtworks.com/radar/techniques/context-engineering

16. ThoughtWorks Technology Radar, "Curated Shared Instructions for Software Teams" (April 15, 2026)
    https://www.thoughtworks.com/radar/techniques/curated-shared-instructions-for-software-teams

17. ThoughtWorks Technology Radar, "Agent Skills" (April 15, 2026)
    https://www.thoughtworks.com/radar/techniques/agent-skills

18. ThoughtWorks Technology Radar, "Codebase Cognitive Debt" (April 15, 2026)
    https://www.thoughtworks.com/radar/techniques/codebase-cognitive-debt

19. ThoughtWorks Technology Radar, "Feedback Flywheel" (April 15, 2026)
    https://www.thoughtworks.com/radar/techniques/feedback-flywheel

20. ThoughtWorks Technology Radar, "Measuring Collaboration Quality with Coding Agents" (April 15, 2026)
    https://www.thoughtworks.com/radar/techniques/measuring-collaboration-quality-with-coding-agents

21. ThoughtWorks Technology Radar, Techniques listing (April 2026)
    https://www.thoughtworks.com/radar/techniques

22. ThoughtWorks Technology Radar, Tools listing (April 2026)
    https://www.thoughtworks.com/radar/tools

23. GitClear, "AI Copilot Code Quality Research"
    https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research

24. GitClear, "AI Copilot Code Quality 2025 Report" (PDF)
    https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf

25. arXiv 2604.12311, "Is Vibe Coding the Future?"
    https://arxiv.org/abs/2604.12311

26. Stack Overflow Developer Survey 2025, AI Section
    https://survey.stackoverflow.co/2025/ai
