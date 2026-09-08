from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)

    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)

    return list(groups.values())


words = input("Enter words separated by spaces: ").split()

print("Grouped anagrams:", group_anagrams(words))