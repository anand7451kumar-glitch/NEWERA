from pathlib import Path

folder = Path(input("Folder path: "))
word = input("Search word: ").lower()

for file in folder.glob("*.txt"):
    text = file.read_text(errors="ignore").lower()

    if word in text:
        print("Found in:", file.name)
