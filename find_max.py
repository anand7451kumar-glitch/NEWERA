def find_maximum(numbers):
    if not numbers:
        return None

    maximum = numbers[0]

    for num in numbers[1:]:
        if num > maximum:
            maximum = num
    return maximum

numbers = list(map(int, input("Enter numbers: ").split()))

result = find_maximum(numbers)

if result is None:
    print("No numbers entered")

else:
    print("Maximum:", result)
