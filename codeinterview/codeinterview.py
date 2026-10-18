import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random


# -------------------- CODING QUESTIONS --------------------

QUESTIONS = [
    {
        "title": "Two Sum",
        "category": "Arrays",
        "difficulty": "Easy",
        "description": (
            "Given a list of integers and a target, return the "
            "indices of two numbers whose sum equals the target.\n\n"
            "Example:\n"
            "nums = [2, 7, 11, 15], target = 9\n"
            "Output: [0, 1]"
        ),
        "hint": (
            "Can you store previously seen numbers in a dictionary "
            "and check whether target - current_number exists?"
        ),
        "solution": '''def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        needed = target - num

        if needed in seen:
            return [seen[needed], i]

        seen[num] = i

    return []''',
        "explanation": (
            "For each number, calculate its complement: target - num. "
            "If that complement is already in the dictionary, return "
            "both indices. Otherwise, store the current number and "
            "its index.\n\n"
            "Time complexity: O(n)\n"
            "Space complexity: O(n)"
        )
    },
    {
        "title": "Valid Palindrome",
        "category": "Strings",
        "difficulty": "Easy",
        "description": (
            "Determine whether a string is a palindrome, ignoring "
            "spaces, punctuation, and letter case.\n\n"
            "Example:\n"
            'Input: "A man, a plan, a canal: Panama"\n'
            "Output: True"
        ),
        "hint": (
            "Keep only letters and digits, convert to lowercase, "
            "and compare the result with its reverse."
        ),
        "solution": '''def is_palindrome(s):
    cleaned = "".join(
        char.lower()
        for char in s
        if char.isalnum()
    )

    return cleaned == cleaned[::-1]''',
        "explanation": (
            "The isalnum() method keeps letters and digits. "
            "The lower() method ignores case. Python's [::-1] "
            "reverses a string.\n\n"
            "Time complexity: O(n)\n"
            "Space complexity: O(n)"
        )
    },
    {
        "title": "Contains Duplicate",
        "category": "Arrays",
        "difficulty": "Easy",
        "description": (
            "Return True if any value appears at least twice "
            "in a list. Otherwise, return False.\n\n"
            "Example:\n"
            "Input: [1, 2, 3, 1]\n"
            "Output: True"
        ),
        "hint": (
            "A set stores unique values. Compare the number "
            "of elements in the set with the original list."
        ),
        "solution": '''def contains_duplicate(nums):
    return len(nums) != len(set(nums))''',
        "explanation": (
            "A set removes duplicates. If the set is shorter "
            "than the original list, at least one duplicate exists.\n\n"
            "Time complexity: O(n) on average\n"
            "Space complexity: O(n)"
        )
    },
    {
        "title": "Valid Anagram",
        "category": "Strings",
        "difficulty": "Easy",
        "description": (
            "Given two strings, determine whether one is an "
            "anagram of the other.\n\n"
            "An anagram uses exactly the same letters with "
            "the same frequencies.\n\n"
            'Example: "listen", "silent" -> True'
        ),
        "hint": (
            "Two anagrams have the same character frequencies. "
            "Python's sorted() can help you compare them."
        ),
        "solution": '''def is_anagram(s, t):
    return sorted(s) == sorted(t)''',
        "explanation": (
            "Sorting both strings places their characters in the "
            "same order if they contain exactly the same characters.\n\n"
            "Time complexity: O(n log n)\n"
            "Space complexity: O(n)"
        )
    },
    {
        "title": "Maximum Subarray",
        "category": "Arrays",
        "difficulty": "Medium",
        "description": (
            "Find the largest sum of any non-empty contiguous "
            "subarray.\n\n"
            "Example:\n"
            "Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]\n"
            "Output: 6\n"
            "Explanation: [4, -1, 2, 1] has sum 6."
        ),
        "hint": (
            "At each position, decide whether to extend the "
            "previous subarray or start a new one."
        ),
        "solution": '''def max_subarray(nums):
    current = nums[0]
    best = nums[0]

    for num in nums[1:]:
        current = max(num, current + num)
        best = max(best, current)

    return best''',
        "explanation": (
            "This is Kadane's algorithm. Keep the best sum ending "
            "at the current position and the best sum found overall.\n\n"
            "Time complexity: O(n)\n"
            "Space complexity: O(1)"
        )
    },
    {
        "title": "Valid Parentheses",
        "category": "Stacks",
        "difficulty": "Easy",
        "description": (
            "Given a string containing (), {}, and [], determine "
            "whether every opening bracket has the correct "
            "matching closing bracket.\n\n"
            'Example: "{[]}" -> True\n'
            'Example: "([)]" -> False'
        ),
        "hint": (
            "Use a stack. When you encounter a closing bracket, "
            "check whether the stack's last opening bracket matches."
        ),
        "solution": '''def is_valid(s):
    stack = []
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{"
    }

    for char in s:
        if char in "([{":
            stack.append(char)
        else:
            if not stack or stack.pop() != pairs.get(char):
                return False

    return len(stack) == 0''',
        "explanation": (
            "A stack follows last-in, first-out order. The most "
            "recent opening bracket must be closed first.\n\n"
            "Time complexity: O(n)\n"
            "Space complexity: O(n)"
        )
    },
    {
        "title": "Binary Search",
        "category": "Searching",
        "difficulty": "Easy",
        "description": (
            "Given a sorted list and a target, return its index. "
            "Return -1 if the target does not exist.\n\n"
            "Example:\n"
            "nums = [1, 3, 5, 7, 9], target = 7\n"
            "Output: 3"
        ),
        "hint": (
            "Look at the middle element. If it is too small, "
            "search the right half; otherwise, search the left half."
        ),
        "solution": '''def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1''',
        "explanation": (
            "Binary search repeatedly halves the search range. "
            "The list must be sorted.\n\n"
            "Time complexity: O(log n)\n"
            "Space complexity: O(1)"
        )
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "category": "Arrays",
        "difficulty": "Easy",
        "description": (
            "Given daily stock prices, find the maximum profit "
            "from buying once and selling later. Return 0 if "
            "no profit is possible.\n\n"
            "Example:\n"
            "Input: [7, 1, 5, 3, 6, 4]\n"
            "Output: 5"
        ),
        "hint": (
            "Track the lowest price seen so far and the best "
            "profit you could make at each later price."
        ),
        "solution": '''def max_profit(prices):
    minimum = float("inf")
    best = 0

    for price in prices:
        minimum = min(minimum, price)
        best = max(best, price - minimum)

    return best''',
        "explanation": (
            "Keep the lowest buying price seen so far. For each "
            "price, calculate the profit from buying at that minimum.\n\n"
            "Time complexity: O(n)\n"
            "Space complexity: O(1)"
        )
    },
    {
        "title": "Move Zeroes",
        "category": "Arrays",
        "difficulty": "Easy",
        "description": (
            "Move all zeroes to the end of a list while preserving "
            "the order of non-zero elements.\n\n"
            "Example:\n"
            "Input: [0, 1, 0, 3, 12]\n"
            "Output: [1, 3, 12, 0, 0]"
        ),
        "hint": (
            "Use one index to track where the next non-zero "
            "element should be placed."
        ),
        "solution": '''def move_zeroes(nums):
    position = 0

    for num in nums:
        if num != 0:
            nums[position] = num
            position += 1

    while position < len(nums):
        nums[position] = 0
        position += 1

    return nums''',
        "explanation": (
            "First move every non-zero value to the front in "
            "its original order. Then fill the remaining positions "
            "with zeroes.\n\n"
            "Time complexity: O(n)\n"
            "Extra space complexity: O(1)"
        )
    },
    {
        "title": "First Non-Repeating Character",
        "category": "Hash Maps",
        "difficulty": "Easy",
        "description": (
            "Find the index of the first character that appears "
            "only once. Return -1 if no such character exists.\n\n"
            'Example: "leetcode" -> 0\n'
            'Example: "aabb" -> -1'
        ),
        "hint": (
            "Count each character first. Then scan the string "
            "again to find the first character with count 1."
        ),
        "solution": '''from collections import Counter

def first_unique(s):
    counts = Counter(s)

    for index, char in enumerate(s):
        if counts[char] == 1:
            return index

    return -1''',
        "explanation": (
            "Counter counts how often each character occurs. "
            "The second loop preserves the original character order "
            "and finds the first unique character.\n\n"
            "Time complexity: O(n)\n"
            "Space complexity: O(n)"
        )
    }
]


