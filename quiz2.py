import random

questions = [
    {
        "question": "What is the capital of India?",
        "options": ["A. Mumbai", "B. Delhi", "C. Kolkata", "D. Chennai"],
        "answer": "B"
    },
    {
        "question": "Which is the largest planet in our Solar System?",
        "options": ["A. Earth", "B. Mars", "C. Jupiter", "D. Saturn"],
        "answer": "C"
    },
    {
        "question": "How many continents are there?",
        "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
        "answer": "C"
    },
    {
        "question": "Who wrote the national anthem of India?",
        "options": [
            "A. Rabindranath Tagore",
            "B. Mahatma Gandhi",
            "C. Bankim Chandra Chattopadhyay",
            "D. Sarojini Naidu"
        ],
        "answer": "A"
    },
    {
        "question": "Which gas do humans need for respiration?",
        "options": ["A. Carbon dioxide", "B. Oxygen", "C. Nitrogen", "D. Hydrogen"],
        "answer": "B"
    },
    {
        "question": "What is the boiling point of water at sea level?",
        "options": ["A. 50°C", "B. 75°C", "C. 100°C", "D. 150°C"],
        "answer": "C"
    },
    {
        "question": "Which programming language is known for its simplicity and readability?",
        "options": ["A. Python", "B. Assembly", "C. Machine Code", "D. COBOL"],
        "answer": "A"
    },
    {
        "question": "How many sides does a hexagon have?",
        "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
        "answer": "B"
    },
    {
        "question": "Which is the fastest land animal?",
        "options": ["A. Lion", "B. Horse", "C. Cheetah", "D. Tiger"],
        "answer": "C"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["A. Ag", "B. Gd", "C. Go", "D. Au"],
        "answer": "D"
    },
    {
        "question": "Which ocean is the largest?",
        "options": ["A. Atlantic", "B. Indian", "C. Pacific", "D. Arctic"],
        "answer": "C"
    },
    {
        "question": "How many days are there in a leap year?",
        "options": ["A. 364", "B. 365", "C. 366", "D. 367"],
        "answer": "C"
    },
    {
        "question": "Which organ pumps blood through the human body?",
        "options": ["A. Brain", "B. Heart", "C. Liver", "D. Kidney"],
        "answer": "B"
    },
    {
        "question": "What is 12 × 12?",
        "options": ["A. 124", "B. 132", "C. 144", "D. 154"],
        "answer": "C"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["A. China", "B. Japan", "C. Korea", "D. Thailand"],
        "answer": "B"
    }
]

random.shuffle(questions)

score = 0

print("=" * 40)
print("        GENERAL KNOWLEDGE QUIZ")
print("=" * 40)

for number, q in enumerate(questions, 1):
    print(f"\nQuestion {number}: {q['question']}")

    for option in q["options"]:
        print(option)

    answer = input("Your answer (A/B/C/D): ").upper()

    if answer == q["answer"]:
        print("✅ Correct!")
        score += 1
    else:
        print("❌ Wrong!")
        print("Correct answer:", q["answer"])

print("\n" + "=" * 40)
print("QUIZ COMPLETE")
print("=" * 40)

print("Score:", score, "/", len(questions))
print("Percentage:", round(score / len(questions) * 100, 2), "%")

if score == len(questions):
    print("🏆 Perfect score!")
elif score >= len(questions) * 0.7:
    print("🔥 Great job!")
elif score >= len(questions) * 0.5:
    print("👍 Good effort!")
else:
    print("📚 Keep practicing!")
