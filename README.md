# EcoTwin-FM

EcoTwin-FM is a production-oriented MVP for a foundation-model-ready smart city environmental digital twin. It ingests environmental data, forecasts air quality, temperature, and energy demand, shows a city dashboard, simulates policy scenarios, raises WHO-threshold alerts, and answers natural-language planning questions.

## What works now

- FastAPI backend with health, sensors, predictions, alerts, simulation, and assistant endpoints.
- React dashboard with Leaflet map, KPI cards, prediction charts, scenario controls, alerts, and assistant query box.
- PostgreSQL/PostGIS schema for readings, forecasts, simulations, and alerts.
- OpenAQ integration hook with deterministic demo-data fallback when no API key is configured.
- Dataset manager for UCI Air Quality, OpenAQ readiness, and WeatherBench/ERA5 local files.
- Preprocessing utilities for cleaning, timestamp alignment, lag features, normalization, and chronological splitting.
- Lightweight forecasting engine with the same interface expected from a future LSTM, TCN, Transformer, or graph model.
- Dataset-backed Random Forest training pipeline using UCI Air Quality and optional WeatherBench weather joins.
- Docker Compose for backend, dashboard, and PostGIS.
- Focused tests for the API, forecasting, and preprocessing.

## Run locally without Docker

```bash
cd ecotwin-fm
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

In another terminal:

```bash
cd ecotwin-fm/dashboard
npm install
npm run dev
```

Open `http://localhost:5173`.

## Run with Docker Compose

```bash
cd ecotwin-fm
copy .env.example .env
docker compose up --build
```

The API runs on `http://localhost:8000`; the dashboard runs on `http://localhost:5173`.

## API highlights

- `GET /api/health`
- `GET /api/datasets/status`
- `POST /api/datasets/download/uci`
- `GET /api/sensors?city=Delhi`
- `GET /api/sensors/history?city=UCI-Italian-City&limit=250`
- `GET /api/predictions?city=Delhi&horizon_hours=72`
- `GET /api/alerts?city=Delhi`
- `POST /api/simulation`
- `POST /api/assistant`

## Dataset setup

The problem statement names OpenAQ, WeatherBench ERA5, and UCI Air Quality. EcoTwin-FM now has explicit support for all three.

### UCI Air Quality

This dataset is small enough to download directly:

```bash
python -m data.dataset_manager download-uci
python -m models.train_from_datasets
python -m data.load_to_database --uci
```

The downloaded file belongs at:

```text
data/raw/uci_air_quality/AirQualityUCI.csv
```

UCI contains CO, NO2, NOx, benzene, temperature, humidity, and O3 sensor response. It does not directly contain PM2.5 or PM10, so the current trainer creates documented PM proxy targets until OpenAQ historical PM records are added.

### OpenAQ

Create `.env` from `.env.example`, then set:

```text
OPENAQ_API_KEY=your_key_here
```

The app will use OpenAQ for live/recent PM2.5, PM10, NO2, O3, CO, and SO2. Without the key, the dashboard still works using deterministic demo data.

### WeatherBench / ERA5

WeatherBench/ERA5 is much larger than the UCI dataset and is often distributed as NetCDF or Zarr. Put one of these into:

```text
data/raw/weatherbench/
```

Supported forms:

- CSV export with columns like `timestamp`, `city`, `temperature`, `humidity`, `wind_speed`, `pressure`, `precipitation`
- NetCDF file: `.nc`
- Zarr store: `.zarr`

For NetCDF support, install the full requirements:

```bash
pip install -r requirements.txt
```

For Zarr stores, additionally install Zarr in your own Python environment:

```bash
pip install zarr
```

Then rerun:

```bash
python -m data.dataset_manager status
python -m models.train_from_datasets
```

## Next upgrades

- Replace the statistical forecaster with a trained temporal model in `models/model.py`.
- Store fetched OpenAQ records through SQLAlchemy repositories.
- Expand WeatherBench regridding from city-level joins to 1km spatial interpolation.
- Add map heat overlays from gridded forecast output.
- Add authentication and role-based dashboard access for real deployments.
