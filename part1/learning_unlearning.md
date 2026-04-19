# 언러닝 개념과 AI Agent 및 Harness 교육용 선행 수업 클립 설계 보고서

## Executive Summary

이 보고서에서 다루는 언러닝은 “기존 지식을 완전히 지우는 것”이라기보다, 새 판단을 방해하는 낡은 가정·루틴·해석틀의 우선권을 낮추고 새로운 근거와 행동 규칙에 맞게 재구성하는 과정에 가깝다. 조직학습 연구에서는 이를 환경 변화에 적응하기 위한 조건으로 다뤄 왔고, 교육학에서는 개념변화·성찰·성인학습과 긴밀하게 연결된다. 인지과학 차원에서도 오래된 기억이 새 학습을 방해하는 선행간섭, 회상된 기억이 수정 가능한 상태로 다시 열리는 재응고화, 변화에 맞춰 사고와 행동을 전환하는 인지유연성이 핵심 근거가 된다. 다만 이는 사람과 조직의 학습 언러닝이며, 학습데이터의 영향을 모델에서 제거하는 machine unlearning과는 다른 범주의 개념이다. citeturn32view0turn33search3turn25view0turn27view1turn29view0turn35view0

entity["organization","OpenAI","san francisco, ca, us"]와 entity["organization","Anthropic","san francisco, ca, us"]의 공식 가이드는 에이전트를 단순 챗봇이 아니라 도구를 사용해 워크플로를 실행·조정하는 시스템으로 정의하며, 복잡성을 기본값으로 두지 말고 단일 에이전트·명확한 도구·평가·인간 개입에서 시작하라고 권한다. 한편 entity["organization","NIST","gaithersburg, md, us"]와 entity["organization","OWASP","global nonprofit"]는 automation bias, confabulation, prompt injection, system prompt leak, harmful bias를 핵심 위험으로 제시한다. entity["company","Harness","san francisco, ca, us"]의 공식 문서는 agent가 pipeline-native로 권한·비밀·거버넌스를 상속받고, 실제 플랫폼 상태를 참조하며, 최소권한·정책 게이트·가시성을 전제로 운용되어야 함을 강조한다. 따라서 AI Agent·Harness 교육의 앞부분에서는 “기능 설명”보다 먼저 “낡은 확신 교정”이 필요하다. citeturn12view1turn12view2turn39view0turn39view2turn9view2turn9view5turn11view4turn41view2

따라서 권장되는 5~7분 수업 클립은 지식을 많이 넣는 영상이 아니라, 이후 본 교육의 해석틀을 맞추는 “마인드셋 리셋 장치”여야 한다. 목표는 세 가지다. 첫째, 학습자가 자신이 버려야 할 가정을 즉시 식별하게 한다. 둘째, 불편함과 인지갈등을 실패가 아니라 전문성 업그레이드의 신호로 재해석하게 한다. 셋째, 이후 본 강의 전체에서 반복 사용할 행동 규칙—최신 상태 조회, 권한 최소화, 평가 선행, 고위험 승인—을 미리 심어 둔다. microlearning은 보조 학습장치로는 효과적일 수 있지만, 짧은 영상 하나에 너무 많은 내용을 압축하면 피상화 위험이 있으므로 이 클립은 “언러닝 프레임 설치 + 행동 체크리스트 부여”까지만 담당하는 것이 적절하다. citeturn17search12turn16search1turn16search4turn19view2

## 개념 프레임

이 보고서의 언러닝은 “사람과 팀이 낡은 가정의 지배력을 낮추는 교육적·조직적 언러닝”이다. 즉, AI 모델의 파라미터에서 특정 데이터 영향을 제거하는 machine unlearning과는 구분해야 한다. 교육 현장에서는 이 둘을 분리해서 설명해야 초반 오해를 줄일 수 있다. citeturn35view0turn32view0

| 설계 변수 | 현재 값 |
|---|---|
| 적용 위치 | AI Agent 및 Harness 본교육의 맨 앞 5~7분 |
| 권장 길이 | 6분 10초 권장안 |
| 학습 목적 | 마인드셋 리셋 + 행동 규칙 선제 정렬 |
| 교육 대상 | AI 엔지니어, 제품기획자, 운영/SRE, 보안/컴플라이언스, 교육담당/리더 |
| 운영 형식 | 미지정 |
| 학습자 규모 | 미지정 |
| 실습 계정/샌드박스 제공 여부 | 미지정 |
| LMS/사내 포털 탑재 방식 | 미지정 |
| 나레이션 톤·브랜딩 템플릿 | 미지정 |
| 운영 KPI 연동 방식 | 미지정 |

