# Gajae-Code 소스 Walkthrough

이 문서는 `packages/coding-agent/`를 중심으로 Gajae-Code 소스를 실제 파일 순서대로 따라 읽기 위한 안내서입니다. [ARCHITECTURE.md](ARCHITECTURE.md)가 아이디어 지도라면, 이 문서는 “어느 파일에서 시작해 어떤 호출 관계를 확인할 것인가”에 초점을 둡니다.

기본 원칙은 세 가지입니다.

- GitNexus wiki로 먼저 지도를 잡고, 중요한 결론은 직접 소스에서 확인합니다.
- `packages/coding-agent/`를 주 제품 표면으로 읽고, 나머지는 의존/보조 경계로 읽습니다.
- Claude Code, Codex CLI 같은 host agent tool과 Anthropic/OpenAI/Codex Responses 같은 model provider를 분리해서 봅니다.

## 먼저 읽을 생성 지도

로컬 GitNexus wiki가 있다면 다음 순서로 읽는 것이 좋습니다.

1. `.gitnexus/wiki/overview.md`
2. `.gitnexus/wiki/module_tree.json`
3. `.gitnexus/wiki/coding-agent-cli-and-commands.md`
4. `.gitnexus/wiki/coding-agent-session-runtime.md`
5. `.gitnexus/wiki/execution-and-tools.md`
6. `.gitnexus/wiki/coding-agent-workflow-skills-and-state-runtime.md`
7. `.gitnexus/wiki/subagents-and-async-jobs.md`
8. `.gitnexus/wiki/support-boundary-ai-provider-layer.md`
9. `.gitnexus/wiki/dependency-and-support-boundary.md`

이 문서의 파일 경로와 호출 흐름은 위 GitNexus 결과를 출발점으로 삼되, 실제 소스 파일에서 다시 확인한 기준점입니다.

## 전체 읽기 순서

처음부터 모든 디렉터리를 펼쳐 보면 흐름을 놓치기 쉽습니다. 아래 순서대로 읽으면 제품 표면에서 하위 runtime으로 자연스럽게 내려갈 수 있습니다.

```text
CLI entry
  -> launch parsing
  -> session construction
  -> AgentSession
  -> @gajae-code/agent-core Agent
  -> packages/ai provider layer
  -> tool registry
  -> workflow state
  -> async job / subagent
  -> UI / external modes
```

## 1. CLI 진입점

시작 파일은 `packages/coding-agent/src/cli.ts`입니다.

확인할 anchor:

- `installRuntimeGlobals()`
- `isSubcommand(first)`
- `runSmokeTest()`
- `runCli(argv)`

읽을 때 봐야 할 점:

- `gjc` 실행 파일이 Bun runtime을 전제로 시작합니다.
- `--help`, `--version`, `--smoke-test` 같은 fast path가 먼저 처리됩니다.
- 첫 번째 인자가 등록된 subcommand가 아니면 전체 호출이 `launch`로 재작성됩니다.
- 실제 명령 목록은 `commands` 배열과 `src/commands/*` 모듈을 통해 등록됩니다.

기본 흐름:

```text
gjc "prompt"
  -> runCli(argv)
  -> isSubcommand(first) === false
  -> ["launch", ...argv]
  -> launch command
  -> runRootCommand()
```

명시적 command는 다른 경로로 갑니다.

```text
gjc config list
  -> runCli(argv)
  -> isSubcommand("config") === true
  -> src/commands/config.ts
  -> src/cli/config-cli.ts
```

## 2. Launch와 초기 입력 구성

다음 파일은 `packages/coding-agent/src/main.ts`입니다. 이 파일은 `launch` command의 실제 본체입니다.

확인할 anchor:

- `main(args)`
- `runRootCommand(parsed, rawArgs, deps)`
- `createSessionManager(parsed, cwd, settings)`
- `buildSessionOptions(...)`
- `applyStartupModelProfiles(...)`
- `runInteractiveMode(...)`
- mode 분기: `runPrintMode`, `runRpcMode`, `runAcpMode`, `runBridgeMode`

함께 읽을 파일:

