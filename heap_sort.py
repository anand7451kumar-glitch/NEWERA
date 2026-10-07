import heapq

def heap_sort(nums):

    heap = nums[:]
    heapq.heapify(heap)

    result = []

    while heap:
        result.append(heapq.heappop(heap))

    return result

nums = [5, 1, 4, 2, 8 , 3]

print("Sorted:", heap_sort(nums))