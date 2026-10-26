import sqlite3
import sys

conn = sqlite3.connect("file:shop.db?mode=ro", uri=True)
for row in conn.execute(sys.argv[1]).fetchall():
    print(row)
