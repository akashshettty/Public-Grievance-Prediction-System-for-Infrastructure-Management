from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.visualization.heatmap import build_complaint_heatmap


INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "grievances_cleaned.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "maps" / "complaint_heatmap.html"


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned data not found at {INPUT_PATH}. Run preprocessing first."
        )

    df = pd.read_csv(INPUT_PATH)
    output_file = build_complaint_heatmap(df=df, output_path=OUTPUT_PATH)

    print("Rows used:", len(df))
    print("Heatmap saved to:", output_file)


if __name__ == "__main__":
    main()
