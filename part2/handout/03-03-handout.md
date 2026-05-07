# Session 3-3 한 장 정리 — 컨텍스트-문서 분리 전략 (Part 2 종합)

본문 대본: [../03-03-context-doc-separation.md](../03-03-context-doc-separation.md)
강사용 근거 자료: [../research/03-03-context-doc-separation-evidence.md](../research/03-03-context-doc-separation-evidence.md)

## 핵심 한 줄

> "긴 프롬프트를 *더 길게* 만들지 말고, 정보의 **성격**에 맞춰 **4계층**으로 나눠 둬라. 이게 컨텍스트 엔지니어링이다."

## 4계층 컨텍스트 모델 (이 세션의 핵심 프레임)

| 계층 | 무엇 | 어디 | 갱신 주기 |
|---|---|---|---|
| ① **즉시 프롬프트** | 지금 한 번만 필요한 요청 | 대화 | 매번 |
| ② **세션 핸드오프** | 내일 이어갈 작업 요약 | `session-handoff.md` | 매 세션 |
| ③ **프로젝트 문서** | 매번 지킬 규칙·명령·결정 | `CLAUDE.md` / `AGENTS.md` | 변경 시 |
| ④ **외부 공식 문서** | 자주 바뀌는 제품 기능 | 링크 + 확인 날짜 | 촬영/실습 전 |

> **결정 기준**: "이 정보가 *얼마나 자주* 필요한가? *얼마나 자주* 바뀌는가?" → 계층이 정해진다.

## 도구별로 어떻게 적용할까

### Claude Code를 쓴다면
1. **③ 프로젝트 문서**: `CLAUDE.md` (전역/프로젝트/하위폴더 계층)
2. **반복 패턴은 Skills로 코드화** — Skills 자체가 작은 ③ 계층 모듈
3. `/compact` 결과를 그대로 두지 말고 `session-handoff.md`로 옮기기 (② 계층 영속화)

### Codex를 쓴다면
1. **③ 프로젝트 문서**: `AGENTS.md` (32KiB cap)
2. `AGENTS.md` import로 계층 분리(공통 / 환경별 / 폴더별)
3. `codex resume` 결과를 ② 핸드오프 노트로 영속화

### 공통 — Context Engineering 원칙
1. **즉시 프롬프트에 모든 걸 욱여넣지 마라.** 길어질수록 모델은 가운데를 흘린다(3-1 Lost in the Middle 참고).
2. **자주 바뀌는 정보를 ③에 박제하지 마라.** 제품 기능은 ④ 외부 공식 문서 링크 + 확인 날짜로.
3. **한 번만 필요한 정보를 ③ 규칙으로 만들지 마라.** 그건 ① 대화에 두고 끝낸다.
4. RAG는 ④와 ③ 사이의 자동화된 사례로 볼 수 있다.

## 자주 하는 실수

| ❌ 이렇게 하지 말기 | ✅ 이렇게 바꾸기 |
|---|---|
| 모든 정보를 프롬프트에 욱여넣기 | 성격에 맞는 계층 ①~④로 분배 |
| 자주 바뀌는 제품 기능을 `CLAUDE.md`에 박제 | 공식 문서 링크 + 확인 날짜로 ④에 |
| 한 번 필요한 요청을 ③ 규칙으로 | 그건 ① 대화에서 끝 |
| 환경 정보를 매 대화에 반복 | `setup` 문서 또는 ③ 규칙 문서에 영속화 |

## 이번 주에 해볼 것 (Part 2 종합 실습)

- [ ] 자주 쓰는 긴 프롬프트 1개를 골라 4계층(①/②/③/④)으로 분해
- [ ] `context-map.md` 만들기 — 각 정보가 *어느 계층에 / 왜 / 갱신 주기는?*
- [ ] **Part 2 종합 루프 한 사이클 돌리기**:
  - 작업 전: 규칙 문서(③) 읽기
  - 작업 중: 공식 문서(④) 확인
  - 작업 후: 검증 결과 + 핸드오프 노트(②) 남기기
  - 반복 정정 발견 시: ③ 규칙으로 옮기기

## 다른 세션과의 연결

- 2-1 (WHAT/WHY/HOW): 잘 짜인 ① 즉시 프롬프트 = 짧고 검증 가능
- 2-2 (CLAUDE.md): ③ 프로젝트 문서 (Claude Code)
- 2-3 (AGENTS.md): ③ 프로젝트 문서 (Codex 공통)
- 3-1 (Context rot): ① 대화가 길어지면 망가지는 이유
- 3-2 (`/compact`): ① → ② 핸드오프로 옮기는 보조 도구

## 더 알아보기

- 공식 (Anthropic): [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) / [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- 공식 (Claude Code): [Skills](https://code.claude.com/docs/en/skills)
- 학술: [Lost in the Middle](https://arxiv.org/abs/2307.03172) / [RAG 원논문](https://arxiv.org/abs/2005.11401)
- 업계: [Cognition AI — Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents)
- 1차 출처 모음: [research/03-03-context-doc-separation-evidence.md](../research/03-03-context-doc-separation-evidence.md)
- 용어집: [glossary.md](./glossary.md) — *4계층 컨텍스트 모델, RAG, Skills, 핸드오프 노트* 참고
