def coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for current in range(1, amount + 1):
        for coin in coins:
            if coin <= current:
                dp[current] = min(
                    dp[current],
                    dp[current - coin] + 1
                )

    if dp[amount] > amount:
        return -1

    return dp[amount]

coins = list(map(int, input("Enter coin values: ").split()))
amount = int(input("Enter amount: "))

print("Minimum coins:", coin_change(coins, amount))
