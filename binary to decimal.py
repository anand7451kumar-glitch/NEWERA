def binary_to_decimal(binary):
    decimal = 0
    power = 0

    while binary > 0:
        digit = binary % 10
        decimal += digit * (2 ** power)
        power += 1
        binary //= 10

    return decimal

binary = int(input("enter a binary number:"))

print("Decimal:", binary_to_decimal(binary))
