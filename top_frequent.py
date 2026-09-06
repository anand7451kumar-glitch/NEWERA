from collections import Counter 
import heapq

def top_k_frequent(numbers, k):
    frequency = Counter(numbers)

    return heapq.nlargest(
        k,
        frequency.keys(),
        key=frequency.get
    )


numbers = list(map(int, input("Enter numbers: ").split()))
k = int(input("Enter k: "))

result = top_k_frequent(numbers, k)

print("Top", k, "frequent elements:", result)
