def build_lps(pattern):
    lps = [0] * len(pattern)

    length = 0
    i = 1

    while i < len(pattern):

        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        elif length > 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    return lps

def kmp_search(text, pattern):
    if not pattern:
        return 0

    lps = build_lps(pattern)

    i = 0
    j = 0

    while i < len(text):

        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                return i - j

        elif j > 0:
            j = lps[j - 1]

        else:
            i += 1

    return -1

text = input("Text: ")
pattern = input("Pattern: ")

index = kmp_search(text, pattern)

if index == -1:
    print("Pattern not found.")
else:
    print("Pattern found at index:", index)