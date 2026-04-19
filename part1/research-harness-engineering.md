# Harness Engineering for AI Coding Agents

Date: 2026-04-18

## Executive Summary

Harness engineering is a practical answer to the central problem of AI coding agents: they can generate a lot of code quickly, but they are still unreliable enough that autonomy without controls is dangerous. The core idea, articulated clearly by Birgitta Bockeler in Martin Fowler's April 2, 2026 article, is to surround the model with a **harness** of guides and sensors that both steer initial generation and catch errors early. In this framing, the best AI coding workflow is not "prompt and pray," but "guide, sense, self-correct, verify, then integrate."

The broader evidence supports that view. A new arXiv paper on "vibe-coded" safety scripts found an overall **~45% Silent Failure Rate** among scripts that executed successfully, meaning many outputs looked functional while still being logically wrong. Meanwhile, official GitHub documentation for non-developer "vibe coding" tutorials explicitly teaches branching, terminal use, and frequent Git commits, and GitHub's cloud-agent documentation argues that Git-based workflows improve **transparency** because every step is captured in commits and logs. Research and industry commentary are converging on the same conclusion: AI coding is useful, but structured workflows with CLI tooling, tests, and Git checkpoints are what turn it into engineering.

## 1. Martin Fowler / Thoughtworks: Harness Engineering

Primary source:
- https://martinfowler.com/articles/harness-engineering.html

### What harness engineering means

Birgitta Bockeler defines harness engineering for coding agents as building an outer control system around the model so the agent is more likely to get things right on the first pass and more likely to self-correct before humans have to intervene.

The article explicitly narrows "harness" to the coding-agent context. It is not just "everything except the model." It is the practical set of controls, context, tools, and feedback loops that govern how an agent works inside a software project.

### The Guide / Sensor framework

The article splits the harness into two core parts:

- **Guides (feedforward controls)**: things that shape the agent's first attempt before it acts.
- **Sensors (feedback controls)**: things that observe the result afterward and produce signals the agent can use to repair its own work.

This is the central mental model:

- Guides reduce the chance of bad output upfront.
- Sensors reduce the chance that bad output survives.
- The combination creates a steering loop rather than a one-shot prompt.

Fowler's page gives concrete examples.

#### Guide examples

- Inferential guides: principles, rules, architecture docs, reference docs, how-to docs
- Computational guides: language servers, CLIs, scripts, codemods

#### Sensor examples

- Inferential sensors: review agents, human review
- Computational sensors: static analysis, logs, browser-based checks, linters, coverage tools

### Computational vs inferential controls

One of the most useful distinctions in the article is between:

- **Computational** controls: deterministic or machine-checkable tools such as LSPs, linters, static analyzers, scripts, browser checks
- **Inferential** controls: judgment-based controls such as review agents, architecture guidance, human review, conventions, design rules

This matters because coding agents need both:

- Computational controls are fast, objective, and automatable.
- Inferential controls cover areas where correctness is contextual, aesthetic, organizational, or architectural.

### The steering loop

The article frames the harness as a self-correcting control loop:

1. Give the agent guides before generation.
2. Run sensors after generation.
3. Feed the sensor output back into the agent.
4. Let the agent correct itself before escalating to a human.

This is the opposite of naive vibe coding. It assumes the first answer is provisional and that quality should be regulated continuously.

### The three regulation categories

Bockeler organizes harnesses into three main quality dimensions:

- **Maintainability harness**: code style, consistency, simplicity, readability, refactoring discipline
- **Architecture fitness harness**: boundaries, layering, dependency rules, API quality, structural integrity
- **Behavior harness**: whether the software actually does the right thing

The behavior harness is treated as the hardest problem. The article explicitly warns that trusting AI-generated tests too much is still unsafe.

### Harnessability

Another important idea is **harnessability**: some codebases are easier to control with agents than others.

Examples of higher harnessability:

- strongly typed languages
- clear module boundaries
- frameworks that remove low-level accidental complexity
- cleaner greenfield systems

Examples of lower harnessability:

- legacy systems
- high technical debt
- unclear boundaries
- weak test surfaces

This is a useful strategic point: the teams that most need strong harnesses may have the hardest time building them.

### Harness templates

The article proposes that organizations may eventually standardize reusable **harness templates** for common service topologies, similar to service templates today. The idea is to package guides and sensors around a known architecture and tech stack so agents start from a controlled environment rather than an unconstrained one.

### The role of the human

One of the strongest claims in the piece is that human developers already function as an implicit harness because they bring accountability, judgment, context, and organizational memory. Harness engineering is an attempt to externalize some of that tacit control.

Notable quote:

> "Harnesses are an attempt to externalise and make explicit what human developer experience brings to the table."

### How CLI and Git fit in

This part is partly direct evidence and partly careful inference from the article.

#### Directly supported by the article

