#Given
# nums = [3, 2, 1, 5, 6, 4]
#k = 2
#Find 2nd largest number 
# Sorted descending order 6, 5, 4, 3, 2, 1 
# answer = 5


import heapq

def kth_largest(nums, k):
    heap = []

    for num in nums:
        heapq.heappush(heap, num)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]

nums = [3, 2, 1, 5, 6, 4]
k = 2

print("Kth largest:", kth_largest(nums, k))