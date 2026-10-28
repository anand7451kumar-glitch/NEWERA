"""Wordle engine plus an information-theory coach. No web code.
Feedback per letter: 2 = right spot (green), 1 = in the word elsewhere (yellow), 0 = not in the word (grey)."""
import math
import random
from collections import Counter

from words import WORDS

MAX_GUESSES = 6


def feedback(guess, answer):
    res = [0] * 5
    left = Counter()
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            res[i] = 2
        else:
            left[a] += 1          # answer letters not yet matched, available for yellows
    for i, g in enumerate(guess):
        if res[i] == 0 and left[g] > 0:
            res[i] = 1
            left[g] -= 1
    return tuple(res)


def entropy(guess, candidates):
    """Expected information (in bits) from playing `guess` when any candidate could be the answer."""
    counts = Counter(feedback(guess, c) for c in candidates)
    n = len(candidates)
    return -sum(k / n * math.log2(k / n) for k in counts.values())


def best_guess(candidates, sample=150):
    """The candidate that is expected to narrow the field the most."""
    if len(candidates) <= 2:
        return candidates[0], math.log2(len(candidates))
    pool = candidates if len(candidates) <= sample else random.Random(1).sample(candidates, sample)
    return max(((w, entropy(w, candidates)) for w in pool), key=lambda t: t[1])


class Game:
    def __init__(self, rng=random):
        self.secret = rng.choice(WORDS)
        self.history = []  # (guess, pattern)

    @property
    def solved(self):
        return bool(self.history) and self.history[-1][0] == self.secret

    @property
    def over(self):
        return self.solved or len(self.history) >= MAX_GUESSES

    def candidates(self):
        """Words that would have produced exactly the feedback seen so far."""
        return [w for w in WORDS if all(feedback(g, w) == p for g, p in self.history)]

    def guess(self, word):
        before = len(self.candidates())
        pattern = feedback(word, self.secret)
        self.history.append((word, pattern))
        after = len(self.candidates())
        return {"pattern": list(pattern), "solved": self.solved, "over": self.over,
                "answer": self.secret if self.over else None,
                "remaining": after, "bits": round(math.log2(before / after), 1)}
