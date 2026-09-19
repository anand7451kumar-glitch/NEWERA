from pathlib import Path

folder = Path(input("Enter folder path: "))
total = 0

for file in folder.rglob("*"):
    if file.is_file():
        total += file.stat().st_size

print(f"Folder size: {total / (1024 ** 2):.2f} MB")
