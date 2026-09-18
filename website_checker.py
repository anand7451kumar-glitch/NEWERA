import urllib.request

url = input("Enter website URL: ")

try:
    response = urllib.request.urlopen(url, timeout=5)
    print("Website is online ✓")
    print("Status:", response.status)

except Exception:
    print("Website is unreachable ")
