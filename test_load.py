import pandas as pd
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "grievances_cleaned.csv"

print(f"Checking {CLEAN_DATA_PATH}...")
if CLEAN_DATA_PATH.exists():
    print("File exists. Loading...")
    df = pd.read_csv(CLEAN_DATA_PATH)
    print(f"Loaded {len(df)} rows.")
    print("Columns:", df.columns.tolist())
else:
    print("File does not exist!")
