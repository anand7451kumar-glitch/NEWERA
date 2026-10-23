# Lights Out

A classic puzzle in your browser, built with **Python + Flask**. Clicking a cell flips it and its four neighbours; turn every light off.

- Puzzles are made by pressing random cells on a dark board, so every one is solvable
- **Hint** asks Python to solve the current board and highlights a cell to press
- The solver is real maths: each cell is an equation over GF(2), solved with Gaussian elimination (`lightsout.py`)

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

- Find the solution with the fewest presses
- Show the number of moves the best solution needs
- Larger boards and a timer
- Wrap-around (toroidal) boards
