"""Deep Dungeon game logic: level generation, fog of war, monster AI. No web code."""
import random
from collections import deque

W, H = 48, 30
SIGHT = 8
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
MONSTERS = [("r", "rat", 1.0), ("g", "goblin", 1.4), ("o", "ogre", 2.0)]  # glyph, name, strength


def centre(room):
    return room[0] + room[2] // 2, room[1] + room[3] // 2


def make_level(rng):
    """Random non-overlapping rooms joined by L-shaped corridors. Returns (grid, rooms)."""
    while True:
        grid = [["#"] * W for _ in range(H)]
        rooms = []
        for _ in range(80):
            w, h = rng.randint(4, 9), rng.randint(3, 6)
            x, y = rng.randint(1, W - w - 2), rng.randint(1, H - h - 2)
            if any(x < rx + rw + 1 and x + w + 1 > rx and y < ry + rh + 1 and y + h + 1 > ry for rx, ry, rw, rh in rooms):
                continue
            rooms.append((x, y, w, h))
            for yy in range(y, y + h):
                for xx in range(x, x + w):
                    grid[yy][xx] = "."
            if len(rooms) == 9:
                break
        if len(rooms) >= 3:
            break
    for a, b in zip(rooms, rooms[1:]):
        (x1, y1), (x2, y2) = centre(a), centre(b)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid[y1][x] = "."
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[y][x2] = "."
    return grid, rooms


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.depth, self.kills, self.over = 0, 0, False
        self.hp = self.max_hp = 24
        self.atk = 3
        self.log = []
        self._descend()
        self.log = ["You enter the dungeon. Find the stairs (>) and go deeper."]

    def _say(self, text):
        self.log.append(text)

    def _free_cell(self, room):
        for _ in range(30):
            x, y = self.rng.randint(room[0], room[0] + room[2] - 1), self.rng.randint(room[1], room[1] + room[3] - 1)
            if self.grid[y][x] == "." and (x, y) not in self.items and (x, y) != (self.x, self.y) \
                    and not any((m["x"], m["y"]) == (x, y) for m in self.monsters):
                return x, y
        return None

    def _descend(self):
        self.depth += 1
        self.grid, rooms = make_level(self.rng)
        self.x, self.y = centre(rooms[0])
        sx, sy = centre(rooms[-1])
        self.grid[sy][sx] = ">"
        self.monsters, self.items, self.seen = [], {}, set()
        kinds = MONSTERS[: min(3, 1 + self.depth // 2)]
        for room in rooms[1:]:
            for _ in range(self.rng.randint(0, 1 + self.depth // 3)):
                cell = self._free_cell(room)
                if cell:
                    glyph, name, power = self.rng.choice(kinds)
                    self.monsters.append({"x": cell[0], "y": cell[1], "g": glyph, "name": name,
                                          "hp": round((3 + self.depth * 2) * power),
                                          "atk": max(1, round((1 + self.depth * 0.7) * power))})
            roll = self.rng.random()
            cell = self._free_cell(room) if roll < 0.45 else None
            if cell:
                self.items[cell] = "!" if roll < 0.35 else "/"
        if self.depth > 1:
            self.hp = min(self.max_hp, self.hp + 4)
        self._look()

    # ----- vision -----
    def _clear(self, x0, y0, x1, y1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx, sy = (1 if x1 > x0 else -1), (1 if y1 > y0 else -1)
        err, x, y = dx - dy, x0, y0
        while (x, y) != (x1, y1):
            if (x, y) != (x0, y0) and self.grid[y][x] == "#":
                return False
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        return True

    def _look(self):
        self.visible = set()
        for y in range(max(0, self.y - SIGHT), min(H, self.y + SIGHT + 1)):
            for x in range(max(0, self.x - SIGHT), min(W, self.x + SIGHT + 1)):
                if (x - self.x) ** 2 + (y - self.y) ** 2 <= SIGHT ** 2 and self._clear(self.x, self.y, x, y):
                    self.visible.add((x, y))
        self.seen |= self.visible

    # ----- turns -----
    def move(self, dx, dy):
        """One player turn. (0, 0) waits. Walking into a wall costs no turn."""
        if self.over:
            return
        if (dx, dy) != (0, 0):
            nx, ny = self.x + dx, self.y + dy
            target = next((m for m in self.monsters if (m["x"], m["y"]) == (nx, ny)), None)
            if target:
                self._attack(target)
            elif self.grid[ny][nx] != "#":
                self.x, self.y = nx, ny
                item = self.items.pop((nx, ny), None)
                if item == "!":
                    gain = min(8, self.max_hp - self.hp)
                    self.hp += gain
                    self._say(f"You drink a potion (+{gain} HP).")
                elif item == "/":
                    self.atk += 1
                    self._say("You find a sharper sword (+1 attack).")
                if self.grid[ny][nx] == ">":
                    self._say(f"You descend to depth {self.depth + 1}.")
                    self._descend()
                    return
            else:
                return
        self._monsters_turn()
        self._look()

    def _attack(self, m):
        dmg = self.rng.randint(max(1, self.atk - 2), self.atk)
        m["hp"] -= dmg
        if m["hp"] <= 0:
            self.monsters.remove(m)
            self.kills += 1
            self._say(f"You slay the {m['name']}.")
        else:
            self._say(f"You hit the {m['name']} for {dmg}.")

    def _distances(self, limit=12):
        dist = {(self.x, self.y): 0}
        queue = deque([(self.x, self.y)])
        while queue:
            x, y = queue.popleft()
            if dist[(x, y)] >= limit:
                continue
            for dx, dy in DIRS:
                n = (x + dx, y + dy)
                if n not in dist and self.grid[n[1]][n[0]] != "#":
                    dist[n] = dist[(x, y)] + 1
                    queue.append(n)
        return dist

    def _monsters_turn(self):
        dist = self._distances()
        for m in self.monsters:
            d = dist.get((m["x"], m["y"]))
            if d is None or d > SIGHT:
                continue
            if d == 1:
                if self.rng.random() < 0.75:
                    dmg = self.rng.randint(1, m["atk"])
                    self.hp -= dmg
                    self._say(f"The {m['name']} hits you for {dmg}.")
                    if self.hp <= 0:
                        self.hp, self.over = 0, True
                        self._say(f"You died on depth {self.depth} with {self.kills} kills.")
                        return
                else:
                    self._say(f"The {m['name']} misses.")
                continue
            taken = {(o["x"], o["y"]) for o in self.monsters} | {(self.x, self.y)}
            for dx, dy in DIRS:
                n = (m["x"] + dx, m["y"] + dy)
                if dist.get(n) == d - 1 and n not in taken:
                    m["x"], m["y"] = n
                    break

    def state(self):
        rows = ["".join(self.grid[y][x] if (x, y) in self.seen else " " for x in range(W)) for y in range(H)]
        mask = ["".join("1" if (x, y) in self.visible else "0" for x in range(W)) for y in range(H)]
        return {
            "w": W, "h": H, "tiles": rows, "visible": mask, "player": [self.x, self.y],
            "monsters": [{"x": m["x"], "y": m["y"], "g": m["g"]} for m in self.monsters if (m["x"], m["y"]) in self.visible],
            "items": [{"x": x, "y": y, "g": g} for (x, y), g in self.items.items() if (x, y) in self.seen],
            "hp": self.hp, "max_hp": self.max_hp, "atk": self.atk, "depth": self.depth, "kills": self.kills,
            "score": self.depth * 100 + self.kills * 10, "over": self.over, "log": self.log[-6:],
        }
