# Session 1-3 - SubAgent 에서 Main Agent 로 결과물을 전달(handoff)할 때

## 핵심 한 줄

SubAgent를 쓰는 이유는 메인 대화에 더 많은 말을 쌓기 위해서가 아니라,  
**노이즈가 큰 탐색을 격리하고 메인 에이전트가 다음 지시를 내릴 수 있는 인덱스만 남기기 위해서**입니다.

> 메인 컨텍스트에는 요구사항, 확정된 결정, 현재 계획, 검증 결과만 남깁니다.  
> raw log, 조사 상세, 중간 추론, open question은 파일로 보내고, 그 파일의 경로와 사용법만 컨텍스트에 남깁니다.

- SubAgent 결과를 `handoff file`과 `context index`로 나눕니다.
- Explorer, Implementer, Verifier의 산출물을 그대로 붙여 넣지 않고, 메인 에이전트가 다음 작업 지시에 필요한 경로와 결론만 선별합니다.
- 다음 세션이 `docs/current-state.md`와 `docs/session-summary.md`만 읽고 이어갈 수 있게 만듭니다.
- "context가 깨끗하다"는 상태를 감각이 아니라 파일 계약과 검증 명령으로 확인합니다.

---

## 1. 왜 파일과 Context 를 구분해서 넘겨야 하는가

SubAgent를 3개 띄웠다고 해서 멀티 에이전트 시스템이 저절로 나아지는 것은 아닙니다. 
오히려 다음과 같은 문제가 생길 수 있습니다.

| 문제 | 증상 | 교정 방향 |
| --- | --- | --- |
| 결과 덤프 | Explorer가 읽은 로그와 파일 요약을 전부 메인에 붙여 넣음 | raw output은 파일로 보내고, 메인에는 결론만 남김 |
| 결정 없음 | 세 agent 의견을 나열만 하고 무엇을 할지 정하지 않음 | `Decision` 섹션을 하나로 고정 |
| 근거 손실 | "아마 race condition"처럼 말하지만 파일 경로가 없음 | `Evidence`에 파일 경로를 남김 |
| 범위 팽창 | 조사 중 나온 주변 개선까지 같이 구현하려 함 | `Implementation scope`와 `Non-goals`를 분리 |
| 검증 공백 | "좋아 보인다"는 말로 끝남 | `Verification`에 명령과 기대 결과를 남김 |

핵심은 **SubAgent 결과 전체를 메인 컨텍스트에 합치는 것이 아니라, 큰 내용은 파일로 남기고 메인에는 그 파일을 다시 찾고 지시할 수 있는 인덱스를 남기는 것**입니다.

---

## 2. 메인 컨텍스트에 남길 것과 파일로 외부화 시킬 것

메인 컨텍스트 내에 남길 정보는 네 가지와 파일 인덱스로 제한하는 걸 추천드립니다.

```text
1. 요구사항
2. 확정된 결정
3. 현재 계획과 그 실행 결과(실행 결과는 가능하면 Git Commit 으로)
4. 검증 결과
5. 다음 작업에 필요한 handoff 파일 인덱스
```

나머지는 파일로 외부화하는게 좋습니다.
왜냐하면 내용이 길고, 다음 판단에 매번 전문이 필요하지 않기 때문입니다.

| 정보 | 저장 위치 | 이유 |
| --- | --- | --- |
| raw log | `fixtures/logs/`, `.harness/traces/` | 길고 반복적이며 메인 판단에 직접 필요하지 않음 |
| 조사 상세 | `docs/decisions/`, `docs/research/` | 근거는 보존하되 필요할 때만 열람 |
| 현재 상태 | `docs/current-state.md` | 다음 세션의 시작점 |
| 세션 요약 | `docs/session-summary.md` | handoff 패킷 |
| 실행 증거 | `.harness/runs/*.json` | 세션이 실행됐다는 evidence ledger |

메인 컨텍스트에는 파일 전문을 붙이지 않고, 다음처럼 **Context Index**만 남깁니다.

```markdown
## Context Index
- `docs/decisions/token-refresh-investigation.md`
  - contains: Explorer 조사 상세, 실패 로그 패턴, 원인 후보
  - use_for: 구현 범위와 위험 확인
- `docs/session-summary.md`
  - contains: 이번 세션의 결정, 남은 질문, 검증 명령
  - use_for: 다음 Main Agent 시작점
- `.harness/runs/01-03.json`
  - contains: 실행 증거와 timestamp
  - use_for: handoff가 실제 실행됐는지 검증
```

