
from collections import deque

def oranges_rotting(grid):
    rows = len(grid)
    cols = len(grid[0])

    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue and fresh > 0:
        for _ in range(len(queue)):
            r, c = queue.popleft()

            for dr, dc in directions:
                nr = r + dr
                nc = c + dc

                if 0 <= nr < rows and 0 <= nc <cols:
                    if grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))

        minutes += 1

    if fresh == 0:
        return minutes

    return -1

rows = int(input("Enter rows: "))
cols = int(input("Enter columns: "))

grid = []

for i in range(rows):
    grid.append(list(map(int, input(f"Enter row {i + 1}: ").split())))

print("Minutes:", oranges_rotting(grid))


