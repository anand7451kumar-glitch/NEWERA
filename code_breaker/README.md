# Code Breaker

A Mastermind-style puzzle game in your browser, built with **Python + Flask**.
The computer picks a hidden 4-colour code; you have 10 guesses to crack it.

- White hint dot: right colour, right slot
- Grey hint dot: right colour, wrong slot

The secret code is kept on the server and only revealed when the game ends, so you can't peek at it in the browser.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Test

```bash
python -m unittest discover -s tests -t .
```

## Project layout

| Path | What it does |
| --- | --- |
| `game.py` | Game rules and scoring (no web code) |
| `app.py` | Flask routes: `/`, `/api/state`, `/api/new`, `/api/guess` |
| `templates/`, `static/` | The web UI |
| `tests/` | Unit tests for the game logic |

## Ideas to extend it

- Daily puzzle with a seeded code
- Difficulty levels (5 slots, 8 colours)
- Leaderboard stored in SQLite
- A solver that cracks the code in 5 guesses or fewer

## Publish to GitHub

```bash
git init && git add . && git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<you>/code-breaker.git
git push -u origin main
```
