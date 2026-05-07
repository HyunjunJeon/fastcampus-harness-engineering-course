# Session 2-1. 좋은 지시형 프롬프트는 무엇이 다른가: WHAT, WHY, HOW

## 목표

AI에게 일을 맡길 때 필요한 맥락을 빠뜨리지 않고, 
`검증 가능한(Closed Question) 형태의 작업 지시문`을 작성한다.

## Main

구조화 (계층적) 강조, 작업 목적에 대한 명시, 길어진 프롬프트를 다루기

1. WHAT, WHY, HOW를 설명한다.
   - WHAT: 무엇을 바꿀 것인가(만들것인가)
   - WHY: 왜 바꾸는가(하는가), 무엇을 보존해야 하는가(하지말아야 하는가)
   - HOW: 어떤 방식과 제약으로 진행할 것인가

> Prompt Guide 2개를 비교한다
> GPT: https://developers.openai.com/api/docs/guides/prompt-guidance
> Claude: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

2. 작업 지시문 구조를 만든다.
   - 배경
   - 목표
   - 작업 범위
   - 제외 범위
   - 진행 방식
   - 검증 방법
   - 보고 형식

3. 긴 프롬프트를 문서로 분리해야 하는 신호를 알려준다.
   - 같은 지시를 반복해서 붙여넣는다.
   - 프로젝트 규칙이 계속 등장한다.
   - 테스트 명령, 금지 사항, 보고 방식이 매번 같다.
   - 이때 `CLAUDE.md` 또는 `AGENTS.md`로 옮긴다.

4. 지시문 리팩터링 실습을 한다.
   - 모호한 지시문을 템플릿에 맞춰 고친다.
   - AI에게 개선안을 받는다.
   - 사람이 최종 선택한다.

## 산출물

```text
목표:
배경:
작업 범위:
제외 범위:
진행 방식:
검증 방법:
완료 후 보고:
```

---

> 강사용 근거 자료: [research/02-01-what-why-how-evidence.md](./research/02-01-what-why-how-evidence.md)
> 수강생용 한 장 정리: [handout/02-01-handout.md](./handout/02-01-handout.md)
> 용어집: [handout/glossary.md](./handout/glossary.md)

====

<role>
당신은 신중한 시니어 소프트웨어 엔지니어입니다.
</role>

<goal>
[무엇을 달성해야 하는지 한 문장으로 작성]
</goal>

<context>
[관련 파일, 로그, 배경, 사용자가 이미 결정한 내용]
</context>

<constraints>
[하지 말아야 할 것, 지켜야 할 아키텍처/스타일/보안 조건]
</constraints>

<process>
1. 먼저 관련 맥락을 확인하세요.
2. 가능한 원인을 2-3개로 좁히세요.
3. 가장 가능성 높은 원인을 선택하고 근거를 제시하세요.
4. 필요한 경우 최소 범위로 수정하세요.
5. 테스트 또는 검증을 실행하세요.
</process>

<output_contract>
- 결론
- 근거
- 수행한 작업
- 검증 결과
- 남은 리스크
</output_contract>

<done_when>
[완료로 인정할 조건]
</done_when>