> **운영 규칙.** "다음 agent가 대화 스크롤백을 읽어야만 이어갈 수 있다"면 context hygiene에 실패한 상태입니다.

---

## 3. 메인 컨텍스트에 남길 Handoff Index 형식

메인 컨텍스트에 남겨둘 형식은 아래 여섯 항목입니다.

```markdown
## Decision
무엇을 하기로 확정했는가?

## Evidence
그 결정을 뒷받침하는 파일, 로그, 테스트, 문서는 무엇인가?

## Implementation scope
이번 작업에서 실제로 바꿀 범위는 어디까지인가?

## Non-goals
이번 작업에서 일부러 하지 않을 것은 무엇인가?

## Verification
완료를 어떤 명령과 기준으로 확인할 것인가?

## Context Index
긴 조사 결과, 로그, 실행 증거는 어느 파일에 있고 다음 agent는 각각을 언제 열어야 하는가?
```

Part 5의 token-refresh 시나리오에 적용하면 다음과 같습니다.

```markdown
# Handoff Index

## Decision
Concurrent refresh 요청은 session 단위 single-flight guard로 묶는다.

## Evidence
- `docs/context-hygiene.md`
- `docs/decisions/token-refresh-investigation.md`
- `fixtures/logs/failing-test.log`

## Implementation scope
- refresh race를 막는 최소 구현
- concurrent refresh test
- raw token logging 금지 확인

## Non-goals
- auth provider 교체
- DB schema 변경
- session model 리디자인

## Verification
- `bash scripts/check.sh --session 01-03`
- 이후 구현 세션에서는 token refresh race test와 전체 `bash scripts/check.sh`

## Context Index
- `docs/decisions/token-refresh-investigation.md`
  - contains: explorer 조사 상세와 실패 원인 후보
  - use_for: 구현 전 근거 확인
- `fixtures/logs/failing-test.log`
  - contains: raw 실패 로그
  - use_for: verifier가 재현 패턴을 확인할 때만 열람
- `.harness/runs/01-03.json`
  - contains: 01-03 실행 evidence
  - use_for: handoff 파일이 실제 실행 결과인지 검증
```

이 패킷은 "세 agent가 각각 무슨 말을 했는가"가 아니라 **메인 에이전트가 다음 지시를 내리기 위해 어떤 파일을 기준으로 삼아야 하는가**를 기록합니다.

## 실습

01-03 실습은 세션 산출물과 실행 evidence를 만들고, 대화 스크롤백이 source of truth가 아님을 파일로 고정합니다.

```bash
cd part5/lab
bash scripts/run_session.sh 01-03
```

실습 후에는 `docs/session-summary.md`, `docs/current-state.md`, `.harness/runs/01-03.json`를 기준으로 다음 Main Agent가 이어갈 수 있어야 합니다.

## Claude Code를 쓴다면

Claude Code에서 01-03을 실제 운영 흐름으로 실행한다면 구조는 다음과 같습니다.

```text
1. explorer subagent가 로그와 코드 흐름을 조사한다.
2. verifier subagent가 Done Criteria와 테스트 gap을 확인한다.
3. 메인 Claude Code 세션은 두 결과를 그대로 붙여 넣지 않는다.
4. 메인 세션이 Decision / Evidence / Scope / Non-goals / Verification / Context Index로 저장한다.
5. 결과를 docs/session-summary.md 또는 docs/decisions/*.md에 저장한다.
```

메인 세션에 요청할 때는 이렇게 씁니다.

```text
Use explorer and verifier subagents for read-heavy investigation.
Do not paste raw logs into the main response.
Write long findings to handoff files.
Return only a handoff index with:
- Decision
- Evidence files
- Implementation scope
- Non-goals
- Verification command
- Context Index: file path, contains, use_for
Then update docs/session-summary.md.
```

주의할 점은 01-02와 같습니다. `tools: Read, Grep, Glob, Bash`인 Explorer는 `Edit` 도구가 없어도 `Bash`로 파일을 수정할 수 있습니다. 따라서 "수정 금지"는 완전한 보안 경계가 아니라 guardrail과 review로 함께 지켜야 하는 운영 규칙입니다.

---

## Codex를 쓴다면