# -------------------- APPLICATION --------------------

class CodeInterviewPrep:

    def __init__(self, root):
        self.root = root
        self.root.title("CodeInterview Prep")
        self.root.geometry("900x720")
        self.root.minsize(700, 600)
        self.root.configure(bg="#f1f5f9")

        self.data_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "progress.json"
        )

        self.solved = self.load_progress()
        self.questions = QUESTIONS.copy()
        self.current_index = 0

        self.category = tk.StringVar(value="All")
        self.difficulty = tk.StringVar(value="All")

        self.create_widgets()
        self.apply_filters()

    # -------------------- PROGRESS --------------------

    def load_progress(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    data = json.load(file)

                if isinstance(data, list):
                    return set(data)

            except (json.JSONDecodeError, OSError):
                pass

        return set()

    def save_progress(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(sorted(self.solved), file, indent=4)
        except OSError as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save progress:\n{error}"
            )

    # -------------------- INTERFACE --------------------

    def create_widgets(self):
        tk.Label(
            self.root,
            text="CODEINTERVIEW PREP",
            font=("Arial", 25, "bold"),
            bg="#f1f5f9",
            fg="#0f172a"
        ).pack(pady=(18, 4))

        tk.Label(
            self.root,
            text="Practice DSA. Understand solutions. Track progress.",
            font=("Arial", 11),
            bg="#f1f5f9",
            fg="#475569"
        ).pack(pady=(0, 15))

        filters = tk.Frame(self.root, bg="#f1f5f9")
        filters.pack(pady=5)

        tk.Label(
            filters,
            text="Topic:",
            bg="#f1f5f9",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5)

        categories = [
            "All",
            "Arrays",
            "Strings",
            "Stacks",
            "Searching",
            "Hash Maps"
        ]

        self.category_menu = ttk.Combobox(
            filters,
            textvariable=self.category,
            values=categories,
            state="readonly",
            width=14
        )
        self.category_menu.grid(row=0, column=1, padx=5)
        self.category_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        tk.Label(
            filters,
            text="Difficulty:",
            bg="#f1f5f9",
            font=("Arial", 11)
        ).grid(row=0, column=2, padx=5)

        self.difficulty_menu = ttk.Combobox(
            filters,
            textvariable=self.difficulty,
            values=["All", "Easy", "Medium", "Hard"],
            state="readonly",
            width=10
        )
        self.difficulty_menu.grid(row=0, column=3, padx=5)
        self.difficulty_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        self.progress_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10, "bold"),
            bg="#f1f5f9",
            fg="#047857"
        )
        self.progress_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(
            self.root,
            mode="determinate",
            length=700
        )
        self.progress_bar.pack(fill="x", padx=45, pady=(0, 12))

        self.card = tk.Frame(
            self.root,
            bg="white",
            padx=25,
            pady=20
        )
        self.card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=5
        )

        self.question_title = tk.Label(
            self.card,
            text="",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#1d4ed8"
        )
        self.question_title.pack(anchor="w", pady=(0, 10))

        self.question_meta = tk.Label(
            self.card,
            text="",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748b"
        )
        self.question_meta.pack(anchor="w", pady=(0, 12))

        self.description = tk.Label(
            self.card,
            text="",
            font=("Arial", 12),
            bg="white",
            fg="#1e293b",
            justify="left",
            anchor="nw",
            wraplength=760
        )
        self.description.pack(fill="x", anchor="w", pady=5)

        self.details = tk.Label(
            self.card,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#475569",
            justify="left",
            anchor="nw",
            wraplength=760
        )
        self.details.pack(fill="both", expand=True, anchor="w", pady=10)
        #Coding editor
        editor_label = tk.Label(
            self.root,
            text="Write your Python solution:",
            font=("Arial", 12, "bold"),
            bg="#f1f5f9"
        
        )
        editor_label.pack(anchor="w", padx=35, pady=(10, 5))

        self.code_editor = tk.Text(
            self.root,
            height=8,
            font=("Courier", 11),
            wrap="none"
        )
        self.code_editor.pack(fill="x", padx=35, pady=5)

        self.run_button = tk.Button(
            self.root,
            text="Run Code",
            command=self.run_code,
            bg="#2563eb",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=7
        )
        self.run_button.pack(pady=5)

        self.output_box = tk.Text(
            self.root,
            height=5,
            font=("Courier", 10),
            state="disabled"
        )
        self.output_box.pack(fill="x", padx=35, pady=5)

        self.actions = tk.Frame(self.root, bg="#f1f5f9")
        self.actions.pack(pady=12)

        self.hint_button = tk.Button(
            self.actions,
            text="Show Hint",
            command=self.show_hint,
            bg="#f59e0b",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=8
        )
        self.hint_button.grid(row=0, column=0, padx=5)

        self.solution_button = tk.Button(
            self.actions,
            text="Show Solution",
            command=self.show_solution,
            bg="#7c3aed",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=8
        )
        self.solution_button.grid(row=0, column=1, padx=5)

        self.solved_button = tk.Button(
            self.actions,
            text="Mark Solved",
            command=self.toggle_solved,
            bg="#059669",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=8
        )
        self.solved_button.grid(row=0, column=2, padx=5)

        self.previous_button = tk.Button(
            self.actions,
            text="Previous",
            command=lambda: self.change_question(-1),
            padx=10,
            pady=8
        )
        self.previous_button.grid(row=1, column=0, padx=5, pady=8)

        self.random_button = tk.Button(
            self.actions,
            text="Random Question",
            command=self.random_question,
            padx=10,
            pady=8
        )
        self.random_button.grid(row=1, column=1, padx=5, pady=8)

        self.next_button = tk.Button(
            self.actions,
            text="Next",
            command=lambda: self.change_question(1),
            padx=10,
            pady=8
        )
        self.next_button.grid(row=1, column=2, padx=5, pady=8)

    # -------------------- FILTERS --------------------

    def apply_filters(self):
        selected_category = self.category.get()
        selected_difficulty = self.difficulty.get()

        self.questions = [
            question for question in QUESTIONS
            if (
                selected_category == "All"
                or question["category"] == selected_category
            )
            and (
                selected_difficulty == "All"
                or question["difficulty"] == selected_difficulty
            )
        ]

        self.current_index = 0
        self.show_question()

    # -------------------- DISPLAY QUESTION --------------------

    def show_question(self):
        total_solved = len(self.solved)
        total_questions = len(QUESTIONS)

        self.progress_bar["maximum"] = total_questions
        self.progress_bar["value"] = min(total_solved, total_questions)

        self.progress_label.config(
            text=(
                f"Overall progress: {min(total_solved, total_questions)}"
                f"/{total_questions} questions solved"
            )
        )

        if not self.questions:
            self.question_title.config(text="No matching questions")
            self.question_meta.config(text="")
            self.description.config(
                text="Try choosing a different topic or difficulty."
            )
            self.details.config(text="")
            self.solved_button.config(state="disabled")
            self.hint_button.config(state="disabled")
            self.solution_button.config(state="disabled")
            self.previous_button.config(state="disabled")
            self.next_button.config(state="disabled")
            self.random_button.config(state="disabled")
            return

        self.solved_button.config(state="normal")
        self.hint_button.config(state="normal")
        self.solution_button.config(state="normal")
        self.random_button.config(state="normal")

        question = self.questions[self.current_index]

        solved = question["title"] in self.solved
        status = "SOLVED ✓" if solved else "NOT SOLVED"

        self.question_title.config(
            text=question["title"]
        )

        self.question_meta.config(
            text=(
                f"Topic: {question['category']}   |   "
                f"Difficulty: {question['difficulty']}   |   "
                f"{status}   |   "
                f"Question {self.current_index + 1}/{len(self.questions)}"
            )
        )

        self.description.config(
            text=question["description"]
        )

        self.details.config(text="")

        self.solved_button.config(
            text="Mark Unsolved" if solved else "Mark Solved"
        )

        self.previous_button.config(
            state="normal" if self.current_index > 0 else "disabled"
        )

        self.next_button.config(
            state=(
                "normal"
                if self.current_index < len(self.questions) - 1
                else "disabled"
            )
        )

    # -------------------- HINT --------------------

    def show_hint(self):
        if not self.questions:
            return

        question = self.questions[self.current_index]

        self.details.config(
            text=f"💡 HINT\n\n{question['hint']}"
        )

    # -------------------- SOLUTION --------------------

    def show_solution(self):
        if not self.questions:
            return

        question = self.questions[self.current_index]

        self.details.config(
            text=(
                f"📖 SOLUTION\n\n"
                f"{question['solution']}\n\n"
                f"EXPLANATION\n\n"
                f"{question['explanation']}"
            ),
            font=("Courier", 10)
        )

    # -------------------- MARK SOLVED --------------------

    def toggle_solved(self):
        if not self.questions:
            return

        question = self.questions[self.current_index]
        title = question["title"]

        if title in self.solved:
            self.solved.remove(title)
        else:
            self.solved.add(title)

        self.save_progress()
        self.show_question()

    # -------------------- NAVIGATION --------------------

    def change_question(self, step):
        if not self.questions:
            return

        new_index = self.current_index + step

        if 0 <= new_index < len(self.questions):
            self.current_index = new_index
            self.show_question()

    def random_question(self):
        if not self.questions:
            return

        if len(self.questions) == 1:
            self.current_index = 0
        else:
            choices = list(range(len(self.questions)))
            choices.remove(self.current_index)
            self.current_index = random.choice(choices)

        self.show_question()

    def run_code(self):
        import subprocess
        import sys
        import tempfile

        code = self.code_editor.get("1.0", "end-1c")

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")

        if not code.strip():
            self.output_box.insert("end", "Write some code first.")
            self.output_box.config(state="disabled")
            return

        filename = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                encoding="utf-8",
                delete=False
            ) as file:
                file.write(code)
                filename = file.name

            result = subprocess.run(
                [sys.executable, filename],
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout

            if result.stderr:
                output += "\nErrors:\n" + result.stderr

            if not output.strip():
                output = (
                    f"Program finished with exit code "
                    f"{result.returncode}, but produced no output."
                )

            self.output_box.insert("end", output)
            self.output_box.config(state="disabled")

        except subprocess.TimeoutExpired:
            self.output_box.insert(
                "end",
                "Execution stopped: your program exceeded 5 seconds."
            )

        except Exception as error:
            self.output_box.insert("end", f"Error: {error}")

        finally:
            if filename and os.path.exists(filename):
                os.unlink(filename)

            self.output_box.config(state="disabled")

    


    


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeInterviewPrep(root)
    root.mainloop()

