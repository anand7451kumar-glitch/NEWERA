def set_zeroes(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    zero_rows = set()
    zero_cols = set()

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0:
                zero_rows.add(i)
                zero_cols.add(j)

    for i in range(rows):
        for j in range(cols):
            if i in zero_rows or j in zero_cols:
                matrix[i][j] = 0

    return matrix

rows = int(input("Enter rows: "))
cools = int(input("Enter columns: "))

matrix = []

for i in range(rows):
    matrix.append(list(map(int, input(f"Enter row {i + 1}: ").split())))

print("Result:")
for row in set_zeroes(matrix):
    print(row)