| 구분 | 핵심 정리 | 교육 설계 해석 | 우선 출처 |
|---|---|---|---|
| 정의 | 언러닝은 오래된 지식·루틴·가정이 더 이상 유효하지 않을 때, 그것을 놓아주고 새 정보·행동을 수용할 수 있도록 재구성하는 과정이다. 단순한 망각보다 “기존 틀의 우선순위 조정”에 가깝다. | 수업에서는 “버려라”보다 “무엇의 지배력을 낮출 것인가”로 설명하는 편이 저항이 적다. | Human Relations의 organizational unlearning 정의, Hedberg의 원전 계보, Becker 계열 정의 정리 citeturn32view0turn42view0turn34search18 |
| 심리학적 근거 | 오래된 기억·습관은 새 학습을 방해하는 선행간섭을 만들고, 회상된 기억은 재응고화 과정에서 수정될 수 있다. | 기존 소프트웨어 상식이 새 agent 이해를 방해하는 이유를 “무지”가 아니라 “간섭”으로 설명해야 한다. | 한국어 논문인 김문수·이혜진(재응고화), PI review citeturn25view0turn27view1 |
| 인지과학적 근거 | 인지유연성은 환경 변화에 맞춰 사고와 행동을 전환하는 능력이며, 반성적 사고·메타학습과 연결된다. 국내 과학교육 연구는 인지갈등의 강도가 태도·성격 같은 정의적 요인과도 관련됨을 보여준다. | 도입 클립은 “정답 제시”보다 “인지갈등을 안전하게 열고, 성찰로 닫는 구조”가 적합하다. | entity["organization","OECD","paris, france"] 인지유연성 문서, 국내 인지갈등 연구 citeturn29view0turn23view1 |
| 학습이론적 위치 | 개념변화 이론에서 학습은 기존 개념으로 새 현상을 설명하는 동화와, 개념을 재조직하는 조절로 나뉜다. 조절이 일어나려면 기존 개념에 대한 불만족과 새 개념의 이해가능성·개연성·생산성이 필요하다. | 언러닝 클립은 “왜 기존 가정으로는 설명이 안 되는가”를 먼저 보여줘야 한다. | entity["people","George J. Posner","science education scholar"]의 conceptual change 원전, 국내 개념변화/인지갈등 연구, entity["organization","한국교육과정평가원","jincheon, chungbuk, kr"] 논문 citeturn43view0turn45view0turn45view1turn45view2turn45view3turn23view2turn23view3 |
| 성인·조직학습상 위치 | double-loop learning은 행동 자체보다 행동을 움직이는 governing variables를 재검토하는 학습이며, transformative learning은 frame of reference를 비판적으로 성찰해 더 포괄적인 관점으로 이동하는 학습이다. | “툴 사용법”이 아니라 “툴을 해석하는 판단 규칙”을 바꾸는 도입이 필요하다. | entity["people","Chris Argyris","organizational learning scholar"], entity["people","Jack Mezirow","adult learning scholar"] citeturn46view0turn46view1 |
| 깊이 구분 | routine unlearning은 습관 교체에 가깝고, deep unlearning은 기존 이해방식과 가치 전제를 흔드는 급격하고 감정적으로 부담 큰 변화일 수 있다. | 도입부는 deep unlearning의 불편함을 최소화하도록 비난 대신 사례 기반으로 설계해야 한다. | Rushmer & Davies 및 후속 정리 citeturn33search3turn33search15 |
| 개념 구분 | 본 보고서의 언러닝은 사람과 조직의 판단모형 재설계이며, machine unlearning은 훈련 데이터 영향 제거 기술이다. | 첫 15초에 두 개념을 분리해 주지 않으면 AI 실무자일수록 혼동 가능성이 높다. | Stanford machine unlearning review citeturn35view0 |

실무적으로 번역하면, 언러닝은 “틀린 지식을 삭제하라”가 아니라 “낡은 가정이 새 판단을 점유하지 못하게 하라”에 가깝다. 그래서 도입 클립의 핵심 과제는 새로운 기능 목록을 요약하는 것이 아니라, 기존 업무 습관이 어디에서 AI Agent와 Harness 활용을 왜곡하는지 먼저 드러내는 데 있다. citeturn45view0turn46view0turn46view1turn29view0

## 필요성

AI Agent 교육과 Harness 교육에서 언러닝이 필요한 직접적 이유는 학습자가 이미 강한 기존 전문성을 가지고 있기 때문이다. 문제는 그 전문성이 agentic system에서는 종종 간섭원이 된다는 점이다. 공식 가이드들은 반복해서 “단순한 것에서 시작하라”, “외부 가드레일을 두라”, “실제 현재 상태를 조회하라”, “고위험 행동에는 인간 개입을 두라”고 말하지만, 현장 학습자는 오히려 deterministic system 경험 때문에 반대로 해석하는 경우가 많다. citeturn12view1turn12view2turn39view0turn11view4turn41view0turn41view2

