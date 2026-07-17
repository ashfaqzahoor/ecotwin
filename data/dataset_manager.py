from pathlib import Path
from zipfile import ZipFile

import httpx

from config.settings import get_settings

UCI_URLS = [
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00360/AirQualityUCI.zip",
    "https://archive.ics.uci.edu/static/public/360/air+quality.zip",
]


def dataset_status() -> dict:
    settings = get_settings()
    uci_path = Path(settings.uci_air_quality_path)
    weatherbench_path = Path(settings.weatherbench_path)
    return {
        "uci_air_quality": {
            "ready": uci_path.exists(),
            "path": str(uci_path),
            "action": "Run: python -m data.dataset_manager download-uci" if not uci_path.exists() else "Ready",
        },
        "weatherbench_era5": {
            "ready": weatherbench_path.exists() and any(weatherbench_path.iterdir()),
            "path": str(weatherbench_path),
            "action": "Place ERA5/WeatherBench .csv, .nc, or .zarr files in data/raw/weatherbench/",
        },
        "openaq": {
            "ready": bool(settings.openaq_api_key),
            "path": "OpenAQ API",
            "action": "Set OPENAQ_API_KEY in .env for live ingestion" if not settings.openaq_api_key else "Ready",
        },
    }


def download_uci() -> Path:
    settings = get_settings()
    raw_dir = Path(settings.data_dir)
    target_dir = raw_dir / "uci_air_quality"
    target_dir.mkdir(parents=True, exist_ok=True)
    zip_path = raw_dir / "air_quality_uci.zip"
    last_error: Exception | None = None
    for url in UCI_URLS:
        try:
            with httpx.stream("GET", url, follow_redirects=True, timeout=90) as response:
                response.raise_for_status()
                with zip_path.open("wb") as handle:
                    for chunk in response.iter_bytes():
                        handle.write(chunk)
            with ZipFile(zip_path) as archive:
                archive.extractall(target_dir)
            expected = target_dir / "AirQualityUCI.csv"
            if expected.exists():
                return expected
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not download UCI Air Quality dataset: {last_error}")


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="EcoTwin-FM dataset manager")
    parser.add_argument("command", choices=["status", "download-uci"])
    args = parser.parse_args()
    if args.command == "status":
        print(json.dumps(dataset_status(), indent=2))
    elif args.command == "download-uci":
        print(download_uci())


if __name__ == "__main__":
    main()
