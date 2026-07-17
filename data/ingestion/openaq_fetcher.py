import httpx

from config.constants import POLLUTANTS, SUPPORTED_CITIES
from config.settings import get_settings
from data.ingestion.demo_data import generate_city_readings


async def fetch_openaq_city(city: str) -> list[dict]:
    settings = get_settings()
    if city not in SUPPORTED_CITIES or not settings.openaq_api_key:
        return generate_city_readings(city if city in SUPPORTED_CITIES else "Delhi", hours=24)

    headers = {"X-API-Key": settings.openaq_api_key}
    params = {"city": city, "parameter": POLLUTANTS, "limit": 100}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"{settings.openaq_base_url}/measurements", headers=headers, params=params)
        response.raise_for_status()
        payload = response.json()

    readings: dict[tuple[str, str], dict] = {}
    for item in payload.get("results", []):
        parameter = item.get("parameter")
        if parameter not in POLLUTANTS:
            continue
        station_id = item.get("location", {}).get("id") or item.get("location", {}).get("name", city)
        observed_at = item.get("period", {}).get("datetimeFrom", {}).get("utc")
        key = (station_id, observed_at)
        row = readings.setdefault(
            key,
            {
                "station_id": str(station_id),
                "city": city,
                "observed_at": observed_at,
                "latitude": item.get("coordinates", {}).get("latitude"),
                "longitude": item.get("coordinates", {}).get("longitude"),
                "source": "openaq",
            },
        )
        row[parameter] = item.get("value")
    return list(readings.values()) or generate_city_readings(city, hours=24)