| 언러닝 대상인 낡은 가정 | 왜 문제인가 | 대표 위험·편향·구식 지식 시나리오 | 새로 심어야 할 원칙 | 근거 |
|---|---|---|---|---|
| “에이전트는 챗봇의 확장판이다.” | 에이전트는 답변만 생성하는 시스템이 아니라, LLM이 workflow execution과 tool use를 통제하는 실행 시스템이다. 이 차이를 놓치면 아키텍처 기대가 어긋난다. | 교육생이 agent를 단순 Q&A UI로 이해해, 평가·권한·종료조건 설계를 생략한다. | “에이전트 = 답변 시스템”이 아니라 “에이전트 = 도구를 가진 실행 시스템”으로 재정의 | OpenAI·Anthropic 공식 정의 citeturn12view1turn39view0 |
| “처음부터 멀티에이전트가 더 고급이고 더 낫다.” | 공식 가이드는 복잡성이 성능을 보장하지 않으며, 단일 에이전트와 단순 패턴에서 시작하라고 권한다. | 데모는 화려하지만 디버깅·평가·유지보수 비용이 급증한다. | 단일 에이전트 → 검증 → 필요 시 다중화 | OpenAI·Anthropic의 simplicity/evaluation 권고 citeturn12view2turn12view3turn12view4 |
| “프롬프트만 잘 쓰면 통제가 된다.” | 시스템 프롬프트만으로 보안 제어를 맡기는 것은 취약하다. 독립적인 가드레일, 인증·인가, 최소권한이 필요하다. | 외부 문서의 간접 prompt injection으로 승인 우회, 시스템 프롬프트 유출, 원치 않는 도구 실행 | “통제는 프롬프트 밖에서” 구현 | NIST·OWASP·OpenAI guardrails guidance citeturn9view2turn9view5turn11view2 |
| “모델은 최신 정책·운영 상태를 대체로 안다.” | 에이전트는 현재 실행을 위해 필요한 문맥을 data tools로 조회해야 하며, Harness도 실제 플랫폼 상태를 바탕으로 판단해야 함을 강조한다. | 만료된 배포 정책, 바뀐 connector, 폐기된 runbook, 오래된 feature flag 규칙을 그대로 따른다. | “최신성은 기억이 아니라 조회에서 온다” | OpenAI data tools, Harness actual platform state/knowledge graph citeturn13view0turn13view1turn13view3turn13view4 |
| “데모가 되면 운영도 된다.” | 운영 신뢰성은 평가 기준, 사전 테스트, 적응형 red teaming, 실패 임계값, human intervention으로 만든다. | 데모에서는 성공했지만 실제 배포에서 edge case, hijacking, retry 폭주가 발생한다. | baseline eval → pre-deploy test → 운영 중 모니터링 | OpenAI evals·human intervention, NIST evaluation guidance citeturn13view0turn12view2turn14view2turn9view2 |
| “정확도만 높으면 공정하다.” | 공식 프레임워크는 demographic group별 성능과 harmful bias를 별도로 측정하라고 요구한다. | 티켓 triage, 고객 응대, 요약, 추천에서 하위집단 품질 차이가 누적된다. | 정확도와 별개로 fairness 확인 | NIST GenAI Profile fairness/bias 항목 citeturn14view0 |
| “완전자율이 곧 효율이다.” | 고위험·비가역적 행동은 인간 승인과 최소권한이 필요하다. Harness도 least-privilege, OPA gate, scoped tools, HITL을 강조한다. | 승인 없는 배포, 과도한 환불, 민감정보 접근, effectful operation의 무인 실행 | 고위험 액션 = 승인 경계 설정 | OpenAI human intervention, Harness security model, OWASP least privilege guidance citeturn12view2turn11view4turn9view5 |
| “자연어로 말하면 스키마도 알아서 맞다.” | Harness 공식 문서는 prompt specificity, dependency 확인, runtime schema discovery를 강조한다. 추정 기반 생성은 오류와 drift를 키운다. | YAML 필드 추정, 없는 connector 참조, 잘못된 namespace, 누락된 secret로 pipeline 생성 실패 | scope 확인 → dependency 확인 → schema 확인 → 생성 | Harness Effective Prompting, Harness Skills operating model citeturn41view0turn41view2 |
| “AI가 만든 설명은 사람이 만든 설명보다 더 질이 좋다.” | NIST는 over-reliance와 automation bias를 별도 위험군으로 다룬다. | 요약문이나 추천문이 그럴듯해 보여 검증 없이 채택된다. | “그럴듯함”과 “검증됨”을 분리 | NIST automation bias guidance citeturn14view3 |

요약하면, 이 도입 클립의 역할은 “새 도구를 배우기 전 낡은 통제 모델을 내려놓게 만드는 것”이다. Agent 교육에서는 “챗봇 확장판” 오해를 깨고, Harness 교육에서는 “숨은 봇/스크립트 자동화” 오해를 깨야 실제 안전성과 생산성이 함께 올라간다. citeturn39view0turn11view4turn41view0turn41view2

