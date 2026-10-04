def subsets(nums):
    result = []

    def backtrack(index, current):
        if index == len(nums):
            result.append(current.copy())
            return

        #Don't take nums[index]
        backtrack(index + 1, current)

        #Take nums[index]
        current.append(nums[index])
        backtrack(index + 1, current)

        #Undo the choice
        current.pop()

    backtrack(0, [])
    return result

nums = list(map(int, input("Enter numbers: ").split()))

for subset in subsets(nums):
    print(subset)
