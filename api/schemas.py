from datetime import datetime

from pydantic import BaseModel, Field


class Reading(BaseModel):
    station_id: str
    city: str
    observed_at: datetime
    pm25: float | None = None
    pm10: float | None = None
    no2: float | None = None
    o3: float | None = None
    co: float | None = None
    so2: float | None = None
    temperature: float | None = None
    humidity: float | None = None
    wind_speed: float | None = None
    pressure: float | None = None
    precipitation: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    source: str = "demo"

    model_config = {"from_attributes": True}


class Prediction(BaseModel):
    city: str
    horizon_hours: int
    predicted_at: datetime
    pm25: float
    pm10: float
    no2: float
    o3: float
    temperature: float
    energy_demand: float


class ScenarioRequest(BaseModel):
    city: str = "Delhi"
    horizon_hours: int = Field(default=72, ge=1, le=168)
    traffic_reduction: float = Field(default=0, ge=0, le=100)
    green_cover_increase: float = Field(default=0, ge=0, le=100)
    industrial_emissions_reduction: float = Field(default=0, ge=0, le=100)
    public_transport_adoption: float = Field(default=0, ge=0, le=100)


class AssistantRequest(BaseModel):
    question: str
    city: str = "Delhi"


class AssistantResponse(BaseModel):
    intent: str
    answer: str
    data: dict | list
