import sqlite3

c = sqlite3.connect("shop.db")


def q(sql):
    return c.execute(sql).fetchall()


print("rows           :", q("SELECT COUNT(*) FROM orders"))
print("customers      :", q("SELECT COUNT(DISTINCT customer_id), MIN(customer_id), MAX(customer_id) FROM orders"))
print("delivery_status:", q("SELECT delivery_status, COUNT(*) FROM orders GROUP BY 1"))
print("category       :", q("SELECT category, COUNT(*) FROM orders GROUP BY 1"))
print("payment_method :", q("SELECT payment_method, COUNT(*) FROM orders GROUP BY 1"))
print("order_date     :", q("SELECT MIN(order_date), MAX(order_date), COUNT(DISTINCT order_date) FROM orders"))
print("price          :", q("SELECT MIN(price), MAX(price) FROM orders"))
print("quantity       :", q("SELECT MIN(quantity), MAX(quantity) FROM orders"))
print("nulls          :", q("SELECT SUM(delivery_status IS NULL), SUM(shipping_date IS NULL) FROM orders"))
