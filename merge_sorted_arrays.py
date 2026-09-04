def merge_sorted_arrays(a, b):
    i =0
    j = 0
    result = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    while i < len(a):
        result.append(a[i])
        i += 1

    while j < len(b):
        result.append(b[j])
        j += 1

    return result

a = list(map(int, input("Enter first sorted array: ").split()))
b = list(map(int, input("Enter second sorted array: ").split()))

print("Merged array:", merge_sorted_arrays(a,b))
