def climbing_stairs(n):
    if n <= 2:
        return n

    first = 1
    second = 2

    for _ in range(3, n + 1):
        first, second = second, first + second

    return second

n = int(input("Enter number of stairs: "))

print("Number of ways:", climbing_stairs(n))
