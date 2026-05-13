# 01-02 Claude Code `settings.json` 강도 3단계

[../../plan.md](../../plan.md) 01-02 진행 흐름의 4단계(짧은 실습)에서 사용. 권한(의사결정) 축과 샌드박스(실행 격리) 축을 분리해 표시한 `settings.json` 초안 3개.

## 강도 비교

| 파일 | 사용 시점 | 권한 |
| --- | --- | --- |
| [settings-strict.json](settings-strict.json) | 사내 코드·운영 데이터 근처에서 작업할 때 | 읽기만 자동, 쓰기는 모두 ask, 파괴·외부 호출 deny |
| [settings-medium.json](settings-medium.json) | 일반 업무 코드 — 매트릭스 "사용자 확인" 비중 균형 | 안전 읽기·쓰기·검증 자동, 외부 영향 명령은 ask, 운영 데이터 deny |
| [settings-loose.json](settings-loose.json) | 개인 실습·오픈소스 탐색, 격리된 샌드박스 안에서만 | 대부분 자동, deny는 최소(`rm -rf /` 류만) |

## 시연 흐름

01-02 진행 흐름 4단계에서:

1. 수강생에게 "본인 매트릭스(01-01)를 보고 어느 강도가 맞나" 묻는다
2. 강사가 medium을 띄우고 "여기서 한 칸을 옮기면 strict가 된다" 시연
3. 수강생이 본인 프로젝트에 medium을 복사한 뒤 매트릭스에 따라 조정