- The article explicitly lists **CLIs** and **scripts** as computational guides.
- It also places tools like linters, coverage, logs, and browser checks inside the feedback harness.
- It emphasizes "keep quality left," meaning cheaper and earlier controls should happen before expensive downstream review.

#### Reasonable inference from the article

Git is not the headline topic, but Git clearly functions as the operational boundary for the harness:

- the article talks about controls that act **before a commit**
- it distinguishes between local loops and later integration/pipeline loops
- it assumes repeated correction cycles that culminate in an integration event

In practice, that makes Git the unit of:

- checkpointing
- review
- rollback
- pipeline verification
- human accountability

So in harness engineering terms:

- **CLI** is how agents access computational guides and sensors efficiently.
- **Git** is how teams turn those guided/sensed edits into auditable, reversible software changes.

## 2. arXiv 2604.12311: "Is Vibe Coding the Future?"

Primary source:
- https://arxiv.org/abs/2604.12311

Full title:
- *Is Vibe Coding the Future? An Empirical Assessment of LLM Generated Codes for Construction Safety*

### What the paper studied

This paper tests a very specific but important risk case: non-technical users generating Python tools for construction-safety calculations with frontier LLMs.

Study design from the abstract:

- **450** generated Python scripts
- **3** models: Claude 3.5 Haiku, GPT-4o-Mini, Gemini 2.5 Flash
- **150** persona-driven prompts
- evaluation pipeline combining sandbox execution with LLM-as-a-judge review

### The silent failure statistic

This is the headline result:

- **~85%** foundational execution viability
- **~45% overall Silent Failure Rate among successfully executed scripts**
- **~56%** mathematically inaccurate outputs for GPT-4o-Mini's functional code

The paper's central warning is that "working" code can still be dangerously wrong. In other words, syntactic success and runtime success do not imply domain correctness.

### Why this matters

This paper is a strong empirical argument for harness engineering because it demonstrates the exact failure mode harnesses are designed to catch:

- the code runs
- the output looks plausible
- the logic is still wrong

That is more dangerous than a visible crash, because it creates false confidence.

In Fowler's terms, this is a failure of the **behavior harness**. A green test suite or runnable script is not enough if the underlying specification, domain checks, or deterministic validation steps are weak.

Notable quote:

> "Among successfully executed scripts, the study identified an alarming ~45% overall Silent Failure Rate."

## 3. Stanford CS146S / AI-Assisted Software Engineering Materials

Official and near-official sources found:

- Stanford Bulletin: https://bulletin.stanford.edu/courses/2274401
- Stanford CS course schedule: https://www.cs.stanford.edu/academics-courses-schedule-autumn-quarter
- Public assignments repository: https://github.com/mihail911/modern-software-dev-assignments
- Course site URL referenced by Stanford schedule and repo: https://themodernsoftware.dev/

### What the official Stanford listings show

The Stanford Bulletin describes **CS146S: The Modern Software Developer** as a course about how AI is changing the full software lifecycle:

- coding
- debugging
- maintenance
- AI-powered IDEs and terminals
- code review
- testing
- trust in AI workflows

The Stanford CS Autumn 2025-26 schedule lists:

- **CS146S**
- title: **The Modern Software Developer**
- instructor: **Eric**
- time: **M, F 8:30-9:20am**

### Public course materials located

The most concrete public material I found is the assignments repository:

- https://github.com/mihail911/modern-software-dev-assignments

What it shows:

- the repo is explicitly labeled as the home of assignments for **CS146S**
- it contains week-by-week directories (`week1` through `week8`)
- `week1` includes an **"LLM Prompting Playground"**
- week 1 files include:
  - `chain_of_thought.py`
  - `k_shot_prompting.py`
  - `rag.py`
  - `reflexion.py`
  - `self_consistency_prompting.py`
  - `tool_calling.py`
- `week2` includes:
  - `app/`
  - `frontend/`
  - `tests/`
  - `assignment.md`
  - `writeup.md`

That structure strongly suggests the course is not merely about prompting. It spans prompting, tool use, application work, and testing, which is consistent with a software-engineering interpretation rather than pure "vibe coding."

### Why CS146S matters here

CS146S is evidence that top-tier software education is already formalizing AI-assisted development as an engineering discipline. The course description and public repo both suggest the curriculum is about controlled workflows, trust, and verification, not just code generation.

## 4. Why Non-Developers Benefit from Learning CLI and Git

This section combines direct evidence and cautious inference.

### Direct evidence: GitHub's official "vibe coding" tutorial is aimed at non-developers

Primary source:
- https://docs.github.com/en/copilot/tutorials/vibe-coding

GitHub explicitly says the tutorial is for:

- **Learners**
- **Non-developers**
- **Individuals**

The tutorial then immediately teaches or requires:

