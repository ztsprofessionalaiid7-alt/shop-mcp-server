import sqlite3

conn = sqlite3.connect("shop.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    city TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
""")

customers = [
    (1, "Rahim Uddin", "rahim@example.com", "Dhaka"),
    (2, "Nusrat Jahan", "nusrat@example.com", "Chattogram"),
    (3, "Karim Hossain", "karim@example.com", "Sylhet"),
    (4, "Sadia Islam", "sadia@example.com", "Dhaka"),
    (5, "Tanvir Ahmed", "tanvir@example.com", "Khulna"),
]

orders = [
    (1, 1, "Laptop", 55000.0, "delivered", "2026-08-02"),
    (2, 1, "Mouse", 800.0, "delivered", "2026-08-10"),
    (3, 2, "Phone", 28000.0, "shipped", "2026-09-15"),
    (4, 3, "Keyboard", 1500.0, "pending", "2026-10-01"),
    (5, 4, "Monitor", 18000.0, "delivered", "2026-09-05"),
    (6, 4, "Headphones", 3200.0, "cancelled", "2026-09-20"),
    (7, 5, "Tablet", 22000.0, "shipped", "2026-10-12"),
    (8, 2, "Charger", 900.0, "pending", "2026-10-20"),
]

cur.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)
cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders)

conn.commit()
conn.close()
print("shop.db created")
