balance = 1300
history = []

def show_balance():
    print(f"\nBalance: ₹{balance}")

def deposit():
    global balance

    amount = float(input("Enter deposit amount: ₹"))

    if amount > 0:
        balance += amount
        history.append(f"Deposited ₹{amount:.2f}")
        print("Deposit successful!")
    else:
        print("Invalid amount.")

def withdraw():
    global balance

    amount = float(input("Enter withdrawal amount: ₹"))

    if amount <= 0:
        print("Invalid amount.")
    elif amount > balance:
        print("Insufficient balance.")

    else:
        balance -= amount
        history.append(f"Withdrew ₹{amount:.2f}")
        print("Withdrawal successful!")

def transactions():
    print("\n--- Transaction History ---")

    if not history:
        print("No transactions yet.")
    else:
        for item in history:
            print(item)

while True:
    print("\n===== ATM ======")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transaction History")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        show_balance()
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        transactions()
    elif choice == "5":
        print("Thank You!")
        break
    else:
        print("Invalid choioce.")
