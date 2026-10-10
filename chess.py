#!/usr/bin/env python3
"""
Command-line chess in pure Python (no dependencies).

Features: full legal-move rules (castling, en passant, promotion), check /
checkmate / stalemate, draw by 50-move rule, threefold repetition and
insufficient material, plus an optional computer opponent (alpha-beta search).

Run:  python chess.py
Enter moves in coordinate form: e2e4, g1f3, e7e8q (promotion; defaults to queen).
Commands: moves, board, resign, quit
"""
import random

FILES = "abcdefgh"
START = [
    list("rnbqkbnr"), list("pppppppp"),
    list("........"), list("........"), list("........"), list("........"),
    list("PPPPPPPP"), list("RNBQKBNR"),
]
UNICODE = dict(zip("KQRBNPkqrbnp", "♔♕♖♗♘♙♚♛♜♝♞♟"))
KNIGHT = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
KING = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
ROOK_D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_D = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
CORNERS = {(7, 0): "Q", (7, 7): "K", (0, 0): "q", (0, 7): "k"}


def on(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def sq_name(r, c):
    return f"{FILES[c]}{8 - r}"


def move_str(m):
    fr, fc, tr, tc, promo = m
    return sq_name(fr, fc) + sq_name(tr, tc) + promo


class Game:
    def __init__(self):
        self.board = [row[:] for row in START]
        self.white = True          # side to move
        self.castle = set("KQkq")  # castling rights
        self.ep = None             # en-passant target square (r, c)
        self.halfmove = 0
        self.fullmove = 1

    # ---------- attack / check ----------
    def attacked(self, r, c, by_white):
        b = self.board
        pawn, knight, king = ("P", "N", "K") if by_white else ("p", "n", "k")
        rook, bishop, queen = ("R", "B", "Q") if by_white else ("r", "b", "q")
        pr = r + 1 if by_white else r - 1  # row a pawn would stand on to hit (r, c)
        for dc in (-1, 1):
            if on(pr, c + dc) and b[pr][c + dc] == pawn:
                return True
        for dr, dc in KNIGHT:
            if on(r + dr, c + dc) and b[r + dr][c + dc] == knight:
                return True
        for dr, dc in KING:
            if on(r + dr, c + dc) and b[r + dr][c + dc] == king:
                return True
        for dirs, pieces in ((ROOK_D, (rook, queen)), (BISHOP_D, (bishop, queen))):
            for dr, dc in dirs:
                rr, cc = r + dr, c + dc
                while on(rr, cc):
                    p = b[rr][cc]
                    if p != ".":
                        if p in pieces:
                            return True
                        break
                    rr += dr
                    cc += dc
        return False

    def in_check(self, white):
        k = "K" if white else "k"
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == k:
                    return self.attacked(r, c, not white)
        return False

    # ---------- move generation ----------
    def pseudo_moves(self):
        moves, b, w = [], self.board, self.white
        for r in range(8):
            for c in range(8):
                p = b[r][c]
                if p == "." or p.isupper() != w:
                    continue
                t = p.upper()
                if t == "P":
                    d = -1 if w else 1
                    start = 6 if w else 1
                    last = 0 if w else 7
                    nr = r + d
                    if not on(nr, c):
                        continue
                    if b[nr][c] == ".":
                        self._pawn_move(moves, r, c, nr, c, last)
                        if r == start and b[r + 2 * d][c] == ".":
                            moves.append((r, c, r + 2 * d, c, ""))
                    for dc in (-1, 1):
                        nc = c + dc
                        if not on(nr, nc):
                            continue
                        q = b[nr][nc]
                        if q != "." and q.isupper() != w:
                            self._pawn_move(moves, r, c, nr, nc, last)
                        elif q == "." and (nr, nc) == self.ep:
                            moves.append((r, c, nr, nc, ""))
                elif t in "NK":
                    for dr, dc in (KNIGHT if t == "N" else KING):
                        nr, nc = r + dr, c + dc
                        if on(nr, nc) and (b[nr][nc] == "." or b[nr][nc].isupper() != w):
                            moves.append((r, c, nr, nc, ""))
                    if t == "K":
                        self._castling(moves, r, c)
                else:
                    dirs = ROOK_D if t == "R" else BISHOP_D if t == "B" else ROOK_D + BISHOP_D
                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        while on(nr, nc):
                            q = b[nr][nc]
                            if q == ".":
                                moves.append((r, c, nr, nc, ""))
                            else:
                                if q.isupper() != w:
                                    moves.append((r, c, nr, nc, ""))
                                break
                            nr += dr
                            nc += dc
        return moves

    @staticmethod
    def _pawn_move(moves, r, c, nr, nc, last):
        if nr == last:
            for promo in "qrbn":
                moves.append((r, c, nr, nc, promo))
        else:
            moves.append((r, c, nr, nc, ""))

    def _castling(self, moves, r, c):
        w, b = self.white, self.board
        row = 7 if w else 0
        if (r, c) != (row, 4) or self.attacked(row, 4, not w):
            return
        ks, qs = ("K", "Q") if w else ("k", "q")
        rook = "R" if w else "r"
        if (ks in self.castle and b[row][5] == b[row][6] == "." and b[row][7] == rook
                and not self.attacked(row, 5, not w) and not self.attacked(row, 6, not w)):
            moves.append((row, 4, row, 6, ""))
        if (qs in self.castle and b[row][1] == b[row][2] == b[row][3] == "." and b[row][0] == rook
                and not self.attacked(row, 3, not w) and not self.attacked(row, 2, not w)):
            moves.append((row, 4, row, 2, ""))

    def legal_moves(self):
        out = []
        for m in self.pseudo_moves():
            if not self.apply(m).in_check(self.white):
                out.append(m)
        return out

    # ---------- making moves ----------
    def apply(self, m):
        """Return a new Game with move m played (does not modify self)."""
        fr, fc, tr, tc, promo = m
        g = Game.__new__(Game)
        g.board = [row[:] for row in self.board]
        g.castle = set(self.castle)
        p = g.board[fr][fc]
        target = g.board[tr][tc]
        capture = target != "."
        g.board[fr][fc] = "."
        if p.upper() == "P" and (tr, tc) == self.ep and fc != tc and not capture:
            g.board[fr][tc] = "."  # en passant capture
            capture = True
        if p.upper() == "K" and abs(tc - fc) == 2:  # castling: move the rook too
            if tc == 6:
                g.board[tr][5], g.board[tr][7] = g.board[tr][7], "."
            else:
                g.board[tr][3], g.board[tr][0] = g.board[tr][0], "."
        if p.upper() == "K":
            g.castle -= set("KQ" if self.white else "kq")
        for sq in ((fr, fc), (tr, tc)):
            g.castle.discard(CORNERS.get(sq, ""))
        if promo:
            p = promo.upper() if self.white else promo.lower()
        g.board[tr][tc] = p
        g.ep = ((fr + tr) // 2, fc) if self.board[fr][fc].upper() == "P" and abs(tr - fr) == 2 else None
        g.halfmove = 0 if (capture or self.board[fr][fc].upper() == "P") else self.halfmove + 1
        g.fullmove = self.fullmove + (0 if self.white else 1)
        g.white = not self.white
        return g

    # ---------- game state ----------
    def key(self):
        return ("".join("".join(r) for r in self.board), self.white,
                "".join(sorted(self.castle)), self.ep)

    def insufficient_material(self):
        pieces = [p for row in self.board for p in row if p not in ".Kk"]
        if not pieces:
            return True
        if len(pieces) == 1 and pieces[0].upper() in "BN":
            return True
        return False

    def __str__(self):
        return self.render(False)

    def render(self, use_unicode=False):
        lines = []
        for r in range(8):
            row = " ".join((UNICODE[p] if use_unicode and p in UNICODE else p) for p in self.board[r])
            lines.append(f"{8 - r}  {row}")
        lines.append("   " + " ".join(FILES))
        return "\n".join(lines)


# ---------- computer player ----------
VALUES = {"P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 0}


def evaluate(g):
    """Material + small centralisation bonus, from White's point of view."""
    score = 0
    for r in range(8):
        for c in range(8):
            p = g.board[r][c]
            if p == ".":
                continue
            v = VALUES[p.upper()]
            if p.upper() in "PNB":
                v += int(10 - 2.5 * (abs(3.5 - r) + abs(3.5 - c)))
            score += v if p.isupper() else -v
    return score


def search(g, depth, alpha, beta):
    moves = g.legal_moves()
    if not moves:
        if g.in_check(g.white):
            return (-99999 - depth) if g.white else (99999 + depth)
        return 0
    if depth == 0:
        return evaluate(g)
    if g.white:
        best = -10**9
        for m in moves:
            best = max(best, search(g.apply(m), depth - 1, alpha, beta))
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    best = 10**9
    for m in moves:
        best = min(best, search(g.apply(m), depth - 1, alpha, beta))
        beta = min(beta, best)
        if alpha >= beta:
            break
    return best


def best_move(g, depth=2):
    moves = g.legal_moves()
    random.shuffle(moves)
    best, best_score = None, None
    for m in moves:
        s = search(g.apply(m), depth - 1, -10**9, 10**9)
        if best is None or (s > best_score if g.white else s < best_score):
            best, best_score = m, s
    return best


# ---------- UI ----------
def parse_move(text, legal):
    text = text.strip().lower().replace("-", "").replace(" ", "")
    if len(text) not in (4, 5):
        return None
    for m in legal:
        s = move_str(m)
        if s == text or (len(text) == 4 and s == text + "q"):
            return m
    return None


def ask(prompt, options, default):
    while True:
        a = input(prompt).strip().lower() or default
        if a in options:
            return a
        print(f"Please enter one of: {', '.join(options)}")


def main():
    print("=== Chess ===")
    mode = ask("Play vs (c)omputer or (t)wo players? [c/t]: ", ("c", "t"), "c")
    human_white = True
    depth = 2
    if mode == "c":
        human_white = ask("Play as (w)hite or (b)lack? [w/b]: ", ("w", "b"), "w") == "w"
        depth = int(ask("Computer strength 1-3 (3 is slow) [2]: ", ("1", "2", "3"), "2"))
    uni = ask("Use unicode pieces? [y/n]: ", ("y", "n"), "n") == "y"

    g = Game()
    seen = {g.key(): 1}
    while True:
        print("\n" + g.render(uni) + "\n")
        legal = g.legal_moves()
        side = "White" if g.white else "Black"
        check = g.in_check(g.white)

        if not legal:
            print(f"Checkmate! {'Black' if g.white else 'White'} wins." if check else "Stalemate - draw.")
            break
        if g.halfmove >= 100:
            print("Draw by the 50-move rule.")
            break
        if g.insufficient_material():
            print("Draw by insufficient material.")
            break
        if seen[g.key()] >= 3:
            print("Draw by threefold repetition.")
            break

        computer_turn = mode == "c" and g.white != human_white
        if computer_turn:
            m = best_move(g, depth)
            print(f"{side} (computer) plays {move_str(m)}" + ("  [check]" if g.apply(m).in_check(not g.white) else ""))
        else:
            if check:
                print("Check!")
            while True:
                text = input(f"{side} to move ({g.fullmove}): ").strip().lower()
                if text in ("quit", "exit", "q"):
                    print("Goodbye!")
                    return
                if text == "resign":
                    print(f"{side} resigns. {'Black' if g.white else 'White'} wins.")
                    return
                if text == "board":
                    print("\n" + g.render(uni) + "\n")
                    continue
                if text == "moves":
                    print(" ".join(sorted(move_str(x) for x in legal)))
                    continue
                m = parse_move(text, legal)
                if m:
                    break
                print("Illegal or unrecognised move. Type 'moves' to list legal moves.")
        g = g.apply(m)
        seen[g.key()] = seen.get(g.key(), 0) + 1


if __name__ == "__main__":
    main()