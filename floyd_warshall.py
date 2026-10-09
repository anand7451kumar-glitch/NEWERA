from math import inf

def floyd_warshall(graph):
    n = len(graph)

    #Copy the graph so the original remains unchanged
    dist = [row[:] for row in graph]

    #Consider every node as an intermediate node
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != inf and dist[k][j] != inf:
                    dist[i][j] = min(
                        dist[i][j],
                        dist[i][k] + dist[k][j]
                        
                    )

    #A negative diagonal value indicates a negative cycle
    for i in range(n):
        if dist[i][i] < 0:
            return None

    return dist

graph = [
    [0, 4,   10,  inf],
    [inf, 0, inf, 2],
    [inf, inf, 0, 3],
    [inf, inf, inf, 0]

]

result = floyd_warshall(graph)

if result is None:
    print("Negative-weight cycle detected!")

else:
    print("All-pairs shortest distances:")

    for row in result:
        print(row)



#Why does the distance from node 0 to node 3 become 6?

#Because the algorithm discovers a shorter route through node 1:

#0 → 1 → 3

#Total cost: 4 + 2 = 6, which is less than the original route through node 2 (10 + 3 = 13).