1. 터미널이 무섭지 않게: 폴더 이동과 파일 다루기

> 내가 원래 PC 에서 하던 작업이 CLI(Command Line Interface) 로 바뀔 수 없을까?

2. Git이 꼭 필요한 이유: 저장, 되돌리기, 브랜치 감각 키우기

> "변경사항"에 대해 관리하는 시스템
> Q: 변경사항을 언제 저장하는게 좋을까요? (Commit)
 >> 뭔가 변했을 때 => Ticket(Task 단위) = 더 쪼개서 아주 작은 작업 단위 - 완성했을 때 저장
> 리눅스 Kernel - 리누스 토발즈
> **역사** = Context => 숨겨진 지식, 암묵지

3. 오늘 바로 쓰는 Git 기본 루틴: clone → branch → commit → push

Conflict(충돌) - '해결' = **AI Coding Agent**랑 같이 해결

내 컴퓨터: main -> branch -> feature-branch(기능) 
                             -> commit 1
                             -> commit 2
                             -> commit 3

 --- 원격 저장소
     Github - Workflow 셋팅 
            - Continuous Integration(CI - AI 도입)
                             -> "main 으로 merge" 요청 = Pull Request = PR
                                - 충돌 검사(정적 검사) 
                                - AI 가 리뷰 
                                  (Ticket = 어떤 기능을 어떤 식으로 구현해주세요.)
                                  -> 그 방향으로 잘 개발했나?
                                  -> 코드의 간결성, 안정성, 정확성 
                                  -> 그래서 실행됌?
                                    >> 테스트 코드가 있고, 테스트의 엣지케이스(예외) 확인
                                  -> 승인 / 거절 
                              -> PR 승인(머지)

--- 내 컴퓨터로 main 브랜치를 "pull"(땡겨와야함) 해옴
