# Session 1-3 - Codex용 실전 스킬 만들기

## 오늘 가져갈 것

- `.agents/skills/<skill-name>/SKILL.md` 형태의 Codex 스킬 초안을 만듭니다.
- `description`을 정확하게 써서 스킬이 필요한 상황을 분명히 합니다.
- 처음에는 `SKILL.md` 하나로 시작하고, 필요할 때만 `scripts/`나 `references/`를 추가합니다.

## 강의 진행 흐름

1. Codex 스킬도 Claude Code 와 다르지 않음.
2. `description`이 스킬 호출 여부를 좌우한다는 점을 설명합니다.

## Codex를 쓴다면

Codex에게는 스킬의 `description`을 특히 신경 써서 작성하게 하세요. "문서 확인"처럼 너무 넓은 설명보다 "코드 변경 뒤 README, 예시 명령, 사용법 문서 업데이트 필요 여부를 점검"처럼 작업 상황이 드러나는 설명이 좋습니다.

Codex CLI에서는 `/skills`로 보유 스킬을 둘러보고, `$skill-name`으로 명시 호출합니다. 강의 중에는 `$skill-creator`를 한 번 실행해 작동했던 대화 한 토막을 스킬 초안으로 만들고, 그 결과를 사람과 함께 다듬는 흐름이 이해가 빠릅니다.

Codex App을 쓰는 경우에도 먼저 스킬 본문 초안을 만들고, 실제 파일 생성은 변경 목록을 확인한 뒤 진행합니다.

## Reference

- 공식 (Codex): [Skills](https://developers.openai.com/codex/skills)
- 공식 (Codex): [CLI Features](https://developers.openai.com/codex/cli/features)
- 공식 (Codex): `$skill-creator` 사용 예시