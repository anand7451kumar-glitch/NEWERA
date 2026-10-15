import tkinter as tk
from tkinter import messagebox
import random
import json
import os

QUESTIONS = [
    {
        "question": "Which keyword defines a function in Python?",
        "options": ["func", "def", "function", "define"],
        "answer": "def",
        "category": "Python"
    },
    {
        "question": "What is the output of 2 ** 3?",
        "options": ["6", "8", "9", "5"],
        "answer": "8",
        "category": "Python"
    },
    {
        "question": "Which data structure stores key-value pairs?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer": "Dictionary",
        "category": "Python"
    },
    {
        "question": "What is the derivative of x²?",
        "options": ["x", "2x", "x²", "2"],
        "answer": "2x",
        "category": "Mathematics"
    },
    {
        "question": "What is the SI unit of electrical resistance?",
        "options": ["Volt", "Ampere", "Ohm", "Watt"],
        "answer": "Ohm",
        "category": "Science"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "answer": "Mars",
        "category": "General Knowledge"
    },
    {
        "question": "Which symbol starts a comment in Python?",
        "options": ["//", "#", "/*", "--"],
        "answer": "#",
        "category": "Python"
    },
    {
        "question": "What is 15% of 200?",
        "options": ["15", "20", "30", "45"],
        "answer": "30",
        "category": "Mathematics"
    },
    {
        "question": "Which gas do plants absorb during photosynthesis?",
        "options": ["Oxygen", "Nitrogen", "Hydrogen", "Carbon dioxide"],
        "answer": "Carbon dioxide",
        "category": "Science"
    },
    {
        "question": "Which language primarily structures a webpage?",
        "options": ["HTML", "Python", "C++", "SQL"],
        "answer": "HTML",
        "category": "Programming"
    }
]

SCORE_FILE = "scores.json"


class QuizMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizMaster")
        self.root.geometry("650x500")
        self.root.minsize(550, 450)

        self.score = 0
        self.question_number = 0
        self.time_left = 15
        self.timer_id = None
        self.questions = []

        self.root.configure(bg="#151923")

        self.title_label = tk.Label(
            root,
            text="QUIZMASTER",
            font=("Arial", 25, "bold"),
            fg="#61dafb",
            bg="#151923"
        )
        self.title_label.pack(pady=(20, 5))

        self.category_label = tk.Label(
            root,
            text="Choose a category and test yourself!",
            font=("Arial", 12),
            fg="white",
            bg="#151923"
        )
        self.category_label.pack(pady=5)

        self.category = tk.StringVar(value="All")

        self.category_menu = tk.OptionMenu(
            root,
            self.category,
            "All",
            "Python",
            "Mathematics",
            "Science",
            "General Knowledge",
            "Programming"
        )
        self.category_menu.config(
            font=("Arial", 11),
            bg="#252b3a",
            fg="white",
            highlightthickness=0
        )
        self.category_menu.pack(pady=8)

        self.start_button = tk.Button(
            root,
            text="START QUIZ",
            command=self.start_quiz,
            font=("Arial", 12, "bold"),
            bg="#61dafb",
            fg="#151923",
            padx=20,
            pady=8
        )
        self.start_button.pack(pady=10)

        self.question_label = tk.Label(
            root,
            text="",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#151923",
            wraplength=560
        )
        self.question_label.pack(pady=15)

        self.timer_label = tk.Label(
            root,
            text="",
            font=("Arial", 12, "bold"),
            fg="#f7c66b",
            bg="#151923"
        )
        self.timer_label.pack()

        self.options_frame = tk.Frame(root, bg="#151923")
        self.options_frame.pack(pady=10)

        self.option_buttons = []

        for _ in range(4):
            button = tk.Button(
                self.options_frame,
                text="",
                width=38,
                font=("Arial", 11),
                bg="#252b3a",
                fg="white",
                activebackground="#39445c",
                activeforeground="white",
                command=lambda: None
            )
            button.pack(pady=4)
            self.option_buttons.append(button)

        self.feedback_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            fg="#61dafb",
            bg="#151923"
        )
        self.feedback_label.pack(pady=5)

        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#151923"
        )
        self.score_label.pack()

        self.leaderboard_button = tk.Button(
            root,
            text="VIEW LEADERBOARD",
            command=self.show_leaderboard,
            bg="#39445c",
            fg="white"
        )
        self.leaderboard_button.pack(pady=10)

        self.set_options_state("disabled")

    def set_options_state(self, state):
        for button in self.option_buttons:
            button.config(state=state)

    def start_quiz(self):
        self.cancel_timer()

        selected_category = self.category.get()

        available = [
            q for q in QUESTIONS
            if selected_category == "All"
            or q["category"] == selected_category
        ]

        if not available:
            messagebox.showinfo("QuizMaster", "No questions available.")
            return

        self.questions = random.sample(
            available, min(5, len(available))
        )

        self.score = 0
        self.question_number = 0
        self.score_label.config(text="Score: 0")
        self.start_button.config(state="disabled")
        self.category_menu.config(state="disabled")

        self.show_question()

    def show_question(self):
        self.cancel_timer()

        if self.question_number >= len(self.questions):
            self.finish_quiz()
            return

        question = self.questions[self.question_number]

        self.time_left = 15
        self.feedback_label.config(text="")
        self.question_label.config(
            text=f"Q{self.question_number + 1}. {question['question']}"
        )

        options = question["options"][:]
        random.shuffle(options)

        for button, option in zip(self.option_buttons, options):
            button.config(
                text=option,
                state="normal",
                command=lambda answer=option: self.check_answer(answer)
            )

        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")

        if self.time_left <= 0:
            self.feedback_label.config(text="Time's up!")
            self.set_options_state("disabled")
            self.question_number += 1
            self.timer_id = self.root.after(1000, self.show_question)
            return

        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def check_answer(self, selected):
        if self.timer_id is None:
            return

        self.cancel_timer()
        self.set_options_state("disabled")

        correct = self.questions[self.question_number]["answer"]

        if selected == correct:
            self.score += 1
            self.feedback_label.config(
                text="Correct! Great job.",
                fg="#72e6a1"
            )
        else:
            self.feedback_label.config(
                text=f"Incorrect! Answer: {correct}",
                fg="#ff8585"
            )

        self.score_label.config(text=f"Score: {self.score}")
        self.question_number += 1
        self.timer_id = self.root.after(1200, self.show_question)

    def cancel_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def finish_quiz(self):
        self.cancel_timer()
        self.set_options_state("disabled")
        self.start_button.config(state="normal")
        self.category_menu.config(state="normal")

        total = len(self.questions)
        percentage = round((self.score / total) * 100)

        self.question_label.config(
            text=f"Quiz complete!\n\nYour score: {self.score}/{total}\nResult: {percentage}%"
        )
        self.timer_label.config(text="")
        self.feedback_label.config(text="Well played!")

        self.save_score(total)

    def save_score(self, total):
        name = "Player"

        scores = []

        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r", encoding="utf-8") as file:
                    scores = json.load(file)
            except (json.JSONDecodeError, OSError):
                scores = []

        scores.append({
            "name": name,
            "score": self.score,
            "total": total,
            "percentage": round(self.score / total * 100)
        })

        scores.sort(
            key=lambda item: item.get("percentage", 0),
            reverse=True
        )

        scores = scores[:10]

        try:
            with open(SCORE_FILE, "w", encoding="utf-8") as file:
                json.dump(scores, file, indent=4)
        except OSError as error:
            messagebox.showerror("Save Error", str(error))

    def show_leaderboard(self):
        if not os.path.exists(SCORE_FILE):
            messagebox.showinfo(
                "Leaderboard",
                "No scores saved yet. Complete a quiz first!"
            )
            return

        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as file:
                scores = json.load(file)
        except (json.JSONDecodeError, OSError):
            messagebox.showerror(
                "Leaderboard",
                "Could not read the saved scores."
            )
            return

        if not scores:
            messagebox.showinfo("Leaderboard", "No scores yet.")
            return

        lines = ["TOP 10 SCORES\n"]

        for index, item in enumerate(scores, start=1):
            lines.append(
                f"{index}. {item['name']} — "
                f"{item['score']}/{item['total']} "
                f"({item['percentage']}%)"
            )

        messagebox.showinfo("Leaderboard", "\n".join(lines))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizMaster(root)
    root.mainloop()