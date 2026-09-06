import json
import os

FILE_NAME = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    expense = {
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully.")


def show_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    print("\n--- All Expenses ---")

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"₹{expense['amount']:.2f}"
        )


def show_total(expenses):
    total = sum(expense["amount"] for expense in expenses)

    print(f"\nTotal expenses: ₹{total:.2f}")


def show_category_summary(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    summary = {}

    for expense in expenses:
        category = expense["category"]
        summary[category] = summary.get(category, 0) + expense["amount"]

    print("\n--- Category Summary ---")

    for category, amount in summary.items():
        print(f"{category}: ₹{amount:.2f}")


def delete_expense(expenses):
    show_expenses(expenses)

    if not expenses:
        return

    try:
        index = int(input("\nEnter expense number to delete: "))
    except ValueError:
        print("Invalid number.")
        return

    if index < 1 or index > len(expenses):
        print("Invalid expense number.")
        return

    removed = expenses.pop(index - 1)
    save_expenses(expenses)

    print(
        f"Deleted: {removed['description']} "
        f"(₹{removed['amount']:.2f})"
    )


def main():
    expenses = load_expenses()

    while True:
        print("\n========================")
        print("      EXPENSE TRACKER")
        print("========================")
        print("1. Add expense")
        print("2. Show expenses")
        print("3. Show total")
        print("4. Category summary")
        print("5. Delete expense")
        print("6. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            show_expenses(expenses)

        elif choice == "3":
            show_total(expenses)

        elif choice == "4":
            show_category_summary(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
