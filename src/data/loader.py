from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MASTER_DATA_PATH = PROCESSED_DATA_DIR / "bengaluru_master.csv"


def load_grievance_data(file_name: str = "grievances_sample.csv") -> pd.DataFrame:
    """Load grievance data, preferring the Bengaluru master dataset when available."""
    if MASTER_DATA_PATH.exists():
        file_path = MASTER_DATA_PATH
    else:
        file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    return pd.read_csv(file_path)


def save_processed_data(df: pd.DataFrame, file_name: str = "grievances_cleaned.csv") -> Path:
    """Save cleaned data to the processed data folder and return output path."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / file_name
    df.to_csv(output_path, index=False)
    return output_path