- `packages/coding-agent/src/cli/args.ts`
- `packages/coding-agent/src/cli/file-processor.ts`
- `packages/coding-agent/src/cli/initial-message.ts`

`runRootCommand()`에서 집중할 흐름:

1. theme, logger, cwd 자동 보정이 먼저 실행됩니다.
2. auth storage와 `ModelRegistry`가 초기화됩니다.
3. `Settings.init({ cwd })`로 프로젝트/사용자 설정을 읽습니다.
4. stdin, 일반 메시지, `@file`, 이미지 입력을 초기 메시지로 합칩니다.
5. `createSessionManager()`가 새 세션, resume, continue, fork, in-memory 모드를 결정합니다.
6. `buildSessionOptions()`가 `createAgentSession()`에 넘길 옵션을 만듭니다.
7. `createAgentSession()` 결과를 실행 mode에 연결합니다.

mode 분기는 제품 표면을 이해하는 데 중요합니다.

| Mode | 대략적 역할 |
| --- | --- |
| interactive | TUI 기반 일반 대화형 세션 |
| print | 비대화형 단발 실행 |
| rpc / rpc-ui | 외부 프로세스가 제어하는 RPC 세션 |
| acp | ACP client가 만드는 격리 세션 |
| bridge | client bridge와 연결되는 세션 |

## 3. Session 조립

핵심 파일은 `packages/coding-agent/src/sdk.ts`입니다.

확인할 anchor:

- `discoverExtensions(...)`
- `withEmbeddedDefaultGjcSkills(skills)`
- `createAgentSession(options)`
- `ToolSession`
- `createTools(toolSession, options.toolNames)`
- `rebuildSystemPrompt(...)`
- `convertToLlmFinal(...)`
- `new Agent(...)`
- `new AgentSession(...)`

`createAgentSession()`은 이 프로젝트의 runtime assembly 함수입니다. 단순히 agent 객체 하나를 만드는 함수가 아니라, 아래 계층을 한 번에 조립합니다.

- `AuthStorage`
- `ModelRegistry`
- `Settings`
- `SessionManager`
- workspace tree와 context file
- AGENTS/rules/skills/prompt template
- built-in/custom/extension/MCP tool
- system prompt
- `@gajae-code/agent-core`의 `Agent`
- `AgentSession`

읽을 때 핵심은 `ToolSession`입니다. 도구는 session 생성 전에도 만들어져야 하지만, 실행 시점에는 최신 session 상태가 필요합니다. 그래서 `ToolSession`은 `cwd`, 현재 model, artifact path, active skill state, plan/goal state, tool choice queue 등을 getter 형태로 늦게 참조합니다.

## 4. AgentSession

다음 중심 파일은 `packages/coding-agent/src/session/agent-session.ts`입니다.

확인할 anchor:

- `export class AgentSession`
- `constructor(config)`
- `prompt(text, options?)`
- `promptCustomMessage(...)`
- `dispose()`
- `setModel(...)`
- `setModelTemporary(...)`
- `toolChoiceQueue`
- plan/goal mode state getter/setter
- `AsyncJobManager.instance()` 사용 지점

`AgentSession`은 모든 실행 mode가 공유하는 세션 객체입니다. interactive, print, RPC, ACP, bridge는 입출력 방식이 다르지만, message 저장, model 변경, tool call 처리, plan/goal 상태, async job cleanup 같은 핵심 동작은 `AgentSession`으로 모입니다.

특히 다음 책임을 확인해야 합니다.

- 사용자 prompt를 내부 message로 변환하고 agent에 전달합니다.
- agent event를 구독해 session file과 UI에 반영합니다.
- tool choice queue를 통해 강제 tool 호출이나 workflow reminder를 제어합니다.
- model과 thinking level 변경을 session state에 반영합니다.
- 세션 종료 시 자기 owner 범위의 async job을 정리합니다.
- plan mode와 goal mode 상태를 model transcript 바깥 runtime state와 연결합니다.

## 5. Agent core loop

`packages/coding-agent/`가 제품 runtime을 소유한다면, 저수준 agent loop는 `packages/agent/`가 담당합니다.

읽을 파일:

- `packages/agent/src/agent.ts`
- `packages/agent/src/agent-loop.ts`
- `packages/agent/src/index.ts`

