#Place N queens on an N × N chessboard so that no two queens attack each other.

def solve_n_queens(n):
    board = [["."] * n for _ in range(n)]
    solutions = []

    columns = set()
    diagonals1 = set()
    diagonals2 = set()

    def backtrack(row):
        if row == n:
            solutions.append(["".join(r) for r in board])
            return

        for col in range(n):

            if col in columns:
                continue

            if row - col in diagonals1:
                continue

            if row + col in diagonals2:
                continue

            board[row][col] = "Q"
            columns.add(col)
            diagonals1.add(row - col)
            diagonals2.add(row + col)

            backtrack(row + 1)

            board[row][col] = "."
            columns.remove(col)
            diagonals1.remove(row - col)
            diagonals2.remove(row + col)

    backtrack(0)

    return solutions

n = int(input("Enter N: "))

solutions = solve_n_queens(n)

print("Number of solutions:", len(solutions))

for solution in solutions:
    print()

    for row in solution:
        print(row)


