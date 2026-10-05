class SegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.build(nums, 1, 0, self.n - 1)

    def build(self, nums, node, left, right):
        if left == right:
            self.tree[node] = nums[left]
            return

        mid = (left + right) // 2

        self.build(nums, node * 2, left, mid)
        self.build(nums, node * 2 + 1, mid + 1, right)

        self.tree[node] = (
            self.tree[node * 2] +
            self.tree[node * 2 + 1]
        )

    def query(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return 0

        if ql <= left and right <= qr:
            return self.tree[node]

        mid = (left + right) // 2

        return (
            self.query(node * 2, left, mid, ql, qr)
            +
            self.query(node * 2 + 1, mid + 1, right, ql, qr)
        )

    def update(self, node, left, right, index, value):
        if left == right:
            self.tree[node] = value
            return

        mid = (left + right) // 2

        if index <= mid:
            self.update(node * 2, left, mid, index,value)
        else:
            self.update(node * 2 + 1, mid + 1, right, index, value)
            
        self.tree[node] = (
            self.tree[node * 2] +
            self.tree[node * 2 + 1]
        )

nums = [2, 4, 5, 7, 8, 9]

st = SegmentTree(nums)

print("Sum from index 1 to 4:",
      st.query(1, 0, len(nums) - 1, 1, 4))

st.update(1, 0, len(nums) -1, 2, 10)

print("After updating index 2 to 10:")
print("Sum from index 1 to 4:",
      st.query(1, 0, len(nums) -1, 1, 4))

    