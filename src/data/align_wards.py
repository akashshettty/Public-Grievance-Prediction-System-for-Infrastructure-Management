from __future__ import annotations

import json
import re
from difflib import get_close_matches
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GEOJSON_PATH = PROJECT_ROOT / "BBMP.geojson"
ALIAS_PATH = PROJECT_ROOT / "config" / "bbmp_ward_aliases.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "aligned"
REPORT_PATH = PROJECT_ROOT / "data" / "processed" / "ward_alignment_report.csv"
UNMATCHED_PATH = PROJECT_ROOT / "data" / "processed" / "ward_alignment_unmatched.csv"


def normalize_ward_name(value: str) -> str:
    """Normalize ward names so CSV names and geojson names can be matched reliably."""
    text = str(value).strip().lower()
    text = re.sub(r"[\.,/()\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(" ward", "")
    text = text.replace("nagara", "nagar")
    return text


def load_geojson_wards(geojson_path: Path) -> tuple[list[str], dict[str, str]]:
    with geojson_path.open("r", encoding="utf-8") as file:
        geojson_data = json.load(file)

    ward_names: list[str] = []
    lookup: dict[str, str] = {}

    for feature in geojson_data.get("features", []):
        properties = feature.get("properties", {})
        ward_name = properties.get("KGISWardName")
        if not ward_name:
            continue
        ward_name = str(ward_name).strip()
        ward_names.append(ward_name)
        lookup[normalize_ward_name(ward_name)] = ward_name

    return ward_names, lookup


def load_aliases(alias_path: Path, lookup: dict[str, str]) -> dict[str, str]:
    """Load optional manual aliases for Bengaluru ward-name variants."""
    alias_lookup: dict[str, str] = {}

    if not alias_path.exists():
        return alias_lookup

    alias_df = pd.read_csv(alias_path)
    required_cols = {"ward_raw", "kgis_ward_name"}
    missing_cols = required_cols - set(alias_df.columns)
    if missing_cols:
        raise ValueError(f"Alias file is missing columns: {sorted(missing_cols)}")

    valid_targets = set(lookup.values())
    for _, row in alias_df.iterrows():
        raw_name = str(row["ward_raw"]).strip()
        target_name = str(row["kgis_ward_name"]).strip()
        if not raw_name or not target_name:
            continue
        if target_name not in valid_targets:
            raise ValueError(
                f"Alias target '{target_name}' does not exist in BBMP.geojson"
            )
        alias_lookup[normalize_ward_name(raw_name)] = target_name

    return alias_lookup


def detect_ward_column(df: pd.DataFrame) -> str:
    candidate_columns = ["Ward Name", "ward_name", "ward", "WARD NAME", "Ward"]
    for column in candidate_columns:
        if column in df.columns:
            return column
    raise ValueError(f"Could not find a ward column in columns: {list(df.columns)}")


def map_ward_name(
    ward_value: str,
    lookup: dict[str, str],
    canonical_keys: list[str],
    alias_lookup: dict[str, str],
) -> tuple[str | None, str, float]:
    normalized_value = normalize_ward_name(ward_value)

    if normalized_value in alias_lookup:
        return alias_lookup[normalized_value], "alias", 1.0

    if normalized_value in lookup:
        return lookup[normalized_value], "exact", 1.0

    close_matches = get_close_matches(normalized_value, canonical_keys, n=1, cutoff=0.82)
    if close_matches:
        best_key = close_matches[0]
        return lookup[best_key], "fuzzy", 0.0

    return None, "unmatched", 0.0


def align_complaint_file(
    csv_path: Path,
    lookup: dict[str, str],
    canonical_keys: list[str],
    alias_lookup: dict[str, str],
) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    ward_column = detect_ward_column(df)

    aligned_rows = []
    for _, row in df.iterrows():
        raw_ward = row[ward_column]
        kgis_ward_name, match_method, match_score = map_ward_name(
            raw_ward,
            lookup,
            canonical_keys,
            alias_lookup,
        )

        aligned_row = row.to_dict()
        aligned_row["ward_raw"] = raw_ward
        aligned_row["ward_key"] = normalize_ward_name(raw_ward)
        aligned_row["kgis_ward_name"] = kgis_ward_name
        aligned_row["ward_match_method"] = match_method
        aligned_row["ward_match_score"] = match_score
        aligned_rows.append(aligned_row)

    return pd.DataFrame(aligned_rows)


def main() -> None:
    if not GEOJSON_PATH.exists():
        raise FileNotFoundError(f"Geojson not found: {GEOJSON_PATH}")

    ward_names, lookup = load_geojson_wards(GEOJSON_PATH)
    canonical_keys = list(lookup.keys())
    alias_lookup = load_aliases(ALIAS_PATH, lookup)

    complaint_files = sorted(
        path
        for path in PROJECT_ROOT.glob("*.csv")
        if path.name not in {"ward_alignment_report.csv"} and path.stem.isdigit()
    )

    if not complaint_files:
        print("No year-based complaint CSV files found in the project root.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report_rows = []
    unmatched_rows = []

    for csv_path in complaint_files:
        aligned_df = align_complaint_file(csv_path, lookup, canonical_keys, alias_lookup)
        output_path = OUTPUT_DIR / f"{csv_path.stem}_aligned.csv"
        aligned_df.to_csv(output_path, index=False)

        ward_column = detect_ward_column(pd.read_csv(csv_path, nrows=1))
        unique_raw_wards = pd.read_csv(csv_path, usecols=[ward_column])[ward_column].dropna().astype(str).unique()
        matched_wards = aligned_df[aligned_df["kgis_ward_name"].notna()]["ward_raw"].nunique()
        unmatched_wards = aligned_df[aligned_df["kgis_ward_name"].isna()]["ward_raw"].nunique()

        report_rows.append(
            {
                "file": csv_path.name,
                "rows": int(len(aligned_df)),
                "unique_ward_names": int(len(unique_raw_wards)),
                "matched_unique_ward_names": int(matched_wards),
                "unmatched_unique_ward_names": int(unmatched_wards),
                "output_file": str(output_path),
            }
        )

        unmatched_df = (
            aligned_df[aligned_df["kgis_ward_name"].isna()]
            .groupby("ward_raw", as_index=False)
            .size()
            .rename(columns={"size": "count"})
        )
        if not unmatched_df.empty:
            unmatched_df["file"] = csv_path.name
            unmatched_rows.append(unmatched_df)

    report_df = pd.DataFrame(report_rows)
    report_df.to_csv(REPORT_PATH, index=False)

    if unmatched_rows:
        pd.concat(unmatched_rows, ignore_index=True).to_csv(UNMATCHED_PATH, index=False)

    print("Aligned files saved to:", OUTPUT_DIR)
    print("Alignment report saved to:", REPORT_PATH)
    if unmatched_rows:
        print("Unmatched ward review saved to:", UNMATCHED_PATH)
    print("Known BBMP wards loaded:", len(ward_names))
    print("Loaded manual aliases:", len(alias_lookup))
    print(report_df.to_string(index=False))


if __name__ == "__main__":
    main()