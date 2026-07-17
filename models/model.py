from datetime import datetime, timedelta, timezone
from math import cos, sin

from config.constants import FORECAST_TARGETS
from data.ingestion.demo_data import generate_city_readings


class EcoTwinForecaster:
    """Lightweight deterministic forecaster used for the MVP runtime.

    The class mirrors a trainable model interface, but it can serve immediately
    from historical observations or demo data. It is intentionally replaceable by
    an LSTM, TCN, Transformer, or Graph model later without changing API routes.
    """

    version = "ecotwin-statistical-v1"

    def predict(self, city: str, horizon_hours: int = 72, history: list[dict] | None = None) -> list[dict]:
        rows = history or generate_city_readings(city, hours=96)
        latest = rows[-24:] if len(rows) >= 24 else rows
        base = {target: self._mean(latest, target) for target in FORECAST_TARGETS}
        base["energy_demand"] = base.get("energy_demand") or self._energy_from_weather(base)
        start = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        forecast = []
        for hour in range(1, horizon_hours + 1):
            daily = sin(hour / 24 * 6.283)
            commute = 1.18 if (start + timedelta(hours=hour)).hour in (8, 9, 18, 19) else 1.0
            trend = 1 + 0.015 * cos(hour / 8)
            point = {"city": city, "horizon_hours": hour, "predicted_at": start + timedelta(hours=hour)}
            point["pm25"] = round(base["pm25"] * trend * commute, 2)
            point["pm10"] = round(base["pm10"] * trend * (1 + 0.04 * daily), 2)
            point["no2"] = round(base["no2"] * commute * (1 + 0.05 * daily), 2)
            point["o3"] = round(max(5, base["o3"] * (1 - 0.07 * daily)), 2)
            point["temperature"] = round(base["temperature"] + 4 * daily, 2)
            point["energy_demand"] = round(self._energy_from_weather(point), 2)
            forecast.append(point)
        return forecast

    @staticmethod
    def _mean(rows: list[dict], key: str) -> float:
        values = [float(row[key]) for row in rows if row.get(key) is not None]
        defaults = {"pm25": 25, "pm10": 50, "no2": 22, "o3": 45, "temperature": 30, "energy_demand": 120}
        return sum(values) / len(values) if values else defaults[key]

    @staticmethod
    def _energy_from_weather(row: dict) -> float:
        temperature = float(row.get("temperature") or 30)
        pm25 = float(row.get("pm25") or 25)
        cooling = max(0, temperature - 24) * 6.5
        pollution_penalty = pm25 * 0.35
        return 95 + cooling + pollution_penalty
