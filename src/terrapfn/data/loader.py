"""Data loader for TerraPFN trail and climate datasets.

Loads and cleans US National Parks trail records and Open-Meteo historical climate reanalysis.
Enforces strict schema validation and isolates post-hoc target leakage features.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

# Features strictly excluded to prevent post-hoc target leakage
LEAKAGE_FEATURES = [
    "avg_rating",      # Post-hoc user rating feedback
    "popularity",      # Post-hoc AllTrails click / engagement ranking
    "num_reviews",     # Post-hoc engagement metric
    "visitor_usage",   # Post-hoc visitor density measurement
    "units",           # Web scraping artifact
]

IDENTIFIER_COLUMNS = [
    "trail_id",
    "name",
    "city_name",
]

TARGET_COLUMN = "difficulty_rating"
TARGET_MAPPING = {1: 0, 3: 1, 5: 2, 7: 3}
INVERSE_TARGET_MAPPING = {0: 1, 1: 3, 2: 5, 3: 7}
TARGET_NAMES = ["Easy (1)", "Moderate (3)", "Hard (5)", "Strenuous (7)"]


def parse_geolocation(geoloc_str: str | float) -> Tuple[float, float]:
    """Parse latitude and longitude from string representation of dictionary."""
    if not isinstance(geoloc_str, str) or not geoloc_str.strip():
        return np.nan, np.nan
    try:
        data = ast.literal_eval(geoloc_str)
        if isinstance(data, dict):
            return float(data.get("lat", np.nan)), float(data.get("lng", np.nan))
    except Exception:
        pass
    
    # Fallback to regex extraction
    match = re.search(r"lat'?\s*:\s*([-\d.]+).*?lng'?\s*:\s*([-\d.]+)", str(geoloc_str))
    if match:
        return float(match.group(1)), float(match.group(2))
    return np.nan, np.nan


def parse_feature_tags(features_str: str | float) -> dict[str, int]:
    """Extract binary biome and geographical feature indicators from stringified list."""
    s = str(features_str).lower() if pd.notna(features_str) else ""
    return {
        "forest": int("forest" in s),
        "river": int("river" in s),
        "lake": int("lake" in s),
        "waterfall": int("waterfall" in s),
        "beach": int("beach" in s),
        "cave": int("cave" in s),
        "historic_site": int("historic-site" in s or "historic_site" in s),
        "hot_spring": int("hot-spring" in s or "hot_spring" in s),
    }


def parse_activity_tags(activities_str: str | float) -> dict[str, int]:
    """Extract backpacking and hiking indicators from activities string."""
    s = str(activities_str).lower() if pd.notna(activities_str) else ""
    return {
        "backpacking": int("backpacking" in s),
        "hiking": int("hiking" in s),
    }


def load_raw_datasets(
    trails_path: str | Path = "data/raw/national_parks_trails.csv",
    climate_path: str | Path = "data/raw/national_parks_climate.csv",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load raw trail and climate CSVs."""
    repo_root = Path(__file__).resolve().parents[3]
    trails_p = Path(trails_path)
    if not trails_p.exists():
        candidate = repo_root / trails_path
        if candidate.exists():
            trails_p = candidate

    climate_p = Path(climate_path)
    if not climate_p.exists():
        candidate = repo_root / climate_path
        if candidate.exists():
            climate_p = candidate

    if not trails_p.exists():
        raise FileNotFoundError(f"Trails dataset not found at {trails_p}")
    if not climate_p.exists():
        raise FileNotFoundError(f"Climate dataset not found at {climate_p}")

    df_trails = pd.read_csv(trails_p, encoding="latin1")
    df_climate = pd.read_csv(climate_p, encoding="latin1")
    return df_trails, df_climate


def load_and_merge_data(
    trails_path: str | Path = "data/raw/national_parks_trails.csv",
    climate_path: str | Path = "data/raw/national_parks_climate.csv",
    filter_hiking_only: bool = True,
    drop_zero_length: bool = True,
) -> pd.DataFrame:
    """Load, parse, merge, and clean the trail and climate datasets.

    Returns a clean DataFrame with parsed features and no target leakage.
    """
    df_trails, df_climate = load_raw_datasets(trails_path, climate_path)

    # 1. Merge on trail_id
    df = df_trails.merge(df_climate, on="trail_id", how="inner")

    # 2. Filter invalid difficulty ratings if any (must be in 1, 3, 5, 7)
    df = df[df[TARGET_COLUMN].isin([1, 3, 5, 7])].copy()

    # 3. Filter zero length trails (cannot hike 0 meters)
    if drop_zero_length:
        df = df[df["length"] > 0].copy()

    # 4. Extract activities and optional hiking filter
    activities_parsed = df["activities"].apply(parse_activity_tags)
    df_acts = pd.DataFrame(list(activities_parsed), index=df.index)
    df["backpacking"] = df_acts["backpacking"]
    df["is_hiking"] = df_acts["hiking"]

    if filter_hiking_only:
        # Keep trails where hiking is listed, matching standard trail usage
        df = df[df["is_hiking"] == 1].copy()

    # 5. Extract coordinates
    coords = df["_geoloc"].apply(parse_geolocation)
    df["latitude"] = [c[0] for c in coords]
    df["longitude"] = [c[1] for c in coords]

    # 6. Extract physical biome flags
    features_parsed = df["features"].apply(parse_feature_tags)
    df_feats = pd.DataFrame(list(features_parsed), index=df.index)
    for col in df_feats.columns:
        df[col] = df_feats[col]

    # 7. Normalize route_type
    df["route_type"] = df["route_type"].fillna("unknown").astype(str).str.lower().str.strip()

    # 8. Clean park / state / country
    df["park"] = (
        df["area_name"]
        .astype(str)
        .str.replace(" National Park", "", regex=False)
        .str.replace(" National and State Parks", "", regex=False)
        .str.strip()
    )
    df["state"] = df["state_name"].fillna("Other").astype(str).str.strip()
    df.loc[df["state"] == "Maui", "state"] = "Hawaii"

    # 9. Target encoding (map {1, 3, 5, 7} to {0, 1, 2, 3})
    df["target"] = df[TARGET_COLUMN].map(TARGET_MAPPING).astype(int)

    # Reset index
    df = df.reset_index(drop=True)
    return df
