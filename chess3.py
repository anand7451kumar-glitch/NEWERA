#!/usr/bin/env python3
"""
Graphical Chess Game using Pygame
Click a piece to select it, then click a destination square to move.
"""

import pygame
import sys
from typing import Optional, List, Tuple

# ---------------------------- Chess Logic (same as before) ----------------------------

EMPTY = '.'
WHITE = 'w'
BLACK = 'b'

class ChessGame:
    def __init__(self):
        self.board = self._starting_board()
        self.turn = WHITE
        self.castling = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant: Optional[Tuple[int, int]] = None
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
            return abs(dc) == 1 and dr == direction

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
            if self.board[r + direction][c] == EMPTY:
                if (color == WHITE and r + direction == 0) or (color == BLACK and r + direction == 7):
                    for promo in 'QRBN':
                        moves.append((r + direction, c, promo if color == WHITE else promo.lower()))
                else:
                    moves.append((r + direction, c, None))
                if r == start_rank and self.board[r + 2 * direction][c] == EMPTY:
                    moves.append((r + 2 * direction, c, None))
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
                    elif self.en_passant == (tr, tc):
                        moves.append((tr, tc, None))

        elif p == 'N':
            for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                add(r + dr, c + dc)

        elif p == 'B':
            for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
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
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
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
            for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
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
                if self.castling['K'] and self.board[7][5] == EMPTY and self.board[7][6] == EMPTY:
                    if not self._is_attacked(7,4,BLACK) and not self._is_attacked(7,5,BLACK) and not self._is_attacked(7,6,BLACK):
                        moves.append((7, 6, None))
                if self.castling['Q'] and self.board[7][3] == EMPTY and self.board[7][2] == EMPTY and self.board[7][1] == EMPTY:
                    if not self._is_attacked(7,4,BLACK) and not self._is_attacked(7,3,BLACK) and not self._is_attacked(7,2,BLACK):
                        moves.append((7, 2, None))
            elif color == BLACK and r == 0 and c == 4:
                if self.castling['k'] and self.board[0][5] == EMPTY and self.board[0][6] == EMPTY:
                    if not self._is_attacked(0,4,WHITE) and not self._is_attacked(0,5,WHITE) and not self._is_attacked(0,6,WHITE):
                        moves.append((0, 6, None))
                if self.castling['q'] and self.board[0][3] == EMPTY and self.board[0][2] == EMPTY and self.board[0][1] == EMPTY:
                    if not self._is_attacked(0,4,WHITE) and not self._is_attacked(0,3,WHITE) and not self._is_attacked(0,2,WHITE):
                        moves.append((0, 2, None))

        return moves

    def get_legal_moves(self) -> List[Tuple[int, int, int, int, Optional[str]]]:
        legal = []
        for r in range(8):
            for c in range(8):
                if self._color(self.board[r][c]) != self.turn:
                    continue
                for tr, tc, promo in self._generate_moves_for_piece(r, c):
                    if self._is_legal_after_move(r, c, tr, tc, promo):
                        legal.append((r, c, tr, tc, promo))
        return legal

    def _is_legal_after_move(self, fr, fc, tr, tc, promo) -> bool:
        board_copy = [row[:] for row in self.board]
        castling_copy = self.castling.copy()
        ep_copy = self.en_passant
        piece = self.board[fr][fc]

        if piece.upper() == 'P' and self.en_passant == (tr, tc) and self.board[tr][tc] == EMPTY:
            if self.turn == WHITE:
                self.board[tr + 1][tc] = EMPTY
            else:
                self.board[tr - 1][tc] = EMPTY

        if piece.upper() == 'K' and abs(tc - fc) == 2:
            if tc == 6:
                self.board[fr][5] = self.board[fr][7]
                self.board[fr][7] = EMPTY
            else:
                self.board[fr][3] = self.board[fr][0]
                self.board[fr][0] = EMPTY

        self.board[tr][tc] = promo if promo else piece
        self.board[fr][fc] = EMPTY

        in_check = self._is_in_check(self.turn)

        self.board = board_copy
        self.castling = castling_copy
        self.en_passant = ep_copy
        return not in_check

    def make_move(self, fr: int, fc: int, tr: int, tc: int, promo: Optional[str] = None) -> bool:
        legal = self.get_legal_moves()
        matching = [m for m in legal if m[0]==fr and m[1]==fc and m[2]==tr and m[3]==tc]
        if promo:
            matching = [m for m in matching if m[4] and m[4].upper() == promo.upper()]
        else:
            matching = [m for m in matching if m[4] is None] or matching

        if not matching:
            return False

        _, _, _, _, actual_promo = matching[0]
        self._apply_move(fr, fc, tr, tc, actual_promo)
        return True

    def _apply_move(self, fr, fc, tr, tc, promo):
        piece = self.board[fr][fc]
        captured = self.board[tr][tc]

        if piece.upper() == 'P' and self.en_passant == (tr, tc) and captured == EMPTY:
            if self.turn == WHITE:
                self.board[tr + 1][tc] = EMPTY
            else:
                self.board[tr - 1][tc] = EMPTY
            captured = 'p' if self.turn == WHITE else 'P'

        if piece.upper() == 'K' and abs(tc - fc) == 2:
            if tc == 6:
                self.board[fr][5] = self.board[fr][7]
                self.board[fr][7] = EMPTY
            else:
                self.board[fr][3] = self.board[fr][0]
                self.board[fr][0] = EMPTY

        self.board[tr][tc] = promo if promo else piece
        self.board[fr][fc] = EMPTY

        if piece == 'K':
            self.castling['K'] = self.castling['Q'] = False
        elif piece == 'k':
            self.castling['k'] = self.castling['q'] = False
        elif piece == 'R':
            if fr == 7 and fc == 0: self.castling['Q'] = False
            elif fr == 7 and fc == 7: self.castling['K'] = False
        elif piece == 'r':
            if fr == 0 and fc == 0: self.castling['q'] = False
            elif fr == 0 and fc == 7: self.castling['k'] = False

        if captured == 'R':
            if tr == 7 and tc == 0: self.castling['Q'] = False
            elif tr == 7 and tc == 7: self.castling['K'] = False
        elif captured == 'r':
            if tr == 0 and tc == 0: self.castling['q'] = False
            elif tr == 0 and tc == 7: self.castling['k'] = False

        self.en_passant = None
        if piece.upper() == 'P' and abs(tr - fr) == 2:
            self.en_passant = ((fr + tr) // 2, fc)

        if piece.upper() == 'P' or captured != EMPTY:
            self.halfmove = 0
        else:
            self.halfmove += 1

        if self.turn == BLACK:
            self.fullmove += 1

        self.turn = self._opposite(self.turn)

        move_alg = self._sq_to_alg(fr, fc) + self._sq_to_alg(tr, tc)
        if promo:
            move_alg += promo.lower()
        self.history.append(move_alg)

        self._check_game_end()

    def _check_game_end(self):
        legal = self.get_legal_moves()
        in_check = self._is_in_check(self.turn)

        if not legal:
            self.game_over = True
            if in_check:
                winner = 'Black' if self.turn == WHITE else 'White'
                self.result = f"Checkmate! {winner} wins."
            else:
                self.result = "Stalemate! Draw."
        elif self.halfmove >= 100:
            self.game_over = True
            self.result = "Draw by 50-move rule."

# ---------------------------- Pygame Graphics ----------------------------

# Colors
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE  = (181, 136, 99)
HIGHLIGHT    = (186, 202, 68)
LAST_MOVE    = (205, 210, 106)
LEGAL_DOT    = (20, 20, 20, 80)
CHECK_RED    = (235, 97, 80)
PANEL_BG     = (40, 40, 40)
TEXT_COLOR   = (240, 240, 240)

# Unicode chess pieces
PIECE_UNICODE = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
}

