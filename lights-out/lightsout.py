"""Lights Out logic. Pressing a cell flips it and its 4 neighbours; goal: all lights off.
The solver treats the board as equations over GF(2) (arithmetic where 1 + 1 = 0)."""
import random

NEIGHBOURS = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))


def press(board, r, c):
    n = len(board)
    for dr, dc in NEIGHBOURS:
        a, b = r + dr, c + dc
        if 0 <= a < n and 0 <= b < n:
            board[a][b] ^= 1


def new_puzzle(n, seed=None):
    """Start from an all-off board and press random cells, so it is always solvable."""
    rng = random.Random(seed)
    board = [[0] * n for _ in range(n)]
    while not any(any(row) for row in board):
        for r in range(n):
            for c in range(n):
                if rng.random() < 0.5:
                    press(board, r, c)
    return board


def solve(board):
    """Return a list of (row, col) presses that turns every light off, or None."""
    n = len(board)
    N = n * n
    rows = []
    for i in range(n):
        for j in range(n):
            mask = 0
            for dr, dc in NEIGHBOURS:
                a, b = i + dr, j + dc
                if 0 <= a < n and 0 <= b < n:
                    mask |= 1 << (a * n + b)
            if board[i][j]:
                mask |= 1 << N  # right-hand side of the equation
            rows.append(mask)
    pivots, r = [], 0
    for col in range(N):
        p = next((k for k in range(r, N) if rows[k] >> col & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for k in range(N):
            if k != r and rows[k] >> col & 1:
                rows[k] ^= rows[r]
        pivots.append(col)
        r += 1
    if any(rows[k] == 1 << N for k in range(r, N)):
        return None
    x = [0] * N
    for k, col in enumerate(pivots):
        x[col] = rows[k] >> N & 1
    return [(i // n, i % n) for i in range(N) if x[i]]
