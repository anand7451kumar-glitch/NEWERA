def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

print(is_power_of_two(1))
print(is_power_of_two(2))
print(is_power_of_two(8))
print(is_power_of_two(10))
print(is_power_of_two(16))