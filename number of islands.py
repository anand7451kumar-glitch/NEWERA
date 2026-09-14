def num_islands(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return

        if grid[r][c] != "1":
            return

        grid[r][c] = "0"

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "1":
                count += 1
                dfs(i, j)

    return count

rows = int(input("Enter rows: "))
cols = int(input("Enter columns: "))

grid = []

for i in range(rows):
    grid.append(input(f"Enter row {i + 1} (use 0 and 1): ").split())

print("Number of islands:", num_islands(grid))
