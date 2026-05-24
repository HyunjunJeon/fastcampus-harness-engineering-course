# Python Hook Review Checklist

훅 구현 리뷰는 코드 스타일보다 운영 결정과 우회 가능성에 집중합니다.

## 1. 입력

- hook payload에서 어떤 필드를 읽는가?
- Claude Code와 Codex의 payload 차이를 흡수하는가?
- 입력이 없거나 JSON이 깨졌을 때 안전하게 실패하는가?

## 2. 결정

- protected, governed, approval, verify 등급이 정책 문서와 맞는가?
- `deny`가 필요한 곳과 `ask`/prompt가 필요한 곳을 구분하는가?
- Codex에서 아직 지원하지 않는 PreToolUse `ask`를 반환하지 않는가?

## 3. 실패 행동

- Agent가 다음에 무엇을 고쳐야 하는지 알 수 있는 메시지를 주는가?
- stderr/stdout이 사람이 읽을 수 있는가?
- exit code와 JSON decision을 섞어 잘못 쓰지 않는가?

## 4. 우회 가능성

- 로컬 훅으로 못 잡는 경우를 CI와 Rulesets가 다시 잡는가?
- 민감 파일은 GitHub Push ruleset에서 다시 차단되는가?
- 훅/정책 파일 변경은 CODEOWNERS 승인을 요구하는가?
