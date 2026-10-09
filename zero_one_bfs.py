#Imagine a graph where moving between some locations costs 0, while other moves cost 1.
# graph = [
#     [(1, 0), (2, 1)],
#     [(3, 1)],
#     [(3, 0)],
#     []
# # ]Each entry (neighbor, weight) means:

# (1, 0): travel to node 1 with cost 0.
# (2, 1): travel to node 2 with cost 1.
# Find the minimum cost to travel from node 0 to node 3.The answer is 0, because we can travel:

# 0 → 1 → 3

# Cost = 0 + 1 = 1
# Actually, the other route is:

# 0 → 2 → 3

# Cost = 1 + 0 = 1
# Both cost 1, so the correct minimum is 1

from collections import deque

def zero_one_bfs(graph, start):
    n = len(graph)
    dist = [float("inf")] * n
    dist[start] = 0

    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbour, weight in graph[node]:
            new_dist = dist[node] + weight

            if new_dist < dist[neighbour]:
                dist[neighbour] = new_dist

                if weight == 0:
                    queue.append(neighbour)
                else:
                    queue.append(neighbour)

    return dist

graph = [
    [(1, 0), (2, 1)],
    [(3, 1)],
    [(3, 0)],
    []
]

distances = zero_one_bfs(graph, 0)

print("Shortest distances:", distances)
print("Minimum cost to node 3:", distances[3])