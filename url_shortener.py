import random
import string

urls = {}

def create_short_url(url):
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    urls[code] = url
    return code

while True:
    print("\n1. Shorten URL")
    print("2. Open URL")
    print("3. Show all URLs")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        url = input("Enter URL: ")
        code = create_short_url(url)
        print("Short code:", code)

    elif choice == "2":
        code = input("Enter short code: ")
        print("Original URL:", urls.get(code, "Not found"))

    elif choice == "3":
        for code, url in urls.items():
            print(code, "->", url)

    elif choice == "4":
        break

    else:
        print("Invalid choice")
