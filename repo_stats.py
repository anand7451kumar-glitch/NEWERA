import requests

username = input("GitHub username: ").strip()

url = f"https:api.github.com/users/{username}/repos"
repos = requests.get(url).json()

if isinstance(repos, dict):
    print("User not Found.")
else:
    repos.sort(key=lambda repo: repo["stargazers_count"], reverse=True)

    print("\n=== TOP REPOSITORIES ===")

    for repo in repos[:5]:
        print(
            repo["name"],
            "🌟", repo["stargazers_count"],
            "| Forks:", repo["forks_count"]
        )