확인할 anchor:

- `Agent`
- `agentLoop(...)`
- `agentLoopContinue(...)`
- `createAgentStream()`
- `runLoopBody(...)`
- `streamAssistantResponse(...)`
- tool execution event 생성 지점

핵심 흐름:

```text
AgentSession.prompt()
  -> Agent.run / Agent stream
  -> agentLoop()
  -> streamAssistantResponse()
  -> packages/ai streamSimple()
  -> assistant message / tool call events
  -> tool execution
  -> tool result message
  -> next loop or agent_end
```

여기서 `packages/agent`는 provider나 CLI 정책을 직접 소유하지 않습니다. model 호출은 `packages/ai`에 위임하고, 실제 tool 구현은 `packages/coding-agent`에서 만든 registry를 사용합니다.

## 6. Tool registry와 실행 경계

tool 계층은 `packages/coding-agent/src/tools/`와 관련 실행 디렉터리에서 시작합니다.

읽을 파일:

- `packages/coding-agent/src/tools/index.ts`
- `packages/coding-agent/src/tools/bash.ts`
- `packages/coding-agent/src/exec/bash-executor.ts`
- `packages/coding-agent/src/edit/index.ts`
- `packages/coding-agent/src/runtime-mcp/`
- `packages/coding-agent/src/web/`

확인할 anchor:

- `ToolSession`
- `BUILTIN_TOOLS`
- `createTools(session, toolNames?)`
- `BashTool`
- `executeBash(command, options)`
- `EditTool`

`tools/index.ts`의 `BUILTIN_TOOLS`가 기본 registry의 출발점입니다. 여기서 `bash`, `edit`, `ast_grep`, `ast_edit`, `ask` 같은 도구가 factory 형태로 등록됩니다.

tool 실행은 크게 세 경계를 가집니다.

| 경계 | 주요 파일 | 역할 |
| --- | --- | --- |
| registry | `tools/index.ts` | session에서 사용할 도구 목록을 구성합니다. |
| policy wrapper | `tools/bash.ts`, `edit/index.ts` | schema, 실행 전 검증, UI metadata, error mapping을 담당합니다. |
| backend | `exec/bash-executor.ts`, `edit/modes/*`, `runtime-mcp/`, `web/` | 실제 shell, patch, MCP, web 동작을 수행합니다. |

가장 중요한 예시는 shell 실행입니다.

```text
Agent tool call: bash
  -> BashTool.execute()
  -> #prepareBashExecution()
  -> executeBash()
  -> shell session / OutputSink
  -> foreground result or AsyncJobManager job
```

문서나 분석에서 “도구를 실행한다”고 말할 때는 이 세 층을 구분해야 합니다. prompt에 tool 설명이 보이는 것과, 실제 tool backend가 timeout/cwd/env/artifact/cancellation을 관리하는 것은 다른 책임입니다.

## 7. Workflow skill과 `.gjc` state

workflow 표면은 `packages/coding-agent/src/defaults/gjc-defaults.ts`에서 시작합니다.

읽을 파일:

- `packages/coding-agent/src/defaults/gjc-defaults.ts`
- `packages/coding-agent/src/defaults/gjc/skills/`
- `packages/coding-agent/src/skill-state/`
- `packages/coding-agent/src/gjc-runtime/state-runtime.ts`
- `packages/coding-agent/src/gjc-runtime/state-writer.ts`
- `packages/coding-agent/src/gjc-runtime/state-schema.ts`
- `packages/coding-agent/src/deep-interview/render-middleware.ts`

공개 workflow skill은 네 개로 읽는 것이 제품 계약에 맞습니다.

| Skill | 역할 |
| --- | --- |
| `deep-interview` | 모호한 요구사항을 구현 전 명확히 합니다. |
| `ralplan` | 변경 전 계획과 검토 게이트를 둡니다. |
| `ultragoal` | 긴 작업을 goal, revision, evidence로 추적합니다. |
| `team` | tmux 기반 병렬 worker 실행을 coordination합니다. |

