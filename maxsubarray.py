def max_subarray(numbers):
    current = numbers[0]
    best = numbers[0]

    for num in numbers[1:]:
        current = max(num, current + num)
        best = max(best, current)

    return best


numbers = list(map(int, input("Enter numbers: ").split()))

print("Maximum subarray sum:", max_subarray(numbers))
