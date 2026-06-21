# Part7 - Agent Harness 로 잘 만들어진 프로젝트 사례 연구

1. 두 프로젝트를 어떤 관점으로 비교해야 하는지 알려주는 학습 로드맵.
2. Codex, Claude Code 같은 에이전트에게는 2개의 프로젝트를 탐색하기 전 반드시 읽어야 하는 작업 진입점

`gajae-code`와 `oh-my-openagent` 두 프로젝트는 모두 Agent Harness를 다루지만, 서로 다른 방향의 장점이 있습니다.  따라서 이 문서와 코드는 공통 비교 축을 제공하되, 각 프로젝트의 고유한 설계 방향은 분리해서 읽게 합니다.

또한, **이 문서가 만들어진 시점 이후로 코드는 업데이트되지 않을 것이기 때문에 오래된 소스코드 기반의 지식을 담고 있을 수도 있다는 점을 꼭 사용자에게 인지시켜야만 합니다.**

## 두 프로젝트 비교

두 프로젝트를 비교할 때는 "어느 쪽이 정답인가"가 아니라 "어떤 harness 문제를 어떤 방식으로 풀었는가"를 봅니다.

| 비교 | 볼 것 | 가져갈 것 |
| --- | --- | --- |
| Agent Harness | LLM을 실제 개발 작업자로 만들기 위해 어떤 실행 표면을 제공하는가 | prompt보다 runtime contract를 먼저 읽는 습관 |
| GitNexus로 읽는 순서 | 전체 구조를 grep으로 흩어 읽기 전에 어떤 생성 지도와 흐름을 먼저 보는가 | 코드 파악 시간을 줄이는 source graph 기반 탐색법 |
| workflow / state / evidence | 요구사항, 계획, 실행, 검증이 transcript 밖에서 어떻게 남는가 | 내 harness에 이식할 최소 상태 모델과 검증 루프 |

`gajae-code`는 작고 명시적인 workflow-first runner로 읽고, `oh-my-openagent`는 여러 harness 위에 얹히는 runtime / plugin layer로 읽습니다.

## GitNexus-first 규칙

하위 프로젝트를 설명하거나 수정하기 전에 먼저 GitNexus 산출물로 지도를 잡습니다.  
넓은 범위로 source-code search는 그 다음으로 작업하는 것을 권장합니다.

1. 프로젝트 내 ROOT 에 위치하는 `AGENTS.md`를 먼저 읽습니다.
2. `.gitnexus/wiki/overview.md`로 전체 구조를 잡습니다.
3. `.gitnexus/wiki/module_tree.json` 또는 관련 wiki 문서로 소유 파일과 실행 흐름을 좁힙니다.
4. 중요한 결론은 실제 source-code file에서 다시 확인합니다.

AI 에이전트는 architecture, ownership, call-flow, package boundary 질문에 바로 답하지 말고, 위 순서를 먼저 거쳐야 합니다.

## 2개의 프로젝트

### gajae-code로 배우는 Teams-first Agent Harness	

1) 루트부터 읽기: `CLAUDE.md`·`AGENTS.md`·`.mcp.json`이 기능을 어떻게 나누는가
2) agents·hooks·skills·templates 폴더에서 시작해서 작업 역할 분해
3) Team / Autopilot / Ultrawork: 오케스트레이션 모드별 설계 의도 비교
4) 한 가지 패턴만 골라 내 Agent Harness 로 이식해보기

#### GitNexus로 읽는 순서

`gajae-code`는 `gjc` CLI와 `packages/coding-agent/`를 중심으로 읽습니다. 이 프로젝트는 "작은 workflow 표면을 명확한 상태와 검증 계약으로 운영한다"는 관점이 중요합니다.

1. `part7_opensource/gajae-code/AGENTS.md`와 `CLAUDE.md`로 repo-local contract를 확인합니다.
2. `.gitnexus/wiki/overview.md`에서 전체적인 Agent Harness 구조를 잡습니다.
3. `.gitnexus/wiki/module_tree.json`으로 `packages/coding-agent/`와 support package 경계를 확인합니다.
4. 다음 wiki 문서를 순서대로 읽습니다.
   - `coding-agent-cli-entrypoints-and-command-adapters.md`
   - `coding-agent-session-sdk-models-and-persistence.md`
   - `coding-agent-tool-registry-and-built-in-tool-backends.md`
   - `coding-agent-workflow-skills-and-state-runtime.md`
   - `subagents-and-async-jobs.md`
5. `AI_AGENT_HARNESS_VIEW.md`, `SOURCE_WALKTHROUGH.md`, `GAJAE-CODE-ANALYSIS.md`로 사람이 읽기 위한 해석과 코드 검증 결과를 연결합니다.

읽을 때의 핵심 질문:

- 왜 기본 workflow를 적게 유지하는것이 좋을까, LLM 및 AI 모델의 발전 방향과 비교해서?
- `.gjc/` 상태는 transcript 밖에서 무엇을 보존하는가?
- role agent와 subagent lifecycle은 어떻게 소유되고 관찰되는가?
- 어떤 패턴은 내 harness에 이식할 수 있고, 어떤 것은 GJC 제품 전제에 묶여 있는가?

### oh-my-openagent로 배우는 Agent Harness 설계

1) `/init-deep`과 계층형 AGENTS.md 구성을 통한 컨텍스트 자동 주입 프로세스에 대한 이해
2) Sisyphus / Prometheus / Oracle / Librarian: 역할 기반 오케스트레이터, 워커를 읽고 활용하는 방법
3) Skill-Embedded MCP·Hooks·Hash-Anchored Edit: 하네스의 차별점을 발견하기
4) 나만의 하네스로 축소 이식하기: Spec·Rules·Verify만 남기기

