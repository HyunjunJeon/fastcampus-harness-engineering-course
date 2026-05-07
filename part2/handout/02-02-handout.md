# Session 2-2 한 장 정리 — CLAUDE.md: 전역, 프로젝트, 하위 폴더 규칙

본문 대본: [../02-02-claude-md.md](../02-02-claude-md.md)
강사용 근거 자료: [../research/02-02-claude-md-evidence.md](../research/02-02-claude-md-evidence.md)

## 핵심 한 줄

> "`CLAUDE.md`는 *반복 지시*를 줄이는 곳이지, *모든 컨텍스트*를 담는 곳이 아니다. 비대해진 `CLAUDE.md`는 **무시당한다.**"

Anthropic 공식 문서 인용: *"Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"*

## 도구별로 어떻게 적용할까

### Claude Code를 쓴다면 (이 세션의 주력)
1. **계층을 알자**: 전역(`~/.claude/CLAUDE.md`) → 프로젝트(`./CLAUDE.md`) → 하위 폴더(`./subdir/CLAUDE.md`). 깊을수록 더 좁고 구체적인 규칙.
2. **분량 가이드**: 200줄 또는 25KB 이내. 한 줄마다 *"이걸 빼면 Claude가 실수할까?"* 라고 묻고, 아니면 지운다.
3. **충돌 방지**: 모노레포처럼 여러 `CLAUDE.md`가 충돌할 수 있는 환경에서는 `claudeMdExcludes` 설정으로 격리.
4. **검증 가능한 구체성**:
   - ❌ "코드 정리하기" → ✅ "2칸 들여쓰기"
   - ❌ "테스트 잘하기" → ✅ "커밋 전에 `npm test` 실행"
   - ❌ "파일 정리" → ✅ "API 핸들러는 `src/api/handlers/` 아래"

### Codex를 쓴다면
1. **Codex는 `CLAUDE.md`를 읽지 않는다**. 대신 다음 세션의 `AGENTS.md`를 사용.
2. 단, *작성 원칙(짧고, 구체적이고, 검증 가능하게)* 은 그대로 적용된다.

### 공통 — Context Engineering 원칙
1. 충돌하는 지시는 모델이 *임의로* 선택한다 → 충돌 자체를 만들지 마라.
2. system prompt 길이가 늘면 instruction adherence가 떨어진다는 연구가 있다 (Same Task More Tokens, OpenAI Instruction Hierarchy).
3. CLAUDE.md/AGENTS.md는 *영속 가드레일*이다. 자연어 컨텍스트(=대화)에만 있는 규칙은 휘발된다 — 다음 모호한 지시 한 줄로 무력화될 수 있음.

## 자주 하는 실수

| ❌ 이렇게 쓰지 말기 | ✅ 이렇게 바꾸기 |
|---|---|
| 200줄 넘는 `CLAUDE.md` | 핵심만 남기고 *배경 설명*은 별도 문서로 분리 |
| "항상 깔끔하게 작성" | "함수 1개당 50줄 이내" 같이 검증 가능한 기준 |
| 오래된 명령 그대로 둠 | 변경할 때마다 `CLAUDE.md`도 함께 갱신 |
| 비밀값/토큰을 적음 | `.env`, secret manager로 분리 |
| 충돌하는 두 줄 모두 유지 | 충돌하는 항목은 한쪽만 남기거나 조건부로 분기 |

## 이번 주에 해볼 것

- [ ] 현재 프로젝트의 `CLAUDE.md`를 한 줄씩 읽으며 *"이 줄을 빼면 Claude가 실수할까?"* 표시하고 빼도 되는 줄 삭제
- [ ] 자주 정정하는 내용(지난 세션에 또 입력한 지시) 1개를 `CLAUDE.md`에 옮기기
- [ ] 모노레포라면 하위 폴더 `CLAUDE.md`가 루트와 충돌하지 않는지 확인

## 더 알아보기

- 공식 (Claude Code): [Memory — How Claude remembers your project](https://code.claude.com/docs/en/memory) / [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- 1차 출처 모음: [research/02-02-claude-md-evidence.md](../research/02-02-claude-md-evidence.md)
- 다음 세션: [02-03 AGENTS.md](../02-03-agents-md.md) — Codex와 공통 사용
- 용어집: [glossary.md](./glossary.md) — *CLAUDE.md, claudeMdExcludes, 검증 가능 지시문* 참고
