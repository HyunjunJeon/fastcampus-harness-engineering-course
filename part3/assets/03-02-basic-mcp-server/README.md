# 03-02 기본 MCP 서버 실습

이 폴더는 가장 작은 MCP 서버를 만들고, 공식 Python MCP SDK 클라이언트로 실제 연결을 검증하는 실습 자산이다.

공식 문서 확인일: 2026-05-13

## MCP를 먼저 이해하기

MCP(Model Context Protocol)는 AI 애플리케이션이 외부 도구와 데이터에 접근하는 방식을 표준화한 클라이언트-서버 프로토콜이다. 핵심 참여자는 세 가지다.

| 구성 | 역할 |
| --- | --- |
| Host | Claude Desktop, Claude Code, Codex 같은 AI 애플리케이션 |
| Client | Host 안에서 특정 MCP 서버와 1:1 연결을 유지하는 구성요소 |
| Server | 도구, 리소스, 프롬프트를 표준 방식으로 제공하는 프로그램 |

서버가 제공하는 대표 기능은 세 가지다.

| 기능 | 누가 주도하나 | 쓰임 |
| --- | --- | --- |
| Tools | 모델 | 계산, API 호출, 파일 생성 같은 실행 동작 |
| Resources | 애플리케이션 | 파일, API 응답, 문서 조각 같은 읽기 가능한 맥락 |
| Prompts | 사용자 | 반복 작업을 위한 재사용 프롬프트 템플릿 |

전송 방식은 로컬 실습에서는 보통 `stdio`가 가장 단순하다. 클라이언트가 서버를 자식 프로세스로 실행하고, `stdin`/`stdout`을 통해 JSON-RPC 메시지를 주고받는다. `stdio` 서버는 `stdout`에 일반 로그를 쓰면 프로토콜 메시지를 깨뜨릴 수 있으므로 로그는 `stderr`나 파일로 보내야 한다.

## 파일 구성

| 파일 | 설명 |
| --- | --- |
| `server.py` | `FastMCP`로 만든 기본 MCP 서버 |
| `client_test.py` | 서버를 `stdio`로 실행하고 도구, 리소스, 프롬프트를 호출하는 클라이언트 검증 스크립트 |

서버가 노출하는 항목:

- Tool: `calculate_discount(price, percent)`
- Tool: `summarize_task(title, owner, due_date)`
- Resource: `course://mcp/overview`
- Prompt: `review_mcp_tool(tool_name)`

## 실행

의존성은 프로젝트에 고정하지 않고 `uv --with`로 일회성 실행한다.

```bash
uv run --with "mcp[cli]" python part3/assets/03-02-basic-mcp-server/client_test.py
```

성공하면 다음 형태의 JSON이 출력된다.

```json
{
  "tools": ["calculate_discount", "summarize_task"],
  "calculate_discount": "Original=120000, discount=15%, final=102000, saved=18000",
  "summarize_task": "Task 'MCP 서버 만들기' is owned by student and due on 2026-05-20.",
  "resource": "MCP servers expose Tools for model-controlled actions, Resources for application-controlled context, and Prompts for user-controlled reusable workflows.",
  "prompt": "Review the MCP tool 'calculate_discount'. Check the tool name, description, input schema, side effects, error behavior, and permission boundary."
}
```

## 호스트 등록 예시

Claude Desktop 계열 설정은 일반적으로 `mcpServers` 아래에 서버 이름, 실행 명령, 인자를 둔다.

```json
{
  "mcpServers": {
    "basic-course-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "python",
        "/Users/jhj/Desktop/personal/fastcampus_harness_online_learning/part3/assets/03-02-basic-mcp-server/server.py"
      ]
    }
  }
}
```

Codex CLI/IDE 설정은 OpenAI 공식 문서 기준으로 `~/.codex/config.toml`의 `[mcp_servers.<name>]` 형식을 사용한다.

```toml
[mcp_servers.basic-course-mcp]
command = "uv"
args = [
  "run",
  "--with",
  "mcp[cli]",
  "python",
  "/Users/jhj/Desktop/personal/fastcampus_harness_online_learning/part3/assets/03-02-basic-mcp-server/server.py",
]
```

## 수업에서 강조할 점

1. MCP 서버는 "AI용 API 서버"에 가깝지만, 일반 REST API와 달리 도구 스키마, 리소스 URI, 프롬프트 템플릿을 LLM 호스트가 발견하고 사용할 수 있게 제공한다.
2. 서버 하나가 곧 권한 확장이다. Tool은 모델이 호출할 수 있는 실행면이므로 이름, 설명, 입력 범위, 부작용, 승인 경계를 명확히 해야 한다.
3. 로컬 `stdio` 서버는 단순하지만 stdout 관리가 중요하다. JSON-RPC 메시지가 오가는 통로이기 때문이다.
4. 실제 도입 전에는 오늘처럼 최소 클라이언트로 `initialize -> list_tools -> call_tool -> read_resource -> get_prompt` 흐름을 검증한다.
