from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
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
        raise ValueError(f"Missing required columns for feature engineering: {missing}")


def build_area_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create area-level features used for risk scoring and prediction."""
    _validate_columns(df)

    work_df = df.copy()
    work_df["timestamp"] = pd.to_datetime(work_df["timestamp"], errors="coerce")
    work_df = work_df.dropna(subset=["timestamp", "area"])

    work_df["is_open"] = work_df["status"].str.lower().eq("open").astype(int)
    work_df["date"] = work_df["timestamp"].dt.date

    max_date = work_df["timestamp"].max()
    last_7_day_start = max_date - pd.Timedelta(days=7)
    last_30_day_start = max_date - pd.Timedelta(days=30)

    base_features = work_df.groupby("area", as_index=False).agg(
        complaint_count=("area", "size"),
        avg_severity=("severity", "mean"),
        open_complaint_count=("is_open", "sum"),
        unique_issue_types=("issue_type", "nunique"),
        active_days=("date", "nunique"),
        center_latitude=("latitude", "mean"),
        center_longitude=("longitude", "mean"),
    )

    last_7_counts = (
        work_df[work_df["timestamp"] >= last_7_day_start]
        .groupby("area")
        .size()
        .rename("last_7_day_count")
    )

    last_30_counts = (
        work_df[work_df["timestamp"] >= last_30_day_start]
        .groupby("area")
        .size()
        .rename("last_30_day_count")
    )

    issue_counts = work_df.groupby(["area", "issue_type"]).size().rename("issue_count")
    recurring_issues = issue_counts[issue_counts > 1].groupby("area").size().rename(
        "recurring_issue_types"
    )

    area_features = base_features.set_index("area")
    area_features = area_features.join(last_7_counts, how="left")
    area_features = area_features.join(last_30_counts, how="left")
    area_features = area_features.join(recurring_issues, how="left")
    area_features = area_features.fillna(0).reset_index()

    area_features["open_ratio"] = (
        area_features["open_complaint_count"] / area_features["complaint_count"]
    )
    area_features["complaints_per_active_day"] = (
        area_features["complaint_count"] / area_features["active_days"]
    )
    area_features["weekly_trend_ratio"] = (
        area_features["last_7_day_count"]
        / area_features["last_30_day_count"].replace(0, 1)
    )
    area_features["recurrence_ratio"] = (
        area_features["recurring_issue_types"]
        / area_features["unique_issue_types"].replace(0, 1)
    )

    numeric_cols = [
        "avg_severity",
        "open_ratio",
        "complaints_per_active_day",
        "weekly_trend_ratio",
        "recurrence_ratio",
    ]
    area_features[numeric_cols] = area_features[numeric_cols].round(3)

    return area_features
