import matplotlib.pyplot as plt

months = ["Jan","Feb", "March", "April", "May"]
sales = [120, 180, 150, 240,300]

plt.plot(months, sales, marker="o")
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show