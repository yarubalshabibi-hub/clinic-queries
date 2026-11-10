import asyncio

from fastmcp import Client

BOOKING_URL = "http://localhost:8001/mcp"
PHARMACY_URL = "http://localhost:8002/mcp"
REPORTS_URL = "http://localhost:8003/mcp"

ToolCall = tuple[str, dict]


async def run_server_calls(server_name: str, url: str, calls: list[ToolCall]) -> list[str]:
    """Connect to one server, list its tools, run the calls in order and return the output lines."""
    lines = []
    async with Client(url) as client:
        tools = await client.list_tools()
        lines.append(f"{server_name} tools: {[tool.name for tool in tools]}")

        for tool_name, arguments in calls:
            result = await client.call_tool(tool_name, arguments)
            lines.append(f"{server_name}.{tool_name} -> {result.data}")
    return lines


async def add_new_medicine_flow() -> None:
    """The diagram's example flow: add a NEW medicine, then view the inventory to prove it appears."""
    async with Client(PHARMACY_URL) as client:
        added = await client.call_tool("add_inventory", {"medicine": "Amoxicillin", "quantity": 30})
        print(f"pharmacy.add_inventory -> {added.data}")

        inventory = await client.call_tool("view_inventory", {})
        print(f"pharmacy.view_inventory -> {inventory.data}")


async def main() -> None:
    booking_calls: list[ToolCall] = [
        ("register_patient", {"name": "Salim", "phone": "99112233"}),
        ("book_appointment", {"patient_id": 1, "doctor": "Dr. Huda", "date": "2026-11-20", "time": "10:00"}),
        ("book_appointment", {"patient_id": 1, "doctor": "Dr. Huda", "date": "2026-11-20", "time": "10:00"}),
        ("book_appointment", {"patient_id": 99, "doctor": "Dr. Huda", "date": "2026-11-20", "time": "11:00"}),
    ]
    pharmacy_calls: list[ToolCall] = [
        ("view_inventory", {}),
        ("add_inventory", {"medicine": "Paracetamol", "quantity": 10}),
        ("add_inventory", {"medicine": "Ibuprofen", "quantity": 0}),
    ]
    reports_calls: list[ToolCall] = [
        ("get_patient_medical_records", {"patient_id": 1}),
        ("get_opd_records", {"patient_id": 1}),
        ("get_patient_medical_records", {"patient_id": 99}),
    ]

    all_lines = await asyncio.gather(
        run_server_calls("booking", BOOKING_URL, booking_calls),
        run_server_calls("pharmacy", PHARMACY_URL, pharmacy_calls),
        run_server_calls("reports", REPORTS_URL, reports_calls),
    )
    for server_lines in all_lines:
        for line in server_lines:
            print(line)
        print()

    print("Example flow: add a NEW medicine in the pharmacy")
    await add_new_medicine_flow()


if __name__ == "__main__":
    asyncio.run(main())
