from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.hotspot_model import (
    build_training_dataset,
    predict_future_hotspots,
    train_hotspot_model,
)


INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "grievances_cleaned.csv"
TRAINING_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "hotspot_training_data.csv"
PREDICTION_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "hotspot_predictions.csv"


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Cleaned input data not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    training_df, threshold = build_training_dataset(df)
    model, metrics = train_hotspot_model(training_df)
    predictions = predict_future_hotspots(df, model=model, hotspot_threshold=threshold)

    training_df.to_csv(TRAINING_OUTPUT_PATH, index=False)
    predictions.to_csv(PREDICTION_OUTPUT_PATH, index=False)

    print("Training rows:", len(training_df))
    print("Hotspot count threshold:", threshold)
    print("Training status:", metrics.get("status"))
    if "test_accuracy" in metrics:
        print("Test accuracy:", metrics["test_accuracy"])
    print("Saved training data to:", TRAINING_OUTPUT_PATH)
    print("Saved hotspot predictions to:", PREDICTION_OUTPUT_PATH)

    if not predictions.empty:
        print("Top predicted hotspot areas:")
        print(
            predictions[["area", "hotspot_probability", "predicted_hotspot"]]
            .head(5)
            .to_string(index=False)
        )


if __name__ == "__main__":
    main()
