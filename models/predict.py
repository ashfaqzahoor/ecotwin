from models.model import EcoTwinForecaster

forecaster = EcoTwinForecaster()


def predict_city(city: str, horizon_hours: int = 72, history: list[dict] | None = None) -> list[dict]:
    return forecaster.predict(city=city, horizon_hours=horizon_hours, history=history)
