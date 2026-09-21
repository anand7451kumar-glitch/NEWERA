from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path("secret.key")
DATA_FILE = Path("secret.txt")

def get_key():
    if not KEY_FILE.exists():
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
    return KEY_FILE.read_bytes()

key = get_key()
cipher = Fernet(key)

print("1. Encrypt text")
print("2. Decrypt text")

choice = input("Choose: ")

if choice == "1":
    text = input("Enter secret text: ")

    encrypted = cipher.encrypt(text.encode())
    DATA_FILE.write_bytes(encrypted)

    print("Text encrypted and saved.")

elif choice == "2":
    if DATA_FILE.exists():
        encrypted = DATA_FILE.read_bytes()
        decrypted = cipher.decrypt(encrypted).decode()

        print("Decrypted text:", decrypted)
    else:
        print("No encrypted data found.")

else:
    print("Invalid choice.")



