import datetime

expenses = []

def add_expense(amount, category):
    expenses.append({
        "amount": amount,
        "category": category,
        "date": datetime.date.today()
    })

def show_summary():
    total = sum(e["amount"] for e in expenses)
    print(f"Total spent: ₹{total}")
    for category in set(e["category"] for e in expenses):
        cat_total = sum(e["amount"] for e in expenses if e["category"] == category)
        print(f"{category}: ₹{cat_total}")

# Example usage
add_expense(200, "Food")
add_expense(100, "Transport")
show_summary()