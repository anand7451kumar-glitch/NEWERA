import math
import unittest

from evolve import STEPS, TARGET, UNREACHABLE, START, Evolver, World, fitness, fly

WALL = [(300, 120, 16, 360)]  # a wall with a gap at the top


class WorldTests(unittest.TestCase):
    def test_distance_shrinks_towards_target(self):
        w = World([])
        self.assertGreater(w.distance(*START), w.distance(300, 200))
        self.assertEqual(w.distance(*TARGET), 0)

    def test_route_must_go_round_walls(self):
        straight = World([]).distance(*START)
        # The only gap is below the start line, so the route has to dip down and come back up.
        around = World([(300, 0, 16, 460)]).distance(*START)
        self.assertGreater(around, straight)

    def test_sealed_off_start_is_unreachable(self):
        sealed = World([(300, 0, 16, 480)])
        self.assertEqual(sealed.distance(*START), UNREACHABLE)


class FlightTests(unittest.TestCase):
    def test_flying_straight_at_the_target_reaches_it(self):
        heading = math.atan2(TARGET[1] - START[1], TARGET[0] - START[0])
        result = fly(World([]), [heading] + [0.0] * (STEPS - 1))
        self.assertEqual(result["status"], "goal")

    def test_leaving_the_screen_is_a_crash(self):
        result = fly(World([]), [math.pi] + [0.0] * (STEPS - 1))
        self.assertEqual(result["status"], "crash")

    def test_hitting_a_wall_is_a_crash(self):
        wall = World([(100, 380, 16, 100)])
        result = fly(wall, [-0.0] + [0.0] * (STEPS - 1))  # heading right along the bottom
        self.assertEqual(result["status"], "crash")

    def test_reaching_the_goal_always_beats_getting_close(self):
        goal = {"status": "goal", "steps": STEPS, "closest": 0}
        close = {"status": "crash", "steps": 10, "closest": 0}
        self.assertGreater(fitness(goal), fitness(close))


class EvolutionTests(unittest.TestCase):
    def test_population_learns_to_get_round_a_wall(self):
        e = Evolver(WALL, seed=1)
        first = e.step()
        for _ in range(59):
            last = e.step()
        self.assertLess(first["goal_pct"], 20)
        self.assertGreaterEqual(last["goal_pct"], 50)

    def test_same_seed_same_evolution(self):
        a, b = Evolver(WALL, seed=7), Evolver(WALL, seed=7)
        self.assertEqual(a.step()["paths"], b.step()["paths"])


try:
    from app import app, clean_walls
except ImportError:  # Flask not installed in this environment
    app = None


@unittest.skipIf(app is None, "Flask not installed")
class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_new_run_then_step(self):
        run = self.client.post("/api/new", json={"walls": [[300, 120, 16, 360]]}).get_json()["run"]
        rep = self.client.post("/api/step", json={"run": run}).get_json()
        self.assertEqual(len(rep["paths"]), 50)
        self.assertEqual(rep["gen"], 0)

    def test_bad_input_is_rejected(self):
        self.assertEqual(self.client.post("/api/new", json={"walls": "nope"}).status_code, 400)
        self.assertEqual(self.client.post("/api/new", json={"walls": [[1, 2, 3]]}).status_code, 400)
        self.assertEqual(self.client.post("/api/step", json={"run": "missing"}).status_code, 404)

    def test_walls_are_clamped_and_made_thick_enough(self):
        self.assertEqual(clean_walls([[-50, 10, 2, 2]]), [(0, 10, 14, 14)])


if __name__ == "__main__":
    unittest.main()
