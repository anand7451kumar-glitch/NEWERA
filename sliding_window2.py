def min_subarray_len(target, nums):
    left = 0
    window_sum = 0
    minimum = float("inf")

    for right in range(len(nums)):
        window_sum += nums[right]

        while window_sum >= target:
            minimum = min(minimum, right - left + 1)
            window_sum -= nums[left]
            left += 1

    if minimum == float("inf"):
        return 0

    return minimum

nums = [2, 3, 1, 2, 4, 3]
target = 7

print("Minimum length:", min_subarray_len(target, nums))

    