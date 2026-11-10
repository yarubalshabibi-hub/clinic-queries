from fastmcp import FastMCP

mcp = FastMCP("Clinic Pharmacy Server")

inventory: dict[str, int] = {
    "Paracetamol": 120,
    "Ibuprofen": 40,
    "Cetirizine": 75,
}


@mcp.tool
def view_inventory() -> dict:
    """Return the full pharmacy inventory as a mapping of medicine name to stock."""
    return inventory


@mcp.tool
def add_inventory(medicine: str, quantity: int) -> dict:
    """Add stock for a medicine, creating it if it is new.

    Quantity must be greater than zero. Returns the medicine and its updated
    stock, or an error if the quantity is not positive.
    """
    if quantity <= 0:
        return {"error": f"Quantity must be greater than 0, got {quantity}"}

    inventory[medicine] = inventory.get(medicine, 0) + quantity
    return {"medicine": medicine, "stock": inventory[medicine]}


if __name__ == "__main__":
    mcp.run(transport="http", port=8002)
