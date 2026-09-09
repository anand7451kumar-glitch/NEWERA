def spiral_order(matrix):
    result = []

    while matrix:
        result += matrix.pop(0)

        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())

        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
        if matrix:
            result += matrix.pop()[::-1]

        if matrix and matrix[0]:
            for row in matrix[::-1]:
                result.append(row.pop(0))

    return result 

rows = int(input("Enter rows: "))

cols = int(input("Enter columns: "))

matrix = []

for _ in range(rows):
    row = list(map(int, input("Enter row: ").split()))
    matrix.append(row)


print("Spiral order:", spiral_order(matrix))
