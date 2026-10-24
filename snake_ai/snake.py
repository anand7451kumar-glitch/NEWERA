"""Snake autopilot. Pure Python, no web code.

Strategy (safe, not just greedy):
1. Find the shortest path to the food (BFS). Imagine the snake following it and eating.
   Only take it if the snake could still reach its own tail afterwards (so it can't trap itself).
2. Otherwise take the safe move with the longest route back to the tail (stalling safely).
3. Otherwise step into the neighbour with the most open space around it.
"""
from collections import deque

DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


def neighbours(p, w, h):
    x, y = p
    for dx, dy in DIRS.values():
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            yield (nx, ny)


def bfs(start, goal, blocked, w, h):
    """Shortest path from start to goal as a list of cells, or None."""
    prev = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            return path[::-1]
        for n in neighbours(cur, w, h):
            if n not in prev and n not in blocked:
                prev[n] = cur
                queue.append(n)
    return None


def open_area(start, blocked, w, h):
    seen = {start}
    queue = deque([start])
    while queue:
        for n in neighbours(queue.popleft(), w, h):
            if n not in seen and n not in blocked:
                seen.add(n)
                queue.append(n)
    return len(seen)


def direction(a, b):
    d = (b[0] - a[0], b[1] - a[1])
    return next(name for name, v in DIRS.items() if v == d)


def next_move(snake, food, w, h):
    """snake: list of (x, y), head first. Returns 'up'/'down'/'left'/'right', or None if trapped."""
    snake = [tuple(p) for p in snake]
    food = tuple(food)
    head, tail = snake[0], snake[-1]
    body = set(snake[:-1])  # the tail cell is free by the time we get there

    path = bfs(head, food, body, w, h)
    if path and len(path) > 1:
        after = (list(reversed(path)) + snake[1:])[: len(snake) + 1]
        if bfs(after[0], after[-1], set(after[1:-1]), w, h) is not None:
            return direction(head, path[1])

    # Food isn't safely reachable: wander through the safe move that keeps the longest
    # route back to our own tail. Taking the long way round gives the board time to open up.
    best, best_len = None, -1
    for n in neighbours(head, w, h):
        if n in body:
            continue
        after = [n] + snake[:-1]
        back = bfs(n, after[-1], set(after[1:-1]), w, h)
        if back is not None and len(back) > best_len:
            best, best_len = n, len(back)
    if best:
        return direction(head, best)

    best, best_area = None, -1
    for n in neighbours(head, w, h):
        if n in body:
            continue
        area = open_area(n, body, w, h)
        if area > best_area:
            best, best_area = n, area
    return direction(head, best) if best else None
