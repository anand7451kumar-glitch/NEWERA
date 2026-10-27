"""Connect Four vs AI: a Flask web game. Run with `python app.py`."""
from flask import Flask, jsonify, render_template, request

from connect4 import COLS, ROWS, play_turn

app = Flask(__name__)
LEVELS = {"easy": 1, "normal": 3, "hard": 5, "expert": 6}  # how many moves ahead the AI looks


def valid_board(b):
    if not (isinstance(b, list) and len(b) == ROWS):
        return False
    if not all(isinstance(r, list) and len(r) == COLS and all(type(v) is int and v in (0, 1, 2) for v in r) for r in b):
        return False
    for c in range(COLS):  # pieces can't float: no piece above an empty cell
        gap = False
        for r in range(ROWS - 1, -1, -1):
            if b[r][c] == 0:
                gap = True
            elif gap:
                return False
    return True


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/ai")
def ai():
    data = request.get_json(silent=True) or {}
    board = data.get("board")
    if not valid_board(board):
        return jsonify(error="Bad board."), 400
    return jsonify(play_turn(board, LEVELS.get(data.get("level"), 3)))


if __name__ == "__main__":
    app.run(debug=True)
