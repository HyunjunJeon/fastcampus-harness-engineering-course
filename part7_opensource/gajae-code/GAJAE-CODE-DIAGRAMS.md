# Gajae-Code 아키텍처 도식

> 본 문서는 [`GAJAE-CODE-ANALYSIS.md`](./GAJAE-CODE-ANALYSIS.md)와 함께 보기 위한 시각 자료 모음이다.

## 목차

1. [전체 시스템 구조](#1-전체-시스템-구조)
2. [CLI 명령 라우팅](#2-cli-명령-라우팅)
3. [Session Assembly 7단계](#3-session-assembly-7단계)
4. [Agent vs AgentSession 책임 분리](#4-agent-vs-agentsession-책임-분리)
5. [Workflow 4종과 Verification Gate](#5-workflow-4종과-verification-gate)
6. [Workflow State 라이프사이클 (`.gjc/`)](#6-workflow-state-라이프사이클-gjc)
7. [Atomic Write + Dual Schema Contract](#7-atomic-write--dual-schema-contract)
8. [Tool Registry 통합 모델](#8-tool-registry-통합-모델)
9. [Bash Tool 실행 흐름과 8개 Lifecycle 차원](#9-bash-tool-실행-흐름과-8개-lifecycle-차원)
10. [Subagent = Owned Task (Lifecycle Metadata)](#10-subagent--owned-task-lifecycle-metadata)
11. [AsyncJobManager 상태머신](#11-asyncjobmanager-상태머신)
12. [Coordinator MCP: File-based Control Surface](#12-coordinator-mcp-file-based-control-surface)
13. [Model Provider Runtime Registry](#13-model-provider-runtime-registry)
14. [핵심 철학: Advisory vs Authoritative](#14-핵심-철학-advisory-vs-authoritative)

---

## 1. 전체 시스템 구조

> **연관 문서:** [Part 2. 아키텍처 철학](./GAJAE-CODE-ANALYSIS.md#part-2-아키텍처-철학), [Part 3. 모노레포 구조](./GAJAE-CODE-ANALYSIS.md#part-3-모노레포-구조)

Gajae-Code의 전체 모노레포 경계를 보여준다. `packages/coding-agent/`가 핵심 제품 표면이고, 나머지 package/crate/python은 명시적 ownership boundary를 가진 support 계층이다.

```mermaid
flowchart TB
    subgraph CORE["핵심 제품 표면"]
        CA["packages/coding-agent/<br/>CLI · Session · Workflow · Tools · TUI"]
    end

    subgraph SUPPORT_TS["Support — TS/Bun 워크스페이스"]
        AGENT["packages/agent/<br/>저수준 agent loop"]
        AI["packages/ai/<br/>model provider layer"]
        TUI["packages/tui/<br/>terminal UI primitive"]
        NATIVES["packages/natives/<br/>native binding 진입점"]
        STATS["packages/stats/<br/>usage / observability"]
        UTILS["packages/utils,<br/>bridge-client"]
    end

    subgraph SUPPORT_RS["Support — Rust 계층"]
        PINATIVES["crates/pi-natives/<br/>search · grep · SIXEL"]
        PISHELL["crates/pi-shell, pi-iso<br/>shell 실행 + isolation"]
        PIAST["crates/pi-ast<br/>AST 작업"]
        BRUSH["crates/brush-*-vendored<br/>vendored Brush 셸"]
    end

    subgraph SUPPORT_PY["Support — Python"]
        GJCRPC["python/gjc-rpc/<br/>RPC 호스트 (--mode rpc)"]
        ROBOGJC["python/robogjc/<br/>GitHub 자동화"]
    end

    CORE --> AGENT
    CORE --> AI
    CORE --> TUI
    CORE --> STATS
    AGENT --> AI
    NATIVES --> PINATIVES
    CORE --> NATIVES
    CORE --> PISHELL
    GJCRPC -.구동.-> CORE
    ROBOGJC -.자동화.-> GJCRPC

    classDef core fill:#ff4d4f,color:#fff,stroke:#b30000,stroke-width:2px
    classDef ts fill:#fff3f3,stroke:#ff4d4f
    classDef rs fill:#f0f7ff,stroke:#1f6feb
    classDef py fill:#fffbe6,stroke:#d4a017
    class CA core
    class AGENT,AI,TUI,NATIVES,STATS,UTILS ts
    class PINATIVES,PISHELL,PIAST,BRUSH rs
    class GJCRPC,ROBOGJC py
```

**설계 원칙:** support domain은 CLI core 밖에 둔다. 각 package는 서로 다른 ownership boundary를 갖는다.

---

## 2. CLI 명령 라우팅

> **연관 문서:** [4.1 CLI 진입점](./GAJAE-CODE-ANALYSIS.md#41-cli-진입점)
> **코드:** `packages/coding-agent/src/cli.ts:188-218`

첫 인자가 subcommand인지 판별하고, 아니면 전체를 `launch` 인자로 취급하는 fast path 로직.

```mermaid
flowchart TD
    START(["gjc <argv>"]) --> CHECK_SMOKE{"argv[0] ==<br/>'--smoke-test'?"}
    CHECK_SMOKE -->|Yes| SMOKE["runSmokeTest()<br/>Worker 로드 + native addon 검증<br/><i>cli.ts:167-185</i>"]
    CHECK_SMOKE -->|No| CHECK_HELP{"--help / -h /<br/>--version / -v?"}
    CHECK_HELP -->|Yes| HELP["renderRootHelp()<br/>또는 버전 출력"]
    CHECK_HELP -->|No| INSTALL["installRuntimeGlobals()<br/>installH2Fetch + procmgr.scrubProcessEnv<br/><i>cli.ts:59-72</i>"]
    INSTALL --> ISSUB{"isSubcommand(first)?<br/><i>cli.ts:150-153</i>"}
    ISSUB -->|Yes| ROUTE_SUB["runArgv = argv<br/>→ 해당 command handler"]
    ISSUB -->|No| ROUTE_LAUNCH["runArgv = ['launch', ...argv]<br/>→ launch command"]
    ROUTE_SUB --> RUN["run(commands, argv)<br/><i>cli.ts:217</i>"]
    ROUTE_LAUNCH --> RUN

    subgraph CMDS["17개 subcommand (lazy import)<br/><i>cli.ts:25-47</i>"]
        direction LR
        C1["launch"]
        C2["config"]
        C3["team"]
        C4["ralplan"]
        C5["ultragoal"]
        C6["deep-interview"]
        C7["coordinator"]
        C8["mcp-serve"]
        C9["...외 9개"]
    end

    RUN --> CMDS
```

---

## 3. Session Assembly 7단계

> **연관 문서:** [4.2 Session Assembly](./GAJAE-CODE-ANALYSIS.md#42-session-assembly)
> **코드:** `packages/coding-agent/src/sdk.ts:827-2058`, `main.ts:715-1036`

`createAgentSession()`이 수행하는 7단계 조립 흐름. `main.ts`가 먼저 auth/modelRegistry/settings를 생성해서 주입하는 점(단계 1의 fallback 성격)을 함께 표현.

```mermaid
flowchart TD
    MAIN["main.ts:715<br/>runRootCommand()"] --> PREP["launch mode 준비<br/>interactive/print/rpc/acp/bridge<br/><i>main.ts:818-884</i>"]
    PREP --> BUILD_DEPS["authStorage, ModelRegistry, Settings,<br/>SessionManager를 먼저 생성<br/><i>main.ts:732-780</i><br/>주의: SDK의 단계 1은 fallback 경로"]
    BUILD_DEPS --> CALL["createAgentSession(sessionOptions)<br/><i>main.ts:913-921</i>"]

    CALL --> S1["① modelRegistry / authStorage / settings<br/>옵션 주입 또는 fallback 생성<br/><i>sdk.ts:839-864</i>"]
    S1 --> S2["② SessionManager 복원 또는 생성<br/>existingSession 발견 시 model/thinking 복원<br/><i>sdk.ts:915-991, 1977-1999</i>"]
    S2 --> S3["③ workspace context, AGENTS.md,<br/>skills, rules, prompts, extensions 로드<br/><i>sdk.ts:868-1091</i><br/>주의: extension discovery는 quarantine"]
    S3 --> S4["④ built-in / custom tool 생성<br/>createTools + image/web/subskill<br/><i>sdk.ts:1306-1369</i>"]
    S4 --> S5["⑤ system prompt 구성<br/>rebuildSystemPrompt()<br/><i>sdk.ts:1603-1674, 1772-1777</i>"]
    S5 --> S6["⑥ Agent 생성<br/>new Agent({systemPrompt, model, tools, ...})<br/><i>sdk.ts:1882-1972</i>"]
    S6 --> S7["⑦ AgentSession wrapping<br/>+ yieldQueue, MCP wiring, LSP warmup<br/><i>sdk.ts:2001-2207</i>"]
    S7 --> RESULT(["CreateAgentSessionResult<br/>{session, extensionsResult, eventBus, ...}"])

    classDef mainNode fill:#1f6feb,color:#fff
    classDef step fill:#fff3f3,stroke:#ff4d4f
    classDef caveat fill:#fffbe6,stroke:#d4a017
    class MAIN,CALL mainNode
    class S1,S2,S3,S4,S5,S6,S7 step
```

> 주의: **ACP 예외:** interactive/print/rpc/bridge는 단일 `AgentSession`을 공유하지만, **ACP는 클라이언트 세션마다 `createAcpSessionFactory`로 새 AgentSession을 생성**한다 (`main.ts:262-293`).

---

## 4. Agent vs AgentSession 책임 분리

> **연관 문서:** [4.2 Agent vs AgentSession 분리](./GAJAE-CODE-ANALYSIS.md#42-session-assembly)
> **코드:** `packages/agent/src/agent.ts:259`, `packages/coding-agent/src/session/agent-session.ts:863`

저수준 model/tool loop(`Agent`)과 그 위의 제품 동작(`AgentSession`)의 책임 분리.

```mermaid
flowchart LR
    subgraph AGENT["@gajae-code/agent — 저수준 core"]
        direction TB
        A_STATE["state<br/>systemPrompt, model, tools,<br/>messages, isStreaming"]
        A_API["public API<br/>prompt(), steer(), followUp(),<br/>replaceMessages(), abort()"]
        A_LOOP["agentLoop / agentLoopContinue<br/>No transport abstraction<br/>calls streamSimple directly"]
        A_STATE --- A_API
        A_API --- A_LOOP
    end

    subgraph SESSION["coding-agent/AgentSession — 제품 동작"]
        direction TB
        S_HOLD["readonly agent: Agent<br/><i>agent-session.ts:864</i>"]
        S_PERSIST["SessionManager 기반 영속화<br/>event-driven auto-save"]
        S_RETRY["retry-fallback chains<br/>+ backoff + cooldown revert"]
        S_MCP["MCP/skill/RPC tool<br/>동적 발견 + refresh"]
        S_GOAL["goal mode / plan mode /<br/>TTSR / IRC registry"]
        S_GUARD["mutation guard wrapping<br/>+ permission boundary"]
        S_HOLD --- S_PERSIST
        S_HOLD --- S_RETRY
        S_HOLD --- S_MCP
        S_HOLD --- S_GOAL
        S_HOLD --- S_GUARD
    end

    AGENT -->|"구성됨(composed)"| SESSION

    classDef agentBox fill:#f0f7ff,stroke:#1f6feb
    classDef sessionBox fill:#fff3f3,stroke:#ff4d4f
    class AGENT agentBox
    class SESSION sessionBox
```

**핵심:** `Agent`는 순수 stateful core. `AgentSession`은 그 위에 persistence, compaction, retry, MCP discovery 등 ~80개 private 필드를 추가.

---

## 5. Workflow 4종과 Verification Gate

> **연관 문서:** [4.3 Workflow State Runtime](./GAJAE-CODE-ANALYSIS.md#43-workflow-state-runtime)
> **코드:** `state-schema.ts:17` (`CANONICAL_GJC_WORKFLOW_SKILLS`), `defaults/gjc/skills/*/SKILL.md`

4개 workflow가 각자 진짜 verification gate를 가지는 구조. schema에 hard-coded된 single source of truth.

```mermaid
flowchart TD
    USER([사용자 요청]) --> DI{{"deep-interview<br/>명확화"}}
    DI -->|"ambiguity ≤ threshold<br/>+ 사용자 명시 승인<br/><i>SKILL.md:52</i>"| GATE_DI{"ambiguity gate<br/>통과?"}
    GATE_DI -->|No| DI
    GATE_DI -->|Yes| RP{{"ralplan<br/>계획 + 비판"}}
    RP --> LOOP["Planner → Architect → Critic 루프<br/>최대 5회 반복 cap<br/><i>SKILL.md:75</i>"]
    LOOP --> GATE_RP{"Critic APPROVE?"}
    GATE_RP -->|No| LOOP
    GATE_RP -->|Yes| UG{{"ultragoal<br/>실행 추적"}}
    UG --> LEDGER["goal · revision · evidence<br/>.gjc/ultragoal/ledger.jsonl<br/>G001/G002 quality gate"]
    LEDGER --> GATE_UG{"--quality-gate-json<br/>통과?"}
    GATE_UG -->|No| REV["revision"]
    REV --> UG
    GATE_UG -->|Yes| DONE([완료])

    UG -.병렬 가치 판단.-> TEAM{{"team (optional)<br/>tmux coordination"}}
    TEAM --> HARDERR{"gjc team<br/>사용 가능?"}
    HARDERR -->|No| STOP([hard error<br/><i>SKILL.md:35</i>"])
    HARDERR -->|Yes| WORKERS["tmux-backed workers<br/>owner-scoped goals"]

    classDef gate fill:#fffbe6,stroke:#d4a017,stroke-width:2px
    classDef wf fill:#fff3f3,stroke:#ff4d4f,stroke-width:2px
    class GATE_DI,GATE_RP,GATE_UG,HARDERR gate
    class DI,RP,UG,TEAM wf
```

> **설계 의도:** workflow는 prompt가 아니라 runtime gate를 갖는다. LLM이 "그냥 수정할게"라고 해도 `assertDeepInterviewMutationAllowed`가 tool wrapper 단에서 차단한다 (`agent-session.ts:228, 3680`).

---

## 6. Workflow State 라이프사이클 (`.gjc/`)

> **연관 문서:** [4.3 Workflow State Runtime](./GAJAE-CODE-ANALYSIS.md#43-workflow-state-runtime), [특성 2. Durable State](./GAJAE-CODE-ANALYSIS.md#특성-2-workflow-state를-transcript-밖에-두기-durable-state-separation)
> **코드:** `gjc-runtime/state-writer.ts`, `state-runtime.ts`

`.gjc/` 디렉토리 layout과 각 파일의 역할. activation record → workflow envelope → ledger로 이어지는 상태 기록 흐름.

```mermaid
flowchart TD
    ACTIVATE["skill activation<br/>(keyword / command)"] --> WRITE_AE["writeActiveEntry()<br/><i>state-writer.ts:745</i>"]
    WRITE_AE --> AE_FILE[(".gjc/state/active/&lt;skill&gt;.json<br/>SkillActiveEntry<br/>{skill, phase, active,<br/>activated_at, session_id,<br/>handoff_from/to, receipt}<br/><i>state-schema.ts:117-150</i>"])]

    WRITE_AE --> WRITE_SNAP["writeActiveEntries + snapshot<br/><i>state-writer.ts:814</i>"]
    WRITE_SNAP --> SNAP_FILE[(".gjc/state/skill-active-state.json<br/>← derived cache<br/>(entries에서 재건됨)")]

    AE_FILE --> ENVELOPE["writeWorkflowEnvelopeAtomic()<br/><i>state-writer.ts:450</i>"]
    ENVELOPE --> ENV_FILE[(".gjc/state/&lt;mode&gt;-state.json<br/>RequiredOnWriteEnvelopeSchema<br/>{content_sha256 필수}")]

    ENVELOPE --> SKILL_SPECIFIC{"어느 workflow?"}
    SKILL_SPECIFIC -->|deep-interview| DI_SPEC[(".gjc/specs/deep-interview-{slug}.md")]
    SKILL_SPECIFIC -->|ralplan| RP_SPEC[(".gjc/plans/ralplan/&lt;run-id&gt;/")]
    SKILL_SPECIFIC -->|ultragoal| UG_SPEC[(".gjc/ultragoal/<br/>brief.md · goals.json<br/>ledger.jsonl")]

    subgraph READERS["누가 읽는가? (3가지 이점)"]
        R1["사람 — JSON/MD 에디터"]
        R2["Hook — gate 검사"]
        R3["UI HUD — buildRalplanHudSummary"]
        R4["이후 세션 — context 압축과 무관"]
    end

    AE_FILE --> READERS
    ENV_FILE --> READERS
    UG_SPEC --> READERS

    AUDIT[(".gjc/state/audit.jsonl<br/>append-only audit log<br/><i>state-writer.ts:951</i>")]
    TXN[(".gjc/state/transactions/&lt;mutation-id&gt;<br/>recovery evidence only")]
    AE_FILE -.감사.-> AUDIT
    ENVELOPE -.저널.-> TXN
```

> **Reconciliation:** `inspectActiveScope` doctor pass가 snapshot과 entries 간 정합성을 검사한다 (`state-runtime.ts:528-577`).

---

## 7. Atomic Write + Dual Schema Contract

> **연관 문서:** [4.3 Atomic write](./GAJAE-CODE-ANALYSIS.md#43-workflow-state-runtime), [특성 3. Dual Schema](./GAJAE-CODE-ANALYSIS.md#특성-3-atomic-write와-dual-schema-contract-lenient-read--strict-write)
> **코드:** `state-writer.ts:375-386`, `state-schema.ts`

crash safety와 forward compatibility를 동시에 달성하는 이중 방어.

```mermaid
flowchart TD
    WRITE(["상태 쓰기 요청"]) --> VALIDATE["RequiredOnWriteEnvelopeSchema 검증<br/><b>STRICT</b><br/>content_sha256 등 필수 필드 누락 시 실패<br/><i>state-schema.ts</i>"]
    VALIDATE -->|실패| REJECT(["거부 (fail-closed)<br/>손상된 state 쓰기 방지"])
    VALIDATE -->|성공| MKDIR["fs.mkdir(dirname, recursive)"]
    MKDIR --> TMP["tempPathFor(filePath)<br/>per-process / ms / uuid<br/><i>state-writer.ts:184-186</i>"]
    TMP --> WRITE_TMP["fs.writeFile(tmpPath, content)"]
    WRITE_TMP --> RENAME["fs.rename(tmpPath, filePath)<br/><b>POSIX atomic</b>"]
    RENAME --> DONE(["완료"])

    WRITE_TMP -.크래시 시.-> CLEANUP["fs.rm(tmpPath, force)<br/>원본 unaffected"]
    RENAME -.크래시 중.-> ATOMIC["rename은 원자적<br/>또는 완전히 안 됨<br/>둘 중 하나만"]

    READ(["상태 읽기"]) --> LENIENT[".passthrough() lenient schema<br/><b>LENIENT</b><br/>알 수 없는 필드 허용<br/><i>state-schema.ts:4-12</i>"]
    LENIENT --> USE(["사용 (forward-compatible)"])

    LOCK["별도: withFileLock<br/>advisory directory lock<br/>read-modify-write 동시성 보장<br/><i>state-writer.ts:5, 534</i>"]
    LOCK -.RMW 경로에만.-> WRITE

    classDef strict fill:#ffe6e6,stroke:#ff4d4f
    classDef lenient fill:#e6f7ff,stroke:#1f6feb
    classDef safety fill:#fffbe6,stroke:#d4a017
    class VALIDATE,REJECT strict
    class LENIENT,USE lenient
    class CLEANUP,ATOMIC,LOCK safety
```

> 주의: 모듈 주석은 "No lockfiles are used"라고 하지만, 실제로는 crash-atomicity(rename)와 concurrency-atomicity(lock)을 구분한 것이다.

---

## 8. Tool Registry 통합 모델

> **연관 문서:** [4.4 Tool Registry](./GAJAE-CODE-ANALYSIS.md#44-tool-registry와-bash-executor), [특성 4. Tool as Capability](./GAJAE-CODE-ANALYSIS.md#특성-4-tool을-capability로-취급-execution-boundary)
> **코드:** `packages/agent/src/types.ts:411-454`, `agent-session.ts:984, 3949-4077`

서로 다른 출처의 tool이 단일 `Map<string, AgentTool>`로 수렴하는 구조. permission은 tool 내부가 아니라 session-level wrapper에.

```mermaid
flowchart TB
    subgraph SOURCES["Tool 출처 (5가지)"]
        BUILTIN["Built-in<br/>createTools()<br/><i>sdk.ts:1306</i>"]
        MCP["MCP tools<br/>refreshMCPTools()<br/><i>agent-session.ts:3949</i>"]
        EXT["Extension tools<br/>ExtensionToolWrapper<br/><i>sdk.ts:1513-1540</i>"]
        CUSTOM["Custom tools<br/>image/web/subskill<br/><i>sdk.ts:1320-1369</i>"]
        SKILL["Skill-specific<br/>refreshGjcSubskillTools()<br/><i>agent-session.ts:4077</i>"]
        RPC["RPC host tools<br/>refreshRpcHostTools()<br/><i>agent-session.ts:3998</i>"]
    end

    BUILTIN --> REG
    MCP --> REG
    EXT --> REG
    CUSTOM --> REG
    SKILL --> REG
    RPC --> REG

    REG[("Map&lt;string, AgentTool&gt;<br/>#toolRegistry<br/><i>agent-session.ts:984</i>")]

    REG --> GUARD["#wrapToolForAcpPermission<br/>+ deep-interview mutation guard<br/><b>session-level permission boundary</b><br/><i>agent-session.ts:3684-3716</i>"]
    GUARD --> AGENT_TOOLS["agent.setTools(...)<br/><i>agent-session.ts:3714-3716</i>"]
    AGENT_TOOLS --> LLM["LLM 호출 가능"]

    subgraph INTERFACE["AgentTool 인터페이스<br/><i>types.ts:411-454</i>"]
        direction LR
        I_NAME["name<br/>description"]
        I_SCHEMA["parameters<br/>(JSON schema)"]
        I_EXEC["execute(...)<br/>→ AgentToolResult"]
        I_RENDER["renderCall?<br/>renderResult?"]
    end

    REG -.각 tool은.-> INTERFACE

    RENDERER["별도: toolRenderers map<br/>name-keyed<br/><i>tools/renderers.ts:49-53</i>"]
    REG -.렌더링 위임.-> RENDERER

    classDef source fill:#fff3f3,stroke:#ff4d4f
    classDef registry fill:#1f6feb,color:#fff,stroke:#0d4ea6,stroke-width:2px
    classDef guard fill:#fffbe6,stroke:#d4a017,stroke-width:2px
    class BUILTIN,MCP,EXT,CUSTOM,SKILL,RPC source
    class REG registry
    class GUARD guard
```

> **핵심 설계:** permission은 tool 내부가 아니라 **바깥 wrapper**에 있다. tool 자체가 권한을 결정하면 우회 가능하므로, 권한은 바깥 층, 실행은 tool 안에서.

---

## 9. Bash Tool 실행 흐름과 8개 Lifecycle 차원

> **연관 문서:** [4.4 Bash lifecycle](./GAJAE-CODE-ANALYSIS.md#44-tool-registry와-bash-executor)
> **코드:** `tools/bash.ts`, `exec/bash-executor.ts:16-380`

대표적 tool인 bash의 실행 경로. 동기/비동기 분기와 8개 lifecycle 차원을 함께 표현.

```mermaid
flowchart TD
    CALL(["LLM tool call: bash"]) --> BT["BashTool.execute<br/><i>tools/bash.ts:714-728</i>"]
    BT --> ASYNC_Q{"async: true<br/>또는 autoBackground<br/>threshold 도?"}

    ASYNC_Q -->|Yes| JOB["#startManagedBashJob<br/>→ AsyncJobManager.instance()<br/>→ jobId 즉시 반환<br/><i>tools/bash.ts:746-803</i>"]
    ASYNC_Q -->|No| SYNC["executeBash()<br/><i>tools/bash.ts:997-1007</i>"]

    SYNC --> BE["executeBash()<br/><i>exec/bash-executor.ts:119-380</i>"]
    BE --> CWD_RESOLVE["cwd: resolveShellCwd()<br/>realpath resolving<br/><i>:95-105</i>"]
    BE --> ENV_MERGE["env: NON_INTERACTIVE_ENV merge<br/><i>:127</i>"]
    BE --> TIMEOUT["timeout: 300s default + abort race<br/><i>:210-217</i>"]
    BE --> CANCEL["cancellation: AbortSignal<br/>+ abortCurrentExecution()<br/><i>:177-184</i>"]
    BE --> SHELL_Q{"oneShot?"}
    SHELL_Q -->|Yes| SHELL_RUN["executeShell()<br/>@gajae-code/natives<br/><i>:223-254</i>"]
    SHELL_Q -->|No| PERSIST["Shell.run() — persistent session<br/>process-global, key = shell+prefix+snapshot+env+sessionKey<br/><i>:62-65, 382-397</i>"]

    SHELL_RUN --> SINK
    PERSIST --> SINK["OutputSink<br/>+ artifactPath/artifactId<br/>+ artifact://&lt;id&gt; footer<br/><i>:133-144, 329-343</i>"]
    SINK --> CHUNK["onChunk (50ms throttle)<br/>onRawChunk (unthrottled)<br/>UI preview<br/><i>:21-27, 140-144</i>"]
    CHUNK --> RESULT(["AgentToolResult"])

    subgraph LIFECYCLE["8개 Lifecycle 차원 (전부 tool 실행의 일부)"]
        direction LR
        L1["cwd: 확인"]
        L2["env: 확인"]
        L3["timeout: 확인"]
        L4["cancellation: 확인"]
        L5["artifact: 확인"]
        L6["background job: 확인"]
        L7["UI preview: 확인"]
        L8["permission: 확인<br/>(session-level wrapper)"]
    end

    BE -.통합.-> LIFECYCLE

    classDef lifecycle fill:#e6f7ff,stroke:#1f6feb
    class LIFECYCLE lifecycle
```

---

## 10. Subagent = Owned Task (Lifecycle Metadata)

> **연관 문서:** [4.5 Subagent = owned task](./GAJAE-CODE-ANALYSIS.md#45-multi-agent--async-job-system), [특성 5. Owned Task](./GAJAE-CODE-ANALYSIS.md#특성-5-subagent를-owned-task로-lifecycle-ownership)
> **코드:** `task/index.ts:650-807`, `task/executor.ts`, `async/job-manager.ts`

이것이 Gajae-Code의 **가장 차별적인 설계**. subagent가 떠다니는 model call이 아니라, lifecycle metadata를 가진 소유된 작업이라는 점을 시각화.

```mermaid
flowchart TD
    PARENT["Parent AgentSession"] --> TASKTOOL["TaskTool 호출<br/><i>task/index.ts</i>"]

    TASKTOOL --> REGISTER["manager.register(...)<br/><b>model call 이전에</b> 등록<br/><i>task/index.ts:650-807</i>"]

    subgraph METADATA["Lifecycle Metadata (전부 코드로 확인됨)"]
        direction TB
        M_OWNER["owner: ownerId<br/>= parent.getAgentId()<br/><i>task/index.ts:764</i><br/><b>격리의 핵심</b>"]
        M_MODEL["model selection<br/>requestedModel/effectiveModel/<br/>modelFellBack<br/><i>executor.ts:1163-1171</i>"]
        M_SESSION["session file<br/>{id}.jsonl<br/><i>executor.ts:568-570</i>"]
        M_OUTPUT["output stream<br/>AgentProgress<br/>{status, tools, output,<br/>tokens, cost, durationMs}<br/><i>executor.ts:524-542</i>"]
        M_PROGRESS["progress events<br/>recordSubagentProgress()<br/><i>job-manager.ts:636</i>"]
        M_DELIVERY["completion delivery<br/>AsyncJobDelivery<br/>+ retry/backoff/dead-letter<br/><i>job-manager.ts:141</i>"]
        M_RESUME["resume descriptor<br/>registerResumeDescriptor()<br/><i>task/index.ts:786</i>"]
    end

    REGISTER --> METADATA
    METADATA --> SPAWN["runSubprocess()<br/><i>executor.ts</i>"]
    SPAWN --> CHILD["Child AgentSession<br/>(별도 session file)"]

    CHILD --> EVENTS["progress 이벤트 스트림"]
    EVENTS --> JM["AsyncJobManager"]
    JM --> DELIVERY_Q["delivery queue<br/>(owner-scoped)"]
    DELIVERY_Q -->|parent 바쁘면| RETRY["retry + backoff<br/>MAX_ATTEMPTS=3"]
    RETRY -->|실패| DLQ["dead-letter store"]
    DELIVERY_Q -->|parent 준비 시| PARENT2["Parent에게 completion 전달"]

    CHILD -.owner 격리.-> ISOLATION["한 agent의 job/cleanup/<br/>output cursor가<br/>다른 agent와 분리됨<br/>registerOwnerCleanup()<br/><i>job-manager.ts:968</i>"]

    classDef owned fill:#fff3f3,stroke:#ff4d4f,stroke-width:2px
    classDef key fill:#fffbe6,stroke:#d4a017,stroke-width:2px
    class METADATA owned
    class M_OWNER key
```

> **가장 강력한 증거:** subagent를 launch하는 모든 경로는 model call 전에 `manager.register(...)`를 거친다. "bare model call로 subagent를 launch하는 코드 경로는 존재하지 않는다."

---

## 11. AsyncJobManager 상태머신

> **연관 문서:** [4.5 AsyncJobManager 기능](./GAJAE-CODE-ANALYSIS.md#45-multi-agent--async-job-system), [특성 6. Cooperative Cancellation](./GAJAE-CODE-ANALYSIS.md#특성-6-cooperative-cancellation과-safe-boundary)
> **코드:** `async/job-manager.ts:76` (`SubagentLifecycle`), `:396-496`

`SubagentLifecycle = running | paused | queued | completed | failed | cancelled` 상태와 transition. cooperative safe-boundary pause가 핵심.

```mermaid
stateDiagram-v2
    [*] --> queued: register()
    queued --> running: resumeSubagent()<br/>(FIFO #resumeQueue에서 drain)

    running --> completed: outcome.kind=completed<br/><i>:443-449</i>
    running --> failed: error 발생<br/><i>:462-467</i>
    running --> paused: requestPause()<br/><b>cooperative safe-boundary</b><br/>(in-flight tool은 완료)<br/><i>:431-435</i>
    running --> cancelled: cancel() during run<br/><i>:496</i>

    paused --> running: resumeSubagent()<br/>sessionFile에서 재개<br/><i>:726-759</i>
    paused --> cancelled: cancel() while paused<br/><i>:486-491</i>

    queued --> cancelled: cancel() while queued<br/><i>:792-819</i>

    completed --> [*]
    failed --> [*]
    cancelled --> [*]

    note right of running
        result validation:
        buildOutputValidator()로
        JSON-Schema 검증
        schema_violation 시 exitCode 1
        <i>executor.ts:189-207</i>
    end note

    note right of paused
        Pause ≠ Cancel:
        Pause = safe boundary,
        tool은 완료 후 정지,
        재개 가능
        <i>job-manager.ts:83-88</i>
    end note
```

> **설계 철학:** "정지"는 두 가지로 나뉜다 — **Pause**(safe boundary, 협력적, 재개 가능) vs **Cancel**(최후 수단). Go의 `context.Cancel()`이나 Rust의 `CancellationToken`과 같은 structured concurrency 철학.

---

## 12. Coordinator MCP: File-based Control Surface

> **연관 문서:** [4.5 Coordinator MCP](./GAJAE-CODE-ANALYSIS.md#45-multi-agent--async-job-system), [특성 7. File-based Coordinator](./GAJAE-CODE-ANALYSIS.md#특성-7-coordinator는-scrollback이-아니라-filestate-기반)
> **코드:** `coordinator-mcp/server.ts`, `harness-control-plane/session-lease.ts`

tmux scrollback 파싱(가장 흔한 안티패턴) 대신, file/state를 진실의 원천로 두는 구조.

```mermaid
flowchart TB
    subgraph EXTERNAL["외부 Controller / Bot"]
        CTRL["Python bot<br/>또는 다른 agent"]
    end

    CTRL -->|"MCP tool call"| MCP["Coordinator MCP<br/><i>coordinator-mcp/server.ts</i>"]

    subgraph OPS["MCP Operations (file/state-based)"]
        direction LR
        OP1["start_session<br/>send_prompt<br/>read_turn / await_turn<br/>submit_question_answer"]
        OP2["report_status<br/>read_coordination_status"]
        OP3["read_artifact<br/>list_artifacts"]
        OP4["read_tail<br/><b>'not tmux scrollback'</b><br/><i>server.ts:381</i>"]
        OP5["watch_events<br/>long-poll event journal"]
    end

    MCP --> OPS

    OPS -->|"mutating tool은<br/>allow_mutation: true 필수"| PERM["permission boundary<br/><i>server.ts:241,266,340,360</i>"]
    PERM --> STATE

    subgraph STATE["Authoritative Source (Durable File State)"]
        direction TB
        EVENT[("event-journal.jsonl<br/>+ latest-seq.json<br/><i>server.ts:524-529</i>")]
        QUESTIONS[("questions/&lt;id&gt;.json<br/>structured Q&A")]
        TURNS[("turns/<br/>durable turn state")]
        ARTIFACTS[("artifacts/<br/>bounded output")]
    end

    STATE -.진실의 원천.-> MCP
    MCP -. advisory only .-> TMUX["tmux<br/>send-keys delivery 채널<br/>(진실 아님)"]

    subgraph LEASE["Lease — 단일 writer 보장<br/><i>harness-control-plane/session-lease.ts</i>"]
        direction TB
        L_OBJ["SessionLease<br/>{ownerId, leaseTokenHash,<br/>leaseEpoch, expiresAt, heartbeatAt}"]
        L_RULE["writeLeaseAtomic()<br/>leaseEpoch 증가로 handoff<br/>만료 lease = NEVER permission<br/>for destructive recovery"]
    end

    STATE -.단일 writer.-> LEASE

    classDef external fill:#fffbe6,stroke:#d4a017
    classDef mcp fill:#1f6feb,color:#fff,stroke:#0d4ea6,stroke-width:2px
    classDef stateBox fill:#e6ffe6,stroke:#2da44e,stroke-width:2px
    classDef lease fill:#ffe6e6,stroke:#ff4d4f,stroke-width:2px
    class CTRL external
    class MCP mcp
    class STATE stateBox
    class LEASE lease
```

> **핵심 설계:** tmux는 `send-keys` delivery 채널일 뿐, **진실의 원천은 durable file state**다. "Read authoritative durable turn state plus bounded advisory tmux status" (`server.ts:302`).

---

## 13. Model Provider Runtime Registry

> **연관 문서:** [4.6 Model Provider 분리](./GAJAE-CODE-ANALYSIS.md#46-model-provider-분리), [특성 8. Runtime Registry](./GAJAE-CODE-ANALYSIS.md#특성-8-provider를-runtime-registry로-dependency-inversion)
> **코드:** `packages/ai/src/`, `config/model-registry.ts:964`, `session/agent-session.ts:5750-5826`

provider-neutral API 뒤에 ~47개 adapter가 있고, `ModelRegistry`가 mutable runtime 객체로 model 선택을 policy로 다루는 구조.

```mermaid
flowchart TB
    subgraph CONSUMERS["Consumer"]
        SESSION["AgentSession"]
        SUBAGENT["Subagent<br/>(inherit or override)"]
    end

    CONSUMERS -->|"runtime 전환"| SWITCH["5개 이상 메서드<br/>setModel / setModelTemporary<br/>cycleModel / cycleRoleModels<br/>setActiveModelProfile<br/><i>agent-session.ts:5750-5826</i>"]
    SWITCH --> REGISTRY

    subgraph REGISTRY["ModelRegistry (mutable runtime 객체)<br/><i>model-registry.ts:964</i>"]
        direction TB
        REG_API["registerProvider()<br/>refresh() / refreshProvider()<br/>runtime overlays"]
        REG_CRED["credential lookup<br/>getApiKey(model, sessionId?)<br/>→ authStorage<br/><i>:2467</i>"]
        REG_FALLBACK["retry-fallback chains<br/>(settings = policy)<br/>cooldown-based revert"]
        REG_DISABLED["disabledFeatures 추적<br/>provider의 조용한 fallback까지<br/><i>types.ts:584-590</i>"]
    end

    REGISTRY -->|"provider-neutral"| AI_LAYER

    subgraph AI_LAYER["packages/ai — Provider-Neutral API"]
        direction TB
        AI_STREAM["stream(model, context, opts)<br/>→ AssistantMessageEventStream<br/><i>stream.ts:197</i><br/>model.api로 dispatch"]
        AI_COMPLETE["complete()<br/><i>stream.ts:276</i>"]
        AI_TYPES["Context, Tool,<br/>AssistantMessage (정규화됨)<br/><i>types.ts:571, 667, 692</i>"]
        AI_CUSTOM["getCustomApi()<br/>runtime API 주입 hook"]
    end

    AI_LAYER -->|"dispatch"| DISPATCH{"model.api?"}

    subgraph ADAPTERS["Provider Adapters (~47개)<br/><i>packages/ai/src/providers/</i>"]
        direction LR
        P_ANT["anthropic.ts<br/>(98KB)"]
        P_OAI["openai-responses.ts<br/>openai-codex-responses.ts<br/>(93KB) + openai-codex/"]
        P_GOOGLE["google*.ts<br/>(6개 파일)"]
        P_CURSOR["cursor.ts + cursor/"]
        P_BEDROCK["amazon-bedrock.ts<br/>aws-credentials.ts"]
        P_ETC["ollama, kimi, gitlab-duo,<br/>... (~47개 KnownProvider)"]
    end

    DISPATCH --> P_ANT
    DISPATCH --> P_OAI
    DISPATCH --> P_GOOGLE
    DISPATCH --> P_CURSOR
    DISPATCH --> P_BEDROCK
    DISPATCH --> P_ETC

    REGISTRY -.catalog.-> CATALOG[("models.json (1.6MB)<br/>bundled static catalog<br/><i>models.ts:2</i><br/>generate-models.ts로 생성<br/>(compile-time only)")]

    FUZZY["fuzzyMatch<br/>tryMatchModel()<br/><i>model-resolver.ts:328</i><br/>주의: model-registry.ts가 아님"]
    REGISTRY -.pattern 해석.-> FUZZY

    classDef consumer fill:#fff3f3,stroke:#ff4d4f
    classDef registry fill:#1f6feb,color:#fff,stroke:#0d4ea6,stroke-width:2px
    classDef neutral fill:#e6f7ff,stroke:#1f6feb
    classDef adapter fill:#f0f0f0,stroke:#666
    classDef catalog fill:#fffbe6,stroke:#d4a017
    class SESSION,SUBAGENT consumer
    class REGISTRY registry
    class AI_LAYER neutral
    class ADAPTERS adapter
    class CATALOG,FUZZY catalog
```

> **핵심 주장:** "model selection은 hard dependency가 아니라 runtime policy다." — `ModelRegistry`는 mutable, 5개 이상의 runtime 전환 메서드, retry-fallback이 settings(정책)로 구성.

---

## 14. 핵심 철학: Advisory vs Authoritative

> **연관 문서:** [Part 6. 8가지 특성의 공통 철학](./GAJAE-CODE-ANALYSIS.md#8가지-특성의-공통-철학)

8가지 설계 특성이 수렴하는 하나의 철학: **"AI agent를 채팅이 아니라 auditable runtime으로 취급하라"**.

```mermaid
flowchart LR
    subgraph ADVISORY["LLM은 장려 (advisory)<br/>— 깨지기 쉬운 접근"]
        direction TB
        A1["Prompt로 행동 유도<br/>(LLM이 무시하면 끝)"]
        A2["Context에 상태 의존<br/>(압축/세션 종료 시 소실)"]
        A3["Fire-and-forget LLM call<br/>(parent 죽으면 자식 증발)"]
        A4["Hard SIGTERM<br/>(in-flight tool 잘림)"]
        A5["Scrollback regex 파싱<br/>(race condition, context limit)"]
        A6["Hard-coded provider<br/>(import Anthropic everywhere)"]
    end

    subgraph AUTHORITATIVE["Runtime은 강제 (authoritative)<br/>— Gajae-Code의 접근"]
        direction TB
        B1["Guard로 행동 보장<br/>assertDeepInterviewMutationAllowed"]
        B2["File에 상태 (durable)<br/>.gjc/ 아래 atomic write"]
        B3["Owned task (lifecycle)<br/>owner + session + delivery"]
        B4["Cooperative safe-boundary<br/>tool 완료 후 pause"]
        B5["Explicit control surface<br/>file/state-based coordinator"]
        B6["Runtime registry<br/>ModelRegistry + 5개 전환 메서드"]
    end

    A1 -.보완.-> B1
    A2 -.보완.-> B2
    A3 -.보완.-> B3
    A4 -.보완.-> B4
    A5 -.보완.-> B5
    A6 -.보완.-> B6

    AUTHORITATIVE --> PRINCIPLE

    PRINCIPLE["핵심 원칙<br/><b>LLM의 비결정성을<br/>시스템의 결정성으로 보완한다</b>"]

    PRINCIPLE --> SE["소프트웨어 공학과의 대응<br/>• Capability-based security<br/>• Event sourcing + snapshot<br/>• Postel's Law (lenient read/strict write)<br/>• Syscall interface (unified contract)<br/>• Process lineage + structured concurrency<br/>• CancellationToken<br/>• Headless API vs scraping<br/>• Strategy pattern + DIP"]

    classDef bad fill:#ffe6e6,stroke:#ff4d4f
    classDef good fill:#e6ffe6,stroke:#2da44e
    classDef principle fill:#1f6feb,color:#fff,stroke:#0d4ea6,stroke-width:3px
    class ADVISORY bad
    class AUTHORITATIVE good
    class PRINCIPLE principle
```

> **결론:** Gajae-Code가 발명한 것은 별로 없다. **오래 검증된 소프트웨어 공학 원칙들을 AI agent라는 새 영역에 충실하게 적용한 것**이 핵심 가치다.

---

## 렌더링 참고

- **GitHub:** mermaid 블록이 자동 렌더링됨
- **VS Code:** [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) 확장 필요
- **CLI:** `npx @mermaid-js/mermaid-cli`로 PNG/SVG export 가능

각 다이어그램의 `> 연관 문서:` 인용은 [`GAJAE-CODE-ANALYSIS.md`](./GAJAE-CODE-ANALYSIS.md)의 해당 섹션 앵커로 연결된다.

---

*본 도식집은 2026-06-18 기준 Gajae-Code 소스 코드를 직접 대조하여 작성됐다.*
