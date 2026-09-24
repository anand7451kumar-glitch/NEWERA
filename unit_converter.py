value = float(input("Enter value: "))
unit = input("Convert (km/miles): ").lower()

if unit == "km":
    print("Miles", round(value * 0.621371, 2))

elif unit == "miles":
    print("Kiolmeters:", round(value * 1.60934, 2))

else:
    print("Invalid unit")