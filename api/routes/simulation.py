from fastapi import APIRouter

from api.schemas import ScenarioRequest
from api.services import simulate

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.post("")
def run_simulation(request: ScenarioRequest) -> dict:
    return simulate(request)
