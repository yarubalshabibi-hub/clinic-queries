from fastmcp import FastMCP

mcp = FastMCP("Hello Server")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two whole numbers and return their sum."""
    return a + b


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
