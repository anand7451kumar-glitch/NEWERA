def generate_parentheses(n):
    result = []

    def backtrack(current, opening, closing):
        if len(current) == 2 * n:
            result.append(current)
            return

        if opening < n:
            backtrack(current + "(", opening + 1, closing)
            
        if closing < opening:
            backtrack(current + ")", opening, closing + 1)

    backtrack("", 0, 0)
    return result

n = int(input("Enter number of pairs: "))

print("Valid parentheses:")
for combination in generate_parentheses(n):
    print(combination)
