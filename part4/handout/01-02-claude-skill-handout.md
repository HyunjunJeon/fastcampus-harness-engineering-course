# Session 1-2 - Claude Code용 실전 스킬 만들기

## 오늘 가져갈 것

- `.claude/skills/<skill-name>/SKILL.md` 형태의 스킬 초안을 만듭니다.
- 스킬 이름, 설명, 작업 절차, 출력 형식을 분리합니다.
- 파일 생성 전에는 항상 계획을 먼저 확인합니다.

## Claude Code를 쓴다면

Claude Code에는 "먼저 계획만 보여주세요"라고 요청한 뒤 파일 생성을 진행하는 흐름이 안전합니다. 
파일 경로와 목적을 먼저 이해하고, 실제 파일 생성은 AI가 제안한 내용을 확인한 뒤 승인합니다.

프로젝트에서 함께 쓸 스킬은 개인 메모가 아니라 저장소 안에 두어야 팀원이 같은 절차를 재사용할 수 있습니다.


## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 파일부터 바로 만들기 | 계획을 먼저 받고 경로를 확인하기 |
| 스킬 설명을 너무 길게 쓰기 | 언제 불러야 하는지 한 문장으로 쓰기 |
| 설명에 트리거 단서가 약하게 들어가기 | "Use when ..."처럼 단호하게 쓰기 — 모델은 스킬을 과소 호출하는 경향이 있습니다 |
| 출력 형식 없이 절차만 쓰기 | 표, 체크리스트, 요약 형식을 명시하기 |
| 위험한 작업까지 자동 실행하게 하기 | 삭제, 배포, push는 승인 대상으로 남기기 |

## Reference

- 공식 (Claude Code): [Skills](https://code.claude.com/docs/en/skills)
- 공식 (Claude Code): [Settings](https://code.claude.com/docs/en/settings)
- 공식 (Anthropic): `anthropics/skills` 저장소의 `skill-creator` — 스킬 작성·평가·개선·벤치마크를 한 묶음으로 묶은 메타 스킬
- 참고: Claude Code 번들 스킬 목록(`/debug`, `/simplify`, `/batch`, `/loop`, `/claude-api`)은 공식 문서의 commands reference에서 확인
