def num_decodings(s):
    if not s or s[0] == "0":
        return 0

    dp = [0] * (len(s) + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, len(s) + 1):
        one_digit = int(s[i - 1])
        two_digits = int(s[i - 2:i])

        if 1 <= one_digit <= 9:
            dp[i] += dp[i - 1]

        if 10 <= two_digits <= 26:
            dp[i] += dp[i - 2]

    return dp[-1]

s = input("Enter encoded number: ")

print("Number of ways:", num_decodings(s))


