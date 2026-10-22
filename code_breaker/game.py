"""Pure game logic for Code Breaker (a Mastermind-style game). No Flask here."""
import random

COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]
CODE_LENGTH = 4
MAX_ATTEMPTS = 10


def new_secret(rng=random):
    return [rng.choice(COLORS) for _ in range(CODE_LENGTH)]


def score_guess(secret, guess):
    """Return (exact, misplaced): right colour+slot, right colour wrong slot."""
    exact = sum(s == g for s, g in zip(secret, guess))
    shared = sum(min(secret.count(c), guess.count(c)) for c in COLORS)
    return exact, shared - exact


def validate_guess(guess):
    if not isinstance(guess, list) or len(guess) != CODE_LENGTH:
        return f"A guess needs exactly {CODE_LENGTH} colours."
    if any(c not in COLORS for c in guess):
        return "Unknown colour in guess."
    return None


class Game:
    def __init__(self, secret=None):
        self.secret = secret or new_secret()
        self.guesses = []  # list of {"guess", "exact", "misplaced"}

    @property
    def won(self):
        return bool(self.guesses) and self.guesses[-1]["exact"] == CODE_LENGTH

    @property
    def over(self):
        return self.won or len(self.guesses) >= MAX_ATTEMPTS

    def guess(self, guess):
        exact, misplaced = score_guess(self.secret, guess)
        self.guesses.append({"guess": guess, "exact": exact, "misplaced": misplaced})

    def to_dict(self):
        data = {
            "guesses": self.guesses,
            "attempts_left": MAX_ATTEMPTS - len(self.guesses),
            "won": self.won,
            "over": self.over,
        }
        if self.over:
            data["secret"] = self.secret  # only revealed once the game ends
        return data
