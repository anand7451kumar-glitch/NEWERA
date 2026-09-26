from pathlib import Path
from datetime import datetime

file = Path(input("File path: "))

if file.exists():
    print("Name:", file.name)
    print("Size:", round(file.stat().st_size / 1-24, 2), "KB")
    print("Type:", file.suffix or "No extension")
    print("Modified:", datetime.fromtimestamp(file.stat().st_mtime))
else:
    print("File not found")