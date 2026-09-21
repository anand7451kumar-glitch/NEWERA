#!/usr/bin/env python3
"""Print the current weather for a city using Open-Meteo (no API key needed)."""

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 80: "Rain showers",
    81: "Moderate rain showers", 82: "Violent rain showers", 95: "Thunderstorm",
    96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def get_json(url: str) -> dict:
    """Fetch JSON with a short timeout and useful errors."""
    try:
        with urlopen(url, timeout=10) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Weather service returned HTTP {error.code}.") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach weather service: {error.reason}") from error


def current_weather(city: str, unit: str) -> dict:
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search?" + urlencode({
        "name": city, "count": 1, "language": "en", "format": "json",
    })
    locations = get_json(geocode_url).get("results", [])
    if not locations:
        raise RuntimeError(f"No location found for {city!r}.")

    place = locations[0]
    weather_url = "https://api.open-meteo.com/v1/forecast?" + urlencode({
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,"
                   "precipitation,weather_code,wind_speed_10m",
        "temperature_unit": "fahrenheit" if unit == "f" else "celsius",
        "wind_speed_unit": "mph" if unit == "f" else "kmh",
    })
    return {"place": place, "current": get_json(weather_url)["current"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Get current weather for a city.")
    parser.add_argument("city", help='City name, e.g. "Bengaluru"')
    parser.add_argument("--unit", choices=("c", "f"), default="c", help="Temperature unit (default: c)")
    args = parser.parse_args()

    try:
        result = current_weather(args.city, args.unit)
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    place, current = result["place"], result["current"]
    temp_unit = "°F" if args.unit == "f" else "°C"
    wind_unit = "mph" if args.unit == "f" else "km/h"
    location = ", ".join(part for part in (place["name"], place.get("admin1"), place.get("country")) if part)
    print(f"Current weather — {location} ({current['time']})")
    print(f"{WEATHER_CODES.get(current['weather_code'], 'Unknown')}: {current['temperature_2m']}{temp_unit} "
          f"(feels like {current['apparent_temperature']}{temp_unit})")
    print(f"Humidity: {current['relative_humidity_2m']}% | Precipitation: {current['precipitation']} mm "
          f"| Wind: {current['wind_speed_10m']} {wind_unit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
