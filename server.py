import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shop-server")

DB_PATH = "shop.db"


def query(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@mcp.tool()
def search_orders(status: str = "", product: str = "") -> list:
    """Search orders by status (pending, shipped, delivered, cancelled) and/or product name."""
    sql = "SELECT * FROM orders WHERE 1=1"
    params = []
    if status:
        sql += " AND status = ?"
        params.append(status)
    if product:
        sql += " AND product LIKE ?"
        params.append(f"%{product}%")
    return query(sql, params)


@mcp.tool()
def get_customer(customer_id: int) -> dict:
    """Get one customer's details by ID."""
    rows = query("SELECT * FROM customers WHERE id = ?", (customer_id,))
    return rows[0] if rows else {"error": "customer not found"}


@mcp.tool()
def get_customer_orders(customer_id: int) -> list:
    """List all orders of one customer."""
    return query("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))


@mcp.tool()
def list_recent_orders(limit: int = 5) -> list:
    """List the most recent orders."""
    return query("SELECT * FROM orders ORDER BY order_date DESC LIMIT ?", (limit,))


if __name__ == "__main__":
    mcp.run()
