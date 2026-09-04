def reverse_string(text):
    result = ""

    for char in text:
        result = char + result

    return result

text = input("Enter a string: ")

print("Reversed string:", reverse_string(text))
