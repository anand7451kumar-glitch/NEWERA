from math import inf

def bellman_ford(n, edges, start):
    dist = [inf], * n
    dist[start] = 0
    
    #Relax all edges uupto n - 1 times
    for _ in range(n - 1):
        updated = False

        for u, v, weight in edges:
            if dist[u] != inf and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                updated = True

        #Stop early if no distance changed
        if not updated:
            break

    #Check for a reachable negative weight cycle
    for u, v, weight in edges:
        if dist[u] != inf and dist[u] + weight < dist[v]:
            return None

    return dist

#Each edge is (source, destination, weight)
edges = [
    (0, 1, 4),
    (0, 2, 5),
    (1, 2, -2),
    (1, 3, 6),
    (2, 3, 3)
]

distances = bellman_ford(4, edges, 0)

if distances is None:
    print("Negative-weight cycle detected!")
else:
    print("Shortest distances:", distances)


       

               


    

