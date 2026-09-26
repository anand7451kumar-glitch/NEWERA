import hashlib

file = input("File path: ")

try:
    with open(file, "rb") as f:
        data = f.read()

    hash_value = hashlib.sha256(data).hexdigest()

    print("SHA-256:", hash_value)

except FileNotFoundError:
    print("File not found")