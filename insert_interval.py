# Given intervals = [[1, 3], [6, 9]]
#new_interval = [2, 5]
#Insert [2, 5] and merge overlaps
# Result: [[1, 5], [6, 9]]


def insert_interval(intervals, new_interval):
    result = []
    i = 0

    #1 . Add intervas completely before new_interval
    while i < len(intervals) and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    #2 Merge overlapping interavls 
    while i < len(intervals) and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1

    result.append(new_interval)

    #3. Add remaining intervals
    while i < len(intervals):
        result.append(intervals[i])
        i += 1

    return result

intervals =[[1, 3], [6, 9]]
new_interval = [2, 5]

print("Result:", insert_interval(intervals, new_interval))

                                          

