# part5/handout - 수강생용 세션 자료 규칙

## 목적

이 폴더는 Part 5의 세부 강의 세션별 실습 handout입니다. 각 handout은 단독으로 읽고 실행할 수 있어야 합니다.

## 작성 규칙

- 각 세션은 하나의 파일로 분리합니다.
- 모든 실습은 `part5/lab` 안의 실행 가능한 명령을 포함합니다.
- live Claude Code, Codex, tmux, MCP가 필요한 단계는 "선택 live smoke"로 표시합니다.
- 기본 검증은 계정 없이 로컬에서 통과해야 합니다.
- `tmux-bridge-mcp`는 커뮤니티 MCP로 표기합니다.
- `claude -p` / `claude --print`는 공식 print mode지만, 이 수업에서는 interactive session 보존과 Agent SDK credit / usage credits 경계 때문에 금지한다고 설명합니다.
- hook은 guardrail이지 보안 경계가 아니라고 설명합니다.

## 표준 섹션

```markdown
# Session X-Y - 제목

## 핵심 한 줄
## 오늘 가져갈 것
## 실습
## 검증
## Claude Code를 쓴다면
## Codex를 쓴다면
## 실습 결과물
## 더 알아보기
```

`강의 진행 흐름`과 `자주 하는 실수`는 세션 성격상 필요할 때만 추가합니다. 필수는 실행 명령, 검증 명령, 산출물, 도구별 적용입니다.
