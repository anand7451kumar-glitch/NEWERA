"""Maze Runner: a Flask web game. Run with `python app.py`."""
import random

from flask import Flask, jsonify, render_template, request

from maze import generate, solve

app = Flask(__name__)


def read_args():
    size = max(5, min(request.args.get("size", 15, type=int), 41))
    seed = request.args.get("seed", type=int)
    if seed is None:
        seed = random.randrange(1_000_000)
    return size, seed


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/maze")
def get_maze():
    size, seed = read_args()
    grid = generate(size, size, seed)
    return jsonify(size=size, seed=seed, grid=grid, start=[1, 1], end=[2 * size - 1, 2 * size - 1])


@app.get("/api/solve")
def get_solution():
    """Shortest path from (r, c) to the exit. Defaults to the start cell."""
    size, seed = read_args()
    grid = generate(size, size, seed)
    pos = (request.args.get("r", 1, type=int), request.args.get("c", 1, type=int))
    path = solve(grid, pos, (2 * size - 1, 2 * size - 1))
    if path is None:
        return jsonify(error="No path from there."), 400
    return jsonify(path=path)


if __name__ == "__main__":
    app.run(debug=True)
