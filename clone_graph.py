from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = []

def clone_graph(node):
    if not node:
        return None

    cloned = {node: Node(node.value)}
    queue = deque([node])

    while queue:
        current = queue.popleft()

        for neighbor in current.neighbors:
            if neighbor not in cloned:
                cloned[neighbor] = Node(neighbor.value)
                queue.append(neighbor)

            cloned[current].neighbors.append(cloned[neighbor])

    return cloned[node]

#Create graph:
#1 -- 2
#|    |
#4 -- 3

node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)

node1.neighbors = [node2, node4]
node2.neighbors = [node1, node3]
node3.neighbors = [node2, node4]
node4.neighbors = [node1, node3]

copy = clone_graph(node1)

print("Original starting node:", node1.value)
print("Cloned starting node:", copy.value)
print("Cloned neighbors:", [n.value for n in copy.neighbors])

