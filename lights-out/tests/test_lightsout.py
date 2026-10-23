import unittest

from lightsout import new_puzzle, press, solve


class LightsOutTests(unittest.TestCase):
    def test_pressing_twice_undoes(self):
        b = new_puzzle(5, seed=1)
        before = [r[:] for r in b]
        press(b, 2, 2); press(b, 2, 2)
        self.assertEqual(b, before)

    def test_corner_press_flips_three_cells(self):
        b = [[0] * 5 for _ in range(5)]
        press(b, 0, 0)
        self.assertEqual(sum(map(sum, b)), 3)

    def test_generated_puzzles_are_solvable_and_solution_works(self):
        for n in (3, 5, 7):
            for seed in range(10):
                b = new_puzzle(n, seed)
                self.assertTrue(any(map(any, b)))
                for r, c in solve(b):
                    press(b, r, c)
                self.assertFalse(any(map(any, b)), (n, seed))

    def test_unsolvable_board_returns_none(self):
        # On a 5x5 board a single lit corner is not solvable.
        b = [[0] * 5 for _ in range(5)]
        b[0][0] = 1
        self.assertIsNone(solve(b))


if __name__ == "__main__":
    unittest.main()
