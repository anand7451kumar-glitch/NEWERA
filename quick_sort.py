def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]

    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)

numbers = [8, 3, 1, 7, 0, 10, 2]

print("Before:", numbers)
print("After: ", quick_sort(numbers))