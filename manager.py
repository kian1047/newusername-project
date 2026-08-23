import sqlite3
import os
from models import Item , User

DB_PATH = os.path.join("data" , "inventory.db")

class InventoryManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._create_table()


    def _create_table(self):
        self.cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT "users"
        )""")
        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity REAL,
        price REAL,
        category TEXT
        )""")


        self.cursor.execute("SELECT * FROM users")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO users(username , password , role) values(?,?,?)",
                                ("admin","admin123","admin"))
            self.cursor.execute("INSERT INTO users(username , password , role) values(?,?,?)",
                                ("user","user123","user"))
            self.conn.commit()


    def authen(self,username,password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? ",
                            (username,password))
        row = self.cursor.fetchone()
        if row:
            return User(row[1],row[2],row[3])
        return None

    def add_item(self):
        items = []
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()
        for row in rows:
            items.append({
                "id":row[0],
                "name":row[1],
                "quantity":row[2],
                "price":row[3],
                "category":row[4]
            }) 
            self.conn.commit()

    def delete_item(self, item_id):
        self.cursor.execute(
            "DELETE FROM items WHERE id = ?",
            (item_id,)
        )
        self.conn.commit()

    def close(self):
        self.conn.close


if __name__ == "__main__":
    l = InventoryManager()