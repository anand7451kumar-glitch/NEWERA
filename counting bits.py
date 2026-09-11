def counting_bits(n):
    result = [0] * (n + 1)

    for i in range(1, n + 1):
        result[i] = result[i >> 1] + ( i & 1)
    
    return result

n = int(input("Enter n: "))

print("Number of 1 bits:", counting_bits(n))
