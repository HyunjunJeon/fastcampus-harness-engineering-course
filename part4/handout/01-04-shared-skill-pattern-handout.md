# Session 1-4 한 장 정리 - Claude Code와 Codex 공용 스킬 재사용 패턴

> 업무 절차는 공통으로, 도구별 파일 위치와 호출 방식은 따로 관리합니다.

## 오늘 가져갈 것

- 공통 업무 절차와 도구별 설정을 분리합니다.
- Claude Code와 Codex 스킬이 같은 체크리스트를 재사용하게 설계합니다.
- 도구별 차이를 기능 대응표가 아니라 운영 위치와 호출 방식으로 정리합니다.

## 흐름

1. 같은 업무를 두 도구에서 반복하려 할 때 생기는 중복 문제를 소개합니다.
2. "업무 절차"와 "도구별 포장"을 분리하는 원칙을 설명합니다.
3. Claude Code 스킬 초안과 Codex 스킬 초안을 나란히 비교합니다.
4. 공통 체크리스트와 도구별 차이를 표로 분리합니다.
5. 재사용을 과하게 추상화하지 않고 실제 산출물 기준으로 마무리합니다.

## Claude Code를 쓴다면

Claude Code에는 Claude 전용 위치, 호출 방식, 설정 문법만 남깁니다. 업무 절차 자체는 공통 문서로 빼 두면 Codex와 함께 쓰기 쉽습니다.

예를 들어 "변경사항 요약" 절차는 공통이고, `.claude/skills/` 위치는 Claude Code 전용입니다.

## Codex를 쓴다면

Codex에는 `.agents/skills/` 구조와 Codex에서 스킬을 발견하는 설명을 둡니다. 공통 체크리스트가 있다면 Codex 스킬은 그 체크리스트를 읽고 실행하는 역할만 맡기면 됩니다.

스킬을 너무 도구 전용으로 쓰면 나중에 다른 도구로 옮기기 어렵습니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| Claude Code용 파일을 그대로 Codex에 복사 | 공통 절차와 도구 전용 문법을 분리 |
| 모든 규칙을 한 스킬에 넣기 | 업무 단위별로 작게 나누기 |
| 도구 이름을 절차 곳곳에 섞기 | 공통 문서는 업무 언어로 작성 |
| 재사용을 이유로 너무 과한 추상화 | 실제 산출물과 검증 기준은 구체적으로 유지 |

## Reference

- 공식 (Claude Code): [Skills](https://code.claude.com/docs/en/skills)
- 공식 (Codex): [Skills](https://developers.openai.com/codex/skills)

## 심화적인 내용

실습 레포 위치: `part4/lab/workflows/`, `part4/lab/.claude/skills/`, `part4/lab/.agents/skills/`

Core + Adapter 패턴으로 구성.
> 스킬 본문은 한 곳에 두고, 도구별 위치에서는 그쪽으로 연결만 합니다.

```
part4/lab/
  workflows/
    debug-loop/SKILL.md          # 진실의 단일 출처
    debug-loop/references/
    debug-loop/scripts/
  .claude/skills/debug-loop  ->  ../../workflows/debug-loop   # symlink
  .agents/skills/debug-loop  ->  ../../workflows/debug-loop   # symlink
```

심볼릭 링크가 막힌 환경에서는 `cp -R`로 동기화하는 단일 스크립트(예: `scripts/install_skills.sh`)를 둡니다. Claude Code 전용 frontmatter(`allowed-tools`)나 Codex 전용 메타데이터는 공통 본문에 두지 말고, 각 AI Agent 도구별 어댑터 파일에만 둡니다.
