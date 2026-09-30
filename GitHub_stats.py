import requests

user = input("GitHub username: ")

data = requests.get(
  f"https://api.github.com/users/{user}"
).json()

print("Name:", data["name"])
print("Public repos:", data["public_repos"])
print("Followers:", data["followers"])
print("Folowing:", data["following"])
