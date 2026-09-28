import sqlite3

db = sqlite3.connect("notes.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
     id INTEGER PRIMARY KEY,
     text TEXT
)
""")

note = input("Write a note: ")

cur.execute("INSERT INTO notes (text) VALUES (?)", (note,))
db.commit()

cur.execute("SELECT * FROM notes")

for row in cur.fetchall():
    print(row)

db.close()

