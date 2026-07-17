from fastapi import APIRouter, Query

from api.services import active_alerts

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def get_alerts(city: str = Query("Delhi")) -> list[dict]:
    return active_alerts(city)