| 교육 대상 | 맞춤 포인트 | 특히 강조할 실패 장면 | 도입 클립에서 꽂히는 메시지 |
|---|---|---|---|
| AI 엔지니어 | schema guessing, tool interface, eval-first, HITL | 없는 resource를 가정한 YAML/툴콜 생성, edge case 미검증 | “모델이 똑똑한 것과 시스템이 신뢰할 수 있는 것은 다르다.” |
| 제품기획자 | task selection, user trust, risk boundaries, fairness | “할 수 있음”을 “맡겨도 됨”으로 오해한 기능 설계 | “좋은 agent 기능은 더 많은 자율성이 아니라 더 나은 통제 설계다.” |
| 운영/SRE 팀 | 현재 상태 조회, 승인 게이트, auditability | 구식 runbook/배포 상태를 근거로 잘못된 판단 | “최신성은 기억이 아니라 운영 데이터에서 온다.” |
| 보안/컴플라이언스 | prompt-only control의 한계, least privilege, independent controls | 간접 prompt injection, prompt leak, credential misuse | “보안 제어는 LLM 밖에 있어야 한다.” |
| 교육담당/리더 | 불편함 관리, 성찰 유도, 짧은 클립의 역할 제한 | 초반 저항이나 냉소로 본강의 몰입 저하 | “언러닝은 무시가 아니라 업그레이드다.” |

대상별 차이는 사례의 언어와 훅의 위치에서 조정하면 된다. 즉, 같은 6분짜리 구조를 유지하되 엔지니어에게는 schema·eval, 기획자에게는 autonomy·trust, 운영팀에게는 current state·approval, 보안팀에게는 least privilege·guardrail을 전면에 배치하면 된다. citeturn12view2turn41view2turn14view3turn19view2

## 클립 설계

짧은 도입 클립은 “완성형 강의”가 아니라 “인지 프레임 설치 장치”로 설계하는 것이 타당하다. 연구 요약들은 microlearning이 보조 학습으로 성과를 높일 수 있음을 시사하지만, short-video format을 독립 완결형으로 과신하면 피상화 위험이 커질 수 있다고 지적한다. 따라서 이 클립은 내용을 많이 넣기보다, 학습자가 본교육 내내 사용할 판단 규칙을 설치하는 데 집중해야 한다. 시청각 구성은 coherence·signaling 중심으로 가고, 화면 문구는 한 장면 하나의 규칙만 남기는 것이 좋다. citeturn17search12turn16search1turn16search4turn16search6

| 영역 | 학습목표 | 관찰 가능한 성공 지표 |
|---|---|---|
| 인지 목표 | 언러닝을 “새 학습을 위해 낡은 가정의 지배력을 낮추는 과정”으로 설명하고, AI Agent와 Harness 교육에서 버려야 할 최소 3개의 낡은 가정을 식별한다. | 사후 문항에서 3개 이상 정확히 진술, 사례에서 잘못된 가정 표시 가능 |
| 정서 목표 | 인지갈등·불편함을 “내가 뒤처졌다”가 아니라 “판단 모델을 업그레이드하는 정상적 과정”으로 재해석한다. | 사후 응답에서 방어적 표현 감소, “불편하지만 필요하다” 유형의 자기서술 증가 |
| 행동 목표 | 실제 업무 적용 전 4단계 점검—현재 상태 조회, 권한 최소화, 평가 기준 정의, 고위험 승인 게이트 설정—를 적용하겠다고 약속한다. | 종료 직후 개인 체크리스트 작성, 1주 후 적용 사례 제출 여부 |

