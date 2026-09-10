def insert_interval(intervals, new_interval):
    result = []
    i = 0

    while i < len(intervals) and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    while i < len(intervals) and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1

    result.append(new_interval)

    

    while i < len(intervals):
        result.append(intervals[i])
        i += 1
    return result

n = int(input("Enter number off intervals:"))
intervals = []

for _ in range(n):
    intervals.append(list(map(int, input("Enter interval:").split())))

new_interval = list(map(int, input("Enter new interval: ").split()))

print("Result:", insert_interval(intervals, new_interval))
