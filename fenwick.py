class FenwickTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)

        for i, value in enumerate(nums):
            self.update(i, value)

    def update(self, index, value):
        index += 1

        while index <= self.n:
            self.tree[index] += value
            index += index & -index   #is the core Fenwick Tree trick.
#Unlike the Segment Tree, a Fenwick Tree uses the binary representation of the index to determine which cumulative ranges each position stores.

    def prefix_sum(self, index):
        total = 0
        index += 1

        while index > 0:
            total += self.tree[index]
            index -= index & -index

        return total

    def range_sum(self, left, right):
        if left == 0:
            return self.prefix_sum(right)

        return (
            self.prefix_sum(right)
            - self.prefix_sum(left - 1)
        )

nums = [2, 4, 5, 7, 8, 9]

ft = FenwickTree(nums)

print("Sum from 1 to 4:",
      ft.range_sum(1, 4))

ft.update(2, 5)

print("After adding 5 to index 2:")
print("Sum from 1 to 4:",
      ft.range_sum(1, 4))


    