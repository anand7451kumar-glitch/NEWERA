#length of the longest substring with no repeated characters.


def longest_substring(s):
    left = 0
    longest = 0
    seen = set()

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1

        seen.add(s[right])
        longest = max(longest, right - left + 1)
        
    return longest

s = "abcabcbb"

print("Longest length:", longest_substring(s))

