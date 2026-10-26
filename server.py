from pathlib import Path
import sqlite3
from typing import Literal, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

mcp = FastMCP("shop-server")

DB_URI = Path(__file__).parent.joinpath("shop.db").as_uri() + "?mode=ro"


class SearchOrdersInput(BaseModel):
    status: Optional[Literal["pending", "shipped", "delivered", "cancelled"]] = None
    product: Optional[str] = Field(default=None, max_length=50)


class CustomerIdInput(BaseModel):
    customer_id: int = Field(gt=0, le=1_000_000)


class RecentOrdersInput(BaseModel):
    limit: int = Field(default=5, ge=1, le=50)


def get_conn():
    conn = sqlite3.connect(DB_URI, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql, params=()):
    conn = get_conn()
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def error_dict(e: ValidationError):
    parts = [f"{'.'.join(str(x) for x in err['loc'])}: {err['msg']}" for err in e.errors()]
    return {"error": "Invalid input - " + "; ".join(parts)}


@mcp.tool()
def search_orders(status: str = "", product: str = "") -> dict:
    """Search orders by status (pending, shipped, delivered, cancelled) and/or product name."""
    try:
        data = SearchOrdersInput(status=status or None, product=product or None)
    except ValidationError as e:
        return error_dict(e)
    sql = "SELECT * FROM orders WHERE 1=1"
    params = []
    if data.status:
        sql += " AND status = ?"
        params.append(data.status)
    if data.product:
        sql += " AND product LIKE ?"
        params.append(f"%{data.product}%")
    return {"results": query(sql, params)}


@mcp.tool()
def get_customer(customer_id: int) -> dict:
    """Get one customer's details by ID."""
    try:
        data = CustomerIdInput(customer_id=customer_id)
    except ValidationError as e:
        return error_dict(e)
    rows = query("SELECT * FROM customers WHERE id = ?", (data.customer_id,))
    return rows[0] if rows else {"error": f"No customer found with id {data.customer_id}"}


@mcp.tool()
def get_customer_orders(customer_id: int) -> dict:
    """List all orders of one customer."""
    try:
        data = CustomerIdInput(customer_id=customer_id)
    except ValidationError as e:
        return error_dict(e)
    return {"results": query("SELECT * FROM orders WHERE customer_id = ?", (data.customer_id,))}


@mcp.tool()
def list_recent_orders(limit: int = 5) -> dict:
    """List the most recent orders (limit 1-50)."""
    try:
        data = RecentOrdersInput(limit=limit)
    except ValidationError as e:
        return error_dict(e)
    return {"results": query("SELECT * FROM orders ORDER BY order_date DESC LIMIT ?", (data.limit,))}


if __name__ == "__main__":
    mcp.run()
