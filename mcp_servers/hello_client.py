import asyncio

from fastmcp import Client

HELLO_SERVER_URL = "http://localhost:8000/mcp"


async def main() -> None:
    async with Client(HELLO_SERVER_URL) as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print(result.data)


if __name__ == "__main__":
    asyncio.run(main())
