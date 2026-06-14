# Session 3-1 - 하네스가 모델보다 중요한 이유

## 핵심 한 줄

좋은 모델보다 중요한 것은 모델이 `해야 할 일, 금지할 일, 검증 방법` 그리고 대화 세션의 주요 내용 등을 참조하기 좋도록 만들며 "출력 결과물이 흔들리지 않게 고정"하는 환경 셋팅입니다.

하네스 실패를 모델의 실패와 구분해야만 합니다.
아래의 원칙은 하네스를 구성할 때 꼭 검증되어야 합니다.

1. 진실은 한 곳에만 두세요(Single Source of True)
2. 코드/문서 등 책임은 절대로 섞지 않기(SoC/SRP)
3. 지시는 모순되지 않도록(헷갈림 방지)
4. 작업은 완료되거나, 완료되지 않았거나 2가지 상태만을 가지도록
5. 위 4번과 연계해서 재시도 작업으로 이전 작업 내용이 손상 되지 않도록 만들기
6. 추측하기 전에 읽고, 고치기 전에 적어두기(Document & Plan-first)
7. 상태를 공유해야 할 때는 꼭 읽기/수정에 대한 경계를 둘 것

모델은 진화하고, 프레임워크도 매번 바뀝니다.
그리고 하네스는 쉽게 갈아끼울 수 있어야만 합니다!

## Claude Code를 쓴다면

`CLAUDE.md`에는 Claude Code subagent 운영, context hygiene, decision doc 위치를 적습니다.

## Codex를 쓴다면

`AGENTS.md`에는 `scripts/check.sh`, scope boundary, hook의 한계, interactive bridge 정책을 적습니다.

## 추가 자료

- OpenAI Harness engineering: https://openai.com/index/harness-engineering/
- Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md

- https://www.anthropic.com/engineering/building-effective-agents
- https://claude.com/blog/the-advisor-strategy
- https://docs.langchain.com/oss/python/langchain/multi-agent#subagents
- https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture
- https://www.langchain.com/blog/the-anatomy-of-an-agent-harness
- https://docs.langchain.com/oss/python/deepagents/harness
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/engineering/harness-design-long-running-apps
- https://openai.com/ko-KR/index/harness-engineering/
