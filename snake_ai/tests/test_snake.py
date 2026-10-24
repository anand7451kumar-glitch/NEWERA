import random
import unittest

from snake import DIRS, next_move

W = H = 10


def play(seed, max_steps=3000):
    """Run a whole headless game with the autopilot. Returns (foods eaten, died?)."""
    rng = random.Random(seed)
    snake = [(5, 5), (4, 5), (3, 5)]

    def new_food():
        free = [(x, y) for x in range(W) for y in range(H) if (x, y) not in snake]
        return rng.choice(free)

    food, eaten = new_food(), 0
    for _ in range(max_steps):
        move = next_move(snake, food, W, H)
        if move is None:
            return eaten, True
        dx, dy = DIRS[move]
        head = (snake[0][0] + dx, snake[0][1] + dy)
        eating = head == food
        body = snake if eating else snake[:-1]
        if not (0 <= head[0] < W and 0 <= head[1] < H) or head in body:
            return eaten, True
        snake.insert(0, head)
        if eating:
            eaten += 1
            if len(snake) == W * H:
                return eaten, False
            food = new_food()
        else:
            snake.pop()
    return eaten, False


class SnakeTests(unittest.TestCase):
    def test_goes_straight_to_food(self):
        self.assertEqual(next_move([(2, 2), (1, 2), (0, 2)], (5, 2), W, H), "right")

    def test_never_steps_into_wall_or_body(self):
        snake = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 2)]
        move = next_move(snake, (9, 9), W, H)
        self.assertIsNone(move)  # completely boxed in

    def test_avoids_wall_in_corner(self):
        move = next_move([(0, 0), (1, 0), (2, 0)], (0, 5), W, H)
        self.assertEqual(move, "down")

    def test_full_games_survive_a_long_time(self):
        for seed in range(5):
            eaten, died = play(seed)
            self.assertGreaterEqual(eaten, 80, (seed, eaten, died))


if __name__ == "__main__":
    unittest.main()
