# Session 4-1 - 추측 대신 측정 가능한 완료 기준 세우기

> "잘 된 것 같다"는 AI Agent 말은 위험 신호입니다. 작업을 시작하기 전에 무엇을 보면 완료라고 말할지 먼저 정합니다.

- 작업 요청을 목표, 제약, 완료 기준 세 칸으로 나누어 적습니다.
- 완료 기준에는 사람이 직접 눈으로 확인할 증거를 적어도 하나 둡니다.
- 테스트가 가능한 작업이라면 실패 테스트부터 먼저 만들게 합니다. (TDD)

## 진행 흐름

1. 흔히 받는 모호한 요청 한 개를 화면에 띄우고, 무엇이 빠져 있는지 함께 짚습니다.
2. 같은 요청을 `목표 / 제약 / 완료 기준` 세 칸 카드로 다시 적습니다.
3. 완료 기준에 "테스트가 통과한다", "문서가 갱신된다", "사람이 확인한다" 중 어떤 증거가 들어갈 수 있는지 토론합니다.
4. AI에게 같은 카드를 입력하고, AI가 빠뜨린 완료 기준을 사람이 채우게 합니다.

## Claude Code를 쓴다면

Claude Code는 완료 기준을 입력으로 받았을 때 분명히 더 잘합니다. 작업 시작 전에 `Done when` 카드를 채팅 맨 위에 붙여 두면, 이후 대화가 길어져도 그 기준이 컨텍스트에 남는 동안 모델이 그것을 향해 움직입니다.

다만 컨텍스트가 길어지면 초반 카드가 흐려질 수 있으므로, 작업 중반에 한 번씩 "현재 완료 기준을 다시 요약해 줘"라고 묻고 그대로인지 확인합니다.

## Codex를 쓴다면

Codex 공식 가이드는 작업 요청에 목표, 컨텍스트, 제약, 완료 기준을 함께 넣으라고 권합니다. Codex App에서는 작업 카드 본문 자체에 이 4가지를 박아 두면, 다른 사람이 같은 카드를 가져가도 같은 기준으로 작업이 진행됩니다.

테스트가 가능한 변경이라면 "먼저 실패 테스트를 만들고, 통과시킬 최소 수정만 하라"는 한 줄을 카드 끝에 두는 것이 효과가 큽니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| "잘 되게 해줘"로 끝나는 요청 | 사람이 확인할 증거를 적어도 하나 적기 |
| 완료 기준에 "AI가 동의함"을 넣기 | 테스트, 문서, 화면 캡처처럼 외부에서 확인 가능한 증거만 인정 |
| 실패 테스트 없이 곧장 구현 요청 | 테스트가 가능한 변경이면 실패 테스트부터 시키기 |
| 제약을 적지 않기 | "기존 API 경로는 바꾸지 않는다" 같은 한 줄이라도 넣기 |

## Reference

- 공식 (Claude Code): [Best practices for Claude Code — "Give Claude a way to verify its work"](https://code.claude.com/docs/en/best-practices)
- 공식 (Codex): [Codex best practices — "Done when" 가이드](https://developers.openai.com/codex/learn/best-practices)
- 공식 (Codex): [Codex prompting — 측정 가능한 목표 작성법](https://developers.openai.com/codex/prompting)

## 실습

실습 레포 위치: `part4/lab/`

`Done when` 카드를 검증 명령으로 묶어 둡니다. 같은 카드를 받으면 누구나 같은 명령으로 통과 여부를 확인할 수 있어야 합니다.

```bash
# 카드의 "완료 기준" 라인을 그대로 명령으로 풀어 쓴 예시
bash part4/lab/scripts/agent_verify.sh
```

```markdown
## Done when (예시)

- `tests/test_notes_api.py::test_search_is_case_insensitive`가 통과한다.
- `ruff check .` 0 위반.
- `mypy app` 0 오류.
- `docs/api-contract.md`의 검색 규칙 섹션이 갱신되어 있다.
- `bash scripts/agent_verify.sh`가 종료 코드 0으로 끝난다.
```
