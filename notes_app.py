import json
from pathlib import Path

file = Path("notes.json")

if file.exists():
    notes = json.loads(file.read_text())

else:
    notes = []

note = input("Enter a note: ")
notes.append(note)

file.write_text(json.dumps(notes, indent=2))

print("\nYour notes:")
for i,  note in enumerate(notes, 1):
    print(f"{i}. {note}")
