def calculate_average(marks):
    return sum(marks) / len(marks)


def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


marks = []

print("Student Grade Analyzer")
print("----------------------")

for i in range(5):
    mark = float(input(f"Enter marks for subject {i + 1}: "))
    marks.append(mark)

average = calculate_average(marks)
grade = calculate_grade(average)

print("\nResults")
print("-------")
print(f"Marks: {marks}")
print(f"Average: {average:.2f}")
print(f"Grade: {grade}")