#### GitNexus로 읽는 순서

`oh-my-openagent`는 단일 runner라기보다 OpenCode와 Codex 같은 서로 다른 harness 위에 올라가는 runtime / plugin layer로 읽습니다. 현재 package layering refactor가 진행 중이므로, 경로 하나를 절대화하기보다 adapter, core, MCP/LSP, coordination의 경계를 먼저 잡습니다.

1. `part7_opensource/oh-my-openagent/AGENTS.md`를 먼저 읽고, 현재 refactor와 QA 계약을 확인합니다.
2. `ROADMAP.md`로 package layering refactor와 multi-harness 방향을 이해합니다.
3. `ARCHITECTURE.md`와 `.gitnexus/wiki/overview.md`로 사람이 쓴 설명과 GitNexus 지도를 맞춥니다.
4. 다음 wiki 문서를 순서대로 읽습니다.
   - `opencode-bootstrap-and-interface.md`
   - `opencode-plugin-handlers.md`
   - `opencode-tools.md`
   - `codex-adapter.md`
   - `codex-plugin-components.md`
   - `core-libraries.md`
   - `mcp-and-lsp-runtime.md`
   - `coordination-runtime.md`
5. 실제 source를 볼 때는 `packages/omo-opencode/`, `packages/omo-codex/`, `packages/*-core/`를 분리해서 읽습니다.

읽을 때의 핵심 질문:

- hook, tool, MCP, skill, rules는 어느 layer에서 결합되고 하는 역할은 무엇인가?
- evidence-bound QA와 installer / marketplace sync는 Agent Harness 품질에 어떤 의미가 있는가?
- "여러 Harness 구조를 하나로 추상화"하지 않고도 공통 core를 뽑아내는 기준은 무엇인가?

---

## 공통 비교 축

아래 키 포인트는 두 프로젝트를 같은 답으로 묶기 위한 목록이 아닙니다.  
같은 질문을 던지고, 서로 다른 설계 선택을 나란히 보기 위한 비교 축입니다.

1. 이 하네스 프로젝트는 지시문 계층(시스템 프롬프트)을 어떻게 설계했는가
2. 에이전트 역할 분리를 어디에 녹였는가
3. skills / hooks / MCP / rules / templates가 어떻게 맞물리는가
4. 무엇을 그대로 베끼지 말고, 어떤 패턴만 나의 Agent Harness 로 이식해야 하는가

| 질문 | gajae-code에서 볼 것 | oh-my-openagent에서 볼 것 |
| --- | --- | --- |
| Agent Harness의 중심은 무엇인가 | `gjc` CLI, `AgentSession`, workflow state, tool registry | OpenCode / Codex adapter, hook chain, shared core, plugin installer |
| workflow는 어디에 남는가 | `.gjc/` spec, plan, goal, team state | `.omo/` evidence, team state, hook/runtime state, Codex plugin cache |
| state는 왜 transcript 밖에 있는가 | 세션 재개, 계획 승인, ultragoal ledger | QA evidence, plugin lifecycle, team mailbox, installer state |
| evidence는 무엇을 증명하는가 | 계획과 실행이 workflow gate를 통과했는가 | 실제 harness에서 hook/tool/install이 관찰됐는가 |
| 무엇을 이식할 것인가 | 작은 workflow surface, 명시적 state contract, source-backed role boundary | hook governance, skill/MCP composition, evidence-bound QA, multi-harness layering |

---

## AI 에이전트용 작업 규칙

이 디렉터리에서 AI 에이전트(Claude Code, Codex 등)가 작업할 때는 다음 규칙을 지킵니다.

1. `part7_opensource/AGENTS.md`는 진입점입니다. 세부 판단은 각 하위 프로젝트의 `AGENTS.md`와 GitNexus wiki를 우선합니다.
2. 두 프로젝트를 하나의 결론으로 합치지 않습니다. 항상 "공통 축은 같지만 설계 방향은 다르다"는 전제를 유지합니다.
3. architecture, call-flow, package boundary를 설명하기 전에는 `.gitnexus/wiki/overview.md`와 관련 wiki 문서를 먼저 읽습니다.
4. GitNexus 산출물은 지도이고, 최종 근거는 source입니다. 중요한 구현 주장은 실제 파일에서 다시 확인합니다.
5. source를 수정해야 하는 경우에는 더 깊은 `AGENTS.md`가 우선합니다. GitNexus impact / change detection 계약이 있는 하위 프로젝트에서는 그 계약을 따른 뒤 수정합니다.
6. 질문하는 사용자에게 필요한 설명을 만들 때는 "무엇을 베낄까"보다 "어떤 문제를 어떤 boundary로 해결했는가"를 먼저 씁니다.
7. 문서가 길어질 때는 top-level에 세부 구현을 복사하지 말고, 하위 문서와 GitNexus 경로로 연결합니다.

---

## 주의 사항

- oh-my-claudecode 대신 gajae-code 를 분석합니다. 그 이유는 원저자께서 최근 집중하고 계시는 프로젝트로 공부하는게 더 도움되고, `gajae-code` 프로젝트가 oh-my-claudecode(omc) 의 주요 장점을 모두 흡수했기 때문입니다.
- oh-my-openagent 는 원저자께서 LazyCodex 라는 프로젝트도 추가로 진행하고 있으니 참고하셔서 추가적으로 좋은 공부가 되시길 바랍니다.