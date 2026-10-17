import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os


# -------------------- QUESTIONS --------------------

QUESTIONS = [
    # PYTHON - EASY
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["func", "def", "function", "define"],
        "answer": "def",
        "category": "Python",
        "difficulty": "Easy"
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["int", "str", "bool", "list"],
        "answer": "bool",
        "category": "Python",
        "difficulty": "Easy"
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["//", "#", "/*", "--"],
        "answer": "#",
        "category": "Python",
        "difficulty": "Easy"
    },
    {
        "question": "What is the output of print(2 + 3)?",
        "options": ["23", "5", "6", "Error"],
        "answer": "5",
        "category": "Python",
        "difficulty": "Easy"
    },

    # PYTHON - MEDIUM
    {
        "question": "Which method adds an item to the end of a list?",
        "options": ["add()", "insert()", "append()", "push()"],
        "answer": "append()",
        "category": "Python",
        "difficulty": "Medium"
    },
    {
        "question": "What does len([10, 20, 30]) return?",
        "options": ["2", "3", "30", "10"],
        "answer": "3",
        "category": "Python",
        "difficulty": "Medium"
    },
    {
        "question": "Which data structure stores key-value pairs?",
        "options": ["Tuple", "Set", "Dictionary", "String"],
        "answer": "Dictionary",
        "category": "Python",
        "difficulty": "Medium"
    },
    {
        "question": "What is the output of 10 // 3?",
        "options": ["3", "3.33", "1", "4"],
        "answer": "3",
        "category": "Python",
        "difficulty": "Medium"
    },

    # PYTHON - HARD
    {
        "question": "Which keyword handles exceptions in Python?",
        "options": ["catch", "except", "error", "handle"],
        "answer": "except",
        "category": "Python",
        "difficulty": "Hard"
    },
    {
        "question": "What is the average time complexity of dictionary lookup?",
        "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"],
        "answer": "O(1)",
        "category": "Python",
        "difficulty": "Hard"
    },
    {
        "question": "Which object is immutable?",
        "options": ["List", "Dictionary", "Set", "Tuple"],
        "answer": "Tuple",
        "category": "Python",
        "difficulty": "Hard"
    },

    # SCIENCE - EASY
    {
        "question": "What is the chemical formula of water?",
        "options": ["CO2", "H2O", "O2", "NaCl"],
        "answer": "H2O",
        "category": "Science",
        "difficulty": "Easy"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Jupiter", "Mars", "Saturn"],
        "answer": "Mars",
        "category": "Science",
        "difficulty": "Easy"
    },
    {
        "question": "What force pulls objects toward Earth?",
        "options": ["Friction", "Gravity", "Magnetism", "Tension"],
        "answer": "Gravity",
        "category": "Science",
        "difficulty": "Easy"
    },

    # SCIENCE - MEDIUM
    {
        "question": "What is the SI unit of electric current?",
        "options": ["Volt", "Ohm", "Ampere", "Watt"],
        "answer": "Ampere",
        "category": "Science",
        "difficulty": "Medium"
    },
    {
        "question": "What is the approximate speed of light in vacuum?",
        "options": [
            "3 × 10^6 m/s",
            "3 × 10^8 m/s",
            "3 × 10^5 m/s",
            "3 × 10^10 m/s"
        ],
        "answer": "3 × 10^8 m/s",
        "category": "Science",
        "difficulty": "Medium"
    },
    {
        "question": "What is the pH of a neutral solution at 25°C?",
        "options": ["0", "5", "7", "14"],
        "answer": "7",
        "category": "Science",
        "difficulty": "Medium"
    },

    # SCIENCE - HARD
    {
        "question": "Which particle has a negative electric charge?",
        "options": ["Proton", "Neutron", "Electron", "Photon"],
        "answer": "Electron",
        "category": "Science",
        "difficulty": "Hard"
    },
    {
        "question": "What is the derivative of sin(x)?",
        "options": ["-sin(x)", "cos(x)", "tan(x)", "-cos(x)"],
        "answer": "cos(x)",
        "category": "Science",
        "difficulty": "Hard"
    },

    # MATH - EASY
    {
        "question": "What is 12 × 8?",
        "options": ["86", "96", "108", "88"],
        "answer": "96",
        "category": "Math",
        "difficulty": "Easy"
    },
    {
        "question": "What is the square root of 144?",
        "options": ["10", "11", "12", "14"],
        "answer": "12",
        "category": "Math",
        "difficulty": "Easy"
    },

    # MATH - MEDIUM
    {
        "question": "What is the derivative of x²?",
        "options": ["x", "2x", "x²", "2"],
        "answer": "2x",
        "category": "Math",
        "difficulty": "Medium"
    },
    {
        "question": "What is the value of 5! (5 factorial)?",
        "options": ["25", "60", "100", "120"],
        "answer": "120",
        "category": "Math",
        "difficulty": "Medium"
    },
    {
        "question": "What is the integral of 2x?",
        "options": ["x² + C", "2 + C", "2x² + C", "x + C"],
        "answer": "x² + C",
        "category": "Math",
        "difficulty": "Medium"
    },

    # MATH - HARD
    {
        "question": "What is the derivative of e^x?",
        "options": ["xe^(x-1)", "e^x", "ln(x)", "1/x"],
        "answer": "e^x",
        "category": "Math",
        "difficulty": "Hard"
    },
    {
        "question": "What is the determinant of [[1, 2], [3, 4]]?",
        "options": ["-2", "2", "10", "4"],
        "answer": "-2",
        "category": "Math",
        "difficulty": "Hard"
    },

    # GENERAL KNOWLEDGE - EASY
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
        "answer": "New Delhi",
        "category": "General Knowledge",
        "difficulty": "Easy"
    },
    {
        "question": "How many days are there in a leap year?",
        "options": ["364", "365", "366", "367"],
        "answer": "366",
        "category": "General Knowledge",
        "difficulty": "Easy"
    },

    # GENERAL KNOWLEDGE - MEDIUM
    {
        "question": "Which is the largest ocean on Earth?",
        "options": [
            "Atlantic Ocean",
            "Indian Ocean",
            "Arctic Ocean",
            "Pacific Ocean"
        ],
        "answer": "Pacific Ocean",
        "category": "General Knowledge",
        "difficulty": "Medium"
    },
    {
        "question": "Which organization developed Python?",
        "options": [
            "Microsoft",
            "Python Software Foundation",
            "Google",
            "Apple"
        ],
        "answer": "Python Software Foundation",
        "category": "General Knowledge",
        "difficulty": "Medium"
    },

    # GENERAL KNOWLEDGE - HARD
    {
        "question": "Which is the smallest prime number?",
        "options": ["0", "1", "2", "3"],
        "answer": "2",
        "category": "General Knowledge",
        "difficulty": "Hard"
    },
    {
        "question": "Which number system uses base 2?",
        "options": ["Decimal", "Binary", "Octal", "Hexadecimal"],
        "answer": "Binary",
        "category": "General Knowledge",
        "difficulty": "Hard"
    }
]


