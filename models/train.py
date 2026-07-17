from pathlib import Path

import joblib

from models.model import EcoTwinForecaster


def train_placeholder(output_dir: str = "models/saved") -> Path:
    """Persist the MVP forecaster interface.

    Replace this function with an LSTM/TCN/Transformer training loop once a
    curated historical dataset is available.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    model_path = out / "model.joblib"
    joblib.dump(EcoTwinForecaster(), model_path)
    return model_path


if __name__ == "__main__":
    print(train_placeholder())
