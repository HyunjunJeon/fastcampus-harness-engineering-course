# 사전 설치 — Superpowers

## 1. 왜 반드시 설치하는가

이 강의에서 진행할 4단계 프로세스는 AI Agent에게 바로 코드를 맡기는 방식이 아니다.

```text
1. PRD / MVP Scope
→ 2. Roadmap / SPEC / TASK
→ 3. Claude Code UI Scaffold
→ 4. Codex 병렬 구현 / 검증
```

이 흐름을 안정적으로 반복하려면 agent가 매번 즉흥적으로 행동하지 않고, **검증된 작업 절차를 skill로 불러와야 한다.**

수강생은 실습 전에 Superpowers를 설치한다.

Superpowers는 coding agent가 바로 코드부터 쓰지 않고, brainstorming, planning, TDD, subagent-driven development, code review, verification 같은 절차를 skill 기반으로 사용하게 해주는 agentic skills framework다.

핵심 이유:

| 이유 | 설명 |
|---|---|
| 바로 구현 방지 | agent가 아이디어를 들으면 먼저 의도와 설계를 정리하게 만든다 |
| 계획 기반 구현 | approved design 이후 implementation plan으로 쪼개게 한다 |
| TDD 강조 | RED-GREEN-REFACTOR 흐름을 강제한다 |
| SubAgent 활용 | task별 fresh subagent와 review 흐름을 사용하게 한다 |
| 검증 우선 | claims가 아니라 evidence와 verification 기준으로 완료 판단한다 |

이 강의에서 말하는 Harness, Skills, SubAgents, Hooks, Evidence의 사고방식과 매우 잘 맞는다.

---

## 2. 설치 원칙

Superpowers는 사용하는 agent 환경마다 따로 설치해야 한다.

```text
Claude Code에서 쓰려면 Claude Code에 설치
Codex에서 쓰려면 Codex에 설치
```

여러 도구를 함께 쓰는 학생은 각 도구에 따로 설치한다.

---

## 3. Claude Code 설치

Claude Code에서는 공식 플러그인 마켓플레이스 설치를 우선 사용한다.

```bash
/plugin install superpowers@claude-plugins-official
```

대안으로 Superpowers marketplace를 등록한 뒤 설치할 수 있다.

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

수업에서는 Claude Code를 화면 골격, 컴포넌트 경계, SPEC/TASK 읽기, scaffold 작업에 사용한다.

---

## 4. Codex 설치

### Codex App

Codex App에서는 Plugins 사이드바에서 설치한다.

```text
Plugins
→ Coding 섹션
→ Superpowers
→ Install
```

### Codex CLI

Codex CLI에서는 plugin search interface를 연다.

```bash
/plugins
```

검색어:

```text
superpowers
```

`Install Plugin`을 선택한다.

수업에서는 Codex를 작은 TASK 병렬 구현, validation 실행, evidence 생성, review 보조에 사용한다.

---

## 5. 다른 도구

Superpowers는 여러 coding agent를 지원한다.

| 도구 | 설치 방식 |
|---|---|
| Antigravity | `agy plugin install https://github.com/obra/superpowers` |
| Factory Droid | marketplace 등록 후 `droid plugin install superpowers@superpowers` |
| GitHub Copilot CLI | marketplace 등록 후 `copilot plugin install superpowers@superpowers-marketplace` |
| Kimi Code | `/plugins`에서 Superpowers 설치 또는 repo URL 설치 |
| OpenCode | Superpowers repo의 `.opencode/INSTALL.md` 지침 사용 |
| Pi | `pi install git:github.com/obra/superpowers` |

수업에서 직접 다루는 도구가 아니면 선택 설치다. 단, 자신이 실습에 사용할 agent에는 반드시 설치한다.

---

## 6. 설치 후 확인

설치 후 새 agent session을 열고 아래처럼 물어본다.

```text
Superpowers가 설치되어 있는지 확인하고, 현재 사용할 수 있는 개발 workflow skill을 요약해줘.
```

기대하는 방향:

```text
- brainstorming
- writing-plans
- test-driven-development
- subagent-driven-development 또는 executing-plans
- requesting-code-review
- verification-before-completion
```

정확한 표시 이름은 사용하는 도구와 버전에 따라 다를 수 있다. 중요한 것은 agent가 개발 작업 전에 관련 skill을 확인하고 사용하려는 태도를 보이는 것이다.

---

## 7. 주의사항

- 설치 명령은 도구 버전에 따라 바뀔 수 있으므로, 최신 안내는 https://github.com/obra/superpowers 를 확인한다.
- 회사/학교 보안 환경에서는 plugin 설치가 제한될 수 있다.
- Superpowers는 절차를 강하게 유도하지만, 프로젝트별 `allowed_paths`, `forbidden_paths`, validation, evidence 계약은 여전히 직접 작성해야 한다.
- Telemetry를 비활성화해야 하는 환경에서는 Superpowers README의 telemetry opt-out 안내를 따른다.
