from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config.settings import get_settings
from data.dataset_manager import download_uci
from data.fusion import TARGETS, build_training_frame


FEATURES = [
    "co",
    "no2",
    "nox",
    "benzene",
    "temperature",
    "humidity",
    "absolute_humidity",
    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
    "pm25_lag_1",
    "pm25_lag_2",
    "pm25_lag_6",
    "no2_lag_1",
    "no2_lag_2",
    "temperature_lag_1",
]


def train_from_available_datasets() -> dict:
    settings = get_settings()
    uci_path = Path(settings.uci_air_quality_path)
    if not uci_path.exists():
        uci_path = download_uci()
    weather_path = Path(settings.weatherbench_path)
    frame = build_training_frame(uci_path, weather_path if weather_path.exists() and any(weather_path.iterdir()) else None)
    model_frame = frame[FEATURES + TARGETS].dropna()
    x = model_frame[FEATURES]
    y = model_frame[TARGETS]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("regressor", MultiOutputRegressor(RandomForestRegressor(n_estimators=160, random_state=42, min_samples_leaf=3, n_jobs=-1))),
        ]
    )
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(mean_squared_error(y_test, pred) ** 0.5),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "targets": TARGETS,
        "features": FEATURES,
        "notes": "PM2.5/PM10 are UCI-derived proxy targets until OpenAQ history is added.",
    }
    settings.model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "metrics": metrics}, settings.model_dir / "dataset_model.joblib")
    joblib.dump(metrics, settings.model_dir / "dataset_model_metrics.joblib")
    return metrics


if __name__ == "__main__":
    import json

    print(json.dumps(train_from_available_datasets(), indent=2))
