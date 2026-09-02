def second_largest(numbers):
    largest = float("-inf")
    second = float("-inf")

    for num in numbers:
        if num > largest:
            second = largest
            largest = num
        elif largest > num > second:
            second = num

    return second 


numbers = list(map(int, input("Enter numbers: ").split()))

result = second_largest(numbers)

if result == float("-inf"):
    print("No second largest value")
else:
    print("Second largest:", result)
