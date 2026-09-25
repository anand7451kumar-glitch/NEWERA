import sqlite3, datetime
import matplotlib.pyplot as plt

conn = sqlite3.connect("habits.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS habits (date TEXT, habit TEXT)")

def log_habit(habit):
    today = datetime.date.today().isoformat()
    c.execute("INSERT INTO habits VALUES (?, ?)", (today, habit))
    conn.commit()

def show_progress(habit):
    c.execute("SELECT date FROM habits WHERE habit=?", (habit,))
    dates = [row[0] for row in c.fetchall()]
    if not dates:
        print(f"No data found for {habit}")
        return
    plt.hist(dates, bins=len(set(dates)))
    plt.title(f"Progress for {habit}")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.savefig("progress.png")   # Save chart as image
    print("Progress chart saved as progress.png")


#Example
log_habit("Coding")
show_progress("Coding")

conn.close()