from collections import deque

maze = [
    "S....",
    ".###.",
    "...#.",
    ".#...",
    "...#E"
]

start = (0, 0)
end = (4, 4)

queue = deque([(start, [start])])
visited = {start}

while queue:
    (r, c), path = queue.popleft()

    if (r, c) == end:
        print("Path found!")
        print("Steps:", len(path) - 1)

        for row, col in path:
            print(f"({row}, {col})", end=" ")
        print()
        break
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r + dr, c + dc

        if 0 <= nr < len(maze) and 0 <= nc < len(maze[nr]):
            if maze[nr][nc] != "#" and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))