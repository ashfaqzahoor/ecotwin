import pandas as pd


def clean_environmental_frame(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.replace([-200, -999, "NA", "nan", ""], pd.NA)
    if "observed_at" in cleaned.columns:
        cleaned["observed_at"] = pd.to_datetime(cleaned["observed_at"], errors="coerce", utc=True)
        cleaned = cleaned.dropna(subset=["observed_at"]).sort_values("observed_at")
    numeric_cols = cleaned.select_dtypes(include="number").columns
    cleaned[numeric_cols] = cleaned[numeric_cols].interpolate(limit=3).ffill().bfill()
    return cleaned.drop_duplicates()
