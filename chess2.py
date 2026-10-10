#!/usr/bin/env python3
"""
Simple terminal Chess game in pure Python.
Two players take turns entering moves in algebraic notation (e.g. e2e4, g1f3, e7e8q).
"""

from typing import Optional, List, Tuple

# Piece representation: uppercase = White, lowercase = Black
EMPTY = '.'
WHITE = 'w'
BLACK = 'b'

PIECE_VALUES = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
    'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0,
}

class ChessGame:
    def __init__(self):
        self.board = self._starting_board()
        self.turn = WHITE
        self.castling = {'K': True, 'Q': True, 'k': True, 'q': True}  # rights
        self.en_passant: Optional[Tuple[int, int]] = None  # target square
        self.halfmove = 0
        self.fullmove = 1
        self.history: List[str] = []
        self.game_over = False
        self.result = None

    def _starting_board(self) -> List[List[str]]:
        return [
            list('rnbqkbnr'),
            list('pppppppp'),
            list(EMPTY * 8),
            list(EMPTY * 8),
            list(EMPTY * 8),
            list(EMPTY * 8),
            list('PPPPPPPP'),
            list('RNBQKBNR'),
        ]

    def display(self):
        print("\n  a b c d e f g h")
        print("  ---------------")
        for rank in range(8):
            row = self.board[rank]
            print(f"{8 - rank} {' '.join(row)} {8 - rank}")
        print("  ---------------")
        print("  a b c d e f g h")
        print(f"\nTurn: {'White' if self.turn == WHITE else 'Black'}")
        if self.en_passant:
            print(f"En passant target: {self._sq_to_alg(*self.en_passant)}")

    def _sq_to_alg(self, r: int, c: int) -> str:
        return f"{chr(ord('a') + c)}{8 - r}"

    def _alg_to_sq(self, alg: str) -> Tuple[int, int]:
        file = ord(alg[0].lower()) - ord('a')
        rank = 8 - int(alg[1])
        return rank, file

    def _is_on_board(self, r: int, c: int) -> bool:
        return 0 <= r < 8 and 0 <= c < 8

    def _color(self, piece: str) -> Optional[str]:
        if piece == EMPTY:
            return None
        return WHITE if piece.isupper() else BLACK

    def _opposite(self, color: str) -> str:
        return BLACK if color == WHITE else WHITE

    def _find_king(self, color: str) -> Tuple[int, int]:
        target = 'K' if color == WHITE else 'k'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return r, c
        raise RuntimeError("King not found")

    def _is_attacked(self, r: int, c: int, by_color: str) -> bool:
        # Check every possible attacker
        for ar in range(8):
            for ac in range(8):
                piece = self.board[ar][ac]
                if self._color(piece) != by_color:
                    continue
                if self._can_piece_attack(piece, ar, ac, r, c):
                    return True
        return False

    def _can_piece_attack(self, piece: str, fr: int, fc: int, tr: int, tc: int) -> bool:
        dr, dc = tr - fr, tc - fc
        p = piece.upper()

        if p == 'P':
            direction = -1 if piece.isupper() else 1
            # Capture diagonally
            if abs(dc) == 1 and dr == direction:
                return True
            return False

        if p == 'N':
            return (abs(dr), abs(dc)) in [(1, 2), (2, 1)]

        if p == 'B':
            if abs(dr) != abs(dc):
                return False
            return self._clear_path(fr, fc, tr, tc)

        if p == 'R':
            if dr != 0 and dc != 0:
                return False
            return self._clear_path(fr, fc, tr, tc)

        if p == 'Q':
            if abs(dr) != abs(dc) and dr != 0 and dc != 0:
                return False
            return self._clear_path(fr, fc, tr, tc)

        if p == 'K':
            return max(abs(dr), abs(dc)) == 1

        return False

    def _clear_path(self, fr: int, fc: int, tr: int, tc: int) -> bool:
        dr = 0 if tr == fr else (1 if tr > fr else -1)
        dc = 0 if tc == fc else (1 if tc > fc else -1)
        r, c = fr + dr, fc + dc
        while (r, c) != (tr, tc):
            if self.board[r][c] != EMPTY:
                return False
            r += dr
            c += dc
        return True

    def _is_in_check(self, color: str) -> bool:
        kr, kc = self._find_king(color)
        return self._is_attacked(kr, kc, self._opposite(color))

    def _generate_moves_for_piece(self, r: int, c: int) -> List[Tuple[int, int, Optional[str]]]:
        """Returns list of (to_r, to_c, promotion_piece or None)"""
        piece = self.board[r][c]
        color = self._color(piece)
        moves = []
        p = piece.upper()

        def add(tr, tc, promo=None):
            if self._is_on_board(tr, tc):
                target = self.board[tr][tc]
                if target == EMPTY or self._color(target) != color:
                    moves.append((tr, tc, promo))

        if p == 'P':
            direction = -1 if color == WHITE else 1
            start_rank = 6 if color == WHITE else 1
            # Single push
            if self.board[r + direction][c] == EMPTY:
                # Promotion?
                if (color == WHITE and r + direction == 0) or (color == BLACK and r + direction == 7):
                    for promo in 'QRBN':
                        moves.append((r + direction, c, promo if color == WHITE else promo.lower()))
                else:
                    moves.append((r + direction, c, None))
                # Double push
                if r == start_rank and self.board[r + 2 * direction][c] == EMPTY:
                    moves.append((r + 2 * direction, c, None))
            # Captures
            for dc in (-1, 1):
                tr, tc = r + direction, c + dc
                if self._is_on_board(tr, tc):
                    target = self.board[tr][tc]
                    if target != EMPTY and self._color(target) != color:
                        if (color == WHITE and tr == 0) or (color == BLACK and tr == 7):
                            for promo in 'QRBN':
                                moves.append((tr, tc, promo if color == WHITE else promo.lower()))
                        else:
                            moves.append((tr, tc, None))
                    # En passant
                    elif self.en_passant == (tr, tc):
                        moves.append((tr, tc, None))

        elif p == 'N':
            for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                add(r + dr, c + dc)

        elif p == 'B':
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                tr, tc = r + dr, c + dc
                while self._is_on_board(tr, tc):
                    target = self.board[tr][tc]
                    if target == EMPTY:
                        moves.append((tr, tc, None))
                    else:
                        if self._color(target) != color:
                            moves.append((tr, tc, None))
                        break
                    tr += dr
                    tc += dc

        elif p == 'R':
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                tr, tc = r + dr, c + dc
                while self._is_on_board(tr, tc):
                    target = self.board[tr][tc]
                    if target == EMPTY:
                        moves.append((tr, tc, None))
                    else:
                        if self._color(target) != color:
                            moves.append((tr, tc, None))
                        break
                    tr += dr
                    tc += dc

        elif p == 'Q':
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                tr, tc = r + dr, c + dc
                while self._is_on_board(tr, tc):
                    target = self.board[tr][tc]
                    if target == EMPTY:
                        moves.append((tr, tc, None))
                    else:
                        if self._color(target) != color:
                            moves.append((tr, tc, None))
                        break
                    tr += dr
                    tc += dc

        elif p == 'K':
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    add(r + dr, c + dc)
            # Castling
            if color == WHITE and r == 7 and c == 4:
                # Kingside
                if self.castling['K'] and self.board[7][5] == EMPTY and self.board[7][6] == EMPTY:
                    if not self._is_attacked(7, 4, BLACK) and not self._is_attacked(7, 5, BLACK) and not self._is_attacked(7, 6, BLACK):
                        moves.append((7, 6, None))
                # Queenside
                if self.castling['Q'] and self.board[7][3] == EMPTY and self.board[7][2] == EMPTY and self.board[7][1] == EMPTY:
                    if not self._is_attacked(7, 4, BLACK) and not self._is_attacked(7, 3, BLACK) and not self._is_attacked(7, 2, BLACK):
                        moves.append((7, 2, None))
            elif color == BLACK and r == 0 and c == 4:
                if self.castling['k'] and self.board[0][5] == EMPTY and self.board[0][6] == EMPTY:
                    if not self._is_attacked(0, 4, WHITE) and not self._is_attacked(0, 5, WHITE) and not self._is_attacked(0, 6, WHITE):
                        moves.append((0, 6, None))
                if self.castling['q'] and self.board[0][3] == EMPTY and self.board[0][2] == EMPTY and self.board[0][1] == EMPTY:
                    if not self._is_attacked(0, 4, WHITE) and not self._is_attacked(0, 3, WHITE) and not self._is_attacked(0, 2, WHITE):
                        moves.append((0, 2, None))

        return moves

    def get_legal_moves(self) -> List[Tuple[int, int, int, int, Optional[str]]]:
        """Returns list of (from_r, from_c, to_r, to_c, promotion)"""
        legal = []
        for r in range(8):
            for c in range(8):
                if self._color(self.board[r][c]) != self.turn:
                    continue
                for tr, tc, promo in self._generate_moves_for_piece(r, c):
                    # Make temporary move and check if king is safe
                    if self._is_legal_after_move(r, c, tr, tc, promo):
                        legal.append((r, c, tr, tc, promo))
        return legal

    def _is_legal_after_move(self, fr, fc, tr, tc, promo) -> bool:
        # Save state
        board_copy = [row[:] for row in self.board]
        castling_copy = self.castling.copy()
        ep_copy = self.en_passant
        piece = self.board[fr][fc]
        captured = self.board[tr][tc]

        # Handle en passant capture
        if piece.upper() == 'P' and self.en_passant == (tr, tc) and captured == EMPTY:
            # Remove the pawn that was captured en passant
            if self.turn == WHITE:
                self.board[tr + 1][tc] = EMPTY
            else:
                self.board[tr - 1][tc] = EMPTY

        # Handle castling rook move
        if piece.upper() == 'K' and abs(tc - fc) == 2:
            if tc == 6:  # kingside
                self.board[fr][5] = self.board[fr][7]
                self.board[fr][7] = EMPTY
            else:  # queenside
                self.board[fr][3] = self.board[fr][0]
                self.board[fr][0] = EMPTY

        # Move the piece
        self.board[tr][tc] = promo if promo else piece
        self.board[fr][fc] = EMPTY

        # Check if own king is in check
        in_check = self._is_in_check(self.turn)

        # Restore
        self.board = board_copy
        self.castling = castling_copy
        self.en_passant = ep_copy
        return not in_check

    def make_move(self, move_str: str) -> bool:
        """Parse algebraic like e2e4 or e7e8q and make the move if legal."""
        move_str = move_str.strip().lower().replace(' ', '')
        if len(move_str) < 4:
            return False

        try:
            fr, fc = self._alg_to_sq(move_str[0:2])
            tr, tc = self._alg_to_sq(move_str[2:4])
            promo = move_str[4] if len(move_str) > 4 else None
            if promo:
                promo = promo.upper() if self.turn == WHITE else promo.lower()
        except Exception:
            return False

        legal = self.get_legal_moves()
        matching = [m for m in legal if m[0] == fr and m[1] == fc and m[2] == tr and m[3] == tc]
        if promo:
            matching = [m for m in matching if m[4] and m[4].upper() == promo.upper()]
        else:
            # Prefer non-promotion if both exist (shouldn't normally)
            matching = [m for m in matching if m[4] is None] or matching

        if not matching:
            return False

        _, _, _, _, actual_promo = matching[0]
        self._apply_move(fr, fc, tr, tc, actual_promo)
        return True

    def _apply_move(self, fr, fc, tr, tc, promo):
        piece = self.board[fr][fc]
        captured = self.board[tr][tc]

        # En passant capture
        if piece.upper() == 'P' and self.en_passant == (tr, tc) and captured == EMPTY:
            if self.turn == WHITE:
                self.board[tr + 1][tc] = EMPTY
            else:
                self.board[tr - 1][tc] = EMPTY
            captured = 'p' if self.turn == WHITE else 'P'  # for halfmove clock

        # Castling
        if piece.upper() == 'K' and abs(tc - fc) == 2:
            if tc == 6:  # O-O
                self.board[fr][5] = self.board[fr][7]
                self.board[fr][7] = EMPTY
            else:  # O-O-O
                self.board[fr][3] = self.board[fr][0]
                self.board[fr][0] = EMPTY

        # Move piece (with possible promotion)
        self.board[tr][tc] = promo if promo else piece
        self.board[fr][fc] = EMPTY

        # Update castling rights
        if piece == 'K':
            self.castling['K'] = self.castling['Q'] = False
        elif piece == 'k':
            self.castling['k'] = self.castling['q'] = False
        elif piece == 'R':
            if fr == 7 and fc == 0:
                self.castling['Q'] = False
            elif fr == 7 and fc == 7:
                self.castling['K'] = False
        elif piece == 'r':
            if fr == 0 and fc == 0:
                self.castling['q'] = False
            elif fr == 0 and fc == 7:
                self.castling['k'] = False

        # Also if a rook is captured
        if captured == 'R':
            if tr == 7 and tc == 0:
                self.castling['Q'] = False
            elif tr == 7 and tc == 7:
                self.castling['K'] = False
        elif captured == 'r':
            if tr == 0 and tc == 0:
                self.castling['q'] = False
            elif tr == 0 and tc == 7:
                self.castling['k'] = False

        # En passant target
        self.en_passant = None
        if piece.upper() == 'P' and abs(tr - fr) == 2:
            self.en_passant = ((fr + tr) // 2, fc)

        # Halfmove clock
        if piece.upper() == 'P' or captured != EMPTY:
            self.halfmove = 0
        else:
            self.halfmove += 1

        # Fullmove
        if self.turn == BLACK:
            self.fullmove += 1

        # Switch turn
        self.turn = self._opposite(self.turn)

        # Record
        move_alg = self._sq_to_alg(fr, fc) + self._sq_to_alg(tr, tc)
        if promo:
            move_alg += promo.lower()
        self.history.append(move_alg)

        # Check game end
        self._check_game_end()

    def _check_game_end(self):
        legal = self.get_legal_moves()
        in_check = self._is_in_check(self.turn)

        if not legal:
            if in_check:
                self.game_over = True
                winner = 'Black' if self.turn == WHITE else 'White'
                self.result = f"Checkmate! {winner} wins."
            else:
                self.game_over = True
                self.result = "Stalemate! Draw."
        elif self.halfmove >= 100:
            self.game_over = True
            self.result = "Draw by 50-move rule."

    def play(self):
        print("=== Python Chess ===")
        print("Enter moves in the form: e2e4  or  e7e8q (for promotion)")
        print("Type 'quit' to exit, 'moves' to see legal moves, 'undo' not supported.")
        print()

        while not self.game_over:
            self.display()
            if self._is_in_check(self.turn):
                print("*** CHECK! ***")

            move = input(f"{'White' if self.turn == WHITE else 'Black'} to move > ").strip()
            if move.lower() in ('quit', 'exit', 'q'):
                print("Game aborted.")
                return
            if move.lower() == 'moves':
                legal = self.get_legal_moves()
                print("Legal moves:", ' '.join(
                    self._sq_to_alg(m[0], m[1]) + self._sq_to_alg(m[2], m[3]) + (m[4] or '')
                    for m in legal
                ))
                continue

            if not self.make_move(move):
                print("Illegal move. Try again (example: e2e4).")
                continue

        self.display()
        print("\n" + self.result)
        print("Move history:", ' '.join(self.history))

if __name__ == "__main__":
    game = ChessGame()
    game.play()