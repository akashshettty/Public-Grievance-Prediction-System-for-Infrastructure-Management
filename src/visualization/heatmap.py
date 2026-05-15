from __future__ import annotations

from pathlib import Path

import folium
import pandas as pd
from folium.plugins import HeatMap


def create_complaint_heatmap_map(
    df: pd.DataFrame,
    map_title: str = "Public Grievance Heatmap",
) -> folium.Map:
    """Create a folium heatmap object from complaint latitude/longitude points."""
    required_cols = ["latitude", "longitude", "severity"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for heatmap: {missing}")

    work_df = df.copy()
    work_df["latitude"] = pd.to_numeric(work_df["latitude"], errors="coerce")
    work_df["longitude"] = pd.to_numeric(work_df["longitude"], errors="coerce")
    work_df["severity"] = pd.to_numeric(work_df["severity"], errors="coerce")

    work_df = work_df.dropna(subset=["latitude", "longitude", "severity"])
    if work_df.empty:
        raise ValueError("No valid geo points available after cleaning.")

    center_lat = work_df["latitude"].mean()
    center_lon = work_df["longitude"].mean()

    grievance_map = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="CartoDB positron")

    heat_data = work_df[["latitude", "longitude", "severity"]].values.tolist()
    HeatMap(
        heat_data,
        min_opacity=0.35,
        radius=20,
        blur=16,
        max_zoom=14,
    ).add_to(grievance_map)

    folium.Marker(
        location=[center_lat, center_lon],
        popup="Map center",
        tooltip=map_title,
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(grievance_map)

    return grievance_map


def build_complaint_heatmap(
    df: pd.DataFrame,
    output_path: Path,
    map_title: str = "Public Grievance Heatmap",
) -> Path:
    """Build and save a folium heatmap from complaint latitude/longitude points."""
    grievance_map = create_complaint_heatmap_map(df=df, map_title=map_title)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    grievance_map.save(str(output_path))
    return output_path
