"""Trail catalog and data access service for TerraPFN.

Provides searching, filtering, curated demo trails, and custom route synthesis
with robust validation and no target leakage.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from terrapfn.data.loader import load_and_merge_data, TARGET_MAPPING, TARGET_NAMES

# Curated demo trail definitions representing four distinct difficulty classes
CURATED_DEMO_TRAILS: List[Dict[str, Any]] = [
    {
        "id": "demo_easy",
        "trail_id": 10015395,
        "name": "Delicate Arch Viewpoint Trail",
        "park": "Arches",
        "state": "Utah",
        "label": "Easy",
        "target_class": 0,
        "difficulty_rating": 1,
        "description": "Short, low-incline walk with wide open vistas of Delicate Arch across the canyon.",
    },
    {
        "id": "demo_moderate",
        "trail_id": 10026705,
        "name": "Emerald Lake Trail",
        "park": "Rocky Mountain",
        "state": "Colorado",
        "label": "Moderate",
        "target_class": 1,
        "difficulty_rating": 3,
        "description": "Classic subalpine lake ascent passing Nymph and Dream Lakes on steady, maintained grade.",
    },
    {
        "id": "demo_hard",
        "trail_id": 10006571,
        "name": "Angels Landing Trail",
        "park": "Zion",
        "state": "Utah",
        "label": "Hard",
        "target_class": 2,
        "difficulty_rating": 5,
        "description": "Steep switchbacks (Walter's Wiggles) followed by an exposed sandstone ridge walk with chains.",
    },
    {
        "id": "demo_strenuous",
        "trail_id": 10005585,
        "name": "Half Dome Trail",
        "park": "Yosemite",
        "state": "California",
        "label": "Strenuous",
        "target_class": 3,
        "difficulty_rating": 7,
        "description": "Exhausting full-day trek through Little Yosemite Valley culminating in the 400-foot cable route.",
    },
]

# Park-level fallback climate averages for custom user routes
DEFAULT_PARK_CLIMATE = {
    "summer_temp": 21.5,  # °C (~71°F)
    "winter_temp": -2.0,  # °C (~28°F)
    "annual_rain": 650.0,  # mm
    "annual_snow": 120.0,  # mm
}


def load_trail_catalog(data_dir: str = "data/raw") -> pd.DataFrame:
    """Load and clean the entire US National Parks trails dataset."""
    trails_p = f"{data_dir}/national_parks_trails.csv"
    climate_p = f"{data_dir}/national_parks_climate.csv"
    df = load_and_merge_data(trails_path=trails_p, climate_path=climate_p)
    return df


def get_demo_trails(catalog_df: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    """Return enriched curated demo trail records from the dataset."""
    if catalog_df is None:
        catalog_df = load_trail_catalog()

    enriched_demos = []
    for demo in CURATED_DEMO_TRAILS:
        matches = catalog_df[catalog_df["name"].str.contains(demo["name"], case=False, na=False)]
        if not matches.empty:
            row = matches.iloc[0].to_dict()
            record = {**demo, **row}
            # Ensure distance_km is explicitly set
            record["distance_km"] = record.get("length", 0.0) / 1000.0
            enriched_demos.append(record)
        else:
            enriched_demos.append(demo)
    return enriched_demos


def get_trail_by_id(trail_id: int | str, catalog_df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Retrieve full trail record by numeric or string trail_id."""
    try:
        tid = int(trail_id)
        match = catalog_df[catalog_df["trail_id"] == tid]
    except (ValueError, TypeError):
        match = catalog_df[catalog_df["trail_id"].astype(str) == str(trail_id)]

    if match.empty:
        return None
    record = match.iloc[0].to_dict()
    record["distance_km"] = record.get("length", 0.0) / 1000.0
    return record


def search_trails(
    catalog_df: pd.DataFrame,
    query: str = "",
    park: Optional[str] = None,
    max_results: int = 50,
) -> pd.DataFrame:
    """Filter trails by text query and optional park name."""
    df = catalog_df.copy()

    if park and park != "All Parks":
        df = df[df["park"].str.lower() == park.lower()]

    if query.strip():
        q = query.strip().lower()
        df = df[
            df["name"].str.lower().str.contains(q, na=False)
            | df["park"].str.lower().str.contains(q, na=False)
            | df["state"].str.lower().str.contains(q, na=False)
        ]

    return df.head(max_results)


def get_all_parks(catalog_df: pd.DataFrame) -> List[str]:
    """Return sorted unique national park names."""
    parks = sorted(catalog_df["park"].dropna().unique().tolist())
    return ["All Parks"] + parks


def validate_custom_trail_input(
    length_km: float,
    elevation_gain_m: float,
) -> Tuple[bool, Optional[str]]:
    """Validate physical plausibility of user-specified trail measurements."""
    if length_km <= 0.0:
        return False, "Trail distance must be strictly greater than 0 km."
    if length_km > 250.0:
        return False, "Trail distance exceeds single-route envelope (max 250 km)."
    if elevation_gain_m < 0.0:
        return False, "Elevation gain cannot be negative."
    if elevation_gain_m > 8000.0:
        return False, "Elevation gain exceeds terrestrial park limits (max 8,000 m)."

    # Gradient check: vertical gain cannot exceed horizontal distance
    length_m = length_km * 1000.0
    if elevation_gain_m > length_m:
        return False, "Elevation gain cannot exceed total horizontal route distance (physically impossible vertical cliff)."

    return True, None


def build_custom_trail_record(
    name: str,
    park: str,
    state: str,
    length_km: float,
    elevation_gain_m: float,
    route_type: str = "out and back",
    biome_features: Optional[Dict[str, int]] = None,
    climate_overrides: Optional[Dict[str, float]] = None,
) -> pd.DataFrame:
    """Synthesize a complete 1-row DataFrame adhering strictly to the training schema."""
    is_valid, err = validate_custom_trail_input(length_km, elevation_gain_m)
    if not is_valid:
        raise ValueError(f"Invalid trail parameters: {err}")

    length_m = float(length_km * 1000.0)
    elevation_m = float(elevation_gain_m)

    # Defaults for biome tags
    default_biomes = {
        "forest": 1,
        "river": 0,
        "lake": 0,
        "waterfall": 0,
        "beach": 0,
        "cave": 0,
        "historic_site": 0,
        "hot_spring": 0,
        "backpacking": int(length_km >= 20.0),
        "is_hiking": 1,
    }
    if biome_features:
        default_biomes.update(biome_features)

    # Climate
    climate = {**DEFAULT_PARK_CLIMATE}
    if climate_overrides:
        climate.update(climate_overrides)

    record = {
        "trail_id": 99999999,
        "name": name.strip() or "Custom Route",
        "park": park.strip() or "Other",
        "state": state.strip() or "Other",
        "length": length_m,
        "elevation_gain": elevation_m,
        "route_type": route_type.lower().strip() or "loop",
        "summer_temp": climate["summer_temp"],
        "winter_temp": climate["winter_temp"],
        "annual_rain": climate["annual_rain"],
        "annual_snow": climate["annual_snow"],
        **default_biomes,
        "target": -1,  # Placeholder (unseen/unlabeled)
    }

    df_custom = pd.DataFrame([record])
    return df_custom
