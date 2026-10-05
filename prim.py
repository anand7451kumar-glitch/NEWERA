import heapq

def prim(graph, start):
    visited = set()
    heap = [(0, start)]
    total_cost = 0

    while heap:
        weight, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)
        total_cost += weight

        for neighbour, edge_weight in graph[node]:
            if neighbour not in visited:
                heapq.heappush(heap, (edge_weight, neighbour))

    return total_cost

graph = {
    0: [(1, 1), (2, 4)],
    1: [(0, 1), (2, 2), (3, 5)],
    2: [(0, 4), (1, 2), (3,3)],
    3: [(1, 5), (2, 3)]

}

print("Minnimum cost:", prim(graph, 0))