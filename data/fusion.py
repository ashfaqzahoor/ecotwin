from pathlib import Path

import pandas as pd

from data.ingestion.uci_loader import load_uci_air_quality
from data.ingestion.weatherbench_loader import load_weatherbench
from data.preprocessing.cleaner import clean_environmental_frame
from data.preprocessing.feature_engineer import add_time_and_lag_features


TARGETS = ["pm25", "pm10", "no2", "o3", "temperature", "energy_demand"]


def build_training_frame(uci_path: str | Path, weather_path: str | Path | None = None) -> pd.DataFrame:
    air = load_uci_air_quality(uci_path)
    if weather_path and Path(weather_path).exists():
        weather = load_weatherbench(weather_path)
        air = pd.merge_asof(
            air.sort_values("observed_at"),
            weather.sort_values("observed_at"),
            on="observed_at",
            direction="nearest",
            tolerance=pd.Timedelta("3h"),
            suffixes=("", "_weather"),
        )
        for col in ["temperature", "humidity"]:
            weather_col = f"{col}_weather"
            if weather_col in air:
                air[col] = air[col].fillna(air[weather_col])
    air["energy_demand"] = 95 + air["temperature"].fillna(air["temperature"].median()).clip(lower=18).sub(24).clip(lower=0) * 6.5 + air["pm25"] * 0.35
    clean = clean_environmental_frame(air)
    return add_time_and_lag_features(clean, TARGETS)
