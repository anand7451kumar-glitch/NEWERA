import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime
from collections import defaultdict

import matplotlib.pyplot as plt


# ==================== CONFIGURATION ====================

DB_NAME = "expenses.db"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Education",
    "Entertainment",
    "Bills",
    "Other"
]


# ==================== DATABASE ====================

connection = sqlite3.connect(DB_NAME)

connection.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT
)
""")

connection.execute("""
CREATE TABLE IF NOT EXISTS budgets (
    month TEXT PRIMARY KEY,
    amount REAL NOT NULL
)
""")

connection.commit()


# ==================== HELPER FUNCTIONS ====================

def current_month():
    return date.today().strftime("%Y-%m")


def get_monthly_total(month):
    result = connection.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
    """, (month,)).fetchone()

    return result[0]


def get_expenses():
    return connection.execute("""
        SELECT id, expense_date, amount, category, description
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """).fetchall()


# ==================== BUDGET ====================

def save_budget():
    try:
        amount = float(budget_entry.get())

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid budget",
            "Enter a valid budget greater than zero."
        )
        return

    month = current_month()

    connection.execute("""
        INSERT INTO budgets (month, amount)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET amount = excluded.amount
    """, (month, amount))

    connection.commit()
    refresh_budget()

    messagebox.showinfo(
        "Budget saved",
        f"Your budget for {month} is ₹{amount:.2f}."
    )


def refresh_budget():
    month = current_month()

    result = connection.execute(
        "SELECT amount FROM budgets WHERE month = ?",
        (month,)
    ).fetchone()

    spent = get_monthly_total(month)

    if result is None:
        budget_label.config(
            text=f"This month: ₹{spent:.2f} spent | No budget set",
            fg="black"
        )
        return

    budget = result[0]
    remaining = budget - spent

    if remaining < 0:
        status = f"Over budget by ₹{-remaining:.2f}"
        color = "red"
    else:
        status = f"₹{remaining:.2f} remaining"
        color = "green"

    budget_label.config(
        text=(
            f"Budget: ₹{budget:.2f}  |  "
            f"Spent: ₹{spent:.2f}  |  {status}"
        ),
        fg=color
    )


# ==================== ADD EXPENSE ====================

def add_expense():
    try:
        expense_date = date.fromisoformat(
            date_entry.get().strip()
        ).isoformat()

        amount = float(amount_entry.get())

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid input",
            "Enter a valid date (YYYY-MM-DD) and an amount greater than zero."
        )
        return

    category = category_box.get()

    if category not in CATEGORIES:
        messagebox.showerror(
            "Invalid category",
            "Please select a category."
        )
        return

    description = description_entry.get().strip()

    connection.execute("""
        INSERT INTO expenses
        (expense_date, amount, category, description)
        VALUES (?, ?, ?, ?)
    """, (expense_date, amount, category, description))

    connection.commit()

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    refresh_expenses()

    messagebox.showinfo(
        "Expense added",
        f"Recorded ₹{amount:.2f} under {category}."
    )


# ==================== SEARCH AND FILTER ====================

def search_expenses():
    keyword = search_entry.get().strip()
    category = search_category.get()
    month = search_month.get().strip()

    if month:
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            messagebox.showerror(
                "Invalid month",
                "Enter the month as YYYY-MM, for example 2026-10."
            )
            return

    query = """
        SELECT id, expense_date, amount, category, description
        FROM expenses
        WHERE COALESCE(description, '') LIKE ?
    """

    params = [f"%{keyword}%"]

    if category != "All":
        query += " AND category = ?"
        params.append(category)

    if month:
        query += " AND substr(expense_date, 1, 7) = ?"
        params.append(month)

    query += " ORDER BY expense_date DESC, id DESC"

    expenses = connection.execute(query, params).fetchall()

    display_expenses(expenses, filtered=True)


def display_expenses(expenses, filtered=False):
    for item in expense_table.get_children():
        expense_table.delete(item)

    total = 0

    for expense in expenses:
        expense_id, expense_date, amount, category, description = expense

        expense_table.insert(
            "",
            tk.END,
            values=(
                expense_id,
                expense_date,
                f"₹{amount:.2f}",
                category,
                description or ""
            )
        )

        total += amount

    if filtered:
        total_label.config(
            text=f"Filtered total: ₹{total:.2f}  |  {len(expenses)} expenses"
        )
    else:
        total_label.config(
            text=f"Total recorded: ₹{total:.2f}  |  {len(expenses)} expenses"
        )


def show_all_expenses():
    search_entry.delete(0, tk.END)
    search_category.set("All")
    search_month.delete(0, tk.END)

    refresh_expenses()


# ==================== REFRESH TABLE ====================

def refresh_expenses():
    display_expenses(get_expenses())
    refresh_budget()


# ==================== DELETE EXPENSE ====================

def delete_expense():
    selected = expense_table.selection()

    if not selected:
        messagebox.showinfo(
            "Select an expense",
            "Select an expense from the table first."
        )
        return

    values = expense_table.item(selected[0], "values")
    expense_id = values[0]

    confirm = messagebox.askyesno(
        "Confirm deletion",
        "Are you sure you want to delete this expense?"
    )

    if not confirm:
        return

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()

    refresh_expenses()


# ==================== CHART ====================

