from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.schemas import Reading
from api.services import latest_readings
from config.constants import SUPPORTED_CITIES
from database.db_connection import get_db
from database.repositories import get_history

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("")
def get_sensors(city: str = Query("Delhi")) -> list[dict]:
    return latest_readings(city if city in SUPPORTED_CITIES else "Delhi")


@router.get("/history", response_model=list[Reading])
def get_sensor_history(
    city: str = Query("UCI-Italian-City"),
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = Query(250, ge=1, le=2000),
    db: Session = Depends(get_db),
) -> list:
    return get_history(db, city=city, start=start, end=end, limit=limit)


@router.get("/cities")
def get_cities() -> dict:
    return SUPPORTED_CITIES
