def largest_rectangle(heights):
    stack = []
    max_area = 0

    for i in range(len(heights)):
        while stack and heights[i] < heights[stack[-1]]:
            height = heights[stack.pop()]

            if stack:
                width = i - stack[-1] - 1
            else:
                width = i

            max_area = max(max_area, height * width)

        stack.append(i)

    n = len(heights)

    while stack:
        height = heights[stack.pop()]

        if stack:
            width = n - stack[-1] - 1

        else:
            width = n

        max_area = max(max_area, height * width)

    return max_area

heights = [2, 1, 5, 6, 2, 3]

print("Largest rectangle:", largest_rectangle(heights))

