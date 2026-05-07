# Session 2-3 한 장 정리 — AGENTS.md: 여러 도구에 통하는 공통 지시문

본문 대본: [../02-03-agents-md.md](../02-03-agents-md.md)
강사용 근거 자료: [../research/02-03-agents-md-evidence.md](../research/02-03-agents-md-evidence.md)

## 핵심 한 줄

> "`AGENTS.md`는 오픈 표준이지만, **Claude Code와 Codex가 그것을 완전히 같게 처리하지는 않는다.** 도구를 1:1로 동등하게 보지 말고, 공통 규칙은 `AGENTS.md` / 도구 전용 운영 팁은 별도 파일로."

## 도구별로 어떻게 적용할까

### Claude Code를 쓴다면
1. **Claude Code는 `AGENTS.md`를 직접 읽지 않는다.** 공식 문서가 명시: *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`."*
2. 해법: `CLAUDE.md`에 다음 한 줄로 import → `@AGENTS.md`. 이러면 두 파일이 동기화된다.
3. 또는 `AGENTS.md`(공통 규칙)와 `CLAUDE.md`(Claude Code 전용 운영 팁)를 *완전히 분리*해서 둘 다 유지.

### Codex를 쓴다면 (이 세션의 주력)
1. **Codex는 `AGENTS.md`를 표준대로 읽는다.** 32KiB 상한.
2. **루트 → 현재 폴더 순서로 concatenate**: 작업 중인 폴더에 가까운 `AGENTS.md`일수록 더 우선.
3. `AGENTS.override.md`로 부분 덮어쓰기 가능 (Codex 고유 의미론, 표준엔 없음).
4. 좋은 예시: [openai/codex 저장소의 nested AGENTS.md](https://raw.githubusercontent.com/openai/codex/main/codex-rs/tui/src/bottom_pane/AGENTS.md) — 깊은 폴더는 *루트 규칙을 반복하지 않고* 그 폴더 한정의 좁은 규칙만 담는다.

### 공통 — Context Engineering 원칙
1. **하위 폴더로 갈수록 더 구체적**. 루트 `AGENTS.md`는 전체 공통 규칙만, 깊은 폴더는 *그 폴더 한정의* 좁은 규칙만.
2. closest-precedence: 가까운 규칙이 먼 규칙을 덮는다.
3. 같은 작업을 두 도구에 시켜 계획이 비슷하게 나오는지 *교차 검증* — 차이가 크면 `AGENTS.md`를 다듬어야 한다는 신호.

## 자주 하는 실수

| ❌ 이렇게 쓰지 말기 | ✅ 이렇게 바꾸기 |
|---|---|
| Claude Code가 `AGENTS.md`를 읽을 거라 가정 | `CLAUDE.md`에 `@AGENTS.md` import 한 줄 |
| `AGENTS.md`에 도구 전용 팁 섞기 | 공통 규칙 → `AGENTS.md`, Claude Code 전용 → `CLAUDE.md` |
| 깊은 폴더 `AGENTS.md`에 루트 규칙 반복 | 깊은 폴더는 *그 폴더 한정* 규칙만 |
| `AGENTS.md`가 32KiB 초과 | 분할 또는 핵심만 남기기 (Codex가 무시할 수 있음) |

## 이번 주에 해볼 것

- [ ] 현재 저장소에 `AGENTS.md`가 없으면 *공통 규칙만으로* 초안 만들기 (빌드/테스트/스타일/금지)
- [ ] Claude Code도 함께 쓴다면 `CLAUDE.md`에 `@AGENTS.md` 한 줄 추가
- [ ] 같은 작업을 Claude Code와 Codex에 시켜 *계획이 얼마나 비슷한지* 비교 → 차이가 나면 `AGENTS.md` 보완

## 더 알아보기

- 공식 (표준): [agents.md](https://agents.md/)
- 공식 (Codex): [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- 공식 (Claude Code의 AGENTS.md 처리): [Claude Code Memory](https://code.claude.com/docs/en/memory)
- 1차 출처 모음: [research/02-03-agents-md-evidence.md](../research/02-03-agents-md-evidence.md)
- 용어집: [glossary.md](./glossary.md) — *AGENTS.md, AGENTS.override.md, closest-precedence* 참고
