def combination_sum(candidates, target):
    candidates.sort()
    result = []

    def backtrack(start, current, total):
        if total == target:
            result.append(current.copy())
            return

        if total > target:
            return

        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            current.append(candidates[i])
            backtrack(i + 1, current, total + candidates[i])
            current.pop()

    backtrack(0, [], 0)
    return result

nums = list(map(int, input("Enter numbers: ").split()))
target = int(input("Enter target: "))

print("Combinations:", combination_sum(nums, target))
