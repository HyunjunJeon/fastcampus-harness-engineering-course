# Session 3-1 한 장 정리 — 긴 대화가 망가지는 이유와 새 세션 타이밍

본문 대본: [../03-01-context-rot-new-session.md](../03-01-context-rot-new-session.md)
강사용 근거 자료: [../research/03-01-context-rot-evidence.md](../research/03-01-context-rot-evidence.md)

## 핵심 한 줄

> "긴 대화가 망가지는 건 **도구의 결함이 아니라 컨텍스트 관리 실패다.** 모델은 길어질수록 *중간을 잊고*, 오래된 전제를 반복하고, 새 결정을 놓친다."

연구가 말하는 결론: *"Claude·GPT·Gemini·Qwen 가릴 것 없이 길이가 길어지면 같은 작업의 정확도가 떨어진다."* (Chroma 2025, 18개 모델 평가)

## 도구별로 어떻게 적용할까

### Claude Code를 쓴다면
1. **새 세션 신호 5가지** 중 2개 이상이면 새 세션으로 가라:
   - 작업 목표가 바뀌었다
   - 중요한 결정이 *대화 안에만* 있다
   - AI가 오래된 전제를 반복한다
   - 수정 범위가 커져 검증 기준을 다시 세워야 한다
   - 사람이 최신 결정을 *설명하기 어려워졌다*
2. `/compact`는 보조 도구일 뿐 (다음 세션 3-2에서 자세히).

### Codex를 쓴다면
1. `codex resume`로 재개 가능. 단, *모든 맥락이 완벽 복원되지는 않는다.*
2. Codex의 `/compact`도 동일 한계.

### 공통 — Context Engineering 원칙 (이 세션의 핵심)
1. **Lost in the Middle** (Stanford 2023): 모델은 컨텍스트 처음·끝은 잘 보지만 *가운데는 통째로 흘려*버린다.
2. **Context Rot** (Chroma 2025): 18개 주요 모델 모두 길이 증가 시 정확도 저하 → *어느 한 도구의 결함이 아님.*
3. **Needle in a Haystack** 평가: 합성 평가지만 실제 한계를 시사한다.
4. *대화를 짧게 유지하는 것* 자체가 컨텍스트 엔지니어링.

## 자주 하는 실수

| ❌ 이렇게 하지 말기 | ✅ 이렇게 바꾸기 |
|---|---|
| 같은 세션을 끝없이 이어가기 | 새 세션 신호 2개 이상 → 핸드오프 후 새 세션 |
| 핸드오프 노트 없이 새 세션 | 6개 항목(목표/완료/남은/결정/제약/검증/첫 프롬프트) 적기 |
| "AI가 잊었네" 도구 탓 | *컨텍스트 관리 실패*로 인식 |
| OS/shell/repo 위치 빠뜨림 | 핸드오프에 `Windows 11 / WSL2 Ubuntu / repo: ... / shell: zsh` 명시 |

## 이번 주에 해볼 것

- [ ] 지금 진행 중인 가장 긴 대화에 **새 세션 신호 5개** 중 몇 개가 켜졌는지 점검
- [ ] 핸드오프 노트 6개 항목 템플릿을 메모해두고 한 번 작성해보기
- [ ] *"모델은 가운데를 흘린다"* 한 줄 외워두기 — 다음번 긴 대화에서 *왜* 새 세션이 필요한지 본인에게 설득력

## 더 알아보기

- 공식 (Claude Code): [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works) / [Context Window](https://code.claude.com/docs/en/context-window)
- 공식 (Codex): [Codex CLI Reference](https://developers.openai.com/codex/cli/reference)
- 학술/연구: [Lost in the Middle](https://arxiv.org/abs/2307.03172) / [Context Rot (Chroma)](https://research.trychroma.com/context-rot) / [Needle in a Haystack](https://github.com/gkamradt/LLMTest_NeedleInAHaystack)
- 1차 출처 모음: [research/03-01-context-rot-evidence.md](../research/03-01-context-rot-evidence.md)
- 다음 세션: [03-02 /compact, resume, memory](../03-02-compact-resume-memory.md)
- 용어집: [glossary.md](./glossary.md) — *컨텍스트 로트, Lost in the Middle, 핸드오프 노트* 참고
