import server

print("1 valid     :", server.get_customer(1))
print("2 bad id    :", server.get_customer(-5))
print("3 not found :", server.get_customer(999))
print("4 bad status:", server.search_orders(status="hack"))
print("5 injection :", server.search_orders(product="x'; DROP TABLE orders;--"))
print("6 big limit :", server.list_recent_orders(1000))
print("7 rows left :", len(server.query("SELECT * FROM orders")))
try:
    server.get_conn().execute("DELETE FROM orders")
    print("8 DELETE    : NOT BLOCKED (problem)")
except Exception as e:
    print("8 DELETE    : blocked ->", e)
