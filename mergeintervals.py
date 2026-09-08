def merge_intervals(intervals):
    intervals.sort()
    result = []

    for start, end in intervals:
        if not result or start > result[-1][1]:
            result.append([start, end])
        else:
            result[-1][1] = max(result[-1][1], end)

    return result

n = int(input("Enter number of intervals: "))

intervals = []
for _ in range(n):
    start, end = map(int, input("Enter start and end: ").split())
    intervals.append([start, end])

print("Merged intervals:", merge_intervals(intervals))
