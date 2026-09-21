import requests

url = "https://hacker-news.firebaseio.com/v0/topstories.json"

response = requests.get(url)
story_ids = response.json()

print("\n====== TOP NEWS ======\n")

for story_id in story_ids[:10]:
    story = requests.get(
        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    ).json()

    print("Title:", story.get("title"))
    print("URL:", story.get("irl", "No link"))
    print("_" * 50)
