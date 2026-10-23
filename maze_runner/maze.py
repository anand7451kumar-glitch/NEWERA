
"""Maze generation (randomised depth-first search) and solving (BFS). No web code here."""
import random
from collections import deque


def generate(w, h, seed=None):
    """Return a (2h+1) x (2w+1) grid where 1 = wall and 0 = open. Same seed -> same maze."""
    rng = random.Random(seed)
    grid = [[1] * (2 * w + 1) for _ in range(2 * h + 1)]
    grid[1][1] = 0
    seen = {(0, 0)}
    stack = [(0, 0)]  # cell coordinates as (col, row)
    while stack:
        cx, cy = stack[-1]
        options = [
            (cx + dx, cy + dy)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if 0 <= cx + dx < w and 0 <= cy + dy < h and (cx + dx, cy + dy) not in seen
        ]
        if not options:
            stack.pop()
            continue
        nx, ny = rng.choice(options)
        grid[2 * ny + 1][2 * nx + 1] = 0      # open the new cell
        grid[cy + ny + 1][cx + nx + 1] = 0    # knock down the wall between
        seen.add((nx, ny))
        stack.append((nx, ny))
    return grid


def solve(grid, start, end):
    """Shortest path from start to end as a list of (row, col), or None. Uses BFS."""
    start, end = tuple(start), tuple(end)
    came_from = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == end:
            path = []
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            return path[::-1]
        r, c = cur
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0 and (nr, nc) not in came_from:
                came_from[(nr, nc)] = cur
                queue.append((nr, nc))
    return None
