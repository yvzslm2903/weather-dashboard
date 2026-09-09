import requests

URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": "temperature_2m,precipitation,wind_speed_10m",
    "timezone": "Europe/Berlin",
    "forecast_days": 2,
}

response = requests.get(URL, params=params)
data = response.json()

print("Status:", response.status_code)
print("Keys:", data.keys())
print()
print("Einheiten:", data["hourly_units"])
print()
print("Erste 5 Zeiten:", data["hourly"]["time"][:5])
print("Erste 5 Temperaturen:", data["hourly"]["temperature_2m"][:5])
print("Anzahl Einträge:", len(data["hourly"]["time"]))