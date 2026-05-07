# Session 1-1. Claude Code / Codex 공식 문서를 통해 기능과 활용법 이해하기

## 목표

공식 문서를 기능 목록처럼 훑는 것이 아니라, 실제 작업에 필요한 정보를 뽑아 쓰는 법을 익힌다. 
새 기능을 만났을 때 `공식 출처`, `사용 조건`, `위험 요소`, `검증 방법`을 함께 기록할 수 있어야 한다.

## 준비물

- Claude Code 공식 문서
- Codex 공식 문서
- 로컬 터미널 또는 Desktop App
- 실습용 프로젝트 폴더
- 공식 문서 탐색 노트 템플릿

## 진행 순서

1. 문제 상황
   - "강의에 없는 기능이 새로 생기면 어떻게 따라갈 것인가?"
   - "블로그와 공식 문서가 다르게 말하면 무엇을 믿을 것인가?"
   - 결론: 공식 문서를 먼저 보고, 로컬 도움말과 작은 실행으로 확인한다.

2. 문서의 큰 지도를 보여준다.
   - Claude Code: slash commands, memory, hooks, MCP, settings, skills, Desktop
   - Codex: CLI, App, AGENTS.md, sandbox, approval, config, Windows
   - 기능 이름보다 "어떤 문제를 해결하는 기능인가"를 기준으로 분류한다.

3. 기능 조사 표를 만든다.
   - 기능명
   - 공식 문서 URL
   - 목적
   - 적용 위치: 대화 명령, 설정 파일, 앱 UI, 프로젝트 문서
   - 위험도: 파일 수정, 명령 실행, 외부 도구 연결, 비용 발생
   - 검증 방법: `/help`, `--help`, 설정 파일 확인, 샘플 실행

4. 같은 문제를 두 도구에서 비교한다.
   - 예: Claude Code의 `CLAUDE.md`/memory와 Codex의 `AGENTS.md`/rules
   - 예: Claude Code permissions와 Codex approval/sandbox
   - "같은 기능"이 아니라 "비슷한 문제를 푸는 다른 방식"으로 설명한다.

5. 문서 최신성을 확인하는 루틴
   - 공식 문서 검색
   - 현재 CLI 버전 확인
   - 로컬 도움말 확인
   - 작은 프로젝트에서 최소 실행
   - 결과를 노트에 기록

---

## Claude vs Codex Plugin

공식 문서 기준으로 보면 둘 다 “재사용 가능한 확장 패키지”지만, **설계 중심이 다릅니다.** Codex Plugin은 Codex/ChatGPT 생태계의 **skills + app integrations + MCP 서버 묶음**에 가깝고, Claude Code Plugin은 Claude Code 터미널 워크플로를 확장하는 **commands + agents + skills + hooks + MCP + LSP + monitors** 패키지에 가깝습니다.

| 구분 | Codex Plugin | Claude Code Plugin |
|---|---|---|
| 기본 목적 | Codex에 재사용 워크플로, 앱 통합, MCP 서버를 배포 | Claude Code에 명령어, 에이전트, 스킬, 훅, MCP/LSP 등을 배포 |
| manifest 위치 | `.codex-plugin/plugin.json` | `.claude-plugin/plugin.json` |
| 주요 구성요소 | `skills/`, `.app.json`, `.mcp.json`, `hooks/`, `assets/` | `skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.lsp.json`, `monitors/`, `bin/`, `settings.json` |
| 호출 방식 | 프롬프트에서 자연어로 요청하거나 `@`로 특정 플러그인/스킬 지정 | `/plugin-name:skill-name`, custom slash command, `/plugin` UI |
| 마켓플레이스 | Codex Plugin Directory, repo/personal marketplace, CLI marketplace add | 공식 Anthropic marketplace 자동 제공, GitHub/git/local/URL marketplace 추가 |
| 설치 캐시 | `~/.codex/plugins/cache/...` | `~/.claude/plugins/cache/...` |
| 팀 배포 | repo marketplace: `$REPO_ROOT/.agents/plugins/marketplace.json` 등 | `.claude/settings.json`의 marketplace/plugin 설정으로 user/project/local/managed scope |
| 강한 특징 | ChatGPT 앱/커넥터 통합, Codex app/CLI/IDE across-surface 사용 | 터미널/CLI 중심, slash command, subagent, LSP code intelligence, background monitor |

