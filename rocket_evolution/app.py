"""Rocket Evolution: a Flask web app. Run with `python app.py`."""
import secrets
from collections import OrderedDict

from flask import Flask, jsonify, render_template, request

from evolve import H, MIN_WALL, W, Evolver

app = Flask(__name__)

MAX_RUNS = 20
MAX_WALLS = 30
RUNS = OrderedDict()  # run id -> Evolver (oldest runs are dropped first)


def clean_walls(raw):
    """Validate walls sent by the browser. Returns a list of (x, y, w, h) or None if invalid."""
    if not isinstance(raw, list) or len(raw) > MAX_WALLS:
        return None
    walls = []
    for r in raw:
        if not (isinstance(r, list) and len(r) == 4 and all(isinstance(v, (int, float)) for v in r)):
            return None
        x, y, w, h = (int(v) for v in r)
        x, y = max(0, min(x, W - 1)), max(0, min(y, H - 1))
        w, h = max(MIN_WALL, min(w, W - x)), max(MIN_WALL, min(h, H - y))
        walls.append((x, y, w, h))
    return walls


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/new")
def new_run():
    walls = clean_walls((request.get_json(silent=True) or {}).get("walls", []))
    if walls is None:
        return jsonify(error="Bad walls."), 400
    run_id = secrets.token_hex(6)
    RUNS[run_id] = Evolver(walls)
    while len(RUNS) > MAX_RUNS:
        RUNS.popitem(last=False)
    return jsonify(run=run_id)


@app.post("/api/step")
def step():
    evolver = RUNS.get((request.get_json(silent=True) or {}).get("run"))
    if evolver is None:
        return jsonify(error="Unknown run. Press Reset."), 404
    return jsonify(evolver.step())


if __name__ == "__main__":
    app.run(debug=True)
