from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.visualization.heatmap import create_complaint_heatmap_map


CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "grievances_cleaned.csv"
RISK_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "area_risk_scores.csv"
HOTSPOT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "hotspot_predictions.csv"


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def _build_recommendations(
    filtered_df: pd.DataFrame,
    risk_df: pd.DataFrame,
    hotspot_df: pd.DataFrame,
) -> list[str]:
    recommendations: list[str] = []

    if filtered_df.empty:
        return ["No data available for recommendation in the selected filters."]

    open_ratio = 0.0
    if "status" in filtered_df.columns and len(filtered_df) > 0:
        open_ratio = (filtered_df["status"].astype(str).str.lower() == "open").mean()

    if not risk_df.empty:
        high_risk_count = int((risk_df["risk_level"].astype(str) == "High").sum())
        if high_risk_count > 0:
            recommendations.append(
                f"Prioritize field action in high-risk areas first (count: {high_risk_count})."
            )

    if not hotspot_df.empty:
        top_hotspots = hotspot_df.head(3)["area"].tolist()
        if top_hotspots:
            recommendations.append(
                "Plan preventive inspections for top predicted hotspots: "
                + ", ".join(top_hotspots)
                + "."
            )

    if open_ratio >= 0.6:
        recommendations.append(
            "Open complaint ratio is high. Increase resolution teams and close old pending issues."
        )

    issue_counts = filtered_df["issue_type"].value_counts()
    if not issue_counts.empty:
        top_issue = issue_counts.index[0]
        recommendations.append(
            f"Most frequent issue is '{top_issue}'. Run a focused mitigation drive for this issue type."
        )

    if not recommendations:
        recommendations.append("Current indicators are stable. Continue regular monitoring and weekly review.")

    return recommendations


def main() -> None:
    st.set_page_config(
        page_title="AI-Driven Infrastructure Risk Dashboard",
        layout="wide",
    )

    st.title("AI-Driven Infrastructure Risk Prediction")
    st.caption("Public grievance analytics: heatmap, risk score, and hotspot prediction")

    clean_df = load_csv(CLEAN_DATA_PATH)
    risk_df = load_csv(RISK_DATA_PATH)
    hotspot_df = load_csv(HOTSPOT_DATA_PATH)

    if clean_df.empty:
        st.error("Cleaned data file is missing. Please run preprocessing first.")
        st.stop()

    clean_df["timestamp"] = pd.to_datetime(clean_df["timestamp"], errors="coerce")
    clean_df = clean_df.dropna(subset=["timestamp", "area", "issue_type"])

    st.sidebar.header("Filters")

    min_date = clean_df["timestamp"].min().date()
    max_date = clean_df["timestamp"].max().date()
    selected_dates = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = min_date
        end_date = max_date

    all_issues = sorted(clean_df["issue_type"].dropna().unique().tolist())
    selected_issues = st.sidebar.multiselect(
        "Issue type",
        options=all_issues,
        default=all_issues,
    )

    all_areas = sorted(clean_df["area"].dropna().unique().tolist())
    selected_areas = st.sidebar.multiselect(
        "Area",
        options=all_areas,
        default=all_areas,
    )

    mask = (
        clean_df["timestamp"].dt.date.between(start_date, end_date)
        & clean_df["issue_type"].isin(selected_issues)
        & clean_df["area"].isin(selected_areas)
    )
    filtered_df = clean_df[mask].copy()

    filtered_risk_df = risk_df[risk_df["area"].isin(selected_areas)].copy() if not risk_df.empty else risk_df
    filtered_hotspot_df = (
        hotspot_df[hotspot_df["area"].isin(selected_areas)].copy() if not hotspot_df.empty else hotspot_df
    )

    st.sidebar.subheader("Export Filtered Data")
    st.sidebar.download_button(
        label="Download Complaints CSV",
        data=_to_csv_bytes(filtered_df),
        file_name="filtered_complaints.csv",
        mime="text/csv",
    )

    if not filtered_risk_df.empty:
        st.sidebar.download_button(
            label="Download Risk Scores CSV",
            data=_to_csv_bytes(filtered_risk_df),
            file_name="filtered_risk_scores.csv",
            mime="text/csv",
        )

    if not filtered_hotspot_df.empty:
        st.sidebar.download_button(
            label="Download Hotspots CSV",
            data=_to_csv_bytes(filtered_hotspot_df),
            file_name="filtered_hotspots.csv",
            mime="text/csv",
        )

    col1, col2, col3, col4 = st.columns(4)
    total_complaints = int(len(filtered_df))
    open_complaints = int((filtered_df["status"].astype(str).str.lower() == "open").sum())
    area_count = int(filtered_df["area"].nunique())
    avg_severity = float(filtered_df["severity"].mean()) if total_complaints > 0 else 0.0

    col1.metric("Total Complaints", total_complaints)
    col2.metric("Open Complaints", open_complaints)
    col3.metric("Areas in View", area_count)
    col4.metric("Average Severity", f"{avg_severity:.2f}")

    st.subheader("Geospatial Complaint Heatmap")
    if filtered_df.empty:
        st.warning("No records available for selected filters.")
    else:
        heatmap_map = create_complaint_heatmap_map(filtered_df)
        st.components.v1.html(heatmap_map._repr_html_(), height=520)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Complaints Over Time")
        if filtered_df.empty:
            st.info("No data to plot.")
        else:
            trend_df = (
                filtered_df.assign(date=filtered_df["timestamp"].dt.date)
                .groupby("date", as_index=False)
                .size()
                .rename(columns={"size": "complaint_count"})
            )
            trend_fig = px.line(
                trend_df,
                x="date",
                y="complaint_count",
                markers=True,
                title="Daily Complaint Trend",
            )
            st.plotly_chart(trend_fig, use_container_width=True)

    with right_col:
        st.subheader("Issue Type Distribution")
        if filtered_df.empty:
            st.info("No data to plot.")
        else:
            issue_df = (
                filtered_df.groupby("issue_type", as_index=False)
                .size()
                .rename(columns={"size": "count"})
                .sort_values("count", ascending=False)
            )
            issue_fig = px.bar(
                issue_df,
                x="issue_type",
                y="count",
                title="Complaints by Issue Type",
            )
            st.plotly_chart(issue_fig, use_container_width=True)

    st.subheader("Area-wise Risk Scores")
    if filtered_risk_df.empty:
        st.warning("Risk score file not found. Run risk scoring step first.")
    else:
        st.dataframe(
            filtered_risk_df.sort_values("risk_score", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("Future Hotspot Prediction")
    if filtered_hotspot_df.empty:
        st.warning("Hotspot prediction file not found. Run hotspot model step first.")
    else:
        st.dataframe(
            filtered_hotspot_df.sort_values("hotspot_probability", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("Basic Recommendations")
    recommendations = _build_recommendations(filtered_df, filtered_risk_df, filtered_hotspot_df)
    for idx, item in enumerate(recommendations, start=1):
        st.write(f"{idx}. {item}")


if __name__ == "__main__":
    main()
