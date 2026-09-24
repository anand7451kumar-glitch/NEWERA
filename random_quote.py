import requests

url = "https://api.quotable.io/random"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("\n" + data["content"])
    print("_", data["author"])
else:
    print("Could not fetch quote.")