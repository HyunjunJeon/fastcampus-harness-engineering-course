# 03-01 MCP 보안 위험 패턴 3가지

[../plan.md](../plan.md) 03-01 진행 흐름의 보완 포인트 또는 4단계에서 사용. MCP 서버를 *만드는 쪽*이 노출하면 안 되는 위험 패턴.

## 위험 패턴 3가지

### 1. 임의 SQL 실행 도구

```text
도구: execute_sql(query: str) -> result
```

**왜 위험한가**: AI가 임의의 SQL을 생성해 DB에 직접 실행. DROP·DELETE·권한 변경 모두 가능. 운영 DB에 붙으면 사고가 *되돌릴 수 없다*.

**안전한 대체**: 미리 정의된 *읽기 전용 쿼리* 1~5개만 노출.

```text
도구: recent_orders(limit: int) -> rows
도구: user_summary(user_id: int) -> row
```

### 2. 무제한 파일 접근 도구

```text
도구: read_file(path: str) -> content
도구: write_file(path: str, content: str)
```

**왜 위험한가**: AI가 `/etc/passwd`, `~/.ssh/id_rsa`, `.env` 등 어떤 파일이든 읽고 쓰기 가능. 비밀 정보 유출, 시스템 파일 손상.

**안전한 대체**: 노출 *디렉토리를 명시적으로 제한*.

```text
도구: read_project_doc(name: str) -> content  # docs/ 아래만 허용
```

### 3. 외부 호출 무제한 위임 도구

```text
도구: http_request(url: str, method: str, body: dict) -> response
```

**왜 위험한가**: AI가 임의 URL로 임의 HTTP 호출. 사내 API에 인증 토큰 첨부해 호출, 외부 서버로 데이터 전송, DOS 공격에 가담 가능.

**안전한 대체**: *허용된 도메인·엔드포인트 패턴*을 화이트리스트로.

```text
도구: fetch_linear_issue(id: int) -> issue  # api.linear.app/v1/issues/{id}만
```

## 한 줄 자가 점검 질문

수강생이 "MCP로 풀고 싶은 문제 3가지"를 적은 뒤 각각에 던지는 질문:

> "이 도구가 받는 입력값이 *임의 문자열*인가, 아니면 *미리 정의된 enum/ID*인가? 임의 문자열이면 위 3가지 위험 중 하나에 해당하지 않는지 다시 본다."

## 시연 흐름

03-01 진행 흐름 4단계에서 수강생이 "MCP로 풀고 싶은 문제 3가지"를 적을 때:

1. 수강생 후보 3개를 화면에 띄움
2. 강사가 위 3가지 위험 패턴 슬라이드로 *자가 점검* 시연
3. 가장 위험이 작은 후보 1개를 03-02 입력 메모로 선택

## 강사가 챙길 자산

- 위 3가지 패턴을 슬라이드 1장에 압축 (도구 시그니처 + 위험 한 줄 + 안전한 대체)
- 수강생이 적은 후보에 위험 패턴이 보이면 *이름*을 짚어주기 ("이건 무제한 파일 접근 패턴이네요")
