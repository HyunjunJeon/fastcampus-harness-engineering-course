# oh-my-openagent 코드 파악 문서

> 목적: 이 문서는 `part7_opensource/oh-my-openagent/`를 처음 읽는 사람이 프로젝트 구조, 주요 실행 흐름, 수정 위치, 검증 기준을 빠르게 잡기 위한 한국어 안내서다.
>
> 범위: 코드 구조와 프로젝트 파악에 필요한 내용만 다룬다. 제품 소개, 철학, 발표용 해석은 [`ARCHITECTURE.md`](./ARCHITECTURE.md)로 분리한다.
>
> 기준일: 2026-06-18
> 기준 버전: `package.json`의 `4.11.0`

---

## 먼저 읽을 것

이 저장소는 일반적인 라이브러리보다 agent harness에 가깝다. 핵심은 모델 호출이 아니라, OpenCode와 Codex라는 서로 다른 실행 표면 위에 agent, tool, hook, skill, installer, MCP/LSP runtime을 얹는 구조다.

처음에는 아래 순서로 읽는 편이 빠르다.

| 순서 | 파일 | 확인할 것 |
| --- | --- | --- |
| 1 | [`AGENTS.md`](./AGENTS.md) | 현재 리팩터링 상태, QA 규칙, OpenCode/Codex 구분 |
| 2 | [`package.json`](./package.json) | 워크스페이스, 빌드 스크립트, 공개 bin alias |
| 3 | [`.gitnexus/wiki/overview.md`](./.gitnexus/wiki/overview.md) | GitNexus가 만든 source-only 전체 지도 |
| 4 | [`packages/omo-opencode/src/testing/create-plugin-module.ts`](./packages/omo-opencode/src/testing/create-plugin-module.ts) | OpenCode edition의 composition root |
| 5 | [`packages/omo-codex/AGENTS.md`](./packages/omo-codex/AGENTS.md) | Codex Light edition 설치와 hook runtime |

`ARCHITECTURE.md`는 아이디어를 얻기 위한 문서다. 실제 수정 위치를 찾을 때는 이 문서와 GitNexus wiki, 각 패키지의 `AGENTS.md`를 우선한다.

## 한 문장 요약

`oh-my-openagent`는 OpenCode용 Ultimate edition과 Codex용 Light edition을 같은 monorepo에서 관리하며, 공통 정책과 runtime primitive를 여러 package로 나눈 multi-harness agent runtime이다.

## 이름과 표면 정리

이 저장소는 이름이 여러 개라 처음에 헷갈리기 쉽다.

| 이름 | 의미 |
| --- | --- |
| `oh-my-opencode` | root `package.json`의 npm package name |
| `oh-my-openagent` | transition name이자 bin alias |
| `omo` | CLI alias. Codex marketplace에서는 `sisyphuslabs/omo` plugin name으로도 쓰인다 |
| `lazycodex`, `lazycodex-ai` | Codex Light edition 설치 경로와 npm/bin alias |
| Ultimate edition | OpenCode plugin 쪽. 주로 `packages/omo-opencode/` |
| Light edition | Codex CLI plugin 쪽. 주로 `packages/omo-codex/` |

핵심 구분은 세 가지다.

| 구분 | 예시 | 책임 |
| --- | --- | --- |
| Harness | OpenCode, Codex CLI | agent가 실행되는 host surface |
| Adapter | `omo-opencode`, `omo-codex` | host의 hook, config, install 방식에 맞춰 연결 |
| Core package | `model-core`, `rules-engine`, `skills-loader-core` 등 | 여러 adapter가 공유하는 정책과 유틸리티 |

## 저장소 구조

현재 root에는 과거 `src/`가 없다. OpenCode-facing 소스는 `packages/omo-opencode/src/`로 이동했고, Codex-facing 소스는 `packages/omo-codex/`에 있다.

