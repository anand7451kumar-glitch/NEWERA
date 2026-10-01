import heapq

graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("A", 4), ("C", 5), ("D", 10)],
    "C": [("A", 2), ("B", 5), ("D", 3)],
    "D": [("B", 10), ("C", 3)]          
}

distances = {node: float("inf") for node in graph}
distances["A"] = 0

heap = [(0, "A")]

while heap:
    distance, node = heapq.heappop(heap)

    if distance > distances[node]:
        continue

    for neighbour, weight in graph[node]:
        new_distance = distance + weight

        if new_distance < distances[neighbour]:
            distances[neighbour] = new_distance
            heapq.heappush(heap, (new_distance, neighbour))

print("Shortest distances from node A:")

for node, distance in distances.items():
    print(node, "=", distance)

                        