| 시간 | 장면 | 핵심 메시지 | 시청각 자료 제안 | 스크립트 요지 |
|---|---|---|---|---|
| 0:00–0:35 | 실패 훅 | “문제는 AI가 틀린 게 아니라, 우리가 낡은 가정으로 AI를 해석한 것이다.” | 빨간 경고 아이콘 3개: 잘못된 배포, 잘못된 요약, 우회된 승인 | “새 도구는 들어왔는데, 옛 판단법은 그대로였습니다. 그래서 자동화는 빨라졌지만, 판단은 낡은 채로 남았습니다.” |
| 0:35–1:15 | 실패 원인 질문 | “당신이 지금 버려야 할 확신은 무엇인가?” | 화면 중앙 한 문장 질문 + 3개 선택지 투표 | “에이전트는 챗봇일까요, 프롬프트면 충분할까요, 모델은 최신 상태를 알고 있을까요?” |
| 1:15–2:00 | 언러닝 정의 | “언러닝은 삭제가 아니라 우선순위 조정이다.” | 낡은 카드가 뒤로 밀리고 새 카드가 앞으로 오는 애니메이션 | “기존 지식을 부정하는 것이 아니라, 지금은 방해가 되는 가정의 우선권을 낮추는 것입니다.” |
| 2:00–2:45 | 왜 어려운가 | “오래된 규칙은 새 규칙보다 먼저 튀어나온다.” | 선행간섭·재응고화·인지유연성 3단 키워드 | “사람은 무지해서가 아니라, 익숙한 판단이 먼저 떠오르기 때문에 잘못 적용합니다. 그래서 먼저 틀을 열어야 합니다.” |
| 2:45–3:40 | AI Agent 재프레이밍 | “Agent는 답변기가 아니라 도구를 가진 실행 시스템이다.” | agent workflow diagram, instructions-tools-guardrails 층 구조 | “좋은 agent 설계는 더 많은 자율성이 아니라, 더 명확한 도구·종료조건·평가·가드레일에서 시작합니다.” |
| 3:40–4:40 | Harness 재프레이밍 | “자연어는 마법 명령이 아니라, 문맥·스키마·권한이 연결된 요청이다.” | pipeline-native, current platform state, policy gate, auditability 강조 | “Harness에서는 추정이 아니라 확인이 필요합니다. 무엇을 만들지보다, 어떤 문맥과 어떤 권한으로 만들지부터 확인해야 합니다.” |
| 4:40–5:35 | 행동 원칙 제시 | “최신 상태 조회 → 권한 최소화 → 평가 선행 → 고위험 승인” | 네 칸 체크리스트 카드 | “이 네 문장은 오늘 본교육 전체를 해석하는 기준입니다. 이 기준 없이 agent를 배우면 기능만 익히고 운영은 놓칩니다.” |
| 5:35–6:10 | 전환 멘트 | “이제부터 배우는 것은 더 많이 맡기는 법이 아니라, 더 안전하게 맡기는 법이다.” | 본교육 첫 장으로 자연스럽게 전환 | “지금부터의 내용은 기능 설명이 아니라, 맡겨도 되는 구조를 만드는 법입니다.” |

| 시청각 자료용 공식 이미지·다이어그램 | 권장 사용 장면 | 활용 포인트 | 링크 |
|---|---|---|---|
| OpenAI agent workflow diagram | 2:45–3:40 | Agent를 “답변”보다 “구성요소를 가진 실행 시스템”으로 시각화 | citeturn37view1turn9view0 |
| OpenAI guardrails & safety flow diagram | 2:45–3:40 또는 4:40–5:35 | 프롬프트 밖의 가드레일 계층을 설명할 때 적합 | citeturn37view2turn11view2 |
| Harness Agents 보안·거버넌스 개요 | 3:40–4:40 | pipeline-native, RBAC, OPA, scoped tools, auditability 설명 | citeturn11view4 |
| OECD cognitive flexibility PDF | 2:00–2:45 | “왜 언러닝이 필요한가”를 executive function 관점에서 짧게 설명 | citeturn29view0turn30view0 |
| 경기도교육청 생성형 AI 활용교육 가이드 | 4:40–5:35 | 과의존 방지·비판적 사고·사전 안전교육의 국내 공식 사례 | citeturn19view2turn22view5 |
| NIST agent hijacking technical blog | 4:40–5:35 | agent hijacking, adaptive evaluation, 공격면 확대 설명 | citeturn9view2 |

실제 제작 시에는 위 표의 공식 도표를 우선 사용하고, 탐색·아이데이션 단계에서는 아래와 같은 비주얼 레퍼런스를 참고해도 좋다. 다만 최종 수업 자료는 공식 출처의 구조도와 문구를 기준으로 정리하는 편이 신뢰성과 업데이트 관리에 유리하다. citeturn37view1turn37view2turn11view4turn29view0turn19view2

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["AI agent workflow diagram","AI guardrails diagram","DevOps pipeline governance dashboard","cognitive flexibility diagram"],"num_per_query":1}

아래 mermaid 타임라인은 실제 6분 10초 구성안을 한눈에 보여주는 강의 흐름도다.

```mermaid
timeline
    title 언러닝 선행 수업 클립 흐름
    0:00 : 실패 훅
    0:35 : 낡은 가정 질문
    1:15 : 언러닝 정의
    2:00 : 왜 어려운가
    2:45 : AI Agent 재프레이밍
    3:40 : Harness 재프레이밍
    4:40 : 행동 체크리스트
    5:35 : 본교육 전환
```

## 활동과 평가

사전·사후 평가는 “지식 확인”보다 “가정 수정”을 측정해야 한다. 특히 model omniscience, prompt-only control, undue autonomy, complexity bias, schema guessing에 대한 태도 변화를 체크하면 도입 클립의 효과를 빠르게 확인할 수 있다. citeturn14view3turn9view2turn12view2turn41view2

