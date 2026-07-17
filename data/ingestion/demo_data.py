from datetime import datetime, timedelta, timezone
from math import cos, sin
from random import Random

from config.constants import SUPPORTED_CITIES


def generate_city_readings(city: str, hours: int = 96) -> list[dict]:
    meta = SUPPORTED_CITIES[city]
    rng = Random(city)
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    city_factor = {
        "Delhi": 1.6,
        "Kanpur": 1.52,
        "Patna": 1.48,
        "Lucknow": 1.42,
        "Kolkata": 1.34,
        "Ludhiana": 1.32,
        "Amritsar": 1.28,
        "Ahmedabad": 1.25,
        "Jaipur": 1.22,
        "Hyderabad": 1.12,
        "Mumbai": 1.15,
        "Chennai": 1.0,
        "Pune": 0.95,
        "Bengaluru": 0.85,
        "Kochi": 0.78,
        "Thiruvananthapuram": 0.72,
        "Jammu": 0.92,
        "Srinagar": 0.88,
    }.get(city, 0.95 + (sum(ord(char) for char in city) % 40) / 100)
    rows = []
    for i in range(hours):
        ts = now - timedelta(hours=hours - i)
        hour_wave = 1 + 0.25 * sin((ts.hour - 7) / 24 * 6.283)
        commute = 1.25 if ts.hour in (8, 9, 18, 19) else 1.0
        weather = 1 + 0.12 * cos(i / 10)
        pm25 = max(4, city_factor * 28 * hour_wave * commute * weather + rng.uniform(-3, 3))
        temp = 24 + city_factor * 4 + 6 * sin((ts.hour - 5) / 24 * 6.283) + rng.uniform(-1, 1)
        rows.append(
            {
                "station_id": f"{city.lower()}-central",
                "city": city,
                "observed_at": ts,
                "pm25": round(pm25, 2),
                "pm10": round(pm25 * 1.8 + rng.uniform(-4, 4), 2),
                "no2": round(pm25 * 0.75 * commute + rng.uniform(-3, 3), 2),
                "o3": round(max(10, 65 - pm25 * 0.5 + 10 * sin(ts.hour / 24 * 6.283)), 2),
                "co": round(0.4 + pm25 / 80, 2),
                "so2": round(6 + city_factor * 5 + rng.uniform(-1, 1), 2),
                "temperature": round(temp, 2),
                "humidity": round(65 - temp * 0.6 + rng.uniform(-4, 4), 2),
                "wind_speed": round(1.5 + rng.random() * 4, 2),
                "pressure": round(1008 + rng.uniform(-5, 5), 2),
                "precipitation": round(max(0, rng.gauss(0.2, 0.7)), 2),
                "latitude": meta["lat"] + rng.uniform(-0.08, 0.08),
                "longitude": meta["lon"] + rng.uniform(-0.08, 0.08),
                "source": "demo",
            }
        )
    return rows
