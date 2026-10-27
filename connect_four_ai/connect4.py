"""Connect Four engine: minimax search with alpha-beta pruning. No web code.
Board: 6 rows x 7 columns, row 0 is the top. 0 = empty, 1 = human, 2 = AI."""
import random

ROWS, COLS = 6, 7
WIN = 10 ** 6
CENTRE_FIRST = sorted(range(COLS), key=lambda c: abs(c - COLS // 2))  # centre columns are stronger, so try them first


def _lines():
    """Every possible row of four cells (69 of them)."""
    out = []
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                cells = [(r + i * dr, c + i * dc) for i in range(4)]
                if all(0 <= rr < ROWS and 0 <= cc < COLS for rr, cc in cells):
                    out.append(cells)
    return out


LINES = _lines()


def legal(board):
    return [c for c in CENTRE_FIRST if board[0][c] == 0]


def drop(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            board[r][col] = player
            return r
    raise ValueError("Column is full")


def winner(board):
    """(player, cells) if someone has four in a row, else None."""
    for cells in LINES:
        v = board[cells[0][0]][cells[0][1]]
        if v and all(board[r][c] == v for r, c in cells):
            return v, [list(p) for p in cells]
    return None


def evaluate(board, me):
    """Score a position for `me`. +-WIN means four in a row; otherwise reward open lines of two or three."""
    opp = 3 - me
    score = 0
    for cells in LINES:
        vals = [board[r][c] for r, c in cells]
        mine, theirs = vals.count(me), vals.count(opp)
        if mine == 4:
            return WIN
        if theirs == 4:
            return -WIN
        if theirs == 0:
            score += (0, 1, 5, 50)[mine]
        elif mine == 0:
            score -= (0, 1, 5, 60)[theirs]
    mid = COLS // 2
    return score + 3 * sum(board[r][mid] == me for r in range(ROWS)) - 3 * sum(board[r][mid] == opp for r in range(ROWS))


def search(board, depth, alpha, beta, to_move, me):
    score = evaluate(board, me)
    if abs(score) >= WIN:
        return score + depth if score > 0 else score - depth  # prefer quick wins and slow losses
    moves = legal(board)
    if not moves:
        return 0
    if depth == 0:
        return score
    if to_move == me:
        best = -float("inf")
        for c in moves:
            r = drop(board, c, to_move)
            best = max(best, search(board, depth - 1, alpha, beta, 3 - to_move, me))
            board[r][c] = 0
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    best = float("inf")
    for c in moves:
        r = drop(board, c, to_move)
        best = min(best, search(board, depth - 1, alpha, beta, 3 - to_move, me))
        board[r][c] = 0
        beta = min(beta, best)
        if alpha >= beta:
            break
    return best


def best_move(board, me, depth, rng=random):
    scores = {}
    for c in legal(board):
        r = drop(board, c, me)
        scores[c] = search(board, depth - 1, -float("inf"), float("inf"), 3 - me, me)
        board[r][c] = 0
    top = max(scores.values())
    return rng.choice([c for c, s in scores.items() if s == top])  # random among equally good moves


def play_turn(board, depth, ai=2, rng=random):
    """Check for a finished game, otherwise let the AI move. Returns the new board and the result."""
    res = {"board": board, "winner": 0, "line": [], "draw": False, "row": None, "col": None}
    done = winner(board)
    if done:
        res.update(winner=done[0], line=done[1])
        return res
    if not legal(board):
        res["draw"] = True
        return res
    col = best_move(board, ai, depth, rng)
    res.update(col=col, row=drop(board, col, ai))
    done = winner(board)
    if done:
        res.update(winner=done[0], line=done[1])
    elif not legal(board):
        res["draw"] = True
    return res
