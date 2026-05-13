"""Smoke-test the basic MCP server through the official Python MCP client."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from pydantic import AnyUrl

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


HERE = Path(__file__).resolve().parent


def _text(block: object) -> str:
    if isinstance(block, (types.TextContent, types.TextResourceContents)):
        return block.text
    raise TypeError(f"Expected TextContent, got {type(block).__name__}")


async def run_smoke_test() -> dict[str, object]:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(HERE / "server.py")],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = sorted(tool.name for tool in tools.tools)
            assert tool_names == ["calculate_discount", "summarize_task"]

            discount = await session.call_tool(
                "calculate_discount",
                arguments={"price": 120_000, "percent": 15},
            )
            discount_text = _text(discount.content[0])
            assert "102000" in discount_text

            summary = await session.call_tool(
                "summarize_task",
                arguments={
                    "title": "MCP 서버 만들기",
                    "owner": "student",
                    "due_date": "2026-05-20",
                },
            )
            summary_text = _text(summary.content[0])
            assert "student" in summary_text
            assert "2026-05-20" in summary_text

            resource = await session.read_resource(AnyUrl("course://mcp/overview"))
            resource_text = _text(resource.contents[0])
            assert "Tools" in resource_text
            assert "Resources" in resource_text

            prompt = await session.get_prompt(
                "review_mcp_tool",
                arguments={"tool_name": "calculate_discount"},
            )
            prompt_text = _text(prompt.messages[0].content)
            assert "calculate_discount" in prompt_text

            return {
                "tools": tool_names,
                "calculate_discount": discount_text,
                "summarize_task": summary_text,
                "resource": resource_text,
                "prompt": prompt_text,
            }


def main() -> None:
    result = asyncio.run(run_smoke_test())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
