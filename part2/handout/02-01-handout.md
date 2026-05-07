# Session 2-1 한 장 정리 — 좋은 지시형 프롬프트의 WHAT/WHY/HOW

본문 대본: [../02-01-what-why-how.md](../02-01-what-why-how.md)
강사용 근거 자료: [../research/02-01-what-why-how-evidence.md](../research/02-01-what-why-how-evidence.md)

## 핵심 한 줄

> "지시문은 단순한 글쓰기가 아니다. AI에게 *작업 범위*와 *위험 범위*를 정해주는 **제어면(control surface)**이다."

이 세션에서 단 하나만 기억해야 한다면: **모호한 지시문은 결과 품질만 떨어뜨리는 게 아니라, AI가 의도하지 않은 파일을 수정하거나 위험한 명령을 실행하게 만든다.**

## 도구별로 어떻게 적용할까

### Claude Code를 쓴다면
1. 위험한 행동(파일 삭제, 강제 push, 외부 서비스 호출) 전에 *확인하라*는 지시를 시스템 프롬프트나 `CLAUDE.md`에 넣는다. Anthropic 공식 가이드도 이 방향을 권한다.
2. 5번 이상 반복한 지시는 그 자리에서 `CLAUDE.md`로 옮긴다 (다음 세션 2-2에서 자세히).
3. Plan Mode를 적극 활용 — 변경 전에 계획을 보여달라고 요청.

### Codex를 쓴다면
1. `AGENTS.md`에 **정지 조건 / 안전한 행동 / 위험한 행동 / 사용자에게 다시 넘길 시점**을 명시. (OpenAI 공식 GPT-5 가이드 권장)
2. 모순된 지시문 절대 금지 — GPT-5는 모순을 화해시키느라 추론 토큰을 낭비해 *다른 모델보다 더* 손해.

### 공통 — Context Engineering 원칙 (어떤 도구에서나)
1. **황금률**: 동료에게 보여줘서 헷갈리면 AI도 헷갈린다.
2. WHAT 다음에 *WHY*를 적어라. 모델은 동기에서 일반화한다.
3. **검증 가능한 성공 기준**(테스트, git diff, 스크린샷)을 함께 줘라 — Anthropic이 직접 *"single highest-leverage thing"* 이라고 표현했다.

## 자주 하는 실수

| ❌ 이렇게 쓰지 말기 | ✅ 이렇게 바꾸기 |
|---|---|
| "이 프로젝트 좀 정리해줘" | "README의 설치 섹션만 최신화. 코드 파일은 수정 금지. 변경 후 `git diff` 보여줘." |
| "절대 markdown 쓰지 마" | "smoothly flowing prose paragraphs로 답해줘" (할 것을 적기) |
| 완료 기준 없이 작업 시작 | "git diff에서 [예상 변경 외에] 변경 없을 것" — 검증 기준 명시 |
| OS 명시 안 함 | "PowerShell에서 실행 / WSL2에서 실행"을 지시문에 명시 |

## 이번 주에 해볼 것

- [ ] 평소 자주 던지는 모호한 프롬프트 1개를 골라 **WHAT / WHY / HOW + 검증 기준 + 금지 사항**으로 다시 써보기
- [ ] AI에게 작업을 시킬 때 *검증 명령*(테스트, `git diff`, 스크린샷)을 항상 지시문에 포함하기
- [ ] 같은 작업 지시를 두 번째로 입력하고 있다는 걸 알아차리면 그 자리에서 메모 → 세션 2-2의 `CLAUDE.md` 후보

## 더 알아보기

- 공식 (Claude Code): [Anthropic Prompting Best Practices](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- 공식 (Codex): [OpenAI GPT-5 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide)
- 1차 출처 모음 (강사 인용 가능): [research/02-01-what-why-how-evidence.md](../research/02-01-what-why-how-evidence.md)
- 용어집: [glossary.md](./glossary.md) — *제어면, WHAT/WHY/HOW, 황금률, 검증 가능 지시문* 참고
