"""Code Breaker: a small Flask web game. Run with `python app.py`."""
import secrets

from flask import Flask, jsonify, render_template, request, session

from game import CODE_LENGTH, COLORS, MAX_ATTEMPTS, Game, validate_guess

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# The secret code lives on the server, so it can't be read from the browser.
GAMES = {}


def current_game():
    gid = session.get("gid")
    if gid not in GAMES:
        gid = secrets.token_hex(8)
        session["gid"] = gid
        GAMES[gid] = Game()
    return GAMES[gid]


@app.get("/")
def index():
    return render_template("index.html", colors=COLORS, length=CODE_LENGTH, max_attempts=MAX_ATTEMPTS)


@app.get("/api/state")
def state():
    return jsonify(current_game().to_dict())


@app.post("/api/new")
def new_game():
    session["gid"] = None
    return jsonify(current_game().to_dict())


@app.post("/api/guess")
def guess():
    game = current_game()
    if game.over:
        return jsonify(error="This game is over. Start a new one."), 400
    body = request.get_json(silent=True) or {}
    error = validate_guess(body.get("guess"))
    if error:
        return jsonify(error=error), 400
    game.guess(body["guess"])
    return jsonify(game.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
