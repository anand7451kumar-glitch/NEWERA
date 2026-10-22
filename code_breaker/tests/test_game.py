import unittest

from game import CODE_LENGTH, MAX_ATTEMPTS, Game, score_guess, validate_guess


class ScoreTests(unittest.TestCase):
    def test_all_correct(self):
        s = ["red", "blue", "green", "yellow"]
        self.assertEqual(score_guess(s, s), (4, 0))

    def test_all_misplaced(self):
        self.assertEqual(score_guess(["red", "blue", "green", "yellow"], ["blue", "red", "yellow", "green"]), (0, 4))

    def test_duplicates_are_not_double_counted(self):
        self.assertEqual(score_guess(["red", "red", "blue", "blue"], ["red", "blue", "blue", "blue"]), (3, 0))
        self.assertEqual(score_guess(["red", "blue", "green", "green"], ["red", "red", "red", "red"]), (1, 0))


class GameTests(unittest.TestCase):
    def test_win(self):
        g = Game(secret=["red"] * CODE_LENGTH)
        g.guess(["red"] * CODE_LENGTH)
        self.assertTrue(g.won and g.over)
        self.assertIn("secret", g.to_dict())

    def test_secret_hidden_until_over(self):
        g = Game(secret=["red"] * CODE_LENGTH)
        g.guess(["blue"] * CODE_LENGTH)
        self.assertNotIn("secret", g.to_dict())

    def test_lose_after_max_attempts(self):
        g = Game(secret=["red"] * CODE_LENGTH)
        for _ in range(MAX_ATTEMPTS):
            g.guess(["blue"] * CODE_LENGTH)
        self.assertTrue(g.over and not g.won)

    def test_validation(self):
        self.assertIsNotNone(validate_guess(["red"]))
        self.assertIsNotNone(validate_guess(["pink"] * CODE_LENGTH))
        self.assertIsNone(validate_guess(["red"] * CODE_LENGTH))


if __name__ == "__main__":
    unittest.main()
