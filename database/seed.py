from database.db_connection import Base, engine
from database.models import Alert, EnvironmentalReading, PredictionResult, SimulationOutput


def init_db() -> None:
    _ = (Alert, EnvironmentalReading, PredictionResult, SimulationOutput)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
