"""Lights Out: a Flask web puzzle. Run with `python app.py`."""
import random

from flask import Flask, jsonify, render_template, request

from lightsout import new_puzzle, solve

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/new")
def new():
    size = max(3, min(request.args.get("size", 5, type=int), 9))
    seed = request.args.get("seed", type=int)
    if seed is None:
        seed = random.randrange(1_000_000)
    return jsonify(size=size, seed=seed, board=new_puzzle(size, seed))


@app.post("/api/hint")
def hint():
    board = (request.get_json(silent=True) or {}).get("board")
    n = len(board) if isinstance(board, list) else 0
    if not 3 <= n <= 9 or any(not isinstance(r, list) or len(r) != n for r in board):
        return jsonify(error="Bad board."), 400
    presses = solve([[1 if v else 0 for v in row] for row in board])
    if presses is None:
        return jsonify(error="This board has no solution."), 400
    return jsonify(presses=presses)


if __name__ == "__main__":
    app.run(debug=True)
