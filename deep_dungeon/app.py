"""Deep Dungeon: a Flask roguelike. Run with `python app.py`."""
import secrets
from collections import OrderedDict

from flask import Flask, jsonify, render_template, request

from dungeon import Game

app = Flask(__name__)
RUNS = OrderedDict()
MAX_RUNS = 50


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/new")
def new_game():
    run = secrets.token_hex(6)
    RUNS[run] = Game()
    while len(RUNS) > MAX_RUNS:
        RUNS.popitem(last=False)
    return jsonify(run=run, state=RUNS[run].state())


@app.post("/api/move")
def move():
    data = request.get_json(silent=True) or {}
    game, dx, dy = RUNS.get(data.get("run")), data.get("dx"), data.get("dy")
    if game is None:
        return jsonify(error="Unknown game. Press New game."), 404
    if not (isinstance(dx, int) and isinstance(dy, int) and abs(dx) + abs(dy) <= 1):
        return jsonify(error="Bad move."), 400
    game.move(dx, dy)
    return jsonify(game.state())


if __name__ == "__main__":
    app.run(debug=True)
