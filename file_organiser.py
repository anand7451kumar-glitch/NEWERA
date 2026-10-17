from pathlib import Path
import shutil

FOLDERS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mov", ".mkv"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".c", ".cpp", ".java", ".js", ".html", ".css"]
}

folder_input = input("Enter folder path to organize: ").strip()
folder = Path(folder_input).expanduser()

if not folder.is_dir():
    print("Error: Folder does not exist.")
else:
    moved = 0

    for file in folder.iterdir():
        if not file.is_file():
            continue

        destination_name = next(
            (name for name, extensions in FOLDERS.items()
             if file.suffix.lower() in extensions),
            "Other"
        )

        destination = folder / destination_name
        destination.mkdir(exist_ok=True)

        target = destination / file.name

        if target.exists():
            print(f"Skipped duplicate: {file.name}")
            continue

        shutil.move(str(file), str(target))
        print(f"Moved: {file.name} -> {destination_name}/")
        moved += 1

    print(f"\nFinished! Organized {moved} files.")