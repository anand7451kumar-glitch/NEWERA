import sqlite3

db = sqlite3.connect("tasks.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     task TEXT NOT NULL,
     done INTEGER DEFAULT 0
)
""")

while True:
    print("\n1. Add 2. View 3. Complete 4. Exit")
    choice = input("> ")

    if choice == "1":
        task = input("Task: ")
        cur.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        db.commit()

    elif choice == "2":
        cur.execute("SELECT * FROM tasks")

        for id, task, done in cur.fetchall():
            mark = "✅" id done else "◻"
            print(f"{id}. [{mark}] { task}")

    elif choice == "3":
        task_id = int(input("Task ID: "))
        cur.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?",
            (task_id,)
        )
        db.commit()

    elif choice == "4":
        break

db.close()

        
        

