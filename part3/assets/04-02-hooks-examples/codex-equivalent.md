# Codex에서 훅과 동등한 효과 내기

Claude Code의 `hooks` 키는 Codex에 동일 이름으로 존재하지 않는다(촬영일 기준 공식 문서 확인). 대신 두 방향이 있다.

## 방향 1 — AGENTS.md에 검증 명령을 명시

Codex는 AGENTS.md를 자동으로 읽는다. 다음과 비슷한 항목을 추가해 모델에게 "변경 후 항상 이 명령을 돌려라"고 지시한다.

````markdown
## 변경 후 검증

코드를 변경하면 반드시 다음을 실행한다.

- `ruff check .` 또는 `npm run lint`
- `pytest -q` 또는 `npm test`

한 명령이라도 실패하면 변경을 되돌리고 사용자에게 보고한다.
````

이 방법은 *모델에게 강제*하는 형태라 100% 보장이 아니다. 강의에서 이 한계를 명시한다.

## 방향 2 — Git pre-commit 훅으로 외부에서 강제

훅을 도구 레벨이 아니라 *저장소 레벨*에 둔다. `pre-commit` 프레임워크로 lint·test를 강제하면 도구가 무엇이든 커밋 단계에서 막힌다.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint
        name: lint
        entry: ruff check .
        language: system
        pass_filenames: false
      - id: test
        name: test
        entry: pytest -q
        language: system
        pass_filenames: false
```

## 강의에서의 메시지

"Claude Code와 Codex의 같은 기능을 1:1로 매핑하지 마라. 같은 문제(변경 후 자동 검증)를 푸는 다른 도구일 뿐이다. Codex 환경에서는 AGENTS.md 또는 git hooks 같은 외부 기제로 동등 효과를 낸다."
