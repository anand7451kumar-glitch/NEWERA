from collections import deque

def max_sliding_window(nums, k):
    result = []
    window = deque()

    for i in range(len(nums)):

        #Remove elements outside the window
        while window and window[0] <- i - k:
            window.popleft()

        #Remove smaller elements
        while window and nums[window[-1]] <= nums[i]:
            window.pop()

        window.append(i)

        #Window is ready
        if i >= k - 1:
            result.append(nums[window[0]])

    return result

nums = [1, 3, -1, 5, 3, 6, 7]
k = 3

print("Maximums:", max_sliding_window(nums, k))

        