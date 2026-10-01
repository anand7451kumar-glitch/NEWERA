from pathlib import Path

folder = Path("documents")
query = input("Search for: ").lower()

found = False

for file in folder.glob("*.txt"):
    text = file.read_text(errors="ignore").lower()

    if query in text:
        print("Found in:", file.name)
        found = True

if not found:
    print("No matches found.")