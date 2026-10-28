"""Wordle Coach: a Flask web game. Run with `python app.py`."""
import secrets
from collections import OrderedDict

from flask import Flask, jsonify, render_template, request

from wordle import Game, best_guess
from words import WORDS

app = Flask(__name__)
WORD_SET = set(WORDS)
GAMES = OrderedDict()
MAX_GAMES = 100


def find_game():
    data = request.get_json(silent=True) or {}
    return GAMES.get(data.get("run")), data


@app.get("/")
def index():
    return render_template("index.html", total=len(WORDS))


@app.post("/api/new")
def new_game():
    run = secrets.token_hex(6)
    GAMES[run] = Game()
    while len(GAMES) > MAX_GAMES:
        GAMES.popitem(last=False)
    return jsonify(run=run, remaining=len(WORDS))


@app.post("/api/guess")
def guess():
    game, data = find_game()
    word = str(data.get("word", "")).lower()
    if game is None:
        return jsonify(error="Unknown game. Press New game."), 404
    if game.over:
        return jsonify(error="This game is over."), 400
    if word not in WORD_SET:
        return jsonify(error="Not in the word list."), 400
    return jsonify(game.guess(word))


@app.post("/api/hint")
def hint():
    game, _ = find_game()
    if game is None or game.over:
        return jsonify(error="No game in progress."), 400
    candidates = game.candidates()
    word, bits = best_guess(candidates)
    return jsonify(word=word, bits=round(bits, 1), remaining=len(candidates))


if __name__ == "__main__":
    app.run(debug=True)
