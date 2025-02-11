# filename: initialize_db.py
import sqlite3

def create_table():
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        stock INTEGER NOT NULL,
        price INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Database and table created successfully.")
