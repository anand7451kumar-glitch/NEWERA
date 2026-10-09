#find bridges in an undirected graph
#A bridge is an edge whose removal increases the number of connected components./ Removing that edge disconnects part of the graph
#GRAPH =
# 0 ─── 1 ─── 3
# │     │
# 2 ────┘
#       │
#       4
#Imagine removing an edge that connects a whole section of the graph to the rest.
# If there is no alternative route, that edge is a bridge.
# Example: if node 4 is connected to the rest of the graph only through node 1, then the edge (1, 4) is a bridge.
#Key idea: If an edge has no alternative path connecting its endpoints after removal , its a bridge
#Use DFS and the discovery time/ low-link technique you learned in Tarjans algorithm

def find_bridges(n, edges):
    graph = [[] for _ in range(n)]

    #Build an undirected graph
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n
    low = [0] * n
    bridges = []
    timer = 0

    def dfs(node, parent):
        nonlocal timer

        disc[node] = low[node] = timer
        timer += 1

        for neighbor in graph[node]:
            if neighbor == parent:
                continue

            if disc[neighbor] == -1:
                dfs(neighbor, node)

                low[node] = min(low[node], low[neighbor])

                #No back route from neighbor's subtree
                #reaches node or an ancestor of node

                if low[neighbor] > disc[node]:
                    bridges.append((node, neighbor))


            else:
                low[node] = min(low[node], disc[neighbor])

    #Handle disconnected graphs too

    for node in range(n):
        if disc[node] == -1:
            dfs(node, -1)

    return bridges

edges = [
    (0, 1),
    (1, 2),
    (2, 0),
    (1, 3),
    (3, 4)
]

bridges = find_bridges(5, edges)

print("Bridges:", bridges)

    


        