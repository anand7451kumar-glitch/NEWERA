from collections import Counter
import re

def analyze_text(text; str) -> Counter:
  words = re.findall(r"\b[a-zA-Z]+\b" , text.lower())
                     return Counter(words)

text = input("Enter a sentence: " )

frequency = analyze_text(text)

print("\nWord frequencies:")
for word, count in frequency.most_common():
print(f"{word}: {count}")