핵심은 workflow 상태가 chat transcript에만 남지 않는다는 점입니다. skill activation, plan, goal, ledger, HUD용 state는 `.gjc/` 아래에 기록되고, runtime helper가 원자적으로 갱신합니다.

workflow 흐름을 읽을 때는 다음 구조를 찾으면 됩니다.

```text
user invokes workflow
  -> keyword / skill detection
  -> record activation
  -> seed workflow state
  -> write .gjc state envelope
  -> prompt / UI / hook state reads same envelope
```

Deep Interview는 특히 스킬 Markdown과 TUI renderer가 맞물려 있습니다. `SKILL.md`의 출력 형식이 `render-middleware.ts`의 parser와 계약을 이루므로, 문구 변경도 UI 계약 변경이 될 수 있습니다.

## 8. Multi-agent와 async job

multi-agent 실행은 `packages/coding-agent/src/task/`와 `packages/coding-agent/src/async/`를 함께 읽어야 합니다.

읽을 파일:

- `packages/coding-agent/src/task/agents.ts`
- `packages/coding-agent/src/task/discovery.ts`
- `packages/coding-agent/src/task/executor.ts`
- `packages/coding-agent/src/task/subprocess-tool-registry.ts`
- `packages/coding-agent/src/task/index.ts`
- `packages/coding-agent/src/async/job-manager.ts`
- `packages/coding-agent/src/coordinator-mcp/server.ts`
- `packages/coding-agent/src/harness-control-plane/`

확인할 anchor:

- `parseAgent(...)`
- `loadBundledAgents()`
- `discoverAgents(cwd, home)`
- `AsyncJobManager`
- `AsyncJobManager.register(...)`
- `appendOutput(...)`
- `readOutputSince(...)`
- `pauseSubagent(...)`
- `resumeSubagent(...)`
- `cancelSubagent(...)`
- `runSubprocess(options)`
- `finalizeSubprocessOutput(...)`
- `createSubagentSettings(...)`

제품 문서의 공개 role agent 계약은 `executor`, `architect`, `planner`, `critic` 네 개를 기준으로 읽습니다. 다만 `agents.ts`에는 숨김 또는 내부 utility agent 정의가 함께 존재할 수 있으므로, “사용자-facing 역할 표면”과 “내부 실행 정의”를 구분해서 확인해야 합니다.

subagent 실행 흐름:

```text
parent AgentSession
  -> task tool / workflow command
  -> AsyncJobManager.register(type: "task")
  -> runSubprocess()
  -> createAgentSession() for subagent
  -> subagent AgentSession events
  -> AgentProgress
  -> yield / report_finding extraction
  -> finalizeSubprocessOutput()
  -> completion delivery queue
  -> parent session receives result
```

중요한 설계 선택:

- subagent는 별도 텍스트 출력만 남기는 모델 호출이 아닙니다.
- 안정적인 owner/subagent ID, session file, output cursor, lifecycle state를 가집니다.
- 완료 기준은 assistant text가 아니라 `yield` 또는 schema-valid fallback입니다.
- `AsyncJobManager`는 bash background job과 task/subagent job을 같은 수명주기 레지스트리에서 관리합니다.
- pause/resume/cancel은 작업 ID뿐 아니라 subagent 안정 ID 기준으로도 동작합니다.

## 9. Model provider와 host agent tool

model/provider 경계는 `packages/ai/`와 `packages/coding-agent/src/config/model-registry.ts`를 함께 읽어야 합니다.

읽을 파일:

- `packages/coding-agent/src/config/model-registry.ts`
- `packages/coding-agent/src/config/model-resolver.ts`
- `packages/ai/src/index.ts`
- `packages/ai/src/types.ts`
- `packages/ai/src/stream.ts`
- `packages/ai/src/models.ts`
- `packages/ai/src/models.json`
- `packages/ai/src/providers/anthropic.ts`
- `packages/ai/src/providers/openai-responses.ts`
- `packages/ai/src/providers/openai-codex-responses.ts`
- `packages/ai/src/providers/google-gemini-cli.ts`
- `packages/ai/src/providers/cursor.ts`
- `packages/ai/src/utils/oauth/`
- `packages/ai/src/utils/discovery/codex.ts`

확인할 anchor:

- `ModelRegistry`
- `ModelRegistry.getApiKey(...)`
- `ModelRegistry.registerProvider(...)`
- `ModelRegistry.resolveCanonicalModel(...)`
- `stream(...)`
- `complete(...)`
- `streamSimple(...)`
- `Context`
- `Tool`
- `AssistantMessage`
- `AssistantMessageEvent`

개념 구분:

| 구분 | 예 | 소스 위치 | 의미 |
| --- | --- | --- | --- |
| host agent tool | Claude Code, Codex CLI, OpenCode, Claw Code | README/사용 방식, 외부 실행 경계 | GJC 옆에서 함께 실행될 수 있는 별도 제품입니다. |
| model provider | Anthropic, OpenAI/Codex Responses, Google, Cursor, OpenAI-compatible provider | `packages/ai`, `ModelRegistry` | GJC runtime이 model response를 받기 위해 통신하는 provider 계층입니다. |

GJC는 Claude Code나 Codex CLI의 내부 plugin처럼 동작하는 구조가 아닙니다. 외부 runner로 실행되며, 자기 내부 model layer는 provider-neutral API를 통해 모델 호출을 정규화합니다.

provider layer가 정규화하는 것:

- streaming event
- tool call block
- model/provider ID
- OAuth/API key lookup
- usage/cost
- provider compatibility flag
- fallback과 model discovery

## 10. UI와 실행 mode

사용자에게 보이는 화면은 `packages/coding-agent/src/modes/`와 `packages/tui/`의 결합으로 이해합니다.

읽을 파일:

- `packages/coding-agent/src/modes/`
- `packages/coding-agent/src/modes/components/`
- `packages/coding-agent/src/modes/rpc/`
- `packages/coding-agent/src/modes/acp/`
- `packages/coding-agent/src/modes/bridge/`
- `packages/tui/src/`

읽을 때 주의할 점:

- `AgentSession`은 제품 상태와 agent event를 소유합니다.
- mode 계층은 입출력 채널을 선택합니다.
- TUI package는 rendering, input, markdown, width 처리 같은 화면 책임을 맡습니다.
- tool renderer는 tool result details를 받아 화면 표현으로 바꿉니다.

이 분리는 중요합니다. session/runtime을 이해하려면 UI 컴포넌트부터 읽는 것보다 `AgentSession`과 mode adapter를 먼저 읽는 편이 빠릅니다.

## 11. 의존/보조 경계

`packages/coding-agent/` 바깥은 다음 기준으로 읽습니다.

| 영역 | 읽을 때 |
| --- | --- |
| `packages/agent/` | model/tool loop, event stream, compaction, append-only context를 볼 때 |
| `packages/ai/` | provider, model catalog, OAuth/API key, streaming compatibility를 볼 때 |
| `packages/tui/` | terminal UI rendering 문제를 볼 때 |
| `packages/natives/`, `crates/` | grep/search/image/native binding, shell/isolation 성능 경계를 볼 때 |
| `packages/stats/` | `gjc stats`와 local observability를 볼 때 |
| `packages/utils/`, `packages/bridge-client/` | 여러 package가 공유하는 utility와 bridge protocol을 볼 때 |
| `python/gjc-rpc/`, `python/robogjc/` | Python RPC host와 GitHub 자동화를 볼 때 |

기본 분석에서는 이 영역을 `packages/coding-agent/`를 보조하는 경계로 다루면 됩니다. 해당 package 자체를 수정하거나 확장해야 할 때만 깊게 들어갑니다.

## 호출 흐름별 빠른 추적

### `gjc "prompt"`를 추적할 때

1. `packages/coding-agent/src/cli.ts`
2. `packages/coding-agent/src/main.ts`
3. `packages/coding-agent/src/sdk.ts`
4. `packages/coding-agent/src/session/agent-session.ts`
5. `packages/agent/src/agent.ts`
6. `packages/agent/src/agent-loop.ts`
7. `packages/ai/src/stream.ts`

핵심 질문:

- 첫 번째 인자가 subcommand로 인식되는가?
- 초기 메시지는 어디서 만들어지는가?
- 어떤 session manager가 선택되는가?
- 어떤 model이 선택되는가?
- system prompt와 tool registry는 언제 확정되는가?

