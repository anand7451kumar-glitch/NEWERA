def longest_palindrome(s):
    best = ""

    for i in range(len(s)):
        left = right = i

        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > len(best):
                best = s[left:right + 1]

            left -= 1
            right += 1 

        left, right = i, i + 1

        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > len(best):
                best = s[left:right + 1]

            left -= 1
            right += 1

    return best

s = input("Enter a string: ")

print("Longest palindrome:", longest_palindrome(s))
