def find_median(nums1, nums2):
    #Always binary search the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m = len(nums1)
    n = len(nums2)

    left = 0
    right = m

    while left <= right:
        cut1 = (left + right) // 2
        cut2 = (m + n + 1) // 2 - cut1

        if cut1 == 0:
            left1 = float("-inf")
        else:
            left1 = nums1[cut1 - 1]

        if cut1 == m:
            right1 = float("inf")
        else:
            right1 = nums1[cut1]

        if cut2 == 0:
            left2 = float("-inf")
        else:
            left2 = nums2[cut2 - 1]

        if cut2 == n:
            right2 = float("inf")
        else: 
            right2 = nums2[cut2]

        if left1 <= right2 and left2 <= right1:

            if (m + n) % 2 == 1:
                return max(left1, left2)

            return (max(left1, left2) + min(right1, right2)) / 2

        elif left1 > right2:
            right = cut1 - 1
        else:
            left = cut1 + 1

    return 0

nums1 = [1, 3]
nums2 = [2]

print("Median:", find_median(nums1, nums2))
        
