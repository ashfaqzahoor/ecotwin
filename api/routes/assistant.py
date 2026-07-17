from fastapi import APIRouter

from api.schemas import AssistantRequest, AssistantResponse
from api.services import answer_question

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("", response_model=AssistantResponse)
def ask_assistant(request: AssistantRequest) -> dict:
    return answer_question(request.question, request.city)
