def kosaraju(graph):
    n = len(graph)
    visited = [False] * n
    stack = []

    #First DFS: record nodes by finishing time
    def dfs1(node):
        visited[node] = True

        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs1(neighbor)

        stack.append(node)

    for node in range(n):
        if not visited[node]:
            dfs1(node)

    #Reverse every edge
    reversed_graph = [[] for _ in range(n)]

    for node in range(n):
        for neighbor in graph[node]:
            reversed_graph[neighbor].append(node)

    #Second DFS: find strongly connected components
    visited = [False] * n
    components = []

    def dfs2(node, component):
        visited[node] = True
        component.append(node)

        for neighbour in reversed_graph[node]:
            if not visited[neighbor]:
                dfs2(neighbor, component)


    while stack:
        node = stack.pop()

        if not visited[node]:
            component = []
            dfs2(node, component)
            components.append(component)

    return components

graph = [
    [1], #0➡️1
    [2], #1➡️2
    [0], #2➡️0
    [4], #3➡️4
    [3], #4➡️3
    []  #5 has no outgoing edges
]

components = kosaraju(graph)

print("Strongly connected components:")

for component in components:
    print(component)


    
    
    
    
    


        

