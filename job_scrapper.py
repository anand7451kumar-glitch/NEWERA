import requests
from bs4 import BeautifulSoup

url = input("Enter website URL: ")

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

for tag in soup.find_all(["h1", "h2", "h3"])[:10]:
    print(tag.get_text(strip=True))


