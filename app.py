import pandas as pd
import streamlit as st

import server

st.set_page_config(page_title="Shop MCP Server Demo", layout="wide")
st.title("Shop MCP Server - tool explorer")
st.caption(
    "The same four read-only tools that Claude Desktop calls over MCP, "
    "run here through a web form. Data: 10,000 synthetic orders "
    "(Hugging Face: millat/e-commerce-orders)."
)

tool = st.sidebar.radio(
    "Tool",
    ["search_orders", "get_order", "get_customer_orders", "customer_summary"],
)
st.sidebar.markdown(
    "Try invalid values too (negative ID, unknown status, SQL-like text) "
    "to see the validation errors."
)

result = None

if tool == "search_orders":
    st.caption("delivery_status: Delivered, Pending, Returned, Shipped | "
               "category: Beauty, Books, Clothing, Electronics, Home, Toys")
    status = st.text_input("delivery_status (optional)", "Pending")
    category = st.text_input("category (optional)", "Toys")
    limit = st.number_input("limit (valid: 1-50)", value=5, step=1)
    if st.button("Run"):
        result = server.search_orders(status, category, int(limit))

elif tool == "get_order":
    order_id = st.text_input("order_id (36-character UUID)")
    if st.button("Run"):
        result = server.get_order(order_id)

elif tool == "get_customer_orders":
    customer_id = st.number_input("customer_id", value=97, step=1)
    if st.button("Run"):
        result = server.get_customer_orders(int(customer_id))

else:
    customer_id = st.number_input("customer_id", value=97, step=1)
    if st.button("Run"):
        result = server.customer_summary(int(customer_id))

if result is not None:
    if "error" in result:
        st.error(result["error"])
    elif "results" in result:
        st.success(f"{result['count']} order(s) found")
        st.dataframe(pd.DataFrame(result["results"]), use_container_width=True)
    else:
        st.json(result)