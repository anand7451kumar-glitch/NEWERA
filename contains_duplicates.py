def contains_duplicates(numbers):
    seen = set()

    for num in numbers:
        if num in seen:
            return True
        seen.add(num)

    return False

numbers = list(map(int, input("Enter numbers: ").split()))

if contains_duplicates(numbers):
    print("Duplicate found")

else:
    print("No duplicates")
