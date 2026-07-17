import pandas as pd

from data.preprocessing.cleaner import clean_environmental_frame
from data.preprocessing.feature_engineer import add_time_and_lag_features
from data.ingestion.uci_loader import load_uci_air_quality


def test_cleaner_and_features():
    df = pd.DataFrame(
        {
            "city": ["Delhi", "Delhi"],
            "observed_at": ["2026-01-01T00:00:00Z", "2026-01-01T01:00:00Z"],
            "pm25": [10, -200],
        }
    )
    cleaned = clean_environmental_frame(df)
    featured = add_time_and_lag_features(cleaned, ["pm25"], lags=(1,))
    assert "hour_sin" in featured
    assert "pm25_lag_1" in featured


def test_uci_loader_when_dataset_present():
    path = "data/raw/uci_air_quality/AirQualityUCI.csv"
    try:
        loaded = load_uci_air_quality(path)
    except FileNotFoundError:
        return
    assert {"pm25", "pm10", "no2", "o3", "temperature", "humidity"}.issubset(loaded.columns)
    assert len(loaded) > 1000
