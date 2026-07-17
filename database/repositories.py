from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import EnvironmentalReading


READING_FIELDS = {
    "station_id",
    "city",
    "observed_at",
    "pm25",
    "pm10",
    "no2",
    "o3",
    "co",
    "so2",
    "temperature",
    "humidity",
    "wind_speed",
    "pressure",
    "precipitation",
    "latitude",
    "longitude",
    "source",
}


def insert_readings(db: Session, rows: list[dict]) -> int:
    objects = [EnvironmentalReading(**{key: value for key, value in row.items() if key in READING_FIELDS}) for row in rows]
    db.bulk_save_objects(objects)
    db.commit()
    return len(objects)


def get_history(db: Session, city: str, start: datetime | None = None, end: datetime | None = None, limit: int = 500) -> list[EnvironmentalReading]:
    statement = select(EnvironmentalReading).where(EnvironmentalReading.city == city)
    if start:
        statement = statement.where(EnvironmentalReading.observed_at >= start)
    if end:
        statement = statement.where(EnvironmentalReading.observed_at <= end)
    statement = statement.order_by(EnvironmentalReading.observed_at.desc()).limit(limit)
    return list(db.scalars(statement))
