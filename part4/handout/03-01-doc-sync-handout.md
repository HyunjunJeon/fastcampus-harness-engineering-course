# Session 3-1 - AI가 코드를 바꾸면 문서도 같이 바뀌게 만들기

> 코드가 바뀌었는데 문서가 그대로면 사용자는 `오래된 길 안내판`을 보게 됩니다.

- 코드 변경 뒤 문서 영향도를 판단하는 질문을 만듭니다.
- README, 사용법, 예시 명령, 스크린샷을 확인 목록에 넣습니다.
- 문서 수정이 필요 없다는 판단에도 이유를 남깁니다.

## 진행 흐름

1. 개발 관련 문서를 "AI Agent 와 사용자가 보는 길 안내판"으로 소개합니다.
2. 코드 변경이 사용자에게 보이는 변화를 만들 수 있음을 설명합니다.
3. AI에게 문서 수정 전에 영향도 판단표만 만들게 합니다.
4. README, 사용법, 예시 명령, 스크린샷을 함께 확인합니다.
5. 수정 필요, 수정 불필요, 추가 확인 필요를 구분해 마무리합니다. "문서가 빠졌으면 끝나지 못한다"는 규칙을 시스템으로 강제할 수 있는지 — 즉, 훅 또는 스크립트로 검사할 수 있는지 함께 토론합니다.

## Claude Code를 쓴다면

Claude Code에는 코드 변경 후 "문서 영향도 판단표만 먼저 만들어 달라"고 요청합니다. 바로 문서를 고치게 하기보다, 어떤 문서가 왜 바뀌어야 하는지 먼저 확인하면 비개발자도 검토하기 쉽습니다.

문서 수정이 필요하다면 수정 전후 요약과 사람이 확인할 화면 또는 명령을 함께 요구합니다.

## Codex를 쓴다면

Codex에서는 `doc-sync-check` 같은 스킬로 코드 변경과 문서 변경을 묶을 수 있습니다. Codex가 변경한 파일 목록을 바탕으로 README, handout, 예시 명령, 설정 키가 영향을 받았는지 확인하게 합니다.

App을 쓰는 경우에는 변경 파일 목록과 diff 화면을 함께 보며 판단표를 확인합니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 코드가 통과하면 문서도 괜찮다고 보기 | 사용자에게 보이는 변화가 있는지 확인 |
| 문서 수정 필요 없음만 적기 | 왜 필요 없는지도 기록 |
| README만 확인 | 예시 명령, 설정 키, 스크린샷도 확인 |
| AI가 문서를 고친 뒤 검토 생략 | 변경 이유와 확인 기준을 다시 받기 |

## Reference

아래 공식 문서 링크는 촬영일과 강의 운영일에 다시 확인하세요.

- 공식 (Codex): [Skills](https://developers.openai.com/codex/skills)
- 공식 (Claude Code): [Skills](https://code.claude.com/docs/en/skills)

## 실습

실습 레포 위치: `part4/lab/workflows/doc-sync/SKILL.md`, `part4/lab/scripts/changed_docs_check.py`, `part4/lab/docs/`

"문서가 빠지면 끝나지 못한다"를 스크립트로 강제합니다.

```python
# scripts/changed_docs_check.py (개념 발췌)
CODE_PREFIXES = ("app/", "tests/")
DOC_PREFIXES = ("docs/",)

# 코드가 변경됐는데 docs/ 안에 변경이 하나도 없으면 1로 종료
```

훅 조합은 두 단계로 둡니다.

- `PostToolUse: Edit|Write` → `post_file_change_hook.py` 안에서 `changed_docs_check.py --soft` 실행 (작업 중 알림)
- `Stop` → `stop_verify_hook.py`가 `agent_verify.sh`를 호출하고, 그 안에서 `changed_docs_check.py` 실행 (작업 종료 전 검증 루프)

부드러운 모드(`--soft`)는 작업 중 흐름을 끊지 않고 경고만 띄우고, 마지막 검증은 강한 모드로 한 번 더 잡아 빠뜨림을 막습니다.
