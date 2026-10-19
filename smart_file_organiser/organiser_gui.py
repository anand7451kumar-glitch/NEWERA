import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt"],
    "Videos": [".mp4", ".mov", ".mkv"],
    "Audio": [".mp3", ".wav", ".m4a"],
    "Code": [".py", ".cpp", ".c", ".js", ".html", ".css"],
    "Archives": [".zip", ".rar", ".7z"],
}


def get_category(filename):
    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"


class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("750x550")
        self.root.configure(bg="#172033")

        self.folder_path = tk.StringVar()

        tk.Label(
            root,
            text="SMART FILE ORGANIZER",
            font=("Arial", 22, "bold"),
            bg="#172033",
            fg="#4ade80",
        ).pack(pady=15)

        folder_frame = tk.Frame(root, bg="#172033")
        folder_frame.pack(fill="x", padx=20)

        tk.Entry(
            folder_frame,
            textvariable=self.folder_path,
            font=("Arial", 11),
            width=48,
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            folder_frame,
            text="Choose Folder",
            command=self.choose_folder,
        ).pack(side="left")

        button_frame = tk.Frame(root, bg="#172033")
        button_frame.pack(pady=15)

        buttons = [
            ("Preview", self.preview),
            ("Organize Files", self.organize),
            ("Summary", self.summary),
            ("Clear", self.clear),
        ]

        for text, command in buttons:
            tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                padx=10,
                pady=7,
            ).pack(side="left", padx=5)

        self.output = scrolledtext.ScrolledText(
            root,
            width=85,
            height=20,
            font=("Menlo", 10),
            bg="#0f172a",
            fg="white",
            insertbackground="white",
        )
        self.output.pack(padx=20, pady=(0, 15), fill="both", expand=True)

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Select a folder")

        if folder:
            self.folder_path.set(folder)
            self.write(f"Selected folder: {folder}\n")

    def get_files(self):
        folder = self.folder_path.get().strip()

        if not os.path.isdir(folder):
            messagebox.showerror("Error", "Please choose a valid folder.")
            return None

        files = []

        for filename in os.listdir(folder):
            source = os.path.join(folder, filename)

            if os.path.isfile(source):
                files.append((filename, source, get_category(filename)))

        return folder, files

    def write(self, text):
        self.output.insert("end", text + "\n")
        self.output.see("end")

    def clear(self):
        self.output.delete("1.0", "end")

    def preview(self):
        result = self.get_files()

        if result is None:
            return

        folder, files = result
        self.write("\n--- PREVIEW ---")

        for filename, source, category in files:
            destination = os.path.join(folder, category, filename)

            if os.path.exists(destination):
                self.write(f"SKIP: {filename} (destination exists)")
            else:
                self.write(f"{filename} -> {category}/")

        self.write(f"Preview complete. {len(files)} files checked.")

    def organize(self):
        result = self.get_files()

        if result is None:
            return

        folder, files = result

        if not files:
            self.write("No files to organize.")
            return

        if not messagebox.askyesno(
            "Confirm",
            f"Organize {len(files)} files in this folder?\n\n"
            "Files will be moved into category folders.",
        ):
            return

        moved = 0
        skipped = 0

        for filename, source, category in files:
            destination_folder = os.path.join(folder, category)
            destination = os.path.join(destination_folder, filename)

            if os.path.exists(destination):
                self.write(f"SKIPPED: {filename}")
                skipped += 1
                continue

            try:
                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(source, destination)
                self.write(f"MOVED: {filename} -> {category}/")
                moved += 1
            except OSError as error:
                self.write(f"ERROR: {filename}: {error}")
                skipped += 1

        self.write(f"\nFinished: {moved} moved, {skipped} skipped.")

    def summary(self):
        result = self.get_files()

        if result is None:
            return

        folder, files = result
        counts = {category: 0 for category in CATEGORIES}
        counts["Other"] = 0

        for filename, source, category in files:
            counts[category] += 1

        self.write("\n--- FILE SUMMARY ---")

        for category, count in counts.items():
            self.write(f"{category}: {count}")

        self.write(f"Total files: {len(files)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizer(root)
    root.mainloop()