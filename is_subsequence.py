def is_subsequence(s, t):
    i = 0

    for char in t:
        if i <len(s) and s[i] == char:
            i += 1

    return i == len(s)

s = input("Enter first string: ")
t = input("Enter second string: ")

if is_subsequence(s, t):
    print("Yes, it is a subsequence")
else:
    print("No, it is not a subsequence")
