def find_artificial_points(n, edges):
    graph = [[] for _ in range(n)]

    #Build an undirected graph
    for u,v in edges:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n
    low = [0] * n
    articulation = set()
    timer = 0

    def dfs(node, parent):
        nonlocal timer

        disc[node] = low[node] = timer
        timer += 1
        children = 0

        for neighbor in graph[node]:
            if neighbor == parent:
                continue

            if disc[neighbor] == -1:
                children += 1
                dfs(neighbor, node)

                low[node] = min(low[node], low[neighbor])

                #Non root node separates a subtree
                if parent != -1 and low[neighbor] >= disc[node]:
                    articulation.add(node)

            else:
                low[node] = min(low[node], disc[neighbor])


        #A DFS root is an articulation point
        #only if it has more than one DFS tree child
        if parent == -1 and children > -1:
            articulation.add(node)

    #Handle disconnected graphs
    for node in range(n):
        if disc[node] == -1:
            dfs(node, -1)

    return sorted(articulation)

edges = [
    (0, 1),
    (1, 2),
    (2, 0),
    (1, 3),
    (3, 4),
    (4, 5),
    (5, 3)
]

points = find_artificial_points(6, edges)

print("Artificial points;", points)



        