```text
oh-my-openagent/
├── packages/
│   ├── omo-opencode/          # OpenCode plugin adapter
│   ├── omo-codex/             # Codex Light edition adapter and installer
│   ├── shared-skills/         # OpenCode/Codex가 공유하는 SKILL.md 묶음
│   ├── model-core/            # model/provider capability와 fallback 정책
│   ├── rules-engine/          # AGENTS.md/rules 주입 계층
│   ├── skills-loader-core/    # skill discovery/loading 공통 로직
│   ├── prompts-core/          # prompt 조립 공통 로직
│   ├── delegate-core/         # 위임/하위 작업 공통 로직
│   ├── team-core/             # multi-agent coordination primitive
│   ├── boulder-state/         # 작업 상태 저장
│   ├── lsp-core/              # LSP 공통 계층
│   ├── lsp-tools-mcp/         # LSP를 MCP tool로 노출
│   ├── lsp-daemon/            # 장기 실행 LSP daemon
│   ├── git-bash-mcp/          # Windows Git Bash 보조 MCP
│   └── web/                   # 사이트. 별도 lockfile과 규칙을 가짐
├── docs/                      # 사용자 문서
├── script/                    # 빌드/배포 자동화
├── assets/                    # schema 산출물
├── dist/                      # build output
└── .gitnexus/wiki/            # source-only 분석 산출물
```

package 이름은 많지만 읽는 기준은 단순하다.

| 읽고 싶은 것 | 먼저 볼 위치 |
| --- | --- |
| OpenCode plugin이 어떻게 뜨는지 | `packages/omo-opencode/src/testing/create-plugin-module.ts` |
| OpenCode hook surface | `packages/omo-opencode/src/plugin-interface.ts`, `packages/omo-opencode/src/create-hooks.ts` |
| OpenCode tool surface | `packages/omo-opencode/src/create-tools.ts`, `packages/omo-opencode/src/plugin/tool-registry.ts` |
| Codex 설치와 config 변경 | `packages/omo-codex/src/install/`, `packages/omo-codex/scripts/` |
| Codex plugin component | `packages/omo-codex/plugin/components/` |
| 공유 skill | `packages/shared-skills/skills/` |
| LSP/MCP runtime | `packages/lsp-core/`, `packages/lsp-tools-mcp/`, `packages/mcp-stdio-core/` |
| Team Mode | `packages/team-core/`, `packages/omo-opencode/src/features/team-mode/` |

## 지시문 계층

이 프로젝트에서 시스템 프롬프트는 한 파일에 고정된 장문이 아니다. 여러 층의 지시문과 runtime context가 합쳐져 최종 agent prompt가 된다.

| 계층 | 위치 | 역할 |
| --- | --- | --- |
| 프로젝트 규칙 | `AGENTS.md`, 하위 `AGENTS.md` | 작업 규칙, QA, 패키지별 책임 경계 |
| agent 정의 | `packages/omo-opencode/src/agents/` | Sisyphus, Hephaestus, Oracle, Librarian 같은 역할별 prompt와 tool 제한 |
| dynamic prompt builder | `dynamic-agent-*.ts` | agent metadata, category, skill, tool 정보를 prompt section으로 조립 |
| shared prompt package | `packages/prompts-core/` | Prometheus 등 일부 agent가 읽는 prompt 원본 |
| skill | `packages/shared-skills/skills/`, builtin skill 경로 | 작업별 절차, reference, embedded MCP, script |
| hook-injected context | `packages/omo-opencode/src/hooks/`, Codex component hooks | 메시지/도구 실행/세션 이벤트 시점에 규칙과 상태를 추가 |

`/init-deep`을 이해하려면 이 계층을 먼저 봐야 한다. 이 저장소는 계층형 `AGENTS.md`를 만들어 “현재 디렉터리에서 어떤 규칙이 우선하는가”를 파일 시스템 구조로 표현한다. 그래서 agent가 모든 지시문을 한 번에 외우는 방식이 아니라, 작업 위치에 맞는 문맥을 주입받는 방식에 가깝다.

읽을 파일:

