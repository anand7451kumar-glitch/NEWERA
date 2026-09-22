from collections import Counter
import re

text = input("Enter your text:\n")

words = re.findall(r"\b[a-zA]+\b", text.lower())

counter = Counter(words)

print("\n==== TEXT ANALYSIS =====")
print("Characters:", len(text))
print("Words:", len(words))
print("Unique words:", len(counter))

if words:
    print("Most common words:")

    for word, count in counter.most_common(5):
        print(f"{word}: {count}")
    reading_time = len(words) / 200
    print("Reading time:", round(reading_time, 2), "minutes")
