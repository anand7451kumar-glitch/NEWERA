class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def print_list(head):
    current = head

    while current:
        print(current.value, end =" -> ")
        current = current.next

    print("None")

def reverse_list(head):
    previous = None
    current = head

    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node 

    return previous

head = Node(10)
head.next = Node(20)
head.next.next = Node(30)
head.next.next.next = Node(40)

print("Original:")
print_list(head)
head = reverse_list(head)
print("Reversed:")
print_list(head)    