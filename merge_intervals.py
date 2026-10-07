def merge(intervals):
    intervals.sort()

    result = [intervals[0]]

    for start, end in intervals[1:]:
        last_end = result[-1][1]

        if start <= last_end:
            result[-1][1] = max(last_end, end)
        else:
            result.append([start, end])

    return result

intervals = [[1, 3], [2, 6], [8, 10], [9, 12]]

print("Merged intervals:", merge(intervals))