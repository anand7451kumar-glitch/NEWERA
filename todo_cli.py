tasks = []

while True:
    print("\n1. Add 2. View 3. Remove 4. Exit")
    choice = input("Choose: ")

    if choice == "1":
        tasks.append(input("Task: "))

    elif choice == "2":
        for i, task in enumerate(tasks, 1):
            print(i, task)

    elif choice == "3":
        n = int(input("Task number: "))
        tasks.pop(n - 1)

    elif choice == "4":
        break