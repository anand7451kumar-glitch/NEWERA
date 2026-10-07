import heapq

def k_closest(points, k):
    heap = []

    for x, y in points:
        distance = x * x + y * y

        #Negative distance makes Pythons' min heap act like a max heap
        heapq.heappush(heap, (-distance, x, y))

        if len(heap) > k:
            heapq.heappop(heap)

    return [[x, y] for distance, x, y in heap]

points = [[1, 3], [-2, 2], [5, 8], [0,1]]
k =2

print("Closest points:", k_closest(points, k))
