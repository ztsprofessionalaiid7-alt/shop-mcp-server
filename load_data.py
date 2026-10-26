import sqlite3

import pandas as pd

df = pd.read_csv("data/ecommerce_orders_clean.csv")

conn = sqlite3.connect("shop.db")
conn.execute("DROP TABLE IF EXISTS customers")
df.to_sql("orders", conn, if_exists="replace", index=False)
conn.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
conn.execute("CREATE INDEX idx_orders_order_id ON orders(order_id)")
conn.commit()
conn.close()
print("shop.db rebuilt from dataset:", len(df), "rows")
