# Maze Runner

A browser maze game in **Python + Flask**. Python generates a fresh maze every time and can also solve it, so you can race the shortest route or ask for a hint.

- Move the teal square to the red one with the arrow keys or WASD (on-screen buttons appear on touch screens)
- **Show path** draws the shortest route from where you are right now
- Your score is moves and time, compared with the perfect route
- Every maze has a **seed**; the same seed always gives the same maze

## How it works

| Idea | Where |
| --- | --- |
| Maze generation: randomised depth-first search (a "recursive backtracker"), which carves a maze with exactly one route between any two cells | `maze.py` `generate()` |
| Solving: breadth-first search (BFS), which always finds the shortest path | `maze.py` `solve()` |
| Web API: `/api/maze` and `/api/solve` | `app.py` |
| Drawing and controls on an HTML canvas | `static/app.js` |

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Test

```bash
python -m unittest discover -s tests -t .
```

## Ideas to extend it

- Share a maze with a friend by putting the seed in the page URL
- A leaderboard per seed, stored in SQLite
- Fog of war: only show the cells near the player
- Swap BFS for A* and compare how many cells each search visits
- Add a second algorithm (Prim's or Kruskal's) for different-looking mazes

## Publish to GitHub

```bash
git init && git add . && git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<you>/maze-runner.git
git push -u origin main
```
