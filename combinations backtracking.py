def combinations_sum(candidates, target):
    result = []

    def backtrack(start, current, total):
        if total == target:
            result.append(current.copy())
            return

        if total > target:
            return

        for i in range(start, len(candidates)):
            current.append(candidates[i])
            backtrack(i, current, total + candidates[i])
            current.pop()

    backtrack(0, [], 0)
    return result

candidates = list(map(int, input("Enter numbers: ").split()))
target = int(input("Enter target: "))

print("Combinations:", combinations_sum(candidates, target))
