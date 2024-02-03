import sqlite3

db = sqlite3.connect('parkovka_sber.db')
cursor = db.cursor()

async def db_baze():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS polzovatel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT,
            name TEXT,
            otchestvo TEXT,
            phone_number INTEGER
        )               
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gos_nomer TEXT
        )               
    """)

    db.commit()
