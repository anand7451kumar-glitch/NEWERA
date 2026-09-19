import subprocess

text = subprocess.check_output(
    ["pbpaste"]
).decode()

words = len(text.split())
characters = len(text)

print("Clipboard:")
print(text)
print("\nWords:", words)
print("Characters:", characters)
