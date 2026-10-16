import time

minutes = int(input("Study duration in minutes: "))
seconds = minutes * 60

print("Focus session satrted!")

try:
    while seconds > 0 :
        mins, secs = divmod(seconds, 60)
        print(f"\rTime remaining: {mins:02d}:{secs:02d}", end="")
        time.sleep(1)
        seconds -= 1

    print("\nSession complete! Take a short break.")
except KeyboardInterrupt:
    print("\nTimer stopped.")
