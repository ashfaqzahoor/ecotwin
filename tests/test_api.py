from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predictions():
    response = client.get("/api/predictions?city=Delhi&horizon_hours=24")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 24
    assert {"pm25", "pm10", "no2", "o3", "temperature", "energy_demand"}.issubset(data[0])


def test_simulation_reduces_pm25():
    response = client.post("/api/simulation", json={"city": "Delhi", "horizon_hours": 24, "traffic_reduction": 50})
    assert response.status_code == 200
    data = response.json()
    assert data["simulated"][0]["pm25"] < data["baseline"][0]["pm25"]


def test_dataset_status():
    response = client.get("/api/datasets/status")
    assert response.status_code == 200
    data = response.json()
    assert {"uci_air_quality", "weatherbench_era5", "openaq"}.issubset(data)


def test_history_endpoint():
    response = client.get("/api/sensors/history?city=UCI-Italian-City&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
