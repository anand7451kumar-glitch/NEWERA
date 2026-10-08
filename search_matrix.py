#binary search to a matrix.
# matrix = [[1, 3, 5, 7],[10, 11, 16, 20],[23, 30, 34, 60]
# target = 3
# find whether 3 exist
    
def search_matrix(matrix, target):
    rows = len(matrix)
    cols = len(matrix[0])

    left = 0
    right = rows * cols - 1

    while left <= right:
        mid = (left + right) // 2

        row = mid // cols
        col = mid % cols

        value = matrix[row][col]

        if value == target:
            return True

        elif value < target:
            left = mid + 1

        else:
            right = mid - 1

    return False

matrix = [
    [1, 3, 5, 7],
    [10, 11, 16, 20],
    [23, 30, 34, 60]
]

target = 3

print("Target found:", search_matrix(matrix, target))


