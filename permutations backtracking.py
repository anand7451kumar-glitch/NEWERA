def permutations(nums):
    result = []

    def backtrack(start):
        if start == len(nums):
            result.append(nums.copy())
            return
        
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]

            backtrack(start + 1)

            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result

nums = list(map(int, input("Enter numbers: ").split()))

print("Permutations:")
for permutation in permutations(nums):
    print(permutation)
