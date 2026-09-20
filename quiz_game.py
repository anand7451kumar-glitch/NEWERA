import random

questions = [
    ("What's capital of India?", "delhi"),
    ("What's 5 * 6?", "30"),
    ("Which language is used for web pages?", "html"),
    ("How many bits are in 1 Byte?", "8")
]

random.shuffle(questions)

score = 0

print("=== QUIZ GAME ===")

for question, answer in questions:
    user_answer = input(question + " ")

    if user_answer.lower() == answer:
        print("Correct!")
        score += 1

    else:
        print("Wrong! Amswer:", answer)

print("\nQuiz finished!")
print("Score: ", score, " / ", len(questions))
print("Percentage:", round(score / len(questions) * 100, 2), "%")

