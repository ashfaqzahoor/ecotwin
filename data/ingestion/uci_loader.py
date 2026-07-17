from pathlib import Path

import pandas as pd


def load_uci_air_quality(path: str | Path) -> pd.DataFrame:
    """Load and normalize the UCI Air Quality dataset into EcoTwin fields.

    The UCI dataset is an hourly urban air-quality series from Italy. It has
    measured CO, NOx, NO2, temperature and humidity, plus metal-oxide sensor
    responses. It does not directly include PM2.5/PM10, so this MVP derives
    transparent proxy estimates for those targets until OpenAQ history is added.
    """
    source = pd.read_csv(path, sep=";", decimal=",", na_values=[-200, ""], engine="python")
    source = source.dropna(axis=1, how="all").dropna(how="all")
    observed_at = pd.to_datetime(source["Date"] + " " + source["Time"].str.replace(".", ":", regex=False), dayfirst=True, errors="coerce", utc=True)
    df = pd.DataFrame(
        {
            "station_id": "uci-air-quality-station",
            "city": "UCI-Italian-City",
            "observed_at": observed_at,
            "co": pd.to_numeric(source.get("CO(GT)"), errors="coerce"),
            "no2": pd.to_numeric(source.get("NO2(GT)"), errors="coerce"),
            "nox": pd.to_numeric(source.get("NOx(GT)"), errors="coerce"),
            "benzene": pd.to_numeric(source.get("C6H6(GT)"), errors="coerce"),
            "temperature": pd.to_numeric(source.get("T"), errors="coerce"),
            "humidity": pd.to_numeric(source.get("RH"), errors="coerce"),
            "absolute_humidity": pd.to_numeric(source.get("AH"), errors="coerce"),
            "o3_sensor": pd.to_numeric(source.get("PT08.S5(O3)"), errors="coerce"),
            "source": "uci_air_quality",
        }
    )
    df["pm25"] = (df["no2"].fillna(df["no2"].median()) * 0.22 + df["co"].fillna(df["co"].median()) * 4.0).clip(lower=1)
    df["pm10"] = (df["pm25"] * 1.8).clip(lower=2)
    df["o3"] = (df["o3_sensor"].fillna(df["o3_sensor"].median()) / 22).clip(lower=5, upper=120)
    return df.dropna(subset=["observed_at"]).sort_values("observed_at").reset_index(drop=True)