# -------------------- APPLICATION --------------------

class QuizMaster:

    def __init__(self, root):
        self.root = root
        self.root.title("QuizMaster")
        self.root.geometry("750x650")
        self.root.minsize(600, 550)

        self.root.configure(bg="#f0f4f8")

        self.player_name = tk.StringVar()
        self.category = tk.StringVar(value="All")
        self.difficulty = tk.StringVar(value="Medium")

        self.questions = []
        self.question_number = 0
        self.score = 0
        self.time_left = 15
        self.timer_id = None
        self.quiz_running = False

        self.score_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "scores.json"
        )

        self.create_widgets()

    # -------------------- INTERFACE --------------------

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="QUIZMASTER",
            font=("Arial", 26, "bold"),
            bg="#f0f4f8",
            fg="#243b53"
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.root,
            text="Test your knowledge!",
            font=("Arial", 12),
            bg="#f0f4f8",
            fg="#52606d"
        )
        subtitle.pack(pady=(0, 15))

        settings_frame = tk.Frame(
            self.root,
            bg="white",
            padx=20,
            pady=15
        )
        settings_frame.pack(fill="x", padx=30, pady=5)

        tk.Label(
            settings_frame,
            text="Player name:",
            font=("Arial", 11),
            bg="white"
        ).grid(row=0, column=0, padx=8, pady=8, sticky="w")

        self.name_entry = tk.Entry(
            settings_frame,
            textvariable=self.player_name,
            font=("Arial", 11),
            width=20
        )
        self.name_entry.grid(row=0, column=1, padx=8, pady=8)

        tk.Label(
            settings_frame,
            text="Category:",
            font=("Arial", 11),
            bg="white"
        ).grid(row=1, column=0, padx=8, pady=8, sticky="w")

        self.category_menu = ttk.Combobox(
            settings_frame,
            textvariable=self.category,
            values=[
                "All",
                "Python",
                "Science",
                "Math",
                "General Knowledge"
            ],
            state="readonly",
            width=18
        )
        self.category_menu.grid(row=1, column=1, padx=8, pady=8)
        self.category_menu.set("All")

        tk.Label(
            settings_frame,
            text="Difficulty:",
            font=("Arial", 11),
            bg="white"
        ).grid(row=2, column=0, padx=8, pady=8, sticky="w")

        self.difficulty_menu = ttk.Combobox(
            settings_frame,
            textvariable=self.difficulty,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=18
        )
        self.difficulty_menu.grid(row=2, column=1, padx=8, pady=8)
        self.difficulty_menu.set("Medium")

        self.start_button = tk.Button(
            settings_frame,
            text="Start Quiz",
            command=self.start_quiz,
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            padx=15,
            pady=5
        )
        self.start_button.grid(
            row=0,
            column=2,
            rowspan=3,
            padx=20
        )

        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            mode="determinate",
            length=600
        )
        self.progress.pack(fill="x", padx=40, pady=(20, 5))

        self.progress_label = tk.Label(
            self.root,
            text="Question 0/0",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#52606d"
        )
        self.progress_label.pack()

        self.timer_label = tk.Label(
            self.root,
            text="Time: --",
            font=("Arial", 13, "bold"),
            bg="#f0f4f8",
            fg="#dc2626"
        )
        self.timer_label.pack(pady=10)

        self.question_label = tk.Label(
            self.root,
            text="Enter your name and click Start Quiz.",
            font=("Arial", 15, "bold"),
            bg="#ffffff",
            fg="#243b53",
            wraplength=620,
            justify="center",
            padx=20,
            pady=25
        )
        self.question_label.pack(
            fill="x",
            padx=40,
            pady=10
        )

        self.options_frame = tk.Frame(
            self.root,
            bg="#f0f4f8"
        )
        self.options_frame.pack(fill="x", padx=50, pady=5)

        self.option_buttons = []

        for i in range(4):
            button = tk.Button(
                self.options_frame,
                text="",
                font=("Arial", 11),
                wraplength=500,
                justify="left",
                anchor="w",
                padx=15,
                pady=10,
                bg="white",
                fg="#243b53",
                activebackground="#dbeafe",
                command=lambda index=i: self.check_answer(index)
            )

            button.pack(fill="x", pady=5)
            self.option_buttons.append(button)

        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "bold"),
            bg="#f0f4f8"
        )
        self.feedback_label.pack(pady=8)

        bottom_frame = tk.Frame(
            self.root,
            bg="#f0f4f8"
        )
        bottom_frame.pack(pady=10)

        self.next_button = tk.Button(
            bottom_frame,
            text="Next Question",
            command=self.next_question,
            font=("Arial", 10, "bold"),
            bg="#059669",
            fg="white",
            padx=12,
            pady=7,
            state="disabled"
        )
        self.next_button.grid(row=0, column=0, padx=8)

        self.leaderboard_button = tk.Button(
            bottom_frame,
            text="Leaderboard",
            command=self.show_leaderboard,
            font=("Arial", 10, "bold"),
            bg="#7c3aed",
            fg="white",
            padx=12,
            pady=7
        )
        self.leaderboard_button.grid(row=0, column=1, padx=8)

    # -------------------- START QUIZ --------------------

    def start_quiz(self):
        name = self.player_name.get().strip()

        if not name:
            messagebox.showwarning(
                "Name Required",
                "Please enter your name before starting."
            )
            self.name_entry.focus_set()
            return

        selected_category = self.category.get()
        selected_difficulty = self.difficulty.get()

        self.questions = [
            question.copy()
            for question in QUESTIONS
            if (
                selected_category == "All"
                or question["category"] == selected_category
            )
            and question["difficulty"] == selected_difficulty
        ]

        if not self.questions:
            messagebox.showerror(
                "No Questions",
                "No questions are available for this selection."
            )
            return

        random.shuffle(self.questions)

        # Limit each quiz to 10 questions when available.
        self.questions = self.questions[:10]

        self.question_number = 0
        self.score = 0
        self.quiz_running = True

        self.progress["maximum"] = len(self.questions)
        self.progress["value"] = 0

        self.start_button.config(state="disabled")
        self.category_menu.config(state="disabled")
        self.difficulty_menu.config(state="disabled")
        self.name_entry.config(state="disabled")

        self.show_question()

    # -------------------- SHOW QUESTION --------------------

    def show_question(self):
        self.cancel_timer()

        if self.question_number >= len(self.questions):
            self.finish_quiz()
            return

        question = self.questions[self.question_number]

        self.progress["value"] = self.question_number + 1
        self.progress_label.config(
            text=(
                f"Question {self.question_number + 1}"
                f"/{len(self.questions)}"
            )
        )

        self.question_label.config(
            text=(
                f"Q{self.question_number + 1}. "
                f"{question['question']}"
            )
        )

        # Shuffle answer options without losing the correct answer.
        options = question["options"].copy()
        random.shuffle(options)

        question["shuffled_options"] = options

        self.feedback_label.config(text="")
        self.next_button.config(state="disabled")

        for index, button in enumerate(self.option_buttons):
            button.config(
                text=f"{chr(65 + index)}. {options[index]}",
                state="normal",
                bg="white",
                fg="#243b53"
            )

        self.time_left = 15
        self.update_timer()

    # -------------------- TIMER --------------------

    def update_timer(self):
        self.timer_label.config(
            text=f"Time remaining: {self.time_left} seconds"
        )

        if self.time_left <= 0:
            self.timer_id = None
            self.time_up()
            return

        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def cancel_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def time_up(self):
        if not self.quiz_running:
            return

        question = self.questions[self.question_number]

        self.set_options_state("disabled")

        self.feedback_label.config(
            text=f"Time's up! Correct answer: {question['answer']}",
            fg="#dc2626"
        )

        self.next_button.config(state="normal")
        self.timer_label.config(text="Time's up!")

    # -------------------- CHECK ANSWER --------------------

    def check_answer(self, selected_index):
        if not self.quiz_running:
            return

        # Ignore additional clicks after an answer.
        if self.next_button["state"] == "normal":
            return

        self.cancel_timer()

        question = self.questions[self.question_number]
        selected_answer = question["shuffled_options"][selected_index]
        correct_answer = question["answer"]

        self.set_options_state("disabled")

        if selected_answer == correct_answer:
            self.score += 1

            self.feedback_label.config(
                text="Correct! Well done!",
                fg="#059669"
            )

            self.option_buttons[selected_index].config(
                bg="#bbf7d0"
            )

        else:
            self.feedback_label.config(
                text=f"Incorrect! Correct answer: {correct_answer}",
                fg="#dc2626"
            )

            self.option_buttons[selected_index].config(
                bg="#fecaca"
            )

            # Highlight the correct answer.
            for index, option in enumerate(
                question["shuffled_options"]
            ):
                if option == correct_answer:
                    self.option_buttons[index].config(
                        bg="#bbf7d0"
                    )
                    break

        self.timer_label.config(
            text=f"Score: {self.score}/{self.question_number + 1}"
        )

        self.next_button.config(state="normal")

    def set_options_state(self, state):
        for button in self.option_buttons:
            button.config(state=state)

    # -------------------- NEXT QUESTION --------------------

    def next_question(self):
        if not self.quiz_running:
            return

        self.question_number += 1

        if self.question_number >= len(self.questions):
            self.finish_quiz()
        else:
            self.show_question()

    # -------------------- FINISH QUIZ --------------------

    def finish_quiz(self):
        self.cancel_timer()
        self.quiz_running = False

        self.set_options_state("disabled")
        self.next_button.config(state="disabled")

        total = len(self.questions)
        percentage = round((self.score / total) * 100) if total else 0
        name = self.player_name.get().strip()

        self.progress["value"] = total
        self.progress_label.config(
            text=f"Completed {total}/{total} questions"
        )

        self.question_label.config(
            text=(
                f"Quiz complete, {name}!\n\n"
                f"Your score: {self.score}/{total}\n"
                f"Result: {percentage}%"
            )
        )

        self.timer_label.config(text="")
        self.feedback_label.config(
            text="Great effort! Play again to improve your score.",
            fg="#2563eb"
        )

        self.save_score(total, percentage)

        self.start_button.config(state="normal")
        self.category_menu.config(state="readonly")
        self.difficulty_menu.config(state="readonly")
        self.name_entry.config(state="normal")

        messagebox.showinfo(
            "Quiz Complete",
            f"Well played, {name}!\n\n"
            f"Score: {self.score}/{total}\n"
            f"Percentage: {percentage}%"
        )

    # -------------------- SAVE SCORE --------------------

    def save_score(self, total, percentage):
        scores = []

        if os.path.exists(self.score_file):
            try:
                with open(
                    self.score_file,
                    "r",
                    encoding="utf-8"
                ) as file:
                    scores = json.load(file)

                if not isinstance(scores, list):
                    scores = []

            except (json.JSONDecodeError, OSError):
                scores = []

        record = {
            "name": self.player_name.get().strip(),
            "score": self.score,
            "total": total,
            "percentage": percentage,
            "category": self.category.get(),
            "difficulty": self.difficulty.get()
        }

        scores.append(record)

        # Best percentage first, then best score.
        scores.sort(
            key=lambda item: (
                item.get("percentage", 0),
                item.get("score", 0)
            ),
            reverse=True
        )

        try:
            with open(
                self.score_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(scores, file, indent=4)

        except OSError as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save your score:\n{error}"
            )

    # -------------------- LEADERBOARD --------------------

    def show_leaderboard(self):
        scores = []

        if os.path.exists(self.score_file):
            try:
                with open(
                    self.score_file,
                    "r",
                    encoding="utf-8"
                ) as file:
                    scores = json.load(file)

                if not isinstance(scores, list):
                    scores = []

            except (json.JSONDecodeError, OSError):
                messagebox.showerror(
                    "Leaderboard Error",
                    "Could not read the leaderboard file."
                )
                return

        if not scores:
            messagebox.showinfo(
                "Leaderboard",
                "No scores saved yet. Complete a quiz first!"
            )
            return

        leaderboard = tk.Toplevel(self.root)
        leaderboard.title("QuizMaster Leaderboard")
        leaderboard.geometry("650x400")
        leaderboard.configure(bg="#f0f4f8")

        tk.Label(
            leaderboard,
            text="LEADERBOARD",
            font=("Arial", 20, "bold"),
            bg="#f0f4f8",
            fg="#243b53"
        ).pack(pady=15)

        columns = (
            "rank",
            "name",
            "score",
            "percentage",
            "category",
            "difficulty"
        )

        table = ttk.Treeview(
            leaderboard,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "rank": "Rank",
            "name": "Player",
            "score": "Score",
            "percentage": "Result",
            "category": "Category",
            "difficulty": "Difficulty"
        }

        widths = {
            "rank": 50,
            "name": 120,
            "score": 70,
            "percentage": 75,
            "category": 140,
            "difficulty": 90
        }

        for column in columns:
            table.heading(column, text=headings[column])
            table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        for rank, record in enumerate(scores[:50], start=1):
            table.insert(
                "",
                "end",
                values=(
                    rank,
                    record.get("name", "Unknown"),
                    (
                        f"{record.get('score', 0)}/"
                        f"{record.get('total', 0)}"
                    ),
                    f"{record.get('percentage', 0)}%",
                    record.get("category", "All"),
                    record.get("difficulty", "Medium")
                )
            )

        table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )


# -------------------- RUN APPLICATION --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizMaster(root)
    root.mainloop()