- `packages/omo-opencode/src/features/builtin-skills/skills/init-deep.ts`
- `packages/agents-md-core/`
- `docs/templates/AGENTS.md.example`
- 각 패키지의 `AGENTS.md`

## 역할 agent 읽기

역할 분리는 [`packages/omo-opencode/src/agents/`](./packages/omo-opencode/src/agents/)에 녹아 있다. `builtin-agents.ts`는 agent source를 모으고, `createBuiltinAgents()`가 disabled agent, model override, category, discovered skill, browser provider, team mode 여부를 반영해 최종 `AgentConfig`를 만든다.

처음에는 네 역할만 잡아도 구조가 보인다.

| Agent | 위치 | 읽을 때 볼 것 |
| --- | --- | --- |
| Sisyphus | `agents/sisyphus*`, `sisyphus-dynamic-prompt-*` | primary orchestrator. available agent/skill/category/tool 정보를 prompt에 반영 |
| Prometheus | `agents/prometheus/`, `prompts-core` | 계획 중심 agent. prompt 원본을 `prompts-core`에서 읽음 |
| Oracle | `agents/oracle.ts` | read-only architecture advisor. write/edit/task 계열 tool 제한 |
| Librarian | `agents/librarian.ts` | 외부 문서와 open-source code 검색. evidence와 permalink 중심 |

역할 agent를 읽을 때는 persona 문장보다 metadata와 제한을 먼저 본다.

| 확인 항목 | 이유 |
| --- | --- |
| `mode` | primary agent인지 subagent인지 결정 |
| `AgentPromptMetadata` | Sisyphus의 delegation table과 trigger 설명에 들어감 |
| tool restrictions | 역할 agent가 실제로 할 수 있는 행동의 경계 |
| model resolution | UI 선택 모델, override, fallback chain의 우선순위 |
| skill resolution | agent별로 어떤 skill이 노출되는지 |

## Skills, hooks, MCP, rules, templates의 연결

이 프로젝트의 차별점은 각 요소를 따로 두지 않는 데 있다. skill은 절차를 제공하고, hook은 시점을 잡고, MCP는 외부 실행 표면을 열고, rules/templates는 반복 가능한 지시문과 파일 형태를 만든다.

| 요소 | 대표 위치 | 맞물리는 방식 |
| --- | --- | --- |
| skills | `packages/shared-skills/skills/`, `features/builtin-skills/` | agent가 필요한 절차와 reference를 지연 로딩 |
| hooks | `packages/omo-opencode/src/hooks/`, `plugin/hooks/` | message, tool, session 이벤트에서 규칙과 상태를 주입 |
| MCP | `lsp-tools-mcp`, `git-bash-mcp`, `mcp-stdio-core` | LSP, Git Bash, 외부 tool을 host tool surface로 노출 |
| rules | `rules-engine`, `agents-md-core`, `hooks/rules-injector/` | AGENTS.md와 rule file을 현재 작업 문맥에 맞춰 반영 |
| templates | `docs/templates/AGENTS.md.example`, command templates, reminder templates | 사용자/agent가 반복해서 쓰는 규칙과 산출물의 기본형 |

코드 파악 순서는 다음이 좋다.

1. `createPluginModule()`에서 `createTools()`와 `createHooks()`가 같은 config와 manager를 공유하는지 확인한다.
2. `createToolRegistry()`에서 MCP 기반 도구와 조건부 도구가 언제 노출되는지 본다.
3. `createHooks()`에서 core/continuation/skill hook이 어떻게 합쳐지는지 본다.
4. `agents/builtin-agents.ts`에서 discovered skill과 available tool/category가 agent prompt에 어떻게 들어가는지 본다.
5. Codex 쪽은 `packages/omo-codex/plugin/components/*/hooks/hooks.json`과 component script를 함께 본다.

## 그대로 베끼지 말고 가져갈 패턴

이 저장소를 나만의 agent harness로 옮길 때는 전체 기능을 복제하지 않는 편이 낫다. 의존성이 많고, OpenCode/Codex 양쪽 runtime 사정에 맞춘 코드가 섞여 있기 때문이다.

가져갈 만한 것은 구조 패턴이다.

| 가져갈 패턴 | 축소 구현 |
| --- | --- |
| 계층형 규칙 주입 | root `AGENTS.md` + 하위 `AGENTS.md` + 현재 경로 기준 merge |
| 역할 agent 분리 | planner, executor, reviewer 정도의 작은 registry |
| skill 단위 절차화 | `SKILL.md` + 필요한 script/reference만 포함 |
| hook 기반 통제 | `before_tool`, `after_tool`, `on_stop` 세 지점부터 시작 |
| evidence-bound QA | 검증 명령, 로그, 스크린샷을 작업별 폴더에 저장 |
| tool registry | 항상 켜는 tool과 config-gated tool을 마지막 단계에서 합성 |

처음부터 그대로 가져오지 않을 것:

- 전체 Team Mode
- 모든 agent persona
- multi-provider fallback chain
- Codex/OpenCode 동시 배포 파이프라인
- hook별 recovery edge case 전체
- 긴 prompt 전문

축소 이식의 기준은 `Spec -> Rules -> Verify`다. 먼저 어떤 작업을 허용할지 spec을 정하고, 그 작업에 적용할 규칙을 파일로 두며, 마지막에 실제 표면에서 검증 증거를 남기는 구조만 가져오면 된다.

## OpenCode edition 읽기

OpenCode edition은 `packages/omo-opencode/`가 중심이다. OpenCode가 plugin module을 로드하면 `createPluginModule()`이 설정, manager, tool, hook, interface를 한 번에 조립한다.

실행 흐름은 다음 순서로 잡으면 된다.

1. `packages/omo-opencode/src/index.ts`
   - 공개 entrypoint다.
   - 실제 조립은 `testing/create-plugin-module.ts`로 넘긴다.
2. `packages/omo-opencode/src/testing/create-plugin-module.ts`
   - duplicate plugin 검사, legacy workspace migration, config load, i18n, OpenClaw, Team Mode, tmux check를 준비한다.
   - 이후 `createManagers()`, `createTools()`, `createHooks()`, `createPluginInterface()`를 순서대로 부른다.
3. `packages/omo-opencode/src/create-managers.ts`
   - background task, skill MCP, tmux, monitor, model fallback 같은 장기 runtime 객체를 만든다.
4. `packages/omo-opencode/src/create-tools.ts`
   - skill context와 available category를 만든 뒤 `createToolRegistry()`에 넘긴다.
5. `packages/omo-opencode/src/create-hooks.ts`
   - core hook, continuation hook, skill hook을 합친다.
6. `packages/omo-opencode/src/plugin-interface.ts`
   - OpenCode가 호출하는 hook 이름과 내부 handler를 연결한다.

이 흐름에서 중요한 점은 `createPluginModule()`이 기능을 직접 많이 구현하지 않는다는 점이다. composition root로서 부팅 순서와 의존성 공유를 고정한다.

## Tool surface

OpenCode에 노출되는 도구는 `createToolRegistry()`에서 합성된다.

```text
createTools()
  -> createSkillContext()
  -> createAvailableCategories()
  -> createToolRegistry()
      -> createCoreTools()
      -> interactive_bash 조건부 추가
      -> team tools 조건부 추가
      -> monitor/task/hashline tools 조건부 추가
      -> filterDisabledTools()
      -> trimToolsToCap()
```

핵심 파일은 [`packages/omo-opencode/src/plugin/tool-registry.ts`](./packages/omo-opencode/src/plugin/tool-registry.ts)다. 새 도구를 읽거나 추가할 때는 먼저 그 도구가 어느 gate에 속하는지 봐야 한다.

| 도구 성격 | 관련 파일 |
| --- | --- |
| 항상 켜지는 기본 도구 | `tool-registry-core-tools.ts` |
| 설정으로 켜지는 도구 | `tool-registry-gated-tools.ts` |
| Team Mode 전용 도구 | `tool-registry-team-tools.ts` |
| disabled/max 정책 | `shared/disabled-tools`, `tool-registry-trimming.ts` |

