import requests

city = input("Enter city: ")

locations = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": city, "count": 1}
).json()

if "results" not in locations:
    print("City not found.")
    exit()

location = locations["results"][0]

weather = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }
).json()

if "current" not in weather:
    print("Weather data unavailable.")
    print(weather)
    exit()

current = weather["current"]

print("\n===== WEATHER =====")
print("City:", location["name"])
print("Temperature:", current["temperature_2m"], "°C")
print("Humidity:", current["relative_humidity_2m"], "%")
print("Wind:", current["wind_speed_10m"], "km/h")
