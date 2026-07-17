import asyncio

from config.constants import SUPPORTED_CITIES
from data.ingestion.openaq_fetcher import fetch_openaq_city


async def hourly_data_update() -> dict[str, int]:
    counts = {}
    for city in SUPPORTED_CITIES:
        readings = await fetch_openaq_city(city)
        counts[city] = len(readings)
    return counts


if __name__ == "__main__":
    print(asyncio.run(hourly_data_update()))