## Hook surface

OpenCode 쪽 hook은 세 묶음으로 조립된다.

| 묶음 | 파일 | 역할 |
| --- | --- | --- |
| core | `plugin/hooks/create-core-hooks.ts` | config, tool 전후 처리, message transform, event 대응 |
| continuation | `plugin/hooks/create-continuation-hooks.ts` | 작업 중단 방지, stop/idle 이후 이어가기 |
| skill | `plugin/hooks/create-skill-hooks.ts` | skill reminder, slash command, skill context 반영 |

`create-hooks.ts`는 이 세 묶음을 합친 뒤 `disposeHooks()`를 함께 돌려준다. hook을 추가할 때는 “어느 이벤트에 붙을 것인가”보다 먼저 “core, continuation, skill 중 어느 책임인가”를 정해야 한다.

## Codex Light edition 읽기

Codex Light edition은 `packages/omo-codex/`에 있다. OpenCode edition처럼 host runtime 안에서 모든 것을 조립하기보다, 설치된 Codex plugin cache를 기준으로 동작한다.

먼저 볼 파일은 [`packages/omo-codex/AGENTS.md`](./packages/omo-codex/AGENTS.md)다. 이 파일이 설치 위치, component 구성, QA 규칙을 가장 정확하게 정리한다.

주요 경계는 아래와 같다.

| 위치 | 역할 |
| --- | --- |
| `packages/omo-codex/src/install/` | Codex cache install, config mutation, agent link, cleanup |
| `packages/omo-codex/scripts/` | published path를 안정적으로 유지하기 위한 Node entrypoint와 테스트 |
| `packages/omo-codex/plugin/` | Codex plugin bundle. marketplace에 배치되는 실제 plugin namespace |
| `packages/omo-codex/plugin/components/` | Codex hook event에 반응하는 component들 |
| `packages/omo-codex/marketplace.json` | `sisyphuslabs/omo` marketplace manifest |

설치기는 `CODEX_HOME` 아래에 plugin cache, marketplace snapshot, agent TOML, config entry, component CLI를 배치한다. 실제 사용자 홈을 오염시키지 않아야 하므로 Codex 관련 변경은 항상 격리된 `CODEX_HOME`에서 검증해야 한다.

## Shared skill과 component

이 저장소에서 skill은 단순 프롬프트 조각이 아니다. `SKILL.md`와 필요한 script, asset, MCP 설정이 함께 움직일 수 있는 작업 단위다.

읽을 위치는 두 군데다.

| 위치 | 용도 |
| --- | --- |
| `packages/shared-skills/skills/` | OpenCode와 Codex가 공유하는 skill 원본 |
| `packages/omo-codex/plugin/components/*/` | Codex hook component와 component-local skill |

OpenCode 쪽은 runtime에서 skill source를 병합해 agent prompt와 tool context에 넣는다. Codex 쪽은 plugin build와 install 흐름에서 aggregate skill directory와 component hook wiring을 맞춘다.

## Multi-agent와 background execution

OpenCode edition의 multi-agent 흐름은 두 축으로 나뉜다.

| 축 | 의미 | 읽을 위치 |
| --- | --- | --- |
| background task | 부모 세션에서 하위 OpenCode 세션을 띄우고 결과를 회수 | `packages/omo-opencode/src/features/background-agent/`, `packages/delegate-core/` |
| Team Mode | mailbox, tasklist, base dir, member config를 가진 coordination runtime | `packages/omo-opencode/src/features/team-mode/`, `packages/team-core/` |

Team Mode는 기본값이 꺼져 있다. 관련 tool도 `team_mode.enabled`일 때만 registry에 들어온다. 그래서 team 관련 버그를 볼 때는 config gate와 tool registry를 같이 확인해야 한다.

## MCP와 LSP runtime

MCP/LSP 계층은 adapter에서 직접 구현하지 않고 별도 package로 분리한다.

