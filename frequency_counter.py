from collections import Counter


def frequency_counter(numbers):
    return Counter(numbers)


numbers = list(
    map(int, input("Enter numbers separated by spaces: ").split())
)

frequency = frequency_counter(numbers)

print("\nNumber Frequencies")
print("------------------")

for number, count in sorted(frequency.items()):
    print(f"{number}: {count}")
