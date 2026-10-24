# Rocket Evolution

Watch Python **evolve** a flock of rockets until they can fly around walls you draw. Nobody programs the route. A genetic algorithm discovers it by breeding the rockets that got closest.

## How to use it

1. Draw walls by dragging on the sky (mouse or finger), or press **Wall** / **Maze**
2. Press **Evolve**. Generation 1 is random steering and almost everyone crashes
3. Each generation the best rockets breed. Watch the green line of the best rocket improve, and the chart climb
4. Change the walls at any time and the flock starts again from scratch. Use **Instant** speed to watch dozens of generations in seconds

## How it works (`evolve.py`)

| Idea | What it does |
| --- | --- |
| **Genome** | A launch heading plus a small steering change for each of 300 time steps |
| **Fitness** | Each rocket is scored by the closest it got to the target *measured around the walls*. A breadth-first search from the target builds a "distance map", so a rocket pressed against a wall scores worse than one lined up with the gap. Reaching the target always beats not reaching it, and sooner is better |
| **Selection** | Tournament selection: pick 4 random rockets, the fittest becomes a parent |
| **Crossover** | A child takes the start of one parent's genome and the end of the other's |
| **Mutation** | Rare random changes everywhere, plus heavier changes in the stretch just before the parent crashed, because genes after a crash never ran |
| **Elitism** | The 2 best genomes survive unchanged, so progress is never lost |

The browser only draws. The web API is two calls in `app.py`: `/api/new` (send walls) and `/api/step` (fly one generation and get every rocket's path).

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

- Moving walls or a moving target
- A second flock evolving against the first (predators and prey)
- Let rockets run out of fuel
- Tune the mutation rates in `evolve.py` and see how the chart changes
- Replace the distance-map fitness with plain straight-line distance and watch the rockets get stuck behind walls
