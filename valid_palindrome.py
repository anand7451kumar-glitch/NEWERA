def is_palindrome(text):
    cleaned = ""

    for char in text.lower():
        if char.isalnum():
            cleaned += char

    return cleaned == cleaned[::-1]

text = input("Enter a string: ")

if is_palindrome(text):
    print("Valid palindrome")
else:
    print("Not a palindrome")