### `bash` tool을 추적할 때

1. `packages/coding-agent/src/tools/index.ts`
2. `packages/coding-agent/src/tools/bash.ts`
3. `packages/coding-agent/src/exec/bash-executor.ts`
4. `packages/coding-agent/src/async/job-manager.ts`
5. `packages/agent/src/agent-loop.ts`

핵심 질문:

- foreground 실행인가 background job인가?
- cwd/env/timeout은 어디서 검증되는가?
- 출력은 UI preview와 raw artifact로 어떻게 나뉘는가?
- non-zero exit은 어떻게 tool error로 변환되는가?

### `deep-interview`를 추적할 때

1. `packages/coding-agent/src/defaults/gjc-defaults.ts`
2. `packages/coding-agent/src/defaults/gjc/skills/deep-interview/SKILL.md`
3. `packages/coding-agent/src/skill-state/`
4. `packages/coding-agent/src/gjc-runtime/`
5. `packages/coding-agent/src/deep-interview/render-middleware.ts`

핵심 질문:

- skill activation은 어디에 기록되는가?
- `.gjc` state envelope은 어떤 schema를 따르는가?
- 질문/진행 출력 형식은 renderer와 맞는가?
- 이 workflow는 실행으로 바로 넘어가는가, 아니면 승인/브리지 게이트를 요구하는가?

### subagent/task를 추적할 때

1. `packages/coding-agent/src/task/agents.ts`
2. `packages/coding-agent/src/task/discovery.ts`
3. `packages/coding-agent/src/task/index.ts`
4. `packages/coding-agent/src/async/job-manager.ts`
5. `packages/coding-agent/src/task/executor.ts`
6. `packages/coding-agent/src/task/subprocess-tool-registry.ts`

핵심 질문:

- 어떤 agent definition이 선택되는가?
- project/user/bundled agent 우선순위는 어떻게 적용되는가?
- job owner ID는 무엇인가?
- subagent session은 부모 session과 어떤 설정을 공유하고 어떤 설정을 끄는가?
- 최종 성공 기준은 `yield`인가, schema-valid fallback인가?

### model fallback을 추적할 때

1. `packages/coding-agent/src/main.ts`
2. `packages/coding-agent/src/config/model-registry.ts`
3. `packages/coding-agent/src/config/model-resolver.ts`
4. `packages/coding-agent/src/sdk.ts`
5. `packages/ai/src/types.ts`
6. `packages/ai/src/providers/*`

핵심 질문:

- CLI `--model`이 명시됐는가?
- session에 저장된 model이 복원되는가?
- credential이 있는 provider인가?
- extension이나 config에서 provider가 runtime 등록되는가?
- fallback이 발생하면 사용자에게 어떤 message로 드러나는가?

## GitNexus와 직접 소스 확인 대조표

| GitNexus 기준 | 직접 확인한 source anchor | 확인 내용 |
| --- | --- | --- |
| `coding-agent-cli-and-commands.md` | `cli.ts`의 `runCli()`, `isSubcommand()`, `main.ts`의 `runRootCommand()` | 일반 prompt가 `launch`로 라우팅되고, 명시적 command는 `commands/*`로 분기됩니다. |
| `coding-agent-session-runtime.md` | `sdk.ts`의 `createAgentSession()`, `AgentSession` 생성 지점 | session assembly가 settings, auth, model, tools, prompt, agent core, session wrapper를 묶습니다. |
| `execution-and-tools.md` | `tools/index.ts`의 `BUILTIN_TOOLS`, `createTools()`, `BashTool`, `executeBash()` | tool은 registry, policy wrapper, backend로 나뉘어 실행됩니다. |
| `coding-agent-workflow-skills-and-state-runtime.md` | `gjc-defaults.ts`, `defaults/gjc/skills/`, `gjc-runtime/`, `skill-state/` | 공개 workflow skill은 작은 표면으로 유지되고 `.gjc` state와 연결됩니다. |
| `subagents-and-async-jobs.md` | `AsyncJobManager`, `runSubprocess()`, `finalizeSubprocessOutput()` | subagent는 async job lifecycle, progress, yield validation을 통해 완료됩니다. |
| `support-boundary-ai-provider-layer.md` | `ModelRegistry`, `packages/ai/src/types.ts`, `providers/*`, `utils/oauth/*` | provider 차이는 `packages/ai`와 model registry 뒤에서 정규화됩니다. |
| `dependency-and-support-boundary.md` | root workspace, `packages/*`, `crates/`, `python/*` | `packages/coding-agent/`가 제품 표면이고 다른 package는 지원 경계입니다. |

