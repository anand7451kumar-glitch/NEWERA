def topological_sort(graph):
    n = len(graph)
    visited = [False] * n
    stack = []

    def dfs(node):
        visited[node] = True

        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

        #Add node only after exploring its neighbors
        stack.append(n)

    for node in range(n):
        if not visited[node]:
            dfs(node)

    #Reverse finishing order
    return stack[::-1]

graph = [
    [1, 2],  #0 to 1, 0 to 2
    [3],     #1 to 3
    [3],     #2 to 3
    []       #3 has no outgoing edges
]

order = topological_sort(graph)
print("Topological order:", order)
    
                     

                     