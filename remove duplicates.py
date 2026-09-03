def remove_duplicates(numbers):
    result = []

    for num in numbers:
        if num not in result:
            result.append(num)

    return result

numbers = list(map(int, input("Enter numbers: "). split()))

print("Without duplicates:", remove_duplicates(numbers))
