# Session 3-1. MCP가 왜 중요한가: AI를 코드 밖으로 꺼내는 도구 호출의 표준.

## 목표

MCP를 단순한 플러그인이나 편의 기능이 아니라, 
AI가 외부 도구와 데이터에 접근하는 도구(Tool)의 표준 연결면으로 이해한다.

REST API != MCP Server Tools

항상 로드되는 곳에서만 사용.
"공통화"
> MCP Server
> 개별 Tools

## 단점
1. 한번에 모두 다 로드를 해야해서, Context 많이 차지한다
> 한번에 모두 다 로드하지 않으면 되는거 아닌가?
> Agent Skills