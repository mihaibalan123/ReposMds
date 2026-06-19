import requests
import re
import sys


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0: "senin",
    1: "predominant senin",
    2: "parțial înnorat",
    3: "înnorat",
    45: "ceață",
    48: "ceață cu chiciură",
    51: "burniță ușoară",
    53: "burniță moderată",
    55: "burniță densă",
    56: "burniță înghețată ușoară",
    57: "burniță înghețată densă",
    61: "ploaie ușoară",
    63: "ploaie moderată",
    65: "ploaie abundentă",
    66: "ploaie înghețată ușoară",
    67: "ploaie înghețată abundentă",
    71: "ninsoare ușoară",
    73: "ninsoare moderată",
    75: "ninsoare abundentă",
    77: "granule de zăpadă",
    80: "averse ușoare de ploaie",
    81: "averse moderate de ploaie",
    82: "averse violente de ploaie",
    85: "averse ușoare de ninsoare",
    86: "averse abundente de ninsoare",
    95: "furtună",
    96: "furtună cu grindină ușoară",
    99: "furtună cu grindină abundentă",
}


def geocode_location(name: str) -> tuple[float, float, str] | None:
    params = {"name": name, "count": 1, "language": "ro", "format": "json"}
    resp = requests.get(GEOCODING_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results")
    if not results:
        return None
    r = results[0]
    lat = r["latitude"]
    lon = r["longitude"]
    label = f"{r.get('name', name)}, {r.get('country', '')}"
    return lat, lon, label


def parse_coordinates(text: str) -> tuple[float, float] | None:
    m = re.match(
        r"^\s*([-+]?\d+(?:\.\d+)?)\s*[,;]\s*([-+]?\d+(?:\.\d+)?)\s*$", text
    )
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


def fetch_weather(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "timezone": "auto",
    }
    resp = requests.get(FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def weather_description(code: int) -> str:
    return WMO_CODES.get(code, "cod necunoscut")


def main():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("Introdu o locație (ex: București) sau coordonate (lat,lon): ").strip()

    if not user_input:
        print("Nicio intrare furnizată.")
        sys.exit(1)

    coords = parse_coordinates(user_input)
    if coords:
        lat, lon = coords
        label = f"Coordonatele {lat}, {lon}"
    else:
        result = geocode_location(user_input)
        if result is None:
            print(f"Nu s-a găsit locația: {user_input}")
            sys.exit(1)
        lat, lon, label = result

    try:
        data = fetch_weather(lat, lon)
    except requests.RequestException as e:
        print(f"Eroare la conectarea cu API-ul meteo: {e}")
        sys.exit(1)

    current = data.get("current_weather", {})
    temp = current.get("temperature", "N/A")
    wind = current.get("windspeed", "N/A")
    wmo = current.get("weathercode", None)

    print(f"\nLocație: {label}")
    print(f"Temperatură: {temp}°C")
    print(f"Viteză vânt: {wind} km/h")
    if wmo is not None:
        print(f"Stare: {weather_description(wmo)}")


if __name__ == "__main__":
    main()
