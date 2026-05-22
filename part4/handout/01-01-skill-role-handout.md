# Session 1-1 - 매번 같은 프롬프트를 입력하지 않기

## 핵심 한 줄

> 스킬은 자주 반복하는 프롬프트를 AI가 다시 꺼내 쓸 수 있는 업무 매뉴얼로 바꾼 것입니다.

## 오늘 가져갈 것

- 반복 프롬프트와 일회성 질문을 구분합니다.
- 스킬을 만들기 전에 입력, 절차, 출력, 검증 기준을 먼저 정합니다.

## 흐름

1. 반복 프롬프트를 "매번 다시 설명하는 업무 요청"으로 소개합니다.
2. 스킬을 "AI에게 맡기는 업무 매뉴얼"로 비유해 설명합니다. 
외부 시스템 연결(MCP)과는 다르다는 점을 한 줄로 짚습니다 — 
MCP는 **어떤 도구를 쓸 수 있는지를 늘리고**, **스킬은 어떻게 일할지를 재사용**합니다.
3. 결과 확인 위험 요소와 사람이 확인할 기준을 함께 점검합니다. 
스킬을 무한정 늘리면 오히려 호출 정확도가 떨어진다는 점도 함께 말합니다(Context Rot).

## Claude Code를 쓴다면

Claude Code에서는 스킬을 특정 작업에 맞는 절차서로 생각하면 됩니다. 
프로젝트에서 반복되는 업무라면 개인 메모가 아니라 프로젝트 안에 둘 후보로 검토합니다.
처음부터 파일을 만들기보다 Claude에게 "이 요청이 스킬로 만들 만한지 판단해 달라"고 먼저 물어보세요. 
스킬이 필요 없는 요청까지 파일로 만들면 관리할 문서만 늘어납니다.

## Codex를 쓴다면

Codex에서도 스킬은 반복 업무를 압축하는 방식입니다. 
중요한 것은 `description`입니다.
 설명이 너무 넓으면 원치 않을 때 자주 불리고, 너무 좁으면 필요할 때 불리지 않습니다.
Codex App을 쓴다면 먼저 채팅에서 스킬 후보 카드만 만들고, 파일 생성은 다음 세션에서 진행해도 충분합니다.

## Reference

아래 공식 문서 링크

- 공식 (Claude Code): [Skills](https://code.claude.com/docs/en/skills)
  - 본 문서의 lifecycle 수치 출처: [Skill content lifecycle](https://code.claude.com/docs/en/skills#skill-content-lifecycle)
- 공식 (Codex): [Skills](https://developers.openai.com/codex/skills)

### Skill content lifecycle — 토큰 비용을 의식하기

> 출처: Anthropic 공식 Claude Code 문서, [Skills > Skill content lifecycle](https://code.claude.com/docs/ko/skills#skill-%EC%BD%98%ED%85%90%EC%B8%A0-%EB%9D%BC%EC%9D%B4%ED%94%84%EC%82%AC%EC%9D%B4%ED%81%B4) 섹션. Anthropic이 정책을 바꾸면 수치도 바뀔 수 있으니 주의해주세요.

- 스킬은 한 번 호출되면 본문이 단일 메시지로 컨텍스트에 들어가 **세션 끝까지 유지**됩니다. Claude Code는 이후 턴에 스킬 파일을 다시 읽지 않습니다.
- 자동 압축(auto-compaction)이 발생하면 각 스킬의 가장 최근 호출 본문이 **앞에서부터 최대 5,000 토큰까지** 살아남습니다.
- 재부착되는 모든 스킬은 **합쳐서 25,000 토큰 예산**을 공유하며, 가장 최근 호출부터 채웁니다. 예산을 넘으면 오래된 스킬은 통째로 빠집니다.

이 메커니즘이 두 가지를 강제합니다.

- 본문은 짧게 — 매 턴 누적되는 토큰 비용이므로.
- 트리거(`description`)는 명확하게 — 호출되지 않으면 본문도 들어오지 않으므로.
