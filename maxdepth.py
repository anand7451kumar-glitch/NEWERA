def max_depth(s):
    depth = 0
    maximum = 0

    for char in s:
        if char == "(":
            depth += 1
            maximum = max(maximum, depth)

        elif char == ")":
            depth -= 1

    return maximum

s = input("Enter parentheses:")
print("Maximum depth:", max_depth(s))
