graph = {
    "A" : ["B"],
    "B": ["C"],
    "C": ["A"],
    "D": ["E"],
    "E": []
}

def has_cycle(node, visited, path):
    visited.add(node)
    path.add(node)

    for neighbour in graph[node]:
        if neighbour not in visited:
            if has_cycle(neighbour, visited, path):
                return True

        elif neighbour in path:
            return True

    path.remove(node)
    return False

visited = set()
path = set()

for node in graph:
    if node not in visited:
        if has_cycle(node, visited, path):
            print("Cycle detected!")
            break

else:
    print("No cycle.")








































































































             