from pathlib import Path
import sqlite3
from typing import Literal, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError, field_validator

mcp = FastMCP("shop-server")

DB_URI = Path(__file__).parent.joinpath("shop.db").as_uri() + "?mode=ro"

COLS = ("order_id, customer_id, product_id, category, price, quantity, "
        "order_date, shipping_date, delivery_status, payment_method")

Status = Literal["Delivered", "Pending", "Returned", "Shipped"]
Category = Literal["Beauty", "Books", "Clothing", "Electronics", "Home", "Toys"]


class SearchOrdersInput(BaseModel):
    delivery_status: Optional[Status] = None
    category: Optional[Category] = None
    limit: int = Field(default=10, ge=1, le=50)

    @field_validator("delivery_status", "category", mode="before")
    @classmethod
    def normalize(cls, v):
        return v.strip().title() if isinstance(v, str) else v


class OrderIdInput(BaseModel):
    order_id: str = Field(pattern=r"^[0-9a-fA-F\-]{36}$")


class CustomerIdInput(BaseModel):
    customer_id: int = Field(gt=0, le=1_000_000)


def query(sql, params=()):
    conn = sqlite3.connect(DB_URI, uri=True)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def error_dict(e: ValidationError):
    parts = [f"{'.'.join(str(x) for x in err['loc'])}: {err['msg']}" for err in e.errors()]
    return {"error": "Invalid input - " + "; ".join(parts)}


@mcp.tool()
def search_orders(delivery_status: str = "", category: str = "", limit: int = 10) -> dict:
    """Search orders, newest first. delivery_status: Delivered, Pending, Returned, Shipped.
    category: Beauty, Books, Clothing, Electronics, Home, Toys. limit 1-50."""
    try:
        data = SearchOrdersInput(
            delivery_status=delivery_status or None,
            category=category or None,
            limit=limit,
        )
    except ValidationError as e:
        return error_dict(e)
    sql = f"SELECT {COLS} FROM orders WHERE 1=1"
    params = []
    if data.delivery_status:
        sql += " AND delivery_status = ?"
        params.append(data.delivery_status)
    if data.category:
        sql += " AND category = ?"
        params.append(data.category)
    sql += " ORDER BY order_date DESC LIMIT ?"
    params.append(data.limit)
    rows = query(sql, params)
    return {"count": len(rows), "results": rows}


@mcp.tool()
def get_order(order_id: str) -> dict:
    """Get one order by its order_id (36-character UUID)."""
    try:
        data = OrderIdInput(order_id=order_id)
    except ValidationError as e:
        return error_dict(e)
    rows = query(f"SELECT {COLS} FROM orders WHERE order_id = ?", (data.order_id.lower(),))
    return rows[0] if rows else {"error": f"No order found with id {data.order_id}"}


@mcp.tool()
def get_customer_orders(customer_id: int) -> dict:
    """List a customer's orders, newest first (max 50)."""
    try:
        data = CustomerIdInput(customer_id=customer_id)
    except ValidationError as e:
        return error_dict(e)
    rows = query(
        f"SELECT {COLS} FROM orders WHERE customer_id = ? ORDER BY order_date DESC LIMIT 50",
        (data.customer_id,),
    )
    if not rows:
        return {"error": f"No orders found for customer {data.customer_id}"}
    return {"count": len(rows), "results": rows}


@mcp.tool()
def customer_summary(customer_id: int) -> dict:
    """Order count, total spent, first and last order date for one customer."""
    try:
        data = CustomerIdInput(customer_id=customer_id)
    except ValidationError as e:
        return error_dict(e)
    row = query(
        "SELECT COUNT(*) AS order_count, ROUND(SUM(price * quantity), 2) AS total_spent, "
        "MIN(order_date) AS first_order, MAX(order_date) AS last_order "
        "FROM orders WHERE customer_id = ?",
        (data.customer_id,),
    )[0]
    if row["order_count"] == 0:
        return {"error": f"No orders found for customer {data.customer_id}"}
    return {"customer_id": data.customer_id, **row}


if __name__ == "__main__":
    mcp.run()
