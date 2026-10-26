import server

r = server.search_orders(delivery_status="returned", category="books", limit=2)
print("1 search   :", r)
oid = r["results"][0]["order_id"]
print("2 get_order:", server.get_order(oid))
print("3 bad id   :", server.get_order("abc"))
print("4 summary  :", server.customer_summary(1))
print("5 no data  :", server.customer_summary(999999))
print("6 bad cust :", server.get_customer_orders(-1))
