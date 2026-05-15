from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


FEATURE_COLUMNS = [
    "complaint_count",
    "avg_severity",
    "open_ratio",
    "weekly_trend_ratio",
    "recurrence_ratio",
]


def _prepare_base_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    work_df = df.copy()
    work_df["timestamp"] = pd.to_datetime(work_df["timestamp"], errors="coerce")
    work_df = work_df.dropna(subset=["timestamp", "area"])
    work_df["is_open"] = work_df["status"].str.lower().eq("open").astype(int)
    work_df["date"] = work_df["timestamp"].dt.floor("D")
    return work_df


def _build_area_window_features(window_df: pd.DataFrame) -> pd.DataFrame:
    if window_df.empty:
        return pd.DataFrame(columns=["area", *FEATURE_COLUMNS, "center_latitude", "center_longitude"])

    issue_counts = window_df.groupby(["area", "issue_type"]).size().rename("issue_count")
    recurring_issues = issue_counts[issue_counts > 1].groupby("area").size().rename(
        "recurring_issue_types"
    )

    max_date = window_df["timestamp"].max()
    last_7_start = max_date - pd.Timedelta(days=7)

    features = window_df.groupby("area", as_index=False).agg(
        complaint_count=("area", "size"),
        avg_severity=("severity", "mean"),
        open_count=("is_open", "sum"),
        unique_issue_types=("issue_type", "nunique"),
        center_latitude=("latitude", "mean"),
        center_longitude=("longitude", "mean"),
    )

    recent_counts = (
        window_df[window_df["timestamp"] >= last_7_start]
        .groupby("area")
        .size()
        .rename("last_7_day_count")
    )

    features = features.set_index("area")
    features = features.join(recent_counts, how="left")
    features = features.join(recurring_issues, how="left")
    features = features.fillna(0).reset_index()

    features["open_ratio"] = features["open_count"] / features["complaint_count"].replace(0, 1)
    features["weekly_trend_ratio"] = (
        features["last_7_day_count"] / features["complaint_count"].replace(0, 1)
    )
    features["recurrence_ratio"] = (
        features["recurring_issue_types"] / features["unique_issue_types"].replace(0, 1)
    )

    return features[["area", *FEATURE_COLUMNS, "center_latitude", "center_longitude"]]


def build_training_dataset(
    df: pd.DataFrame,
    lookback_days: int = 30,
    forecast_horizon_days: int = 7,
) -> tuple[pd.DataFrame, int]:
    """Create area-window samples with future hotspot labels."""
    work_df = _prepare_base_dataframe(df)
    if work_df.empty:
        return pd.DataFrame(), 1

    min_day = work_df["date"].min()
    max_day = work_df["date"].max()
    start_day = min_day + pd.Timedelta(days=lookback_days)
    end_day = max_day - pd.Timedelta(days=forecast_horizon_days)

    snapshot_days = pd.date_range(start=start_day, end=end_day, freq="D")
    training_rows: list[pd.DataFrame] = []

    for snapshot_day in snapshot_days:
        history_start = snapshot_day - pd.Timedelta(days=lookback_days)
        history_mask = (work_df["timestamp"] > history_start) & (work_df["timestamp"] <= snapshot_day)
        future_end = snapshot_day + pd.Timedelta(days=forecast_horizon_days)
        future_mask = (work_df["timestamp"] > snapshot_day) & (work_df["timestamp"] <= future_end)

        history_df = work_df[history_mask]
        future_df = work_df[future_mask]
        if history_df.empty:
            continue

        history_features = _build_area_window_features(history_df)
        future_counts = future_df.groupby("area").size().rename("future_count")

        sample_df = history_features.set_index("area")
        sample_df = sample_df.join(future_counts, how="left").fillna(0).reset_index()
        sample_df["snapshot_day"] = snapshot_day
        training_rows.append(sample_df)

    if not training_rows:
        return pd.DataFrame(), 1

    training_df = pd.concat(training_rows, ignore_index=True)
    hotspot_threshold = max(1, int(np.ceil(training_df["future_count"].quantile(0.75))))
    training_df["hotspot_label"] = (training_df["future_count"] >= hotspot_threshold).astype(int)

    return training_df, hotspot_threshold


def train_hotspot_model(
    training_df: pd.DataFrame,
) -> tuple[RandomForestClassifier | None, dict[str, float | str]]:
    """Train Random Forest to predict hotspot probability."""
    if training_df.empty:
        return None, {"status": "no_training_data"}

    if training_df["hotspot_label"].nunique() < 2:
        return None, {"status": "single_class_data"}

    X = training_df[FEATURE_COLUMNS]
    y = training_df["hotspot_label"]

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.3,
            random_state=42,
            stratify=y,
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.3,
            random_state=42,
        )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    accuracy = float(model.score(X_test, y_test)) if len(X_test) > 0 else 0.0
    metrics = {
        "status": "trained",
        "train_rows": float(len(X_train)),
        "test_rows": float(len(X_test)),
        "test_accuracy": round(accuracy, 4),
    }

    return model, metrics


def _heuristic_probability(features_df: pd.DataFrame) -> pd.Series:
    max_count = max(float(features_df["complaint_count"].max()), 1.0)
    scaled_count = features_df["complaint_count"] / max_count
    scaled_severity = features_df["avg_severity"] / 5.0
    score = 0.5 * scaled_count + 0.3 * features_df["open_ratio"] + 0.2 * scaled_severity
    return score.clip(0, 1)


def predict_future_hotspots(
    df: pd.DataFrame,
    model: RandomForestClassifier | None,
    hotspot_threshold: int,
    lookback_days: int = 30,
) -> pd.DataFrame:
    """Predict next-period hotspot probability per area using latest history window."""
    work_df = _prepare_base_dataframe(df)
    if work_df.empty:
        return pd.DataFrame()

    latest_day = work_df["date"].max()
    history_start = latest_day - pd.Timedelta(days=lookback_days)
    latest_history = work_df[(work_df["timestamp"] > history_start) & (work_df["timestamp"] <= latest_day)]

    latest_features = _build_area_window_features(latest_history)
    if latest_features.empty:
        return pd.DataFrame()

    if model is not None:
        probability = model.predict_proba(latest_features[FEATURE_COLUMNS])[:, 1]
    else:
        probability = _heuristic_probability(latest_features)

    prediction_df = latest_features.copy()
    prediction_df["hotspot_probability"] = np.round(probability * 100, 2)
    prediction_df["predicted_hotspot"] = (prediction_df["hotspot_probability"] >= 50).astype(int)
    prediction_df["model_threshold_count"] = hotspot_threshold

    return prediction_df.sort_values("hotspot_probability", ascending=False).reset_index(drop=True)
