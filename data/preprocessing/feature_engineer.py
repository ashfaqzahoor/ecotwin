import numpy as np
import pandas as pd


def add_time_and_lag_features(df: pd.DataFrame, target_cols: list[str], lags: tuple[int, ...] = (1, 2, 6, 12, 24)) -> pd.DataFrame:
    features = df.copy()
    ts = pd.to_datetime(features["observed_at"], utc=True)
    features["hour_sin"] = np.sin(2 * np.pi * ts.dt.hour / 24)
    features["hour_cos"] = np.cos(2 * np.pi * ts.dt.hour / 24)
    features["dow_sin"] = np.sin(2 * np.pi * ts.dt.dayofweek / 7)
    features["dow_cos"] = np.cos(2 * np.pi * ts.dt.dayofweek / 7)
    for col in target_cols:
        if col not in features:
            continue
        for lag in lags:
            features[f"{col}_lag_{lag}"] = features.groupby("city")[col].shift(lag) if "city" in features else features[col].shift(lag)
    with pd.option_context("future.no_silent_downcasting", True):
        return features.ffill().bfill().infer_objects(copy=False)
