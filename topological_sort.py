from collections import deque

graph = {
    "Python": ["DSA"],
    "DSA": ["Algorithms"],
    "Algorithms": ["ML"],
    "ML": [],
    "Math": ["ML"]

}

def topological_sort(graph):
    indegree = {node: 0 for node in graph}

    for node in graph:
        for neighbour in graph[node]:
            indegree[neighbour] += 1

    queue = deque()

    for node in indegree:
        if indegree[node] == 0:
            queue.append(node)

    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

    for neighbour in graph[node]:
        indegree[neighbour] -= 1

        if indegree[neighbour] == 0:
            queue.append(neighbour)

    if len(order) != len(graph):
        return None

    return order

result = topological_sort(graph)

if result:
    print("Order:")
    print(" -> ".join(result))

else:
    print("Cycle detected. No valid order.")



