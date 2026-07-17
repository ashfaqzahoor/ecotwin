from collections import defaultdict

from config.constants import SCENARIO_EFFECTS, WHO_LIMITS
from data.ingestion.demo_data import generate_city_readings
from models.predict import predict_city


def latest_readings(city: str) -> list[dict]:
    return generate_city_readings(city, hours=8)[-8:]


def predictions(city: str, horizon_hours: int = 72) -> list[dict]:
    return predict_city(city, horizon_hours)


def active_alerts(city: str) -> list[dict]:
    forecast = predictions(city, 72)
    breaches: dict[str, list[float]] = defaultdict(list)
    for row in forecast:
        for pollutant, threshold in WHO_LIMITS.items():
            if row.get(pollutant, 0) > threshold:
                breaches[pollutant].append(row[pollutant])
    alerts = []
    for pollutant, values in breaches.items():
        peak = max(values)
        severity = "critical" if peak > WHO_LIMITS[pollutant] * 1.8 else "warning"
        alerts.append(
            {
                "city": city,
                "pollutant": pollutant,
                "severity": severity,
                "value": round(peak, 2),
                "threshold": WHO_LIMITS[pollutant],
                "predicted_duration_hours": len(values),
                "message": f"{city} is forecast to exceed the {pollutant.upper()} safety threshold.",
                "recommended_action": _recommended_action(pollutant),
            }
        )
    return sorted(alerts, key=lambda item: item["value"] / item["threshold"], reverse=True)


def simulate(request) -> dict:
    baseline = predictions(request.city, request.horizon_hours)
    params = request.model_dump()
    simulated = []
    for point in baseline:
        adjusted = point.copy()
        for knob, effects in SCENARIO_EFFECTS.items():
            intensity = params.get(knob, 0) / 100
            for metric, coefficient in effects.items():
                if metric in adjusted:
                    adjusted[metric] = round(max(0, adjusted[metric] * (1 + coefficient * intensity)), 2)
        simulated.append(adjusted)
    return {"city": request.city, "parameters": params, "baseline": baseline, "simulated": simulated}


def answer_question(question: str, city: str) -> dict:
    lower = question.lower()
    if "traffic" in lower or "green" in lower or "industrial" in lower or "public transport" in lower or "what happens" in lower:
        class Req:
            def __init__(self):
                self.city = city
                self.horizon_hours = 72
                self.traffic_reduction = 20 if "traffic" in lower else 0
                self.green_cover_increase = 20 if "green" in lower else 0
                self.industrial_emissions_reduction = 20 if "industrial" in lower else 0
                self.public_transport_adoption = 20 if "public transport" in lower else 0

            def model_dump(self):
                return self.__dict__

        data = simulate(Req())
        before = data["baseline"][23]["pm25"]
        after = data["simulated"][23]["pm25"]
        return {"intent": "simulation", "answer": f"With the requested policy shift, tomorrow's PM2.5 changes from {before} to {after} in {city}.", "data": data}
    if "alert" in lower or "who" in lower or "exceed" in lower:
        data = active_alerts(city)
        answer = f"{len(data)} alert categories are active for {city}." if data else f"No WHO-threshold alerts are active for {city}."
        return {"intent": "alerts", "answer": answer, "data": data}
    data = predictions(city, 72)
    tomorrow = data[23]
    return {
        "intent": "forecast",
        "answer": f"Tomorrow in {city}, PM2.5 is forecast near {tomorrow['pm25']}, NO2 near {tomorrow['no2']}, and temperature near {tomorrow['temperature']} C.",
        "data": data,
    }


def _recommended_action(pollutant: str) -> str:
    actions = {
        "pm25": "Reduce traffic exposure, restrict dust-generating activity, and prioritize public transport.",
        "pm10": "Increase road dust control, construction-site enforcement, and street cleaning.",
        "no2": "Reduce diesel traffic and industrial combustion during the forecast window.",
        "o3": "Limit precursor emissions and warn vulnerable residents during afternoon peaks.",
        "temperature": "Open cooling centers, increase shade, and shift peak energy loads.",
    }
    return actions.get(pollutant, "Monitor affected zones and apply targeted emission controls.")
