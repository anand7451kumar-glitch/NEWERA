def rotate_array(numbers, k):
    if not numbers:
        return numbers

    k %= len(numbers)

    return numbers[-k:] + numbers[:-k]

numbers = list(map(int, input("Enter numbers: ").split()))
k = int(input("Rotate by: "))

print("Rotated array:", rotate_array(numbers, k))
