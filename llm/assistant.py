from api.services import answer_question


def ask(question: str, city: str = "Delhi") -> dict:
    return answer_question(question, city)