## 시간별 읽기 계획

### 1시간 안에 큰 그림만 볼 때

1. `ARCHITECTURE.md`
2. `.gitnexus/wiki/overview.md`
3. `packages/coding-agent/src/cli.ts`
4. `packages/coding-agent/src/main.ts`
5. `packages/coding-agent/src/sdk.ts`
6. `packages/coding-agent/src/session/agent-session.ts`

목표는 “`gjc` 실행이 어떻게 `AgentSession`으로 이어지는가”를 이해하는 것입니다.

### 반나절 정도로 주요 runtime을 볼 때

1. 위 1시간 경로
2. `packages/coding-agent/src/tools/index.ts`
3. `packages/coding-agent/src/tools/bash.ts`
4. `packages/coding-agent/src/exec/bash-executor.ts`
5. `packages/coding-agent/src/defaults/gjc-defaults.ts`
6. `packages/coding-agent/src/gjc-runtime/`
7. `packages/coding-agent/src/task/executor.ts`
8. `packages/coding-agent/src/async/job-manager.ts`

목표는 CLI, session, tool, workflow, async/subagent가 연결되는 방식을 이해하는 것입니다.

### 깊게 설계 아이디어를 얻을 때

1. 반나절 경로 전체
2. `packages/agent/src/agent-loop.ts`
3. `packages/ai/src/types.ts`
4. `packages/ai/src/providers/`
5. `packages/coding-agent/src/config/model-registry.ts`
6. `packages/coding-agent/src/modes/`
7. `packages/tui/src/`
8. `.gitnexus/wiki/support-boundary-*.md`

목표는 GJC를 “workflow-first local agent harness”로 만들기 위해 어떤 책임이 분리되어 있는지 파악하는 것입니다.

## 오해하기 쉬운 지점

- `packages/coding-agent/`와 `packages/agent/`는 같은 책임이 아닙니다. 전자는 제품 session/runtime이고, 후자는 저수준 agent loop입니다.
- workflow skill과 role agent는 같은 개념이 아닙니다. skill은 사용자 workflow 표면이고, role agent는 task/subagent 실행용 prompt 정의입니다.
- subagent는 단순 비동기 텍스트 생성이 아닙니다. owner, lifecycle, progress, output cursor, completion delivery를 갖는 managed task입니다.
- `.gjc/` state는 부수 파일이 아니라 workflow runtime의 핵심 계약입니다.
- Claude Code/Codex CLI는 provider가 아닙니다. GJC 옆에서 함께 실행될 수 있는 host agent tool입니다.
- OpenAI/Codex Responses, Anthropic, Google, Cursor 등은 provider/runtime adapter 경계입니다.
- GitNexus wiki는 훌륭한 orientation이지만, user-facing 결론은 직접 소스 확인 후 말해야 합니다.

## 다음에 더 확장하면 좋은 문서

이 walkthrough 다음 단계로는 아래 문서가 유용합니다.

- `CALL_FLOW.md`: 주요 실행 흐름만 sequence diagram으로 분리한 문서
- `PACKAGE_BOUNDARIES.md`: `packages/coding-agent/`와 support package의 의존 경계를 더 엄격히 정리한 문서
- `MULTI_AGENT_LIFECYCLE.md`: subagent/task/async job의 상태 전이를 표와 diagram으로 정리한 문서
- `MODEL_PROVIDER_MAP.md`: provider adapter, credential, discovery, fallback을 provider별로 비교한 문서
- `SOURCE_GRAPH_DIAGRAMS.md`: GitNexus 소스 그래프를 Mermaid 중심으로 재표현한 문서
