import time

text = "Python is useful for automation."

print("Type this:")
print(text)

input("Press Enter to satrt...")

start = time.time()
typed = input("Type: ")
elapsed = time.time() - start

words = len(typed.split())
wpm = words / (elapsed / 60)

print("Time:", round(elapsed, 2), "seconds")
print("Speed:", round(wpm, 2), "WPM")