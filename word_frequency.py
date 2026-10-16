from collections import Counter
import re

text = input("Enter a sentence or paragraph: ").lower()

words = re.findall(r"\b[a-z0-9']+\b", text)
frequencies = Counter(words)

print("\nWord frequencies:")

for word, count in frequencies.most_common():
    print(f"{word}: {count}")

print(f"\nTotal words: {len(words)}")
print(f"Unique words: {len(frequencies)}")
