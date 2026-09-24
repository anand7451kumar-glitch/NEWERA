import time

input("Press Enter to satrt...")
start = time.time()

input("Press Enter to stop...")
elapsed = time.time() - start

print("Elapsed time:", round(elapsed, 2), "seconds")

