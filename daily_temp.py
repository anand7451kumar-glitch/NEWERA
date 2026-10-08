#Given daily temperatures, find how many days you have to wait until a warmer temperature. 
# temperatures = [73, 74, 75, 71, 69, 72, 76, 73] 
# Expected [1, 1, 4, 2, 1, 1, 0, 0]

def daily_temperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []

    for i in range(len(temperatures)):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            previous_day = stack.pop()
            result[previous_day] = i - previous_day

        stack.append(i)

    return result

temperatures = [73, 74, 75, 71, 69, 76, 73, 72]

print("Waiting days:", daily_temperatures(temperatures))


