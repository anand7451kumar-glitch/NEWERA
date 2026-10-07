import heapq
from collections import Counter

def top_k_frequent(nums, k):
    frequency = Counter(nums)

    heap = []

    for num, count in frequency.items():
        heapq.heappush(heap, (count, num))

        if len(heap) > k:
            heapq.heappop(heap)

    return [num for count, num in heap]

nums = [1, 2, 1, 2, 2, 3]
k = 2

print("Top frequent elements:", top_k_frequent(nums, k))