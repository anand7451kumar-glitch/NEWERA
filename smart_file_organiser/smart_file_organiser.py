import os
import shutil

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt"],
    "Videos": [".mp4", ".mov", ".mkv"],
    "Audio": [".mp3", ".wav", ".m4a"],
    "Code": [".py", ".cpp", ".c", ".js", ".html", ".css"],
    "Archives": [".zip", ".rar", ".7z"],
}

def show_summary(folder_path):
    if not os.path.isdir(folder_path):
        print("Error: Folder does not exist.")
        return

    summary = {category: 0 for category in CATEGORIES}
    summary["Other"] = 0

    total = 0

    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)

        if not os.path.isfile(path):
            continue

        extension = os.path.splitext(filename)[1].lower()
        category = "Other"

        for name, extensions in CATEGORIES.items():
            if extension in extensions:
                category = name
                break

        summary[category] += 1
        total += 1

    print("\n========== FILE SUMMARY ==========")

    for category, count in summary.items():
        print(f"{category:<12}: {count}")

    print("----------------------------------")
    print(f"Total files : {total}")
    print("==================================")
    
def organize_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Error: Folder does not exist.")
        return

    print("\n1. Preview changes")
    print("2. Organize files")
    choice = input("Choose an option: ").strip()

    if choice not in ("1", "2"):
        print("Invalid choice.")
        return

    preview = choice == "1"
    moved_count = 0
    skipped_count = 0

    for filename in os.listdir(folder_path):
        source = os.path.join(folder_path, filename)

        if not os.path.isfile(source):
            continue

        extension = os.path.splitext(filename)[1].lower()
        category = "Other"

        for name, extensions in CATEGORIES.items():
            if extension in extensions:
                category = name
                break

        destination_folder = os.path.join(folder_path, category)
        destination = os.path.join(destination_folder, filename)

        if os.path.exists(destination):
            print(f"Skipped duplicate: {filename}")
            skipped_count += 1
            continue

        if preview:
            print(f"Would move: {filename} -> {category}/")
        else:
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(source, destination)
            print(f"Moved: {filename} -> {category}/")
            moved_count += 1

    if preview:
        print("\nPreview complete. No files were moved.")
    else:
        print(f"\nFinished! Organized {moved_count} files.")

    print(f"Skipped files: {skipped_count}")


if __name__ == "__main__":
    folder = input("Enter the folder path: ").strip()
    folder = os.path.expanduser(folder)

    while True:
        print("\n===== SMART FILE ORGANIZER =====")
        print("1. Organize files (preview or move)")
        print("2. Show file summary")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            organize_folder(folder)
        elif choice == "2":
            show_summary(folder)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")