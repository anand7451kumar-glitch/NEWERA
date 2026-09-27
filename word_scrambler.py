import random

words = ["python", "coding", "github", "developer", "algorithm"]

word = random.choice(words)
scrambled = list(word)
random.shuffle(scrambled)

print("Guess the word:", "".join(scrambled))

answer = input("Your answer: ")

if answer.lower() == word:
    print("Correct!")
else:
    print("Wrong. The word was:", word)