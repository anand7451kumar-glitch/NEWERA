from collections import deque

class Node:
    def __init__(self, data):
        self.value = data
        self.left = None
        self.right = None

def level_order(root):
    if root is None:
        return

    queue = deque([root])

    while queue:
        node = queue.popleft()
        print(node.value, end=" ")
        
        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

root = Node(50)

root.left = Node(30)
root.right = Node(70)

root.left.left = Node(20)
root.left.right = Node(40)

root.right.left = Node(60)
root.right.right = Node(80)

print("Level order:")
level_order(root)
print()