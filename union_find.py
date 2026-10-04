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
            root_a, root_b, root_a

        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]

        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

uf = UnionFind(6)

uf.union(0, 1)
uf.union(1, 2)
uf.union(3, 4)

print(uf.connected(0, 2))
print(uf.connected(0, 4))
print(uf.connected(3, 4))
