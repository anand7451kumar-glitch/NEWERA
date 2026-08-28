def two_sum(numbers, target):
    seen = {}

    for i, num in enumerate(numbers):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []


numbers = list(map(int, input("Enter numbers: ").split()))
target = int(input("Enter target: "))

result = two_sum(numbers, target)

if result:
    print(f"Indices: {result}")
else:
    print("No pair found.")
