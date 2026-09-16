def rob(nums):
    previous = 0
    current = 0

    for money in nums:
        previous, current = current, max(
            current,
            previous + money
        )
    return current

houses = list(map(int, input("Enter money in each house: ").split()))

print("Maximum money:", rob(houses))
