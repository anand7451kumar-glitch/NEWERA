def majority_element(numbers):
    candidate = None
    count = 0

    for num in numbers:
        if count == 0:
            candidate = num

        if num == candidate:
            count += 1
        else:
            count -= 1

    return candidate

numbers = list(map(int, input("Enter numbers: ").split()))
print("Majority element:", majority_element(numbers))
