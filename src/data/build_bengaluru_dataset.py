from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALIGNED_DIR = PROJECT_ROOT / "data" / "processed" / "aligned"
GEOJSON_PATH = PROJECT_ROOT / "BBMP.geojson"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "bengaluru_master.csv"


def normalize_text(value: str) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[\.,/()\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_ward_centroids(geojson_path: Path) -> dict[str, dict[str, float | str]]:
    """Compute a simple centroid for each BBMP ward polygon."""
    with geojson_path.open("r", encoding="utf-8") as file:
        geojson_data = json.load(file)

    centroids: dict[str, dict[str, float | str]] = {}

    for feature in geojson_data.get("features", []):
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        ward_name = properties.get("KGISWardName")
        if not ward_name:
            continue

        coordinates = geometry.get("coordinates", [])
        points: list[tuple[float, float]] = []

        if geometry.get("type") == "Polygon" and coordinates:
            for ring in coordinates:
                for lon, lat in ring:
                    points.append((float(lat), float(lon)))
        elif geometry.get("type") == "MultiPolygon" and coordinates:
            for polygon in coordinates:
                for ring in polygon:
                    for lon, lat in ring:
                        points.append((float(lat), float(lon)))

        if not points:
            continue

        centroid_lat = sum(lat for lat, _ in points) / len(points)
        centroid_lon = sum(lon for _, lon in points) / len(points)

        centroids[normalize_text(ward_name)] = {
            "kgis_ward_name": ward_name,
            "latitude": round(centroid_lat, 6),
            "longitude": round(centroid_lon, 6),
            "kgis_ward_no": properties.get("KGISWardNo"),
            "kgis_ward_code": properties.get("KGISWardCode"),
            "kgis_ward_id": properties.get("KGISWardID"),
        }

    return centroids


def infer_severity(category: str, sub_category: str) -> int:
    """Simple explainable severity rule for complaint prioritization."""
    text = f"{category} {sub_category}".lower()

    if any(keyword in text for keyword in ["road", "pothole", "footpath", "drain", "sewer", "water"]):
        return 5
    if any(keyword in text for keyword in ["street light", "electrical", "power"]):
        return 4
    if any(keyword in text for keyword in ["garbage", "solid waste", "sweeping", "sanitation"]):
        return 3
    if any(keyword in text for keyword in ["tree", "forest", "animal", "veterinary"]):
        return 2
    if any(keyword in text for keyword in ["revenue", "khata", "advertisement"]):
        return 2
    return 3


def build_master_dataset() -> pd.DataFrame:
    if not GEOJSON_PATH.exists():
        raise FileNotFoundError(f"BBMP geojson not found: {GEOJSON_PATH}")

    if not ALIGNED_DIR.exists():
        raise FileNotFoundError(f"Aligned complaint directory not found: {ALIGNED_DIR}")

    aligned_files = sorted(ALIGNED_DIR.glob("*_aligned.csv"))
    if not aligned_files:
        raise FileNotFoundError(
            f"No aligned complaint files found in: {ALIGNED_DIR}. Run align_wards.py first."
        )

    centroids = load_ward_centroids(GEOJSON_PATH)
    master_rows: list[dict[str, object]] = []

    for csv_path in aligned_files:
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            raw_area_key = row.get("kgis_ward_name")
            if pd.isna(raw_area_key):
                continue

            area_key = normalize_text(raw_area_key)
            centroid = centroids.get(area_key)
            if centroid is None:
                continue

            category = str(row.get("Category", "")).strip()
            sub_category = str(row.get("Sub Category", "")).strip()
            grievance_date = pd.to_datetime(row.get("Grievance Date"), errors="coerce")
            complaint_id = row.get("Complaint ID")
            status = str(row.get("Grievance Status", "")).strip()

            master_rows.append(
                {
                    "complaint_id": complaint_id,
                    "timestamp": grievance_date,
                    "issue_type": sub_category if sub_category else category,
                    "category": category,
                    "sub_category": sub_category,
                    "area": centroid["kgis_ward_name"],
                    "ward_raw": row.get("ward_raw", row.get("Ward Name")),
                    "kgis_ward_name": centroid["kgis_ward_name"],
                    "ward_match_method": row.get("ward_match_method"),
                    "ward_match_score": row.get("ward_match_score"),
                    "latitude": centroid["latitude"],
                    "longitude": centroid["longitude"],
                    "kgis_ward_no": centroid["kgis_ward_no"],
                    "kgis_ward_code": centroid["kgis_ward_code"],
                    "kgis_ward_id": centroid["kgis_ward_id"],
                    "status": status,
                    "severity": infer_severity(category, sub_category),
                    "source_file": csv_path.name,
                    "staff_remarks": row.get("Staff Remarks"),
                    "staff_name": row.get("Staff Name"),
                }
            )

    master_df = pd.DataFrame(master_rows)
    if master_df.empty:
        raise ValueError("No rows were produced while building the Bengaluru master dataset.")

    master_df = master_df.dropna(subset=["timestamp", "area", "latitude", "longitude"])
    master_df = master_df.drop_duplicates(subset=["complaint_id"], keep="last")
    master_df = master_df.sort_values("timestamp").reset_index(drop=True)

    master_df["year"] = master_df["timestamp"].dt.year
    master_df["month"] = master_df["timestamp"].dt.month
    master_df["day"] = master_df["timestamp"].dt.day
    master_df["day_of_week"] = master_df["timestamp"].dt.day_name()
    master_df["hour"] = master_df["timestamp"].dt.hour

    return master_df


def main() -> None:
    master_df = build_master_dataset()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    master_df.to_csv(OUTPUT_PATH, index=False)

    print("Bengaluru master dataset saved to:", OUTPUT_PATH)
    print("Rows:", len(master_df))
    print("Unique wards:", master_df["area"].nunique())
    print("Date range:", master_df["timestamp"].min(), "to", master_df["timestamp"].max())


if __name__ == "__main__":
    main()