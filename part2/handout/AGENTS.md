# part2/handout — 수강생용 학습 보조 작업 규칙

## 목적

이 폴더는 수강생이 *강의 후 다시 펼쳐보는* 한 장 정리(세션별)와 용어집이다. 루트 `AGENTS.md`의 모든 규칙이 그대로 적용되며, 이 파일은 *충돌 시 우선*하는 폴더 한정 규칙을 추가한다.

## 작업 규칙 (이 폴더 한정)

- **분량**: 한 장 정리는 ~3.5KB / ~50줄 (A4 한 장). 강제로 채우지 않음.
- **3-thread 구조 의무**: 각 한 장 정리는 다음 3개 섹션을 명확히 분리한다.
  1. *Claude Code를 쓴다면*
  2. *Codex를 쓴다면*
  3. *공통 — Context Engineering 원칙*
- **Action-oriented 톤**: "이번 주에 해볼 것" 체크리스트 + ❌→✅ 표 포함.
- **친근한 존댓말**, 이모지 0개.
- 학술 용어가 등장하면 본문에는 *짧은 용례*만 두고 정의는 [`glossary.md`](./glossary.md)로 redirect.
- 1차 출처 인용은 *짧게* 두고 깊은 인용은 [`../research/0X-YY-*-evidence.md`](../research/)로 redirect.
- 본문 대본 footer **3종 링크 정합성** 유지: `research/...-evidence.md`, `handout/...-handout.md`, `handout/glossary.md`.

## 한 장 정리 표준 골격

```markdown
# Session X-Y 한 장 정리 — [세션 제목 한 줄]

본문 대본: [../0X-YY-*.md](../0X-YY-*.md)
강사용 근거 자료: [../research/0X-YY-*-evidence.md](../research/0X-YY-*-evidence.md)

## 핵심 한 줄
> "..."

## 도구별로 어떻게 적용할까
### Claude Code를 쓴다면
### Codex를 쓴다면
### 공통 — Context Engineering 원칙 (도구 무관)

## 자주 하는 실수
| ❌ | ✅ |

## 이번 주에 해볼 것
- [ ] ...

## 더 알아보기
- 공식 (Claude Code): ...
- 공식 (Codex): ...
- 1차 출처 모음: research/...
- 용어집: glossary.md
```

## 용어집 정합성

새 용어가 한 장 정리에 등장하면 [`glossary.md`](./glossary.md)에 동기 추가한다. 5그룹 분류 유지:

- ① Context Engineering 핵심
- ② Claude Code 전용
- ③ Codex 전용
- ④ **두 도구에 모두 있지만 의미가 다름** (혼동 주의 — 가장 자주 사고 발생)
- ⑤ 학술 용어

특히 ④ 그룹(예: `/clear`)은 학습자가 *가장 많이 사고를 내는 지점* — 새 용어 발견 시 ④에 들어갈지 *항상* 우선 검토.

## 톤 가이드

- 카메라 인용용 한국어 한 줄: 60자 이내
- "이번 주에 해볼 것"은 *3개 이내* (학습자가 실제로 시도할 분량)
- "❌→✅ 표"는 *4행 이내* (한 페이지에서 한눈에 보이도록)
