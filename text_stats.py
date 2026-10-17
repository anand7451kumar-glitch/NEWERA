import re

text = input("Enter some text: ").strip()

if not text:
    print("Please enter some text.")
else:
    words = re.findall(r"\b\w+\b", text)
    sentences = re.findall(r"[.!?]+", text)

    print("\n--- Text Statistics ---")
    print("Characters:", len(text))
    print("Characters without spaces:", len("".join(text.split())))
    print("Words:", len(words))
    print("Sentences:", len(sentences))
    print("Average word length:",
          round(sum(map(len, words)) / len(words), 2) if words else 0)