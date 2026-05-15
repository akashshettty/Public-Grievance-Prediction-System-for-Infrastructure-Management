import pandas as pd


REQUIRED_COLUMNS = [
    "complaint_id",
    "timestamp",
    "issue_type",
    "area",
    "latitude",
    "longitude",
    "status",
    "severity",
]


def _validate_columns(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def preprocess_grievance_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich grievance data for downstream analysis."""
    _validate_columns(df)

    clean_df = df.copy()

    clean_df["timestamp"] = pd.to_datetime(clean_df["timestamp"], errors="coerce")

    text_columns = ["issue_type", "area", "status"]
    for col in text_columns:
        clean_df[col] = clean_df[col].astype(str).str.strip()

    clean_df["severity"] = pd.to_numeric(clean_df["severity"], errors="coerce")
    clean_df["severity"] = clean_df["severity"].clip(lower=1, upper=5)

    median_severity = clean_df["severity"].median()
    if pd.isna(median_severity):
        median_severity = 3
    clean_df["severity"] = clean_df["severity"].fillna(median_severity)

    clean_df["latitude"] = pd.to_numeric(clean_df["latitude"], errors="coerce")
    clean_df["longitude"] = pd.to_numeric(clean_df["longitude"], errors="coerce")

    clean_df = clean_df.dropna(
        subset=["timestamp", "issue_type", "area", "latitude", "longitude"]
    )

    clean_df = clean_df.drop_duplicates(subset=["complaint_id"], keep="last")

    clean_df["year"] = clean_df["timestamp"].dt.year
    clean_df["month"] = clean_df["timestamp"].dt.month
    clean_df["day"] = clean_df["timestamp"].dt.day
    clean_df["day_of_week"] = clean_df["timestamp"].dt.day_name()
    clean_df["hour"] = clean_df["timestamp"].dt.hour

    clean_df = clean_df.sort_values("timestamp").reset_index(drop=True)

    return clean_df
