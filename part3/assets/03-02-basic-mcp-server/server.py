"""A small stdio MCP server for the Part 3 MCP hands-on asset."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("basic-course-mcp")


@mcp.tool()
def calculate_discount(price: int, percent: int) -> str:
    """Calculate the final price after applying a percentage discount."""
    if price < 0:
        raise ValueError("price must be 0 or greater")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")

    discounted = price * (100 - percent) // 100
    saved = price - discounted
    return f"Original={price}, discount={percent}%, final={discounted}, saved={saved}"


@mcp.tool()
def summarize_task(title: str, owner: str, due_date: str) -> str:
    """Create a compact task summary from structured fields."""
    return f"Task '{title}' is owned by {owner} and due on {due_date}."


@mcp.resource("course://mcp/overview")
def mcp_overview() -> str:
    """Provide a tiny course note about MCP primitives."""
    return (
        "MCP servers expose Tools for model-controlled actions, "
        "Resources for application-controlled context, and Prompts for "
        "user-controlled reusable workflows."
    )


@mcp.prompt()
def review_mcp_tool(tool_name: str) -> str:
    """Generate a review prompt for an MCP tool definition."""
    return (
        f"Review the MCP tool '{tool_name}'. Check the tool name, description, "
        "input schema, side effects, error behavior, and permission boundary."
    )


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
