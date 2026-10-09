def tarjan_scc(graph):
    n = len(graph)

    disc = [-1] * n
    low = [0] * n
    on_stack = [False] * n

    stack = []
    components = []
    timer = 0

    def dfs(node):
        nonlocal timer

        disc[node] = low[node] = timer
        timer += 1

        stack.append(node)
        on_stack[node] = True

        for neighbor in graph[node]:

            #Neighbor has not been visited
            if disc[neighbor] == -1:
                dfs(neighbor)
                low[node] = min(low[node], low[neighbor])

            #Neighbor is still in the current SCC stack
            elif on_stack[neighbor]:
                low[node] = min(low[node], disc[neighbor])

        # This node is the root of an SCC
        if low[node] == disc[node]:
            component = []

            while True:
                current = stack.pop()
                on_stack[current] = False
                component.append(current)

                if current == node:
                    break

            components.append(component)

    for node in range(n):
        if disc[node] == -1:
            dfs(node)

    return components

graph = [
    [1],
    [2],
    [0, 3],
    [4],
    [3],
    []
]

components = tarjan_scc(graph)

print("Strongly connected components:")

for component in components:
    print(component)


        