| package | 책임 |
| --- | --- |
| `mcp-stdio-core` | stdio 기반 MCP server 공통 기반 |
| `mcp-client-core` | MCP client 공통 로직 |
| `lsp-core` | language server 기능 공통화 |
| `lsp-tools-mcp` | LSP 기능을 MCP tool로 노출 |
| `lsp-daemon` | 장기 실행 LSP 상태 재사용 |
| `git-bash-mcp` | Windows Git Bash 환경 지원 |

OpenCode 쪽 `lsp_*` 도구는 built-in MCP로 노출된다. Codex 쪽은 component와 설치 경로가 함께 맞아야 하므로 `test:codex`와 격리 설치 검증을 같이 봐야 한다.

## 수정 위치 고르기

| 하고 싶은 일 | 먼저 볼 곳 | 같이 확인할 것 |
| --- | --- | --- |
| OpenCode 부팅 순서 변경 | `create-plugin-module.ts` | root `AGENTS.md`의 OpenCode QA |
| OpenCode tool 추가 | `tool-registry.ts`와 관련 `tool-registry-*.ts` | disabled/max policy, schema normalization |
| OpenCode hook 추가 | `create-hooks.ts`, `plugin/hooks/` | hook enable/disable config, dispose |
| agent prompt 변경 | `packages/omo-opencode/src/agents/`, `prompts-core` | dynamic prompt metadata, available skills |
| shared skill 변경 | `packages/shared-skills/skills/` | OpenCode skill loading, Codex aggregate skill build |
| Codex installer 변경 | `packages/omo-codex/src/install/` | isolated `CODEX_HOME`, config.toml before/after |
| Codex component 변경 | `packages/omo-codex/plugin/components/<name>/` | component hook JSON, component tests |
| LSP 기능 변경 | `lsp-core`, `lsp-tools-mcp`, `lsp-daemon` | MCP schema, daemon lifecycle |
| Team Mode 변경 | `features/team-mode`, `team-core` | config gate, mailbox/task state, tool registry |

## 검증 기준

문서만 바꿀 때는 Markdown 구조와 링크를 확인하면 된다. 코드가 OpenCode나 Codex surface에 닿으면 단순 typecheck로 끝내면 안 된다.

| 변경 범위 | 최소 검증 |
| --- | --- |
| 문서만 변경 | Markdown heading/link sanity check |
| 일반 TypeScript package | 관련 package test, `bun run typecheck` 또는 더 좁은 tsconfig |
| `packages/omo-opencode/` | root `AGENTS.md`의 OpenCode QA. evidence를 `.omo/evidence/`에 기록 |
| `packages/omo-codex/` | 격리된 `CODEX_HOME` 설치, `bun run test:codex`, real `~/.codex` 미변경 증거 |
| schema/config 변경 | `bun run build:schema`와 관련 config test |
| shared skill 변경 | OpenCode/Codex 양쪽 skill build 또는 loading 확인 |

## 이 문서가 남기지 않는 것

아래 내용은 일부러 줄였다.

- 긴 Mermaid 갤러리
- 검증되지 않은 수치와 성능 향상 주장
- 같은 말을 다른 heading으로 반복하는 설명
- “핵심”, “본질”, “시사점” 같은 결론형 문구의 반복
- 발표용 수사

대신 실제 파일 경로, 책임 경계, 실행 순서, 검증 기준을 남겼다. 이 문서는 읽는 사람이 다음 파일을 바로 열 수 있게 하는 색인에 가깝다.

## 참고 지도

- GitNexus overview: [`.gitnexus/wiki/overview.md`](./.gitnexus/wiki/overview.md)
- OpenCode adapter wiki: [`.gitnexus/wiki/opencode-adapter.md`](./.gitnexus/wiki/opencode-adapter.md)
- Codex adapter wiki: [`.gitnexus/wiki/codex-adapter.md`](./.gitnexus/wiki/codex-adapter.md)
- 설계 아이디어 문서: [`ARCHITECTURE.md`](./ARCHITECTURE.md)
- 사용자 README: [`README.ko.md`](./README.ko.md)
