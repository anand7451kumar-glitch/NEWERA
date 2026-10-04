def knapsack(weights, values, capacity):
    n = len(weights)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]

        for limit in range(1, capacity + 1):

            if weight <= limit:
                take = value + dp[i - 1][limit - weight]
                skip = dp[i - 1][limit]

                dp[i][limit] = max(take, skip)

            else:
                dp[i][limit] = dp[i -1][limit]

    return dp[n][capacity]

weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]

capacity = int(input("Bag capacity: "))

print("Maximum value:", knapsack(weights, values, capacity))