"""Rocket evolution: a genetic algorithm that breeds rockets to fly around obstacles.

Each rocket has a genome: one thrust direction (an angle) for every time step.
Every generation: fly all rockets, score them, then breed the next generation from the best ones.
Pure Python, no web code.
"""
import math
import random
from collections import deque

W, H = 640, 480
START = (40.0, 440.0)
TARGET = (600.0, 60.0)
TARGET_R = 18.0
STEPS = 300           # genes per genome = time steps per flight
TURN = 0.3            # max turn per step (radians); a gene is a steering change, not a direction
POP = 50
CELL = 8              # grid cell size for the distance map
THRUST = 0.5
MAX_SPEED = 6.0
UNREACHABLE = 9999
NEAR_WINDOW, P_NEAR, P_BASE = 40, 0.10, 0.002  # mutation: high near where a parent crashed, low elsewhere
MIN_WALL = 14         # thinner walls could be tunnelled through at top speed


class World:
    """The obstacles, plus a map of how far (around the walls) every spot is from the target."""

    def __init__(self, rects):
        self.rects = [tuple(r) for r in rects]
        self.cols, self.rows = W // CELL, H // CELL
        self.field = self._distance_field()

    def hits(self, x, y):
        if not (0 <= x < W and 0 <= y < H):
            return True
        return any(rx <= x < rx + rw and ry <= y < ry + rh for rx, ry, rw, rh in self.rects)

    def _blocked(self, c, r):
        x0, y0 = c * CELL, r * CELL
        return any(rx < x0 + CELL and rx + rw > x0 and ry < y0 + CELL and ry + rh > y0
                   for rx, ry, rw, rh in self.rects)

    def _distance_field(self):
        """Breadth-first search outwards from the target. Distance is in grid cells."""
        field = [[UNREACHABLE] * self.cols for _ in range(self.rows)]
        queue = deque()
        for r in range(self.rows):
            for c in range(self.cols):
                cx, cy = c * CELL + CELL / 2, r * CELL + CELL / 2
                if math.hypot(cx - TARGET[0], cy - TARGET[1]) <= TARGET_R + CELL and not self._blocked(c, r):
                    field[r][c] = 0
                    queue.append((c, r))
        while queue:
            c, r = queue.popleft()
            for nc, nr in ((c + 1, r), (c - 1, r), (c, r + 1), (c, r - 1)):
                if 0 <= nc < self.cols and 0 <= nr < self.rows and field[nr][nc] == UNREACHABLE \
                        and not self._blocked(nc, nr):
                    field[nr][nc] = field[r][c] + 1
                    queue.append((nc, nr))
        return field

    def distance(self, x, y):
        c, r = int(x // CELL), int(y // CELL)
        if 0 <= c < self.cols and 0 <= r < self.rows:
            return self.field[r][c]
        return UNREACHABLE


def fly(world, genes):
    """Simulate one rocket. Returns its path and how the flight ended."""
    x, y = START
    vx = vy = 0.0
    path = [(round(x), round(y))]
    closest = world.distance(x, y)
    status = "time"
    heading = 0.0
    for i, gene in enumerate(genes):
        heading = gene if i == 0 else heading + gene   # gene 0 is the launch heading, the rest are turns
        vx += THRUST * math.cos(heading)
        vy += THRUST * math.sin(heading)
        speed = math.hypot(vx, vy)
        if speed > MAX_SPEED:
            vx, vy = vx * MAX_SPEED / speed, vy * MAX_SPEED / speed
        x += vx
        y += vy
        path.append((round(x), round(y)))
        if world.hits(x, y):
            status = "crash"
            break
        closest = min(closest, world.distance(x, y))
        if math.hypot(x - TARGET[0], y - TARGET[1]) <= TARGET_R:
            status, closest = "goal", 0
            break
    return {"path": path, "status": status, "closest": closest, "steps": len(path) - 1}


def fitness(result):
    if result["status"] == "goal":
        return 2.0 + (STEPS - result["steps"]) / STEPS   # reaching it always beats not reaching it
    return 1.0 / (1.0 + result["closest"]) ** 2


class Evolver:
    def __init__(self, rects, seed=None, pop=POP):
        self.rng = random.Random(seed)
        self.world = World(rects)
        self.pop = [[self.rng.uniform(0, math.tau)] + [self.rng.uniform(-TURN, TURN) for _ in range(STEPS - 1)]
                    for _ in range(pop)]
        self.gen = 0

    def step(self):
        """Fly the current generation, report on it, then breed the next one."""
        results = [fly(self.world, g) for g in self.pop]
        for r in results:
            r["fitness"] = fitness(r)
        order = sorted(range(len(results)), key=lambda i: -results[i]["fitness"])
        report = {
            "gen": self.gen,
            "best": order[0],
            "paths": [r["path"] for r in results],
            "status": [r["status"] for r in results],
            "goal_pct": round(100 * sum(r["status"] == "goal" for r in results) / len(results)),
            "closest": results[order[0]]["closest"],
        }
        self.pop = self._breed(results, order)
        self.gen += 1
        return report

    def _pick(self, results, tries=4):
        return max((self.rng.randrange(len(results)) for _ in range(tries)), key=lambda i: results[i]["fitness"])

    def _breed(self, results, order, elites=2):
        nxt = [list(self.pop[i]) for i in order[:elites]]
        while len(nxt) < len(self.pop):
            a, b = self._pick(results), self._pick(results)
            cut = self.rng.randrange(1, STEPS)
            child = self.pop[a][:cut] + self.pop[b][cut:]
            # Genes after the crash point never ran, so mutate hardest around where the parent failed.
            fail = results[a]["steps"] if results[a]["status"] == "crash" else STEPS
            for i in range(STEPS):
                near_failure = fail - NEAR_WINDOW <= i <= fail
                p = P_NEAR if near_failure else P_BASE
                if self.rng.random() < p:
                    child[i] = self.rng.uniform(0, math.tau) if i == 0 else self.rng.uniform(-TURN, TURN)
            nxt.append(child)
        return nxt
