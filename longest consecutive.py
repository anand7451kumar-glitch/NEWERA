def longest_consecutive(nims):
    numbers = set(nums)
    longest = 0

    for num in numbers:
        if num - 1 not in numbers:
            current = num
            length = 1

            while current + 1 in numbers:
                current += 1
                length += 1

            longest = max(longest, length)

    return longest

nums = list(map(int, input("Enter numnbers:").split()))

print("Longest consecutive sequence:", longest_consecutive(nums))
