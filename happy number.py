def is_happy(n):
    seen = set()

    while n != 1 and n not in seen:
        seen.add(n)
        total = 0

        while n > 0:
            digit = n % 10
            total += digit * digit
            n //= 10

        n = total

    return n == 1

n = int(input("Enter a number: "))

print("Happy number:", is_happy(n))
