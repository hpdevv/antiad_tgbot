import sqlite3

conn = sqlite3.connect('db.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        text TEXT NOT NULL,
        answer TEXT NOT NULL,
        username TEXT NOT NULL,
        gpt_ver TEXT NOT NULL
    )
''')

conn.commit()