**Codex Plugin의 특징**

Codex 문서에서 플러그인은 “skills, app integrations, MCP servers를 재사용 워크플로로 묶는 것”으로 정의됩니다. 즉 Codex 쪽 플러그인은 **외부 앱/커넥터와 Codex 워크플로를 함께 패키징**하는 성격이 강합니다. Gmail, Google Drive, Slack 같은 앱 통합 예시가 공식 문서에 나옵니다.  
출처: [OpenAI Codex Plugins](https://developers.openai.com/codex/plugins)

Codex에서 reusable workflow의 작성 단위는 **Skill**이고, 배포 단위가 **Plugin**입니다. Skill은 `SKILL.md` 기반이고, Codex가 설명을 보고 암묵적으로 선택하거나 사용자가 명시적으로 호출할 수 있습니다.  
출처: [OpenAI Agent Skills](https://developers.openai.com/codex/skills)

Codex Plugin을 직접 만들 때는 `.codex-plugin/plugin.json`이 필수이고, `skills`, `mcpServers`, `apps`, `hooks`, `interface` 같은 필드로 구성요소와 UI 메타데이터를 연결합니다. OpenAI 문서는 `$plugin-creator`로 스캐폴딩하는 흐름도 공식으로 안내합니다.  
출처: [OpenAI Build plugins](https://developers.openai.com/codex/plugins/build)

**Claude Code Plugin의 특징**

Claude Code 문서에서 플러그인은 custom commands, agents, hooks, Skills, MCP servers를 확장하는 시스템입니다. 최근 문서 기준으로는 여기에 **LSP 서버, background monitors, bin 실행파일, plugin-level settings**까지 포함됩니다. 그래서 Claude Code 플러그인은 Codex보다 **CLI 개발환경 자체를 바꾸는 확장 포인트가 더 많습니다.**  
출처: [Claude Code Create plugins](https://code.claude.com/docs/en/plugins), [Claude Code Plugins reference](https://code.claude.com/docs/en/plugins-reference)

Claude Code는 custom slash command가 1급 구성요소입니다. 예를 들어 `commands/hello.md`를 만들면 `/hello` 같은 명령으로 쓸 수 있고, 플러그인 스킬은 `/plugin-name:skill-name`처럼 namespace가 붙습니다. Codex도 skill 호출이 있지만, Claude Code 쪽이 slash-command UX를 더 전면에 둡니다.  
출처: [Claude Code Plugins](https://docs.claude.com/en/docs/claude-code/plugins)

또 Claude Code에는 공식 Anthropic marketplace가 자동으로 제공되고, `/plugin`의 Discover/Installed/Marketplaces/Errors 탭에서 탐색/설치/관리합니다. 설치 scope도 user, project, local, managed로 나뉩니다.  
출처: [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)

**가장 큰 실무적 차이**

Codex Plugin은 “Codex가 어떤 작업을 더 잘 수행하게 할 것인가”와 “어떤 앱/MCP와 연결할 것인가”에 초점이 있습니다. 특히 Codex app, CLI, IDE extension, ChatGPT connector 흐름과 맞물립니다.

Claude Code Plugin은 “Claude Code라는 터미널 에이전트의 동작면을 어떻게 확장할 것인가”에 초점이 더 강합니다. commands, agents, hooks, LSP, monitors, `bin/`, settings까지 포함하므로 개발자 로컬 워크플로를 세밀하게 패키징하기 좋습니다.

짧게 말하면: **Codex Plugin은 앱/스킬/MCP 중심의 Codex 생태계 패키지**, **Claude Code Plugin은 CLI 에이전트 런타임을 확장하는 더 넓은 구성요소 패키지**입니다.

