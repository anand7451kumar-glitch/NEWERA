import heapq

graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("A", 4), ("C", 2), ("D", 5)],
    "C": [("A", 1), ("B", 2), ("D", 8)],
    "D": [("B", 5), ("C", 8)]
}

def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    heap = [(0, start)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if current_distance > distances[current_node]:
            continue

        for neighbour, weight in graph[current_node]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                heapq.heappush(heap, (new_distance, neighbour))

    return distances

result = dijkstra(graph, "A")

for node, distance in result.items():
    print(node, ":", distance)