def intersection(a, b):
    set_b = set(b)
    result = []

    for num in a:
        if num in set_b and num not in result:
            result.append(num)

    return result

a = list(map(int, input("Enter first array: ").split()))
b = list(map(int, input("Enter second array: ").split()))

print("Intersection:", intersection(a, b))