| 단계 | 활동·토론 설계 | 사전·사후 진단 문항 예시 | 평가 포인트 |
|---|---|---|---|
| 사전 진단 | 1분 모바일 투표. 익명 응답 권장. | ① “에이전트는 챗봇보다 조금 더 복잡한 UI일 뿐이다.” ② “프롬프트를 잘 쓰면 외부 가드레일 없이도 충분히 안전하다.” ③ “최신 정책과 운영 상태는 모델의 기본 지식이 대체할 수 있다.” ④ “멀티에이전트는 단일 에이전트보다 대체로 낫다.” ⑤ “AI가 만든 pipeline/YAML은 schema 확인 없이도 바로 적용 가능하다.” | 오개념 분포 파악. 교육 대상별 훅 조정 기준 확보 |
| 짝 토론 | “내가 실제로 가장 자주 믿는 낡은 가정 1개”를 30초씩 공유 | 개방형: “최근 AI 기능을 과신해 검증을 줄인 적이 있는가?” | 자기 고백형 문항이 나오면 정서적 몰입도 상승 |
| 사례 카드 분류 | 4개 카드(최신성, 권한, 평가, 승인)를 old assumption vs new rule로 분류 | 예: “모델이 알아서 현재 상태를 안다” → old assumption / “실행 전 현재 상태를 조회한다” → new rule | 행동 규칙으로 전환되는지 확인 |
| 본교육 연결 토론 | “우리 팀에서 AI Agent/Harness 도입 시 가장 먼저 끊어야 할 습관은?” | 부서별 응답 기록: 엔지니어링/기획/운영/보안 | 부서별 언러닝 포인트 도출 |
| 사후 진단 | 동일 문항 재측정 + 적용 의지 문항 2개 추가 | ① “나는 앞으로 AI 사용 전 현재 상태 조회를 기본값으로 두겠다.” ② “고위험 액션에는 인간 승인 경계를 두겠다.” | 단순 지식보다 태도 전환과 행동 의도 측정 |
| 전이 평가 | 1주 후 5분 follow-up | “지난 1주 내 내가 실제로 바꾼 프롬프트/검증/승인 규칙 1개를 적어라.” | 현업 전이 여부 확인 |

권장 채점 기준은 복잡하지 않아야 한다. 사후에 ①~⑤ 문항에서 역문항 점수가 평균 20% 이상 하락하고, 적용 의지 문항이 4점 이상이며, 1주 후 실제 변경 사례가 1개라도 제출되면 도입 클립의 1차 목적은 달성된 것으로 봐도 된다. 이 클립은 전문가 양성 자체가 아니라, 본교육을 잘 받기 위한 선행 정렬이 목표이기 때문이다. citeturn17search12turn16search1

## 후속 학습 경로

후속 학습은 “국내 공식·국내 학술 → 국제 원전·국제 공식 → 도구 실습·사례” 순으로 가는 것이 가장 안정적이다. 특히 한국어 공식 자료를 먼저 배치하면 윤리·과의존·비판적 사고 메시지를 조직 내 교육 언어로 번역하기 쉽고, 이후 국제 원전과 공식 실무 가이드를 통해 agent 설계와 Harness 운용으로 연결하기 좋다. citeturn19view2turn19view0turn18search6turn12view2turn11view4

**우선순위 기준**  
A = 국내 공식·국내 학술  
B = 국제 원전·국제 공식  
C = 실무 사례·보조 강의

