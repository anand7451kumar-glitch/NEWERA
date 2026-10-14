import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from collections import defaultdict
import matplotlib.pyplot as plt

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

# ---------------- DATABASE ----------------

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

connection.commit()
connection.execute("""
CREATE TABLE IF NOT EXISTS budgets (
    month TEXT PRIMARY KEY,
    amount REAL NOT NULL
)
""")

connection.commit()

def current_month():
    return date.today().strftime("%Y-%m")


def get_monthly_total(month):
    result = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
        """,
        (month,)
    ).fetchone()

    return result[0]


def save_budget():
    try:
        amount = float(budget_entry.get())

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid budget",
            "Enter a budget greater than zero."
        )
        return

    month = current_month()

    connection.execute(
        """
        INSERT INTO budgets (month, amount)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET amount = excluded.amount
        """,
        (month, amount)
    )

    connection.commit()
    refresh_budget()


def refresh_budget():
    month = current_month()

    result = connection.execute(
        "SELECT amount FROM budgets WHERE month = ?",
        (month,)
    ).fetchone()

    spent = get_monthly_total(month)

    if result is None:
        budget_label.config(
            text=f"This month: ₹{spent:.2f} spent | No budget set"
        )
        return

    budget = result[0]
    remaining = budget - spent

    if remaining < 0:
        status = f"OVER BUDGET by ₹{-remaining:.2f}"
    else:
        status = f"₹{remaining:.2f} remaining"

    budget_label.config(
        text=f"Monthly budget: ₹{budget:.2f} | "
             f"Spent: ₹{spent:.2f} | {status}"
    )

    if spent >= budget:
        budget_label.config(fg="red")
    else:
        budget_label.config(fg="green")


def add_expense():
    try:
        amount = float(amount_entry.get())

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid amount",
            "Enter an amount greater than zero."
        )
        return

    description = description_entry.get().strip()
    category = category_box.get()

    connection.execute(
        """
        INSERT INTO expenses
        (expense_date, amount, category, description)
        VALUES (?, ?, ?, ?)
        """,
        (date_entry.get(), amount, category, description)
    )

    connection.commit()

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    refresh_expenses()


def get_expenses():
    return connection.execute(
        """
        SELECT id, expense_date, amount, category, description
        FROM expenses
        ORDER BY expense_date DESC, id DESC
        """
    ).fetchall()


def refresh_expenses():
    for item in expense_table.get_children():
        expense_table.delete(item)

    expenses = get_expenses()
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
                description
            )
        )

        total += amount

    total_label.config(text=f"Total recorded: ₹{total:.2f}")
    refresh_budget()


def delete_expense():
    selected = expense_table.selection()

    if not selected:
        messagebox.showinfo(
            "Select an expense",
            "Choose an expense to delete."
        )
        return

    item = expense_table.item(selected[0])
    expense_id = item["values"][0]

    confirm = messagebox.askyesno(
        "Confirm deletion",
        "Delete this expense permanently?"
    )

    if confirm:
        connection.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        connection.commit()
        refresh_expenses()


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

    plt.figure(figsize=(8, 5))

    plt.bar(totals.keys(), totals.values())

    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()


# ---------------- INTERFACE ----------------

root = tk.Tk()
root.title("MoneyMap — Expense Tracker")
root.geometry("950x600")

heading = tk.Label(
    root,
    text="MONEYMAP",
    font=("Arial", 24, "bold")
)
heading.pack(pady=10)

budget_frame = tk.Frame(root)
budget_frame.pack(pady=5)

tk.Label(
    budget_frame,
    text="Monthly Budget (₹):"
).pack(side="left", padx=5)

budget_entry = tk.Entry(budget_frame, width=15)
budget_entry.pack(side="left", padx=5)

tk.Button(
    budget_frame,
    text="Save Budget",
    command=save_budget
).pack(side="left", padx=5)

budget_label = tk.Label(
    root,
    text="Set your monthly budget",
    font=("Arial", 12, "bold")
)
budget_label.pack(pady=5)

form = tk.Frame(root)
form.pack(pady=5)

tk.Label(form, text="Date (YYYY-MM-DD)").grid(
    row=0, column=0, padx=5, pady=5
)

date_entry = tk.Entry(form, width=15)
date_entry.insert(0, date.today().isoformat())
date_entry.grid(row=1, column=0, padx=5)

tk.Label(form, text="Amount (₹)").grid(
    row=0, column=1, padx=5, pady=5
)

amount_entry = tk.Entry(form, width=15)
amount_entry.grid(row=1, column=1, padx=5)

tk.Label(form, text="Category").grid(
    row=0, column=2, padx=5, pady=5
)

category_box = ttk.Combobox(
    form,
    values=CATEGORIES,
    state="readonly",
    width=17
)
category_box.set("Food")
category_box.grid(row=1, column=2, padx=5)

tk.Label(form, text="Description").grid(
    row=0, column=3, padx=5, pady=5
)

description_entry = tk.Entry(form, width=22)
description_entry.grid(row=1, column=3, padx=5)

tk.Button(
    form,
    text="Add Expense",
    command=add_expense
).grid(row=1, column=4, padx=8)

columns = (
    "ID",
    "Date",
    "Amount",
    "Category",
    "Description"
)

expense_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for column in columns:
    expense_table.heading(column, text=column)

expense_table.column("ID", width=50)
expense_table.column("Date", width=120)
expense_table.column("Amount", width=120)
expense_table.column("Category", width=150)
expense_table.column("Description", width=300)

expense_table.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

total_label = tk.Label(
    root,
    text="Total recorded: ₹0.00",
    font=("Arial", 16, "bold")
)
total_label.pack(pady=5)

buttons = tk.Frame(root)
buttons.pack(pady=10)

tk.Button(
    buttons,
    text="Delete Selected",
    command=delete_expense
).pack(side="left", padx=8)

tk.Button(
    buttons,
    text="View Spending Chart",
    command=show_chart
).pack(side="left", padx=8)

refresh_expenses()

root.mainloop()
