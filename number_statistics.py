def analyze_numbers(numbers):
  total = sum(numbers)
  average = total / len(numbers)
  largest = max(numbers)
  smallest = min(numbers)

return total, average, largest, smallest

numbers = list(map(float, input("Enter numbers separated by spaces: ").split()))

if numbers:
  total, average, largest, smallest = analyze_numbers(numbers)

print("\nStatistics")
print("----------")
print(f"Total: {total:g}")
print(f"Average: {average:.2f}")
print(f"Largest: {largest:g}")
print(f"Smallest: {smallest:g}")
else:
print("No numbers entered.")
