def rotate_matrix(matrix):
    n = len(matrix)

    #transport matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    #reverse every row
    for row in matrix:
        row.reverse()

    return matrix

n = int(input("Enter matrix size: "))

matrix = []

for i in range(n):
    matrix.append(list(map(int, input(f"Enter row {i + 1}: ").split())))

print("Rotated matric:")
for row in rotate_matrix(matrix):
    print(row)
