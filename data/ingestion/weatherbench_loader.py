from pathlib import Path

import pandas as pd


def load_weatherbench(path: str | Path) -> pd.DataFrame:
    """Load WeatherBench/ERA5 data from CSV, NetCDF, or Zarr.

    CSV is the easiest MVP route and should contain timestamp/city/weather
    columns. NetCDF and Zarr are supported through lazy xarray imports so the
    normal API runtime does not require the heavier WeatherBench stack unless
    those files are actually used.
    """
    path = Path(path)
    if path.is_dir() or path.suffix.lower() == ".zarr":
        return _load_xarray(path, kind="zarr")
    if path.suffix.lower() in {".nc", ".netcdf"}:
        return _load_xarray(path, kind="netcdf")
    df = pd.read_csv(path)
    return _standardize_weather_columns(df)


def _load_xarray(path: Path, kind: str) -> pd.DataFrame:
    try:
        import xarray as xr
    except ImportError as exc:
        raise RuntimeError("Install optional WeatherBench dependencies with: pip install xarray netCDF4 zarr") from exc

    dataset = xr.open_zarr(path) if kind == "zarr" else xr.open_dataset(path)
    frame = dataset.to_dataframe().reset_index()
    return _standardize_weather_columns(frame)


def _standardize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = df.rename(
        columns={
            "time": "observed_at",
            "timestamp": "observed_at",
            "t2m": "temperature",
            "2m_temperature": "temperature",
            "r": "humidity",
            "relative_humidity": "humidity",
            "u10": "wind_u",
            "v10": "wind_v",
            "tp": "precipitation",
            "msl": "pressure",
        }
    )
    if "observed_at" in renamed:
        renamed["observed_at"] = pd.to_datetime(renamed["observed_at"], utc=True, errors="coerce")
    if "temperature" in renamed and renamed["temperature"].median() > 100:
        renamed["temperature"] = renamed["temperature"] - 273.15
    if {"wind_u", "wind_v"}.issubset(renamed.columns):
        renamed["wind_speed"] = (renamed["wind_u"] ** 2 + renamed["wind_v"] ** 2) ** 0.5
    return renamed
