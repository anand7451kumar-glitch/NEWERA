import random


class Maze:
    def __init__(self):
        self.width = 6
        self.height = 6

        self.start = (0, 0)
        self.goal = (5, 5)

        self.walls = {
            (1, 1),
            (1, 2),
            (3, 1),
            (3, 2),
            (3, 3),
        }

        self.traps = {
            (2, 4),
            (4, 2),
        }

        self.reset()

    def reset(self):
        self.position = self.start
        return self.position

    def step(self, action):
        x, y = self.position

        moves = {
            0: (0, -1),   # Up
            1: (0, 1),    # Down
            2: (-1, 0),   # Left
            3: (1, 0),    # Right
        }

        dx, dy = moves[action]

        new_position = (x + dx, y + dy)
        nx, ny = new_position

        # Prevent walking outside the maze.
        if not (
            0 <= nx < self.width
            and 0 <= ny < self.height
        ):
            new_position = self.position

        # Prevent walking through walls.
        if new_position in self.walls:
            new_position = self.position

        self.position = new_position

        # Reward the AI for reaching the goal.
        if self.position == self.goal:
            return self.position, 100, True

        # Penalize falling into a trap.
        if self.position in self.traps:
            return self.position, -100, True

        # A small penalty encourages shorter routes.
        return self.position, -1, False

    def display(self):
        for y in range(self.height):
            row = []

            for x in range(self.width):
                position = (x, y)

                if position == self.position:
                    symbol = "A"
                elif position == self.goal:
                    symbol = "G"
                elif position in self.walls:
                    symbol = "#"
                elif position in self.traps:
                    symbol = "X"
                else:
                    symbol = "."

                row.append(symbol)

            print(" ".join(row))

        print()