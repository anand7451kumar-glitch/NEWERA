class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]

        return True

def kruskal(n, edges):
    edges.sort(key=lambda edge: edge[2])

    uf = UnionFind(n)

    total_cost = 0
    chosen_edges = []

    for a, b, weight in edges:
        if uf.union(a, b):
            chosen_edges.append((a, b, weight))
            total_cost += weight

            if len(chosen_edges) == n - 1:
                break

    return total_cost, chosen_edges

edges = [
    (0, 1, 1),
    (0, 2, 4),
    (1, 2, 2),
    (1, 3, 5),
    (2, 3, 3)
]

cost, chosen = kruskal(4, edges)

print("Chosen edges:")

for a, b, weight in chosen:
    print(a, "_", b, ":", weight)

print("Minimum cost:", cost)