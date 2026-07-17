from pathlib import Path

from config.settings import get_settings
from data.ingestion.uci_loader import load_uci_air_quality
from database.db_connection import SessionLocal
from database.repositories import insert_readings
from database.seed import init_db


def load_uci_to_database(limit: int | None = None) -> int:
    settings = get_settings()
    path = Path(settings.uci_air_quality_path)
    if not path.exists():
        raise FileNotFoundError(f"UCI file not found at {path}. Run: python -m data.dataset_manager download-uci")
    frame = load_uci_air_quality(path)
    if limit:
        frame = frame.tail(limit)
    rows = frame.where(frame.notna(), None).to_dict(orient="records")
    init_db()
    with SessionLocal() as db:
        return insert_readings(db, rows)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load EcoTwin datasets into the configured database")
    parser.add_argument("--uci", action="store_true", help="Load UCI Air Quality rows")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    if args.uci:
        print(load_uci_to_database(limit=args.limit))
