import heapq

graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("A", 4), ("C", 2), ("D", 5)],
    "C": [("A", 1), ("B", 2), ("D", 8)],
    "D": [("B", 5), ("C", 8)]
}

def shortest_path(graph, start, target):
    distances = {node: float("inf") for node in graph}
    previous= {node: None for node in graph}

    distances[start] = 0
    heap = [(0, start)]

    while heap:
        distance, node = heapq.heappop(heap)

        if distance > distances[node]:
            continue

        if node == target:
            break

        for neighbour, weight in graph[node]:
            new_distance = distance + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = node

                heapq.heappush(
                    heap,
                    (new_distance, neighbour)

                )
    if distances[target] == float("inf"):
        return None

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[target]

start = input("Start: ")
target = input("Target: ")

result = shortest_path(graph, start, target)

if result is None:
    print("No path exists.")
else:
    path, distance = result

    print("Shortest path:", " -> ".join(path))
    print("Distance:", distance)


                                  