import json
from pathlib import Path

FILE = Path("contacts.json")


def load_contacts():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return {}


def save_contacts(contacts):
    FILE.write_text(json.dumps(contacts, indent=4))


contacts = load_contacts()

while True:
    print("\n===== CONTACT BOOK =====")
    print("1. Add contact")
    print("2. Search contact")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Show all contacts")
    print("6. Exit")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")

        contacts[name] = {
            "phone": phone,
            "email": email
        }

        save_contacts(contacts)
        print("Contact saved!")

    elif choice == "2":
        name = input("Enter name: ")

        if name in contacts:
            print("Phone:", contacts[name]["phone"])
            print("Email:", contacts[name]["email"])
        else:
            print("Contact not found.")

    elif choice == "3":
        name = input("Enter name: ")

        if name in contacts:
            contacts[name]["phone"] = input("New phone: ")
            contacts[name]["email"] = input("New email: ")
            save_contacts(contacts)
            print("Contact updated!")
        else:
            print("Contact not found.")

    elif choice == "4":
        name = input("Enter name: ")

        if name in contacts:
            del contacts[name]
            save_contacts(contacts)
            print("Contact deleted!")
        else:
            print("Contact not found.")

    elif choice == "5":
        if not contacts:
            print("No contacts.")
        else:
            for name, info in contacts.items():
                print(f"{name}: {info['phone']} | {info['email']}")

    elif choice == "6":
        break

    else:
        print("Invalid choice.")