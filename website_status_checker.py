import requests
import time

websites = [
    "https;//google.com",
    "https://github.com",
    "https://youtube.com",
    "https://openai.com"

]

print("====== WEBSITE STATUS ========")

for website in websites:
    try:
        start = time.time()

        response = requests.get(
            website,
            timeout=5,
            allow_redirects=True
        )

        elapsed = round((time.time() - start) * 1000, 2)

        print(f"\n{website}")
        print("Status:", response.status_code)
        print("Response time:", elapsed, "ms")

    except requests.RequestException:
        print(f"\n{website}")
        print("Status: OFFLINE / UNREACHABLE")
