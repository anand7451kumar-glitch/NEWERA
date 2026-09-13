def subsets(nums):
    result = []

    def backtrack(index, current):
        if index == len(nums):
            result.append(current.copy())
            return

        #dont include nums[index]
        backtrack(index + 1, current)

        #include nums[index]
        current.append(nums[index])
        backtrack(index + 1, current)
        current.pop()

    backtrack(0, [])
    return result


nums = list(map(int, input("Enter numbers: ").split()))

print("All subsets:")
for subset in subsets(nums):
    print(subset)
