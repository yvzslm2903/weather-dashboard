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


zeiten = data["hourly"]["time"]
temperaturen = data["hourly"]["temperature_2m"]

for i in range(len(zeiten)):
    print(zeiten[i], temperaturen[i])

def parse_hourly(data):
    zeiten = data["hourly"]["time"]
    temperaturen = data["hourly"]["temperature_2m"]
    niederschlag = data["hourly"]["precipitation"]
    wind = data["hourly"]["wind_speed_10m"]

    zeilen = []
    for i in range(len(zeiten)):
        eintrag = {
            "time": zeiten[i],
            "temperature": temperaturen[i],
            "precipitation": niederschlag[i],
            "wind_speed": wind[i],
        }
        zeilen.append(eintrag)
    return zeilen

zeilen = parse_hourly(data)
print(zeilen[:3])
print("Anzahl:", len(zeilen))

from datetime import datetime
from models import WeatherRecord, Session, init_db

def save_records(zeilen):
    session = Session()
    neu = 0
    for zeile in zeilen:
        zeitpunkt = datetime.fromisoformat(zeile["time"])
        
        vorhanden = session.query(WeatherRecord).filter_by(time=zeitpunkt).first()
        if vorhanden is None:
            eintrag = WeatherRecord(
                time=zeitpunkt,
                temperature=zeile["temperature"],
                precipitation=zeile["precipitation"],
                wind_speed=zeile["wind_speed"],
            )
            session.add(eintrag)
            neu += 1

    session.commit()
    session.close()
    return neu

init_db()
zeilen = parse_hourly(data)
print("Neu gespeichert:", save_records(zeilen))
