def length_of_lis(nums):
    dp = [1] *len(nums)

    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

nums = list(map(int, input("Enter numbers: ").split()))

print("Longest increasing subsequence length:", length_of_lis(nums))
