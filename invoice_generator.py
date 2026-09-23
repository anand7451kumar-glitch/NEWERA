from datetime import datetime

items = []

print("===== INVOICE GENERATOR =====")

while True:
    name = input("\nItem name (or 'done'): ")

    if name.lower() == "done":
        break

    quantity = int(input("Quantity: "))
    price = float(input("Price per item: ₹"))

    items.append({
        "name": name,
        "quantity": quantity,
        "price": price
    })

subtotal = sum(item["quantity"] * item["price"] for item in items)
gst = subtotal * 0.18
total = subtotal + gst

print("\n" + "=" * 45)
print("                 INVOICE")
print("=" * 45)
print("Date:", datetime.now().strftime("%d-%m-%Y %H:%M"))
print("-" * 45)

for item in items:
    amount = item["quantity"] * item["price"]
    print(
        f"{item['name']:<20}"
        f"{item['quantity']:>5}"
        f" ₹{amount:>10.2f}"
    )

print("-" * 45)
print(f"{'Subtotal':<30} ₹{subtotal:>10.2f}")
print(f"{'GST (18%)':<30} ₹{gst:>10.2f}")
print(f"{'TOTAL':<30} ₹{total:>10.2f}")
print("=" * 45)