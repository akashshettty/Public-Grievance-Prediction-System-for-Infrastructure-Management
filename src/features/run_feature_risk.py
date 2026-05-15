from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.features.feature_engineering import build_area_features
from src.models.risk_scoring import calculate_area_risk_scores


INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "grievances_cleaned.csv"
FEATURE_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "area_features.csv"
RISK_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "area_risk_scores.csv"


def main() -> None:
    df = pd.read_csv(INPUT_PATH)

    area_features = build_area_features(df)
    area_risk_scores = calculate_area_risk_scores(area_features)

    area_features.to_csv(FEATURE_OUTPUT_PATH, index=False)
    area_risk_scores.to_csv(RISK_OUTPUT_PATH, index=False)

    print("Input records:", len(df))
    print("Areas found:", area_features["area"].nunique())
    print("Saved features to:", FEATURE_OUTPUT_PATH)
    print("Saved risk scores to:", RISK_OUTPUT_PATH)
    print("Top risk areas:")
    print(area_risk_scores[["area", "risk_score", "risk_level"]].head(5).to_string(index=False))


if __name__ == "__main__":
    main()
