from models.predict import predict_city


def test_forecaster_horizon():
    forecast = predict_city("Delhi", 12)
    assert len(forecast) == 12
    assert all(point["energy_demand"] > 0 for point in forecast)
