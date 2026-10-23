import unittest

from maze import generate, solve


class MazeTests(unittest.TestCase):
    def test_same_seed_same_maze(self):
        self.assertEqual(generate(10, 10, seed=5), generate(10, 10, seed=5))
        self.assertNotEqual(generate(10, 10, seed=5), generate(10, 10, seed=6))

    def test_every_cell_is_reachable(self):
        w = h = 12
        grid = generate(w, h, seed=1)
        for cy in range(h):
            for cx in range(w):
                self.assertIsNotNone(solve(grid, (1, 1), (2 * cy + 1, 2 * cx + 1)))

    def test_maze_is_a_perfect_maze(self):
        # A perfect maze has exactly one route between any two cells (no loops):
        # open cells = cells + passages, and passages = cells - 1.
        w = h = 10
        grid = generate(w, h, seed=3)
        open_cells = sum(v == 0 for row in grid for v in row)
        self.assertEqual(open_cells, w * h + (w * h - 1))

    def test_path_is_valid_and_steps_are_adjacent(self):
        grid = generate(8, 8, seed=2)
        path = solve(grid, (1, 1), (15, 15))
        self.assertEqual(path[0], (1, 1))
        self.assertEqual(path[-1], (15, 15))
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            self.assertEqual(abs(r1 - r2) + abs(c1 - c2), 1)
            self.assertEqual(grid[r2][c2], 0)

    def test_blocked_returns_none(self):
        self.assertIsNone(solve([[0, 1, 0]], (0, 0), (0, 2)))


if __name__ == "__main__":
    unittest.main()
