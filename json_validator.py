import json

file = input("JSON file: ")

try:
    with open(file) as f:
        json.load(f)
    print("Valid JSON")

except json.JSONDecodeError as e:
    print("Invalid JSON")
    print("Error:", e)

except FileNotFoundError:
    print("File not found")
