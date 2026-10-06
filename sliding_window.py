def max_sum(nums, k):
    window_sum = sum(nums[:k])
    maximum = window_sum

    for i in range(k, len(nums)):
        window_sum += nums[i]
        window_sum -= nums[i - k]

        maximum = max(maximum, window_sum)

    return maximum

nums = [2, 1, 5, 1, 3, 2]
k = 3

print("Maximum sum:", max_sum(nums, k))