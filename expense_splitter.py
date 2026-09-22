people = int(input("How many people?"))
total = float(input("Enter total bill: ₹"))

tip = float(input("Enter tip percentage: "))

tip_amount = total * tip / 100
final_bill = total + tip_amount
share = final_bill / people

print("/n======== BILL SUMMARY ========")
print("Original bill: ₹", round(total, 2))
print("Tip amount: ₹", round(tip_amount, 2))
print("Final bill: ₹", round(final_bill, 2))
print("Each person pays: ₹", round(share, 2))
