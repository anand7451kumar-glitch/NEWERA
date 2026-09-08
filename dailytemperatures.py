def daily_temperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []

    for i, temp in enumerate(temperatures):
        while stack and temp > temperatures[stack[-1]]:
            previous = stack.pop()
            result[previous] = i - previous

        stack.append(i)

    return result

temperatures = list(map(int, input("Enter temperatures: ").split()))

print("Days until warmer temoerature:", daily_temperatures(temperatures))