SQUARE_SIZE = 80
BOARD_SIZE  = 8 * SQUARE_SIZE
PANEL_WIDTH = 220
WINDOW_WIDTH  = BOARD_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = BOARD_SIZE

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Chess")
        self.clock = pygame.time.Clock()

        # Try to load a font that supports chess symbols well
        try:
            self.piece_font = pygame.font.SysFont("segoe ui symbol", 56)
        except:
            self.piece_font = pygame.font.SysFont("dejavusans", 56)
        self.ui_font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 18)

        self.game = ChessGame()
        self.selected: Optional[Tuple[int, int]] = None
        self.legal_targets: List[Tuple[int, int]] = []
        self.last_move: Optional[Tuple[Tuple[int,int], Tuple[int,int]]] = None
        self.promotion_pending: Optional[Tuple[int,int,int,int]] = None  # fr,fc,tr,tc

    def board_to_screen(self, r: int, c: int) -> Tuple[int, int]:
        return c * SQUARE_SIZE, r * SQUARE_SIZE

    def screen_to_board(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            return None
        return y // SQUARE_SIZE, x // SQUARE_SIZE

    def draw_board(self):
        for r in range(8):
            for c in range(8):
                color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

        # Highlight last move
        if self.last_move:
            for (r, c) in self.last_move:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                s.fill((*LAST_MOVE, 120))
                self.screen.blit(s, self.board_to_screen(r, c))

        # Highlight selected square
        if self.selected:
            r, c = self.selected
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((*HIGHLIGHT, 160))
            self.screen.blit(s, self.board_to_screen(r, c))

        # Highlight king in check
        if self.game._is_in_check(self.game.turn):
            kr, kc = self.game._find_king(self.game.turn)
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((*CHECK_RED, 140))
            self.screen.blit(s, self.board_to_screen(kr, kc))

    def draw_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.game.board[r][c]
                if piece == EMPTY:
                    continue
                text = self.piece_font.render(PIECE_UNICODE[piece], True, (20, 20, 20))
                # Center the piece
                x = c * SQUARE_SIZE + (SQUARE_SIZE - text.get_width()) // 2
                y = r * SQUARE_SIZE + (SQUARE_SIZE - text.get_height()) // 2 - 4
                self.screen.blit(text, (x, y))

    def draw_legal_moves(self):
        for tr, tc in self.legal_targets:
            center = (tc * SQUARE_SIZE + SQUARE_SIZE // 2,
                      tr * SQUARE_SIZE + SQUARE_SIZE // 2)
            # If target has enemy piece → bigger ring, else small dot
            target_piece = self.game.board[tr][tc]
            if target_piece != EMPTY:
                pygame.draw.circle(self.screen, (20, 20, 20), center, SQUARE_SIZE // 2 - 6, 4)
            else:
                pygame.draw.circle(self.screen, (20, 20, 20), center, 12)

    def draw_panel(self):
        panel_rect = pygame.Rect(BOARD_SIZE, 0, PANEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)

        y = 20
        # Title
        title = self.ui_font.render("Python Chess", True, TEXT_COLOR)
        self.screen.blit(title, (BOARD_SIZE + 20, y))
        y += 40

        # Turn
        turn_text = "White to move" if self.game.turn == WHITE else "Black to move"
        if self.game.game_over:
            turn_text = "Game Over"
        color = (100, 200, 100) if not self.game.game_over else (220, 80, 80)
        txt = self.ui_font.render(turn_text, True, color)
        self.screen.blit(txt, (BOARD_SIZE + 20, y))
        y += 35

        # Check indicator
        if not self.game.game_over and self.game._is_in_check(self.game.turn):
            check = self.ui_font.render("CHECK!", True, CHECK_RED)
            self.screen.blit(check, (BOARD_SIZE + 20, y))
            y += 30

        # Result
        if self.game.game_over and self.game.result:
            for i, line in enumerate(self.game.result.split('!')):
                t = self.small_font.render(line.strip() + ("!" if i == 0 else ""), True, (255, 200, 80))
                self.screen.blit(t, (BOARD_SIZE + 15, y))
                y += 22
            y += 10

        # Instructions
        y = WINDOW_HEIGHT - 140
        instructions = [
            "How to play:",
            "• Click a piece to select",
            "• Click destination to move",
            "• Click again to deselect",
            "• Promotion: auto-queen",
            "• Press R to restart",
            "• Press Esc to quit",
        ]
        for line in instructions:
            t = self.small_font.render(line, True, (180, 180, 180))
            self.screen.blit(t, (BOARD_SIZE + 15, y))
            y += 20

    def draw_promotion_dialog(self):
        if not self.promotion_pending:
            return
        # Simple overlay – auto promotes to Queen for simplicity
        # (You can expand this later with clickable buttons)
        pass

    def handle_click(self, pos):
        if self.game.game_over:
            return

        board_pos = self.screen_to_board(*pos)
        if board_pos is None:
            return

        r, c = board_pos

        # If a piece is already selected → try to move
        if self.selected:
            fr, fc = self.selected
            # Clicking the same square deselects
            if (r, c) == self.selected:
                self.selected = None
                self.legal_targets = []
                return

            # Try the move (auto-promote to Queen)
            promo = None
            piece = self.game.board[fr][fc]
            if piece.upper() == 'P' and (r == 0 or r == 7):
                promo = 'Q' if self.game.turn == WHITE else 'q'

            if self.game.make_move(fr, fc, r, c, promo):
                self.last_move = ((fr, fc), (r, c))
                self.selected = None
                self.legal_targets = []
            else:
                # If the click is on another of our pieces, select it instead
                if self.game._color(self.game.board[r][c]) == self.game.turn:
                    self.selected = (r, c)
                    self._update_legal_targets()
                else:
                    self.selected = None
                    self.legal_targets = []
        else:
            # Select a piece of the current player
            if self.game._color(self.game.board[r][c]) == self.game.turn:
                self.selected = (r, c)
                self._update_legal_targets()

    def _update_legal_targets(self):
        self.legal_targets = []
        if not self.selected:
            return
        fr, fc = self.selected
        for move in self.game.get_legal_moves():
            if move[0] == fr and move[1] == fc:
                self.legal_targets.append((move[2], move[3]))

    def restart(self):
        self.game = ChessGame()
        self.selected = None
        self.legal_targets = []
        self.last_move = None
        self.promotion_pending = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.restart()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            # Draw everything
            self.draw_board()
            self.draw_legal_moves()
            self.draw_pieces()
            self.draw_panel()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ChessGUI().run()