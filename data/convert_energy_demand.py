from pathlib import Path

from data.ingestion.energy_loader import convert_energy_xlsx_folder


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    output = convert_energy_xlsx_folder(
        source_dir=project / "data/raw/energy/source_xlsx",
        output_path=project / "data/raw/energy/energy_demand.csv",
        cities_path=project / "data/raw/cities/india_cities.csv",
    )
    print(output)


if __name__ == "__main__":
    main()