def show_chart():
    expenses = get_expenses()

    if not expenses:
        messagebox.showinfo(
            "No expenses",
            "Add some expenses before viewing the chart."
        )
        return

    totals = defaultdict(float)

    for expense in expenses:
        category = expense[3]
        amount = expense[2]
        totals[category] += amount

    plt.figure(figsize=(9, 5))

    plt.bar(totals.keys(), totals.values())

    plt.title("MoneyMap - Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()


# ==================== CSV EXPORT ====================

def export_expenses():
    expenses = get_expenses()

    if not expenses:
        messagebox.showinfo(
            "No expenses",
            "There are no expenses to export."
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="Export MoneyMap Expenses",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="moneymap_expenses.csv"
    )

    if not file_path:
        return

    try:
        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Date",
                "Amount (INR)",
                "Category",
                "Description"
            ])

            writer.writerows(expenses)

        messagebox.showinfo(
            "Export successful",
            f"Your expenses were exported to:\n{file_path}"
        )

    except OSError as error:
        messagebox.showerror(
            "Export failed",
            str(error)
        )


# ==================== CLOSE APPLICATION ====================

def close_app():
    connection.close()
    root.destroy()


# ==================== USER INTERFACE ====================

root = tk.Tk()

root.title("MoneyMap - Personal Expense Tracker")
root.geometry("1100x720")
root.minsize(900, 600)

heading = tk.Label(
    root,
    text="MONEYMAP",
    font=("Arial", 25, "bold")
)
heading.pack(pady=(12, 4))

subtitle = tk.Label(
    root,
    text="Track your spending. Control your budget.",
    font=("Arial", 11)
)
subtitle.pack(pady=(0, 8))


# Budget section

budget_frame = tk.LabelFrame(
    root,
    text="Monthly Budget",
    padx=10,
    pady=8
)
budget_frame.pack(fill="x", padx=15, pady=5)

tk.Label(
    budget_frame,
    text="Budget (₹):"
).pack(side="left", padx=5)

budget_entry = tk.Entry(budget_frame, width=15)
budget_entry.pack(side="left", padx=5)

tk.Button(
    budget_frame,
    text="Save Budget",
    command=save_budget
).pack(side="left", padx=5)

budget_label = tk.Label(
    budget_frame,
    text="Set your monthly budget",
    font=("Arial", 11, "bold")
)
budget_label.pack(side="left", padx=15)


# Add expense section

form = tk.LabelFrame(
    root,
    text="Add New Expense",
    padx=8,
    pady=8
)
form.pack(fill="x", padx=15, pady=5)

tk.Label(form, text="Date (YYYY-MM-DD)").grid(
    row=0, column=0, padx=5, pady=4
)

date_entry = tk.Entry(form, width=14)
date_entry.insert(0, date.today().isoformat())
date_entry.grid(row=1, column=0, padx=5)

tk.Label(form, text="Amount (₹)").grid(
    row=0, column=1, padx=5, pady=4
)

amount_entry = tk.Entry(form, width=13)
amount_entry.grid(row=1, column=1, padx=5)

tk.Label(form, text="Category").grid(
    row=0, column=2, padx=5, pady=4
)

category_box = ttk.Combobox(
    form,
    values=CATEGORIES,
    state="readonly",
    width=15
)
category_box.set("Food")
category_box.grid(row=1, column=2, padx=5)

tk.Label(form, text="Description").grid(
    row=0, column=3, padx=5, pady=4
)

description_entry = tk.Entry(form, width=25)
description_entry.grid(row=1, column=3, padx=5)

tk.Button(
    form,
    text="Add Expense",
    command=add_expense
).grid(row=1, column=4, padx=8)


# Search and filter section

search_frame = tk.LabelFrame(
    root,
    text="Search and Filter",
    padx=8,
    pady=8
)
search_frame.pack(fill="x", padx=15, pady=5)

tk.Label(search_frame, text="Description:").pack(
    side="left", padx=4
)

search_entry = tk.Entry(search_frame, width=17)
search_entry.pack(side="left", padx=4)

tk.Label(search_frame, text="Category:").pack(
    side="left", padx=4
)

search_category = ttk.Combobox(
    search_frame,
    values=["All"] + CATEGORIES,
    state="readonly",
    width=13
)
search_category.set("All")
search_category.pack(side="left", padx=4)

tk.Label(search_frame, text="Month (YYYY-MM):").pack(
    side="left", padx=4
)

search_month = tk.Entry(search_frame, width=10)
search_month.pack(side="left", padx=4)

tk.Button(
    search_frame,
    text="Search",
    command=search_expenses
).pack(side="left", padx=4)

tk.Button(
    search_frame,
    text="Show All",
    command=show_all_expenses
).pack(side="left", padx=4)


# Expense table

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=15, pady=8)

columns = (
    "ID",
    "Date",
    "Amount",
    "Category",
    "Description"
)

expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:
    expense_table.heading(column, text=column)

expense_table.column("ID", width=55, anchor="center")
expense_table.column("Date", width=120, anchor="center")
expense_table.column("Amount", width=130, anchor="e")
expense_table.column("Category", width=150, anchor="center")
expense_table.column("Description", width=350)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=expense_table.yview
)

expense_table.configure(yscrollcommand=scrollbar.set)

expense_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Total

total_label = tk.Label(
    root,
    text="Total recorded: ₹0.00",
    font=("Arial", 14, "bold")
)
total_label.pack(pady=5)


# Action buttons

buttons = tk.Frame(root)
buttons.pack(pady=(5, 12))

tk.Button(
    buttons,
    text="Delete Selected",
    command=delete_expense
).pack(side="left", padx=6)

tk.Button(
    buttons,
    text="View Spending Chart",
    command=show_chart
).pack(side="left", padx=6)

tk.Button(
    buttons,
    text="Export to CSV",
    command=export_expenses
).pack(side="left", padx=6)

tk.Button(
    buttons,
    text="Exit",
    command=close_app
).pack(side="left", padx=6)


# Start application

root.protocol("WM_DELETE_WINDOW", close_app)

refresh_expenses()

root.mainloop()