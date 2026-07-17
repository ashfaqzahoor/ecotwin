from pathlib import Path

import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def fit_transform(df: pd.DataFrame, columns: list[str], scaler_path: str | Path) -> pd.DataFrame:
    scaler = MinMaxScaler()
    out = df.copy()
    out[columns] = scaler.fit_transform(out[columns])
    Path(scaler_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, scaler_path)
    return out


def transform(df: pd.DataFrame, columns: list[str], scaler_path: str | Path) -> pd.DataFrame:
    scaler = joblib.load(scaler_path)
    out = df.copy()
    out[columns] = scaler.transform(out[columns])
    return out
