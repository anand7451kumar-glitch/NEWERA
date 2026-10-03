class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def inorder(root):
    if root is None:
        return

    inorder(root.left)
    print(root.value, end=" ")
    inorder(root.right)

root = Node(10)

root.left = Node(20)
root.right = Node(30)

root.left.left = Node(40)
root.left.right = Node(50)

root.right.left = Node(12)
root.right.right = Node(90)

print("Inorder traversal:")
inorder(root)
print() 
