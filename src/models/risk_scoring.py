from __future__ import annotations

import pandas as pd


DEFAULT_WEIGHTS = {
    "complaint_count": 0.35,
    "avg_severity": 0.25,
    "open_ratio": 0.20,
    "weekly_trend_ratio": 0.20,
}


def _normalize_to_100(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()

    if pd.isna(min_val) or pd.isna(max_val):
        return pd.Series([0.0] * len(series), index=series.index)

    if max_val == min_val:
        return pd.Series([50.0] * len(series), index=series.index)

    return ((series - min_val) / (max_val - min_val)) * 100


def calculate_area_risk_scores(
    area_features: pd.DataFrame,
    weights: dict[str, float] | None = None,
) -> pd.DataFrame:
    """Calculate explainable risk scores in the range 0-100."""
    use_weights = weights or DEFAULT_WEIGHTS

    required_cols = list(use_weights.keys())
    missing = [col for col in required_cols if col not in area_features.columns]
    if missing:
        raise ValueError(f"Missing columns required for risk scoring: {missing}")

    score_df = area_features.copy()

    normalized_cols = []
    for col in required_cols:
        normalized_col = f"norm_{col}"
        score_df[normalized_col] = _normalize_to_100(score_df[col].astype(float))
        normalized_cols.append(normalized_col)

    score_df["risk_score"] = 0.0
    for feature_name, weight in use_weights.items():
        score_df["risk_score"] += score_df[f"norm_{feature_name}"] * weight

    score_df["risk_score"] = score_df["risk_score"].clip(0, 100).round(2)

    score_df["risk_level"] = pd.cut(
        score_df["risk_score"],
        bins=[-1, 35, 70, 100],
        labels=["Low", "Medium", "High"],
    )

    ordered_cols = [
        "area",
        "risk_score",
        "risk_level",
        "complaint_count",
        "avg_severity",
        "open_ratio",
        "weekly_trend_ratio",
        "norm_complaint_count",
        "norm_avg_severity",
        "norm_open_ratio",
        "norm_weekly_trend_ratio",
    ]

    available_ordered_cols = [col for col in ordered_cols if col in score_df.columns]
    remaining_cols = [col for col in score_df.columns if col not in available_ordered_cols]

    return score_df[available_ordered_cols + remaining_cols].sort_values(
        "risk_score", ascending=False
    ).reset_index(drop=True)
