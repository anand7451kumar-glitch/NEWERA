#We have packages 
# weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#days = 5 
#Packages must be shipped in order.
#Find the smallest ship capacity that can ship everything within 5 days.
#ans = 15 
# Day 1: 1 + 2 + 3 + 4 + 5 = 15
#Day 2: 6 + 7 = 13
#Day 3: 8 = 8
#Day 4: 9 = 9
#Day 5: 10 = 10

def ship_within_days(weights, days, capacity):
    current_weight = 0
    required_days = 1

    for weight in weights:
        if current_weight + weight > capacity:
            required_days += 1
            current_weight = 0

        current_weight += weight

    return required_days <= days

def min_capacity(weights, days):
    left = max(weights)
    right = sum(weights)

    while left < right:
        capacity = (left + right) // 2

        if ship_within_days(weights, days, capacity):
            right = capacity
        else: 
            left = capacity + 1

    return left

weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = 5

print("Minimum capacity:" , min_capacity(weights, days))