| 경로 단계 | 자료 유형 | 권장 자료 | 우선순위 | 적합 대상 | 링크 |
|---|---|---|---|---|---|
| 기초 윤리·과의존 | 국내 공식 가이드 | entity["organization","경기도교육청","suwon, gyeonggi, kr"] 「생성형 인공지능 활용교육 교사용 가이드라인」 | A | 전 대상 | citeturn19view2 |
| 국가 정책 맥락 | 국내 공식 가이드 | entity["organization","방송통신위원회","sejong, kr"] 「생성형 인공지능 서비스 이용자 보호 가이드라인」 발표 | A | 리더, 교육담당, 컴플라이언스 | citeturn19view0 |
| 윤리 입문 교재 | 국내 공식 가이드북 | entity["organization","한국지능정보사회진흥원","seoul, kr"] 「생성형 AI 윤리 가이드북」 | A | 전 대상 | citeturn18search6turn20search0 |
| 개념변화 이해 | 국내 학술 논문 | 권재술 외 「인지갈등과 개념변화의 필요조건과 충분조건」, 왕경수 「개념학습의 대안적 관점과 교육적 함의」 | A | 교육담당, 리더, 실무 멘토 | citeturn23view2turn23view3 |
| 인지과학 이해 | 국내 학술 논문 | 김문수·이혜진 「기억 응고화 또는 재응고화를 이용한…」 | A | 교육담당, HRD, 팀리드 | citeturn25view0 |
| 개념변화 원전 | 국제 원전 논문 | Posner et al. 「Accommodation of a Scientific Conception」 | B | 교육설계자, 기술리드 | citeturn43view0turn45view0turn45view1turn45view2turn45view3 |
| 성찰·조직학습 원전 | 국제 원전 논문/장 | Argyris 「Double Loop Learning in Organizations」, Mezirow 「Transformative Learning: Theory to Practice」 | B | 리더, 교육담당, PM | citeturn46view0turn46view1 |
| agent 설계 실무 | 국제 공식 가이드 | OpenAI practical guide, Anthropic building effective agents | B | AI 엔지니어, PM | citeturn9view0turn39view0turn39view2 |
| 위험·평가 실무 | 국제 공식 가이드 | NIST AI RMF GenAI Profile, NIST agent hijacking blog, OWASP LLM Top 10 한국어판 | B | 보안, 운영, 아키텍트 | citeturn9view4turn9view2turn9view5turn14view0turn14view3 |
| Harness 실습 진입 | 공식 제품 교육 | Harness Training, Harness Agents, Effective Prompting | B | AI 엔지니어, DevOps, 운영 | citeturn9view6turn11view4turn41view0 |
| Harness 심화 실무 | 공식 제품 문서 | Harness Skills, DevOps Agent privacy/data handling, Chat History & Memory | B | 엔지니어, 보안, 운영 | citeturn41view2turn41view1turn40search1 |
| 온라인 강의 | 공개 강좌 | K-MOOC 「생성형 AI 활용 실무」, 「인공지능 윤리」, 「생성형 인공지능 입문」 | B | 전 대상 | citeturn38search0turn38search1turn38search2 |
| 보조 학습 허브 | 공식 온라인 리소스 | OpenAI Learning Hub, OpenAI Academy | B | PM, 엔지니어, 교육담당 | citeturn38search3turn38search7 |
| 사례 리포트 | 공식/준공식 사례 | OECD AI risks & incidents, OpenAI Harness engineering case | C | 리더, 전략, 교육담당 | citeturn8search14turn7search15 |

핵심 참고문헌으로는 국내에서는 권재술 외, 왕경수, 김문수·이혜진을 먼저 읽고, 국제 원전으로는 entity["people","Bo Hedberg","organizational learning scholar"]의 계보를 잇는 조직 언러닝 논의, entity["people","Chris Argyris","organizational learning scholar"]의 double-loop learning, entity["people","Jack Mezirow","adult learning scholar"]의 transformative learning, entity["people","George J. Posner","science education scholar"]의 conceptual change를 우선하는 구성이 적절하다. 시청각 설계 원리까지 같이 보려면 entity["people","Richard E. Mayer","multimedia learning scholar"]의 multimedia learning 계열 자료를 더하면 좋다. citeturn23view2turn23view3turn25view0turn42view0turn46view0turn46view1turn43view0turn16search4turn16search12

## 리스크 관리

언러닝은 강력한 개념이지만, 잘못 쓰면 “기존 전문성을 무시하는 유행어”처럼 받아들여질 수 있다. 특히 deep unlearning은 기존 전제를 흔들기 때문에 정체성 위협, 체면 손상, 방어적 태도, 과도한 회의주의를 유발할 수 있다. 또한 에이전트 안전을 강조하는 과정에서 인지부하를 과도하게 높이면 본교육 진입 동력이 떨어질 수 있다. 그러므로 리스크 관리는 개념 설명보다 설계 방식의 문제다. citeturn33search15turn14view3turn16search4turn16search6