Codex에서는 조사와 검증을 native subagent로 분리하되, **무엇을 파일로 남기고 무엇을 컨텍스트에 남길지 결정하는 일은 메인 thread가 소유**하는 편이 안전합니다.

```text
Use Codex subagents in parallel for read-heavy investigation:

1. auth-flow-explorer
   - read only
   - return max 3 findings with file paths

2. log-triager
   - read only
   - summarize log patterns, no raw log dump

3. test-gap-reviewer
   - read only
   - compare current tests with DONE_CRITERIA.md

Main Codex thread:
- wait for all three results
- decide what becomes handoff files and what remains in context
- write or update handoff files for long results
- list Evidence files
- define Implementation scope and Non-goals
- record Verification command
- leave a Context Index in the main thread
```

운영 규칙:

| 규칙 | 이유 |
| --- | --- |
| read-heavy만 subagent로 보냄 | context bloat를 격리하기 위해 |
| write-heavy 구현은 한 owner가 맡음 | concurrent edit 충돌 방지 |
| raw output은 파일에 저장 | 메인 context가 불필요하게 길어지는 것을 방지 |
| 최종 decision과 context index는 메인 thread가 확정 | subagent 의견 나열을 방지하고 다음 지시의 기준을 고정 |

---

## 검증

```bash
cd part5/lab
bash scripts/check.sh --session 01-03
```

검증의 핵심은 다음 세 가지입니다.

- 세션 산출물이 파일로 남아 있다.
- raw log와 장문 조사 결과가 메인 대화에 남지 않는다.
- 메인 컨텍스트에는 다음 지시에 필요한 `Context Index`가 남는다.

## 실습 결과물

| 산출물 | 확인 방법 | 의미 |
| --- | --- | --- |
| `docs/session-summary.md` | `grep -n "Terminal scrollback is not used" docs/session-summary.md` | 대화 스크롤백을 기준 원본에서 제외 |
| `.harness/runs/01-03.json` | `cat .harness/runs/01-03.json` | 세션 실행 evidence |
| `bash scripts/check.sh --session 01-03` | 명령이 0으로 종료 | handout, hook policy, 테스트 계약 통과 |

---

## 5. SubAgent to Main Handoff 안티패턴

| 안티패턴 | 증상 | 교정 방향 |
| --- | --- | --- |
| SubAgent transcript 붙여 넣기 | 메인 context가 raw log와 장문 요약으로 불필요하게 길어짐 | handoff file은 파일에, context index만 메인에 남김 |
| 다수결식 결정 | agent 2개가 말했으니 맞다고 처리 | evidence file과 verifier rubric으로 판단 |
| 결정 없는 요약 | "A는 이렇게 말했고 B는 저렇게 말함"에서 끝남 | `Decision`을 한 문장으로 고정 |
| 근거 없는 결정 | "single-flight가 좋아 보인다"는 말만 남음 | `Evidence`에 파일 경로를 남김 |
| 파일만 만들고 인덱스를 안 남김 | 다음 Main Agent가 어떤 파일을 열어야 할지 다시 추론 | `Context Index`에 `path / contains / use_for`를 남김 |
| non-goal 누락 | 주변 리팩터링으로 범위가 커짐 | 하지 않을 일을 명시 |
| 검증을 나중으로 미룸 | handoff 후 다음 agent가 검증 방법을 다시 추론 | `Verification`에 명령과 기대 결과 기록 |
| current-state 방치 | 다음 세션이 이전 대화를 다시 읽어야 함 | `docs/current-state.md`와 `docs/session-summary.md` 갱신 |

### 완료 기준

```text
- 메인 대화에는 최종 Handoff Index만 남았다.
- 각 결정은 evidence file을 가진다.
- raw log와 중간 탐색 결과는 파일로 외부화됐다.
- 긴 파일 산출물은 `Context Index`를 통해 다시 찾을 수 있다.
- 다음 세션은 docs/current-state.md와 docs/session-summary.md만 읽고 이어갈 수 있다.
- bash scripts/check.sh --session 01-03이 통과한다.
```

---

## 더 알아보기

- OpenAI Harness engineering: https://openai.com/index/harness-engineering/
- 01-01 SubAgents와 context isolation: `part5/handout/01-01-subagents.md`
- 01-02 Explorer / Implementer / Verifier: `part5/handout/01-02-role-split.md`
- 이후 연결: 03-04 Skill / Hook / Eval, 03-05 Harness Retro
