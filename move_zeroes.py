def move_zeroes(nums):
  position = 0

  for i in range(len(nums)):
    if nums[i] != 0:
      nums[position], nums[i] = nums[i], nums[position]
      position +=1

  return nums


mumbers = list(map(int, input("Enter numbers: ").split()))

print("After moving zeroes:", move_zeroes(numbers))
