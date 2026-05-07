# Session 3-2 한 장 정리 — /compact, resume, memory를 언제 어떻게 쓸까

본문 대본: [../03-02-compact-resume-memory.md](../03-02-compact-resume-memory.md)
강사용 근거 자료: [../research/03-02-compact-resume-memory-evidence.md](../research/03-02-compact-resume-memory-evidence.md)

## 핵심 한 줄

> "`/compact`, `resume`, `memory`는 **손실 압축**이지 만능이 아니다. **중요한 결정은 기능에 맡기지 말고 *문서*로 남겨라.**"

Anthropic 공식 문서가 글자 그대로 인정: *"It replaces the verbatim conversation: full tool outputs and intermediate reasoning are **gone**."* / *"detailed instructions from early in the conversation **may be lost**."*

## 도구별로 어떻게 적용할까

### Claude Code를 쓴다면
| 명령 | 무엇을 하나 | 한계 / 주의 |
|---|---|---|
| `/compact` | 현재 대화를 요약해서 이어감 | tool outputs · 중간 추론 *사라짐* |
| `/clear` | 새 대화 시작 | **Codex의 `/clear`와 의미가 다르다!** |
| `/resume` | 이전 대화 다시 열기 | 모든 맥락이 완벽 복원되지 *않는다* |
| `/memory` | 메모리 관리 | 200줄 / 25KB cap |
| `/fork` | 세션 분기 | `CLAUDE_CODE_FORK_SUBAGENT` 환경변수에 따라 의미 달라짐 |

> **버전 변동성**: 위 명령은 *도구 버전마다 이름·동작이 다를 수 있다.* 촬영/실습 당일 `claude --version` + `/help`로 재확인.

### Codex를 쓴다면
| 명령 | 무엇을 하나 | 한계 / 주의 |
|---|---|---|
| `codex resume` | 세션 재개 | 모든 맥락 복원 X |
| `/compact` (Codex) | 압축 | Claude Code와 세부 동작 다를 수 있음 |
| `/clear` (Codex) | **터미널 화면만 정리** (대화는 유지) | Claude Code와 정반대! |
| `AGENTS.md` | 영속 규칙 | 32KiB cap |

### 공통 — Context Engineering 원칙
1. **compact = 요약 = 손실**. *무엇이 사라졌는지* 모른다는 게 핵심 위험.
2. *결정은 영속화*: 핸드오프 노트, `CLAUDE.md`/`AGENTS.md`, 별도 문서로 박아둔다.
3. Anthropic 공식 FAQ가 직접 권하는 문구: *"Add conversation-only instructions to CLAUDE.md to make them persist."*

## 자주 하는 실수

| ❌ 이렇게 하지 말기 | ✅ 이렇게 바꾸기 |
|---|---|
| `/compact` 후 결정이 살아있을 거라 가정 | `/compact` *전에* 결정을 문서로 옮기기 |
| `/clear`가 두 도구에서 같다고 생각 | Claude Code = 새 대화, Codex = 터미널만. 외워두기 |
| `memory` 기능에 핵심 결정을 의존 | `memory`는 보조, 문서가 본체 |
| 도구 명령을 1년 전 정보로 인용 | 촬영/실습 당일 `/help`로 재확인 |

## 이번 주에 해볼 것

- [ ] 본인 도구의 `/help` 또는 `--help` 출력해서 *현재 사용 가능한 명령*을 확인 (이 자료와 차이 표시)
- [ ] `/compact` *전에* 핵심 결정을 핸드오프 노트나 `CLAUDE.md`에 옮기는 습관 들이기
- [ ] Claude Code와 Codex 둘 다 쓴다면 `/clear` 의미 차이 외워두기

## 더 알아보기

- 공식 (Claude Code): [Memory](https://code.claude.com/docs/en/memory) / [Slash Commands](https://code.claude.com/docs/en/commands) / [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)
- 공식 (Codex): [Codex Slash Commands](https://developers.openai.com/codex/cli/slash-commands) / [Codex Features](https://developers.openai.com/codex/cli/features)
- 1차 출처 모음: [research/03-02-compact-resume-memory-evidence.md](../research/03-02-compact-resume-memory-evidence.md)
- 다음 세션: [03-03 컨텍스트-문서 분리](../03-03-context-doc-separation.md)
- 용어집: [glossary.md](./glossary.md) — *손실 압축, /compact, /clear (의미 차이), /resume* 참고
