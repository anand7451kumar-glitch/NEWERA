import tkinter as tk
import random
import json
import os

HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "highscore.json"
)


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return json.load(file).get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump({"high_score": score}, file)


# Game settings
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
SPEED = 120

COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        self.root.configure(bg="#172033")

        self.score = 0
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_over = False
        self.paused = False
        self.after_id = None

        # Title
        tk.Label(
            root,
            text="SNAKE GAME",
            font=("Arial", 24, "bold"),
            bg="#172033",
            fg="#4ade80"
        ).pack(pady=(12, 4))

        # Score
        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            bg="#172033",
            fg="white"
        )
        self.score_label.pack(pady=5)
        self.high_score = load_high_score()

        self.high_score_label = tk.Label(
            root, 
            text=f"High Score: {self.high_score}",
            font=("Arial", 12),
            bg="#172033",
            fg="#facc15"
        )
        self.high_score_label.pack(pady=2)

        # Game canvas
        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#0f172a",
            highlightthickness=0
        )
        self.canvas.pack(padx=12, pady=8)

        # Buttons
        button_frame = tk.Frame(root, bg="#172033")
        button_frame.pack(pady=(5, 12))

        tk.Button(
            button_frame,
            text="Restart",
            command=self.restart,
            font=("Arial", 11, "bold"),
            bg="#4ade80",
            fg="#172033",
            padx=18,
            pady=7
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="Quit",
            command=root.destroy,
            font=("Arial", 11, "bold"),
            bg="#140397",
            fg="#FF0000",
            padx=18,
            pady=7
        ).grid(row=0, column=1, padx=8)

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))

        # WASD controls
        self.root.bind("w", lambda event: self.change_direction("Up"))
        self.root.bind("s", lambda event: self.change_direction("Down"))
        self.root.bind("a", lambda event: self.change_direction("Left"))
        self.root.bind("d", lambda event: self.change_direction("Right"))
        self.root.bind("<space>", self.toggle_pause)

        self.restart()

    def toggle_pause(self, event=None):
        if self.game_over:
            return
        
        self.paused = not self.paused

        if self.paused:
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            self.show_message("PAUSED")
        else:
            self.draw()
            self.after_id = self.root.after(SPEED, self.update_game)
    

    def restart(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.score = 0
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_over = False

        self.snake = [
            (5, 5),
            (4, 5),
            (3, 5)
        ]

        self.food = self.create_food()
        self.score_label.config(text="Score: 0")

        self.draw()
        self.after_id = self.root.after(SPEED, self.update_game)

    def create_food(self):
        empty_cells = [
            (x, y)
            for x in range(COLS)
            for y in range(ROWS)
            if (x, y) not in self.snake
        ]

        return random.choice(empty_cells) if empty_cells else None

    def change_direction(self, new_direction):
        opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }

        if opposite[new_direction] != self.direction:
            self.next_direction = new_direction

    def update_game(self):
        if self.game_over:
            return

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]

        movement = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }

        dx, dy = movement[self.direction]

        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        x, y = new_head

        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            self.end_game()
            return

        # Check whether food is eaten
        eating = new_head == self.food

        # Moving into the old tail position is allowed
        # if the snake is not growing on this move.
        body = self.snake if eating else self.snake[:-1]

        if new_head in body:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if eating:
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")

            if self.score > self.high_score:
                self.high_score = self.score
                save_high_score(self.high_score)
                self.high_score_label.config(
                    text=f"High Score: {self.high_score}"
                )

            self.food = self.create_food()

            if self.food is None:
                self.game_over = True
                self.draw()
                self.show_message("YOU WIN!")
                return
        else:
            self.snake.pop()

        self.draw()

        # Gradually increase speed as the score rises.
        speed = max(55, SPEED - (self.score // 50) * 5)

        self.after_id = self.root.after(speed, self.update_game)

    def draw(self):
        self.canvas.delete("all")

        # Draw food
        if self.food is not None:
            x, y = self.food

            self.canvas.create_oval(
                x * CELL_SIZE + 3,
                y * CELL_SIZE + 3,
                (x + 1) * CELL_SIZE - 3,
                (y + 1) * CELL_SIZE - 3,
                fill="#f87171",
                outline=""
            )

        # Draw snake
        for index, (x, y) in enumerate(self.snake):
            color = "#4ade80" if index == 0 else "#22c55e"

            self.canvas.create_rectangle(
                x * CELL_SIZE + 1,
                y * CELL_SIZE + 1,
                (x + 1) * CELL_SIZE - 1,
                (y + 1) * CELL_SIZE - 1,
                fill=color,
                outline=""
            )

    def end_game(self):
        self.game_over = True
        self.show_message("GAME OVER")

    def show_message(self, message):
        self.canvas.create_rectangle(
            100, 145, 500, 255,
            fill="#172033",
            outline="#4ade80",
            width=2
        )

        self.canvas.create_text(
            WIDTH // 2,
            180,
            text=message,
            fill="#4ade80",
            font=("Arial", 24, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            220,
            text=f"Final Score: {self.score}  |  Click Restart",
            fill="white",
            font=("Arial", 12)
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()