def flood_fill(image, sr, sc, color):
    original = image[sr][sc]

    if original == color:
        return image 

    rows = len(image)
    cols = len(image[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return

        if image[r][c] != original:
            return

        image[r][c] = color

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image

rows = int(input("Enter rows: "))
cols = int(input("Enter columns:"))

image = []

for i in range(rows):
    image.append(list(map(int, input(f"Enter row {i + 1}: ").split())))

sr = int(input("Enter starting row: "))
sc = int(input("Enter starting column:"))
color = int(input("Enter new color: "))

result = flood_fill(image, sr, sc, color)

print("Updated image:")
for row in result:
    print(row)