| 반대 의견·리스크 | 실제 문제 | 대응 전략 | 참고 근거 |
|---|---|---|---|
| “언러닝은 기존 전문성을 부정한다.” | 학습자가 방어적으로 반응하고 강의 전체 몰입이 떨어질 수 있다. | “버릴 것/남길 것” 이중 프레임 사용. 기존 전문성은 유지하되, 지금 맥락에서 방해되는 가정만 재조정한다고 설명 | deep unlearning의 감정 비용, transformative learning citeturn33search15turn46view1 |
| “경고만 많아지면 도입 의지가 꺾인다.” | 과도한 위험 프레이밍은 adoption paralysis를 만들 수 있다. | 위험 1개당 행동 규칙 1개를 바로 붙인다. 예: prompt injection → 프롬프트 밖 통제 | NIST/OWASP/OpenAI의 layered defense·HITL 권고 citeturn9view5turn11view2turn12view2 |
| “초반부터 너무 복잡하다.” | 5~7분 클립에 개념을 과하게 넣으면 피상화와 이탈이 생긴다. | 한 장면 하나의 판단 규칙. coherence·signaling 원칙 적용 | multimedia learning·CLT, short-video caution citeturn16search4turn16search6turn16search1 |
| “보안은 결국 모델이 알아서 막아야 하지 않나?” | prompt-only control 환상은 프롬프트 유출, 간접 injection, tool misuse를 낳는다. | 인증·인가·정책 게이트·권한 분리·출력 검사 등 외부 통제 강조 | OWASP·NIST·OpenAI 공식 가이드 citeturn9view2turn9view5turn11view2 |
| “완전자율이 더 효율적이다.” | 고위험·비가역 작업에 대한 무인 실행이 사고를 키울 수 있다. | 고위험 액션은 human approval, failure threshold, least privilege 적용 | OpenAI HITL, Harness security first model citeturn12view2turn11view4 |
| “가시성을 높이면 오히려 민감정보 노출 위험이 있다.” | 로그·요약·메모리가 편리하지만 노출면도 커진다. | 로그는 decision visibility 중심으로 두고, 비밀·민감정보는 mask/redact·retention policy로 통제 | Harness privacy/data handling, OWASP prompt leak guidance citeturn41view1turn9view5 |
| “Agent와 Harness를 한 클립에 같이 넣으면 산만하다.” | 지나치게 추상적이거나 반대로 제품 홍보처럼 보일 수 있다. | 공통 mental model 1개만 공유하고, 예시는 Agent 1개 + Harness 1개만 사용 | OpenAI/Anthropic/Harness 모두 공통적으로 단순성·명확성·문맥 확인을 중시 citeturn39view0turn39view2turn41view0turn41view2 |

핵심은 “모든 오래된 것을 버리는 수업”이 아니라, “무엇을 유지하고 무엇을 재설계할지를 구분하는 수업”이어야 한다는 점이다. 이 메시지가 분명하면 언러닝은 유행어가 아니라 실제 업무 전환을 여는 안전한 도구가 된다. citeturn32view0turn46view1

## 즉시 사용 가능한 문구

아래 문구는 바로 슬라이드와 나레이션 초안으로 옮겨 쓸 수 있도록 짧고 단정하게 정리했다.

| 슬라이드 | 화면 문구 | 강사 스크립트 |
|---|---|---|
| 슬라이드 하나 | 새 기능보다 먼저 버릴 가정이 있다 | “오늘의 목표는 기능 설명이 아닙니다. 기능을 잘못 신뢰하게 만드는 오래된 가정을 먼저 내려놓는 것입니다.” |
| 슬라이드 둘 | Agent는 답변기가 아니라 실행기다 | “에이전트는 질문에 답만 하는 존재가 아니라, 도구를 사용해 과업을 실행하는 시스템입니다.” |
| 슬라이드 셋 | 프롬프트만으로는 통제되지 않는다 | “안전은 문장 안이 아니라 시스템 바깥의 권한, 승인, 정책, 검증에서 만들어집니다.” |
| 슬라이드 넷 | 최신성은 기억이 아니라 조회에서 온다 | “모델의 상식보다 현재 데이터와 실제 플랫폼 상태를 먼저 보아야 합니다.” |
| 슬라이드 다섯 | 자연어는 명세가 아니다 | “무엇을 만들지 말하기 전에, 어떤 문맥과 어떤 스키마, 어떤 권한으로 만들지부터 확인해야 합니다.” |
| 슬라이드 여섯 | 운영 전 평가, 운영 중 승인 | “좋은 자동화는 더 많은 자율성이 아니라, 더 명확한 평가와 승인 경계에서 시작합니다.” |
| 슬라이드 일곱 | 오늘 버릴 세 가지 확신 | “프롬프트 만능주의, 모델 최신성 환상, 완전자율 환상을 오늘 이 자리에서 버리고 시작하겠습니다.” |

다음은 1페이지 요약 슬라이드로 바로 붙여 넣을 수 있는 텍스트다.

**제목**  
AI Agent·Harness 교육 전에 먼저 해야 할 일

**부제**  
새 기능 학습보다 먼저, 낡은 판단 규칙을 정렬한다

- 언러닝은 기존 지식을 부정하는 것이 아니라, 지금 맥락에서 방해가 되는 가정의 우선권을 낮추는 과정이다.
- Agent는 챗봇이 아니라 도구를 가진 실행 시스템이다.
- 복잡성이 답이 아니다. 단순한 구조와 평가에서 시작해야 한다.
- 프롬프트는 통제의 전부가 아니다. 보안과 승인 경계는 시스템 밖에 있어야 한다.
- 최신 상태는 모델 기억이 아니라 조회와 현행 문맥에서 온다.
- Harness에서는 자연어 요청보다 scope, dependency, schema, permission 확인이 먼저다.
- 본교육의 공통 행동 규칙은 네 가지다.  
  ① 현재 상태 조회  
  ② 권한 최소화  
  ③ 평가 기준 정의  
  ④ 고위험 승인 게이트 설정
