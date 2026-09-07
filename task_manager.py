tasks = []

def add_task():
    title = input("Enter task: ").strip()

    if not title:
        print("Task cannot be empty.")
        return

    task = {
        "title": title,
        "completed": False
    }

    tasks.append(task)
    print("Task added successfully.")


def show_tasks():
    if not tasks:
        print("No tasks available.")
        return

    print("\n--- Tasks ---")

    for i, task in enumerate(tasks, 1):
        status = "Done" if task["completed"] else "Pending"
        print(f"{i}. {task['title']} - {status}")

def complete_task():
    show_tasks()

    if not tasks:
        return

    try:
        number = int(input("Enter task number: "))
        task = tasks[number - 1]

        task["completed"] = True
        print("Task marked as completed. ")

    except (ValueError, IndexError):
        print("Invalid task number.")


def delete_task():
    show_tasks()

    if not tasks:
        return

    try:
        number = int(input("Enter task number: "))
        removed = tasks.pop(number - 1)

        print(f"Deleted: {removed['title']}")

    except (ValueError, IndexError):
        print("Invalid task number.")

def main():
    while True:
        print("\n===== TASK MANAGER ======")
        print("1. Add task")
        print("2. Show tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_task()

        elif choice == "2":
            show_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    main()
