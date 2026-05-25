# Session 4-1 - AI가 코드를 바꾸면 문서도 같이 바뀌게 만들기

> 코드가 바뀌었는데 문서가 그대로면 어떤 문제가 발생할까요?

1. AI Agent 가 읽는 문서
> 코드의 위치, 주요 내용, 주요 맥락
> 코드 폴더 내에 AGENTS.md(CLAUDE.md) - 코드 파일 내에서 Docstring 작성
> 커밋 단위로 문서를 업데이트 하는게 좋습니다.
> Stop 훅
 1) 코드 Verify 
 (수정)
 2) 커밋
 3) 문서 업데이트
 4) 커밋 후 문서 Verify
 진짜 종료.

2. 사람이 보는 문서
> 중요한 변화가 있을 때
> 매번 PR(Github)을 머지한뒤에 문서를 업데이트를 진행하도록
> Github Actions(외부) / Claude Code 및 Codex 내부적으로 한다면 스킬로 만들어둔 것을 실행

- 코드 변경 뒤 문서 영향도를 판단하는 질문을 만듭니다.
- README, 사용법, 예시 명령, 스크린샷을 확인 목록에 넣습니다.
- 문서 수정이 필요 없다는 판단에도 이유를 남깁니다.

## 진행 흐름

1. 개발 관련 문서를 "AI Agent 와 사용자가 보는 길 안내판"으로 소개합니다.
2. 코드 변경이 사용자에게 보이는 변화를 만들 수 있음을 설명합니다.
3. AI에게 문서 수정 전에 영향도 판단표만 만들게 합니다.
4. README, 사용법, 예시 명령, 스크린샷을 함께 확인합니다.
5. 수정 필요, 수정 불필요, 추가 확인 필요를 구분해 마무리합니다. 
> "문서가 빠졌으면 끝나지 못한다"는 규칙을 시스템으로 강제할 수 있는지 => 즉, 훅을 어떻게 작성해야할지?

## Claude Code를 쓴다면

Claude Code에는 코드 변경 후 "문서 영향도 판단표만 먼저 만들어 달라"고 요청합니다. 
바로 문서를 고치게 하기보다, 어떤 문서가 왜 바뀌어야 하는지 먼저 확인하면 비개발자도 검토하기 쉽습니다.

문서 수정이 필요하다면 수정 전후 요약과 사람이 확인할 화면 또는 명령을 함께 요구합니다.

## Codex를 쓴다면

Codex에서도 마찬가지로 코드 변경과 문서 변경을 훅으로 묶을 수 있습니다. 
Codex가 변경한 파일 목록을 바탕으로 각종 문서를 업데이트하도록 합니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 코드가 통과하면 문서도 괜찮다고 보기 | 사용자에게 보이는 변화가 있는지 확인 |
| 문서 수정 필요 없음만 적기 | 왜 필요 없는지도 기록 |
| README만 확인 | 예시 명령, 설정 키, 스크린샷도 확인 |
| AI가 문서를 고친 뒤 검토 생략 | 변경 이유와 확인 기준을 다시 받기 |

## Reference

- 공식 (Codex): [Hooks](https://developers.openai.com/codex/hooks)
- 공식 (Claude Code): [Hooks](https://code.claude.com/docs/en/hooks)

## 실습

실습 레포 위치: `part4/lab/workflows/doc-sync/SKILL.md`, `part4/lab/scripts/docs_impact_check.py`, `part4/lab/docs/`

"문서가 빠지면 끝나지 못한다"를 두 단계로 강제합니다. 작업 중에는 판단표를 먼저 만들고, 종료 전에는 그 판단표가 비어 있지 않은지 검증합니다.

```python
# scripts/docs_impact_check.py (개념 발췌)
CODE_PREFIXES = ("app/", "tests/", "scripts/")
DOC_PREFIXES = ("docs/", "README.md")
REPORT_PATH = ".agent/reports/docs-impact.md"

# --soft: 코드 변경 파일 목록을 바탕으로 판단표 템플릿을 생성하고 통과
# --require-report: 판단표의 필수 항목이 비어 있으면 실패
```

훅 조합은 두 단계로 둡니다.

- `PostToolUse: Edit|Write|MultiEdit` 또는 `apply_patch|Edit|Write` → `docs_impact_check.py --soft` 실행 (작업 중 판단표 생성)
- `Stop` → `stop_verify_hook.py`가 `agent_verify.sh`를 호출하고, 그 안에서 `docs_impact_check.py --require-report` 실행 (작업 종료 전 검증 루프)

판단표는 `.agent/reports/docs-impact.md`에 만들어집니다. 여기에는 다음 항목이 들어갑니다.

| 확인 항목 | 봐야 할 것 |
|---|---|
| README.md | 사용법, 설치, 실행 명령 변화 |
| docs/ | 아키텍처, 팀 정책, API 계약 변화 |
| 예시 명령 | CLI, 테스트, 훅 실행 명령 변화 |
| 설정 파일 | `.claude`, `.codex`, GitHub 설정 변화 |
| API 계약 | 입출력, 상태 코드, 데이터 구조 변화 |
| 스크린샷 | 화면이나 UI 설명 변화 |

중요한 점은 `--soft`가 문서를 자동으로 고치지 않는다는 것입니다. 먼저 판단표만 만들고, 사람이 "문서 수정 필요 여부", "수정 불필요 사유", "수정 전후 요약", "사람 확인 방법"을 확인합니다. 마지막 `--require-report` 검증은 판단표가 없거나 필수 항목이 `TODO`로 남아 있으면 실패시켜 Agent가 그냥 끝나지 못하게 합니다.

실습 확인 명령은 다음과 같습니다.

```bash
cd part4/lab
python scripts/docs_impact_check.py --soft
python scripts/docs_impact_check.py --require-report
bash scripts/agent_verify.sh
```
