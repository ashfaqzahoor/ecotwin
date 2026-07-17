from fastapi import APIRouter, Query

from api.services import predictions

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("")
def get_predictions(city: str = Query("Delhi"), horizon_hours: int = Query(72, ge=1, le=168)) -> list[dict]:
    return predictions(city, horizon_hours)