- cloning a repository
- creating a new branch
- opening a terminal in the IDE
- approving commands run by the agent
- allowing files to be added to Git
- committing after each successful iteration

This is highly significant. GitHub's own workflow for non-developers does **not** say "ignore the terminal and version control." It does the opposite: it treats basic terminal/Git competence as the minimum control surface for safe iteration.

GitHub gives a direct reason for frequent commits:

- commit after each successful iteration so you can return to a previous version easily

That is the clearest practical answer to why non-developers benefit from Git:

- it provides rollback
- it makes AI experimentation reversible
- it reduces fear of trying changes
- it creates visible checkpoints

### Direct evidence: GitHub prefers Git-native workflows for agent transparency

Primary source:
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent

GitHub's cloud-agent docs argue that GitHub-based workflows improve transparency because:

- work happens on branches
- changes are committed
- logs are retained
- the whole team can review the result

Key point from the docs:

- "Working on GitHub adds transparency, with every step happening in a commit and being viewable in logs."

This is exactly why Git matters for AI-agent use. For non-developers especially, Git converts an opaque AI session into something inspectable and reversible.

### Direct evidence: CLI is where agents can use real engineering controls

Primary source:
- https://arxiv.org/abs/2603.05344

The OPENDEV paper argues that terminal-native agents operate directly where developers:

- manage source control
- execute builds
- deploy environments

This is a strong explanation for why learning some CLI is valuable even for non-developers:

- the CLI exposes the real execution surface
- the CLI is where deterministic sensors live
- the CLI is where tests, linters, logs, package managers, and scripts can be invoked

Without at least a little CLI literacy, a user becomes dependent on whatever the agent chooses to say. With CLI literacy, the user can ask for and inspect evidence.

### Direct evidence: non-developers are part of the target audience, but not exempt from verification

GitHub's tutorial says non-developers may mainly care about UX or proof-of-concept functionality. But it still requires testing, approvals, and version-control checkpoints.

This implies a useful principle:

- AI lowers the barrier to **starting**
- CLI and Git lower the risk of **continuing**

### Reasonable inference

For non-developers, learning a small subset of CLI and Git yields disproportionate leverage:

- `git checkout -b ...` gives isolation
- `git status` gives situational awareness
- `git diff` exposes what the agent changed
- `git commit` creates safe restore points
- terminal output exposes build/test/log evidence directly

This is not about becoming a professional developer first. It is about gaining enough control to supervise an unreliable but useful system.

## 5. Criticism of "Vibe Coding" and Why Structured Git Workflows Are Preferred

### Simon Willison: vibe coding is not the same as responsible AI-assisted programming

Primary sources:
- https://simonwillison.net/2025/Mar/19/vibe-coding/
- https://simonwillison.net/2025/Mar/6/vibe-coding/

Willison's distinction is one of the cleanest in the whole discourse:

- **Vibe coding** = letting the model write code without really reviewing or understanding it
- **Responsible AI-assisted programming** = reviewing, testing, understanding, and being able to explain the code

Notable quote:

> "If an LLM wrote every line of your code but you've reviewed, tested and understood it all, that's not vibe coding in my book."

Another short quote:

> "Vibe coding your way to a production codebase is clearly a terrible idea."

This is effectively a philosophical argument for harness engineering.

### Research evidence: professional developers do not "just vibe"

Primary source:
- https://arxiv.org/abs/2512.14012

The paper *Professional Software Developers Don't Vibe, They Control* reports:

- **N=13** field observations
- **N=99** qualitative survey responses

Its main finding is that experienced developers use agents as productivity tools while retaining control over quality-critical decisions. The paper explicitly says their behavior reflects established software-development best practices and control strategies.

This supports a strong conclusion:

- professional use of agents is converging toward **supervised engineering**
- casual vibe coding is not the dominant professional pattern

### Reliability evidence: trust remains low

Primary source:
- https://survey.stackoverflow.co/2025/ai

Official Stack Overflow 2025 survey findings:

- **46%** of respondents actively distrust AI output accuracy
- only **33%** trust it overall
- only **3.1%** highly trust it
- **69.2%** do not plan to mostly use AI for project planning
- **58.7%** do not plan to use AI for committing/reviewing code
- **75.8%** do not plan to use AI for deployment/monitoring

This is a strong sign that developers are comfortable using AI for assistance, but not for unsupervised high-accountability tasks.

### Code-quality evidence: AI speed often trades off against maintainability

Primary sources:
- https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research
- https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf

GitClear reports:

- **211 million** changed lines analyzed
- moved/refactored code fell from **24.8% in 2021** to **9.5% in 2024**
- copy/pasted code rose from **8.4% in 2021** to **12.3% in 2024**
- 2024 was the first year **copy/paste frequency exceeded moved/refactored code**

Interpretation:

- AI can accelerate addition of code
- but teams may under-invest in consolidation, reuse, and refactoring
- that increases long-term maintenance cost

