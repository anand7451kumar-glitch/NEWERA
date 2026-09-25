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
