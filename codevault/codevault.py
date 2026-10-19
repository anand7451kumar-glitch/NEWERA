import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_FILE = "codevault.db"

BG = "#0A0A0A"
PANEL = "#006aff"
GREEN = "#4ade80"
TEXT = "#454572"


class CodeVault:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeVault - Snippet Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG)

        self.connection = sqlite3.connect(DB_FILE)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                language TEXT NOT NULL,
                description TEXT,
                code TEXT NOT NULL
            )
        """)
        self.connection.commit()

        self.build_ui()
        self.load_snippets()

    def build_ui(self):
        tk.Label(
            self.root,
            text="CODEVAULT",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=GREEN
        ).pack(pady=(15, 2))

        tk.Label(
            self.root,
            text="Your personal code library",
            font=("Arial", 11),
            bg=BG,
            fg=TEXT
        ).pack(pady=(0, 15))

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=15, pady=5)

        left = tk.Frame(main, bg=PANEL, width=300)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        tk.Label(
            left, text="SAVED SNIPPETS",
            bg=PANEL, fg=GREEN,
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        self.search_var = tk.StringVar()

        search = tk.Entry(
            left,
            textvariable=self.search_var,
            font=("Arial", 11)
        )
        search.pack(fill="x", padx=10, pady=5)
        search.bind("<KeyRelease>", lambda event: self.load_snippets())

        self.snippet_list = tk.Listbox(
            left,
            bg=BG,
            fg=TEXT,
            selectbackground=GREEN,
            selectforeground=BG,
            font=("Arial", 11),
            borderwidth=0
        )
        self.snippet_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.snippet_list.bind("<<ListboxSelect>>", self.select_snippet)

        right = tk.Frame(main, bg=PANEL)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(
            right, text="SNIPPET DETAILS",
            bg=PANEL, fg=GREEN,
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        form = tk.Frame(right, bg=PANEL)
        form.pack(fill="x", padx=15)

        tk.Label(form, text="Title", bg=PANEL, fg=TEXT).grid(
            row=0, column=0, sticky="w", pady=5
        )

        self.title_entry = tk.Entry(form, font=("Arial", 11))
        self.title_entry.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(form, text="Language", bg=PANEL, fg=TEXT).grid(
            row=1, column=0, sticky="w", pady=5
        )

        self.language = ttk.Combobox(
            form,
            values=["Python", "C++", "Java", "JavaScript", "C", "Other"],
            state="readonly"
        )
        self.language.set("Python")
        self.language.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(form, text="Description", bg=PANEL, fg=TEXT).grid(
            row=2, column=0, sticky="w", pady=5
        )

        self.description_entry = tk.Entry(form, font=("Arial", 11))
        self.description_entry.grid(row=2, column=1, sticky="ew", pady=5)

        form.columnconfigure(1, weight=1)

        tk.Label(
            right, text="Code",
            bg=PANEL, fg=TEXT
        ).pack(anchor="w", padx=15, pady=(10, 3))

        self.code_text = tk.Text(
            right,
            bg=BG,
            fg=TEXT,
            insertbackground=TEXT,
            font=("Menlo", 11),
            wrap="none",
            height=15
        )
        self.code_text.pack(fill="both", expand=True, padx=15, pady=5)

        buttons = tk.Frame(right, bg=PANEL)
        buttons.pack(pady=12)

        actions = [
            ("Save New", self.save_snippet),
            ("Update", self.update_snippet),
            ("Delete", self.delete_snippet),
            ("Copy Code", self.copy_code),
            ("Clear", self.clear_form)
        ]

        for label, action in actions:
            tk.Button(
                buttons,
                text=label,
                command=action,
                bg=GREEN if label == "Save New" else "#374151",
                fg=BG if label == "Save New" else TEXT,
                font=("Arial", 9, "bold"),
                padx=8
            ).pack(side="left", padx=3)

        self.selected_id = None

    def load_snippets(self):
        search = self.search_var.get().strip()

        rows = self.connection.execute("""
            SELECT id, title, language
            FROM snippets
            WHERE title LIKE ? OR language LIKE ?
            ORDER BY title COLLATE NOCASE
        """, (f"%{search}%", f"%{search}%")).fetchall()

        self.snippet_list.delete(0, tk.END)
        self.visible_ids = []

        for snippet_id, title, language in rows:
            self.snippet_list.insert(
                tk.END, f"{title} [{language}]"
            )
            self.visible_ids.append(snippet_id)

    def select_snippet(self, event=None):
        selection = self.snippet_list.curselection()

        if not selection:
            return

        self.selected_id = self.visible_ids[selection[0]]

        row = self.connection.execute("""
            SELECT title, language, description, code
            FROM snippets WHERE id = ?
        """, (self.selected_id,)).fetchone()

        if row:
            title, language, description, code = row

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)

            self.language.set(language)

            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, description or "")

            self.code_text.delete("1.0", tk.END)
            self.code_text.insert("1.0", code)

    def save_snippet(self):
        title = self.title_entry.get().strip()
        language = self.language.get()
        description = self.description_entry.get().strip()
        code = self.code_text.get("1.0", "end-1c")

        if not title or not code.strip():
            messagebox.showwarning(
                "Missing information",
                "Enter a title and some code."
            )
            return

        self.connection.execute("""
            INSERT INTO snippets (title, language, description, code)
            VALUES (?, ?, ?, ?)
        """, (title, language, description, code))

        self.connection.commit()
        self.load_snippets()
        messagebox.showinfo("Saved", "Snippet saved successfully!")
        self.clear_form()

    def update_snippet(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No selection",
                "Select a saved snippet first."
            )
            return

        title = self.title_entry.get().strip()
        language = self.language.get()
        description = self.description_entry.get().strip()
        code = self.code_text.get("1.0", "end-1c")

        if not title or not code.strip():
            messagebox.showwarning(
                "Missing information",
                "Enter a title and some code."
            )
            return

        self.connection.execute("""
            UPDATE snippets
            SET title = ?, language = ?, description = ?, code = ?
            WHERE id = ?
        """, (
            title, language, description, code, self.selected_id
        ))

        self.connection.commit()
        self.load_snippets()
        messagebox.showinfo("Updated", "Snippet updated successfully!")

    def delete_snippet(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No selection",
                "Select a saved snippet first."
            )
            return

        if not messagebox.askyesno(
            "Confirm deletion",
            "Delete this snippet permanently?"
        ):
            return

        self.connection.execute(
            "DELETE FROM snippets WHERE id = ?",
            (self.selected_id,)
        )
        self.connection.commit()
        self.clear_form()
        self.load_snippets()

    def copy_code(self):
        code = self.code_text.get("1.0", "end-1c")

        if not code.strip():
            messagebox.showwarning("Empty", "There is no code to copy.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        messagebox.showinfo("Copied", "Code copied to clipboard!")

    def clear_form(self):
        self.selected_id = None
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.language.set("Python")
        self.code_text.delete("1.0", tk.END)
        self.snippet_list.selection_clear(0, tk.END)

    def close(self):
        self.connection.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeVault(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()