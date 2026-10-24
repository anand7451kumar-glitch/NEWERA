"""Snake + AI autopilot: a Flask web game. Run with `python app.py`."""
from flask import Flask, jsonify, render_template, request

from snake import next_move

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


def is_cell(p, w, h):
    return (isinstance(p, list) and len(p) == 2 and all(isinstance(v, int) for v in p)
            and 0 <= p[0] < w and 0 <= p[1] < h)


@app.post("/api/ai")
def ai():
    data = request.get_json(silent=True) or {}
    w, h, snake, food = data.get("width"), data.get("height"), data.get("snake"), data.get("food")
    ok = (isinstance(w, int) and isinstance(h, int) and 5 <= w <= 60 and 5 <= h <= 60
          and isinstance(snake, list) and 1 <= len(snake) <= w * h
          and all(is_cell(p, w, h) for p in snake) and is_cell(food, w, h))
    if not ok:
        return jsonify(error="Bad game state."), 400
    return jsonify(move=next_move(snake, food, w, h))


if __name__ == "__main__":
    app.run(debug=True)
