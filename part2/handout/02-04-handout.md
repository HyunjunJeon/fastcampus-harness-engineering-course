# Session 2-4 한 장 정리 — 나쁜 지시문을 고치는 실전 리팩터링

본문 대본: [../02-04-instruction-refactor.md](../02-04-instruction-refactor.md)
강사용 근거 자료: [../research/02-04-instruction-refactor-evidence.md](../research/02-04-instruction-refactor-evidence.md)

## 핵심 한 줄

> "AI는 **진단자**와 **초안 작성자**다. 최종 결정은 *사람*이 내린다. 한 번에 고치게 하지 말고 — *진단 → 사람이 선택 → AI가 다시 고치기 → 사람이 검증* 루프로 만들어라."

## 도구별로 어떻게 적용할까

### Claude Code를 쓴다면
1. **Plan Mode**: "고치기 전에 계획을 먼저 보여달라"고 요청. 진단자 패턴이 도구화된 형태.
2. **Anthropic Console의 Prompt Improver**: 자동 진단 + 개선안 제안.
3. **AskUserQuestion 패턴**: AI가 모호함을 발견하면 *고치기 전에* 사람에게 묻게 만든다.

### Codex를 쓴다면
1. **GPT-5 Metaprompting**: *"이 프롬프트의 문제점을 진단하고 개선안 3개를 제안해줘. 직접 고치지는 마."*
2. `/compact` 전에 진단 받기 — 압축 후엔 원본을 못 본다.

### 공통 — Context Engineering 원칙 (가장 중요)
1. **LLM-as-Judge에는 self-enhancement bias**가 있다 — 자기가 쓴 결과를 자기가 채점하면 후하게 매긴다 (arXiv:2306.05685).
2. **Self-Refine은 외부 신호 없으면 효과가 제한적**이다 — *"LLMs Cannot Self-Correct Reasoning Yet"* 연구가 결론.
3. 사람이 **Reflexion의 *외부 신호* 역할**을 한다. 사람이 빠지면 AI는 자기 오류를 강화한다.
4. 도구 선택까지 명시하라: `replace`(좁은 수정) vs `write_file`(통째 덮어쓰기) — 지시 안 하면 광범위 덮어쓰기로 이어질 수 있음.

## 자주 하는 실수

| ❌ 이렇게 쓰지 말기 | ✅ 이렇게 바꾸기 |
|---|---|
| "이 프롬프트 고쳐줘" 한 번에 끝 | "먼저 진단해줘. 고치지는 마" → 사람이 선택 → 그 선택대로 고쳐줘 |
| AI가 만든 규칙을 검증 없이 적용 | 새 규칙으로 같은 작업을 *다시* 시키고 결과 비교 |
| 모호함을 그대로 두고 작업 시작 | 모호함 발견 시 AI가 *질문하게* 만들기 |
| AI가 자기 결과를 자평 | 외부 검증(테스트, 사람, 다른 도구)을 거쳐야 |

## 이번 주에 해볼 것

- [ ] 본인의 `CLAUDE.md`/`AGENTS.md`를 AI에게 *진단만* 시키기 (고치지 말고): "모호한 표현 / 충돌 / 오래된 정보 / 분리 가능한 배경 / 유지할 핵심" 5분류
- [ ] 진단 결과 중 본인이 *동의하는 항목만* 고르기
- [ ] 고친 후 같은 작업을 AI에 다시 시켜 결과가 일관되는지 검증

## 더 알아보기

- 공식 (Claude Code): [Plan Mode 관련 페이지](https://code.claude.com/docs/en/best-practices) / [Prompt Improver](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompt-improver)
- 공식 (Codex): [OpenAI GPT-5 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) (Metaprompting 섹션)
- 학술: [Self-Refine](https://arxiv.org/abs/2303.17651) / [LLMs Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) / [LLM-as-Judge](https://arxiv.org/abs/2306.05685)
- 1차 출처 모음: [research/02-04-instruction-refactor-evidence.md](../research/02-04-instruction-refactor-evidence.md)
- 용어집: [glossary.md](./glossary.md) — *Self-Refine, LLM-as-Judge, Plan Mode, Reflexion* 참고