This is one of the best quantitative arguments for structured workflows with Git:

- smaller commits
- visible diffs
- explicit review
- refactoring passes
- regression testing before merge

Git does not solve AI quality problems by itself, but it creates the environment where those problems can be detected and corrected.

### Why Git-based structure is preferred

Across Fowler, GitHub Docs, Willison, Stack Overflow, GitClear, and the Stanford course materials, the same pattern appears:

- natural-language generation is useful
- unstructured acceptance is risky
- teams want evidence, auditability, and rollback

Git-based workflows are preferred because they provide:

- **branch isolation**: experiments do not immediately damage the main line
- **diff visibility**: humans can inspect what actually changed
- **commit checkpoints**: easy rollback after bad generations
- **PR review**: inferential sensors can be applied by humans and agents
- **pipeline hooks**: computational sensors run automatically after changes
- **accountability**: changes become attributable and discussable

In harness-engineering language, Git is where the guide/sensor system meets team process.

## Key Statistics At a Glance

| Statistic | Value | Source |
|---|---:|---|
| Silent Failure Rate among successfully executed vibe-coded safety scripts | ~45% | https://arxiv.org/abs/2604.12311 |
| GPT-4o-Mini mathematically inaccurate outputs in functional code | ~56% | https://arxiv.org/abs/2604.12311 |
| Scripts evaluated in the construction-safety study | 450 | https://arxiv.org/abs/2604.12311 |
| Foundational execution viability in that study | ~85% | https://arxiv.org/abs/2604.12311 |
| Professional developers using AI tools daily | 50.6% | https://survey.stackoverflow.co/2025/ai |
| Developers distrusting AI accuracy | 46% | https://survey.stackoverflow.co/2025/ai |
| Developers trusting AI accuracy overall | 33% | https://survey.stackoverflow.co/2025/ai |
| Developers highly trusting AI accuracy | 3.1% | https://survey.stackoverflow.co/2025/ai |
| Developers who do not plan to use AI for project planning | 69.2% | https://survey.stackoverflow.co/2025/ai |
| Developers who do not plan to use AI for deployment/monitoring | 75.8% | https://survey.stackoverflow.co/2025/ai |
| Changed lines analyzed by GitClear | 211 million | https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf |
| Moved/refactored code share | 24.8% (2021) -> 9.5% (2024) | https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf |
| Copy/pasted code share | 8.4% (2021) -> 12.3% (2024) | https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf |

## Bottom Line

The most useful way to understand "harness engineering" is as the discipline that turns AI coding from a novelty into a controllable engineering workflow.

The evidence points in one direction:

- AI coding agents are productive
- they are still too error-prone for unsupervised trust
- "working code" can fail silently
- professionals compensate with process, tests, architecture rules, and review
- CLI and Git are not legacy developer habits in this world; they are the main control surfaces

For non-developers, that means the highest-leverage skills are probably not "learn all of software engineering first." They are:

1. learn enough CLI to inspect and run what the agent is doing
2. learn enough Git to checkpoint, diff, branch, and roll back
3. learn enough testing/review discipline to distinguish plausible output from trustworthy output

That is the heart of harness engineering.

## Source List

- Martin Fowler / Thoughtworks, "Harness engineering for coding agent users"  
  https://martinfowler.com/articles/harness-engineering.html

- arXiv 2604.12311, "Is Vibe Coding the Future? An Empirical Assessment of LLM Generated Codes for Construction Safety"  
  https://arxiv.org/abs/2604.12311

- Stanford Bulletin, CS146S  
  https://bulletin.stanford.edu/courses/2274401

- Stanford CS Autumn course schedule  
  https://www.cs.stanford.edu/academics-courses-schedule-autumn-quarter

- CS146S assignments repository  
  https://github.com/mihail911/modern-software-dev-assignments

- GitHub Docs, "Vibe coding with GitHub Copilot"  
  https://docs.github.com/en/copilot/tutorials/vibe-coding

- GitHub Docs, "About GitHub Copilot cloud agent"  
  https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent

- arXiv 2603.05344, "Building Effective AI Coding Agents for the Terminal"  
  https://arxiv.org/abs/2603.05344

- Simon Willison, "Not all AI-assisted programming is vibe coding (but vibe coding rocks)"  
  https://simonwillison.net/2025/Mar/19/vibe-coding/

- Simon Willison, "Will the future of software development run on vibes?"  
  https://simonwillison.net/2025/Mar/6/vibe-coding/

- arXiv 2512.14012, "Professional Software Developers Don't Vibe, They Control"  
  https://arxiv.org/abs/2512.14012

- Stack Overflow Developer Survey 2025, AI section  
  https://survey.stackoverflow.co/2025/ai

- GitClear research summary page  
  https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research

- GitClear PDF report  
  https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf
