import requests

url = input("Enter URL: ")

response = requests.get(
    "https://tinyurl.com/api-create.php",
    params={"url": url}
)

if response.status_code == 200:
    print("Short URL:", response.text)
else:
    print("Could not shorten URL.") 