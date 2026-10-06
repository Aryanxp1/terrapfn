"""Generate comprehensive data quality and integrity report for TerraPFN.

Analyzes raw datasets, schema validity, missing values, target balance,
and documents features excluded for post-hoc target leakage prevention.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from terrapfn.data.loader import (
    IDENTIFIER_COLUMNS,
    LEAKAGE_FEATURES,
    TARGET_COLUMN,
    TARGET_NAMES,
    load_and_merge_data,
    load_raw_datasets,
)
from terrapfn.data.preprocessor import TrailFeaturePreprocessor


def generate_report(output_dir: str | Path = "data/processed") -> dict:
    """Generate and save data quality report."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    df_trails_raw, df_climate_raw = load_raw_datasets()
    df_clean = load_and_merge_data()

    preprocessor = TrailFeaturePreprocessor(scale_numeric=True)
    X_mat = preprocessor.fit_transform(df_clean)
    feature_names = preprocessor.get_feature_names_out()

    # Target distribution
    target_counts = df_clean[TARGET_COLUMN].value_counts().sort_index().to_dict()
    target_percentages = (
        (df_clean[TARGET_COLUMN].value_counts(normalize=True).sort_index() * 100)
        .round(2)
        .to_dict()
    )

    # Missing values in raw datasets
    raw_trails_missing = df_trails_raw.isnull().sum()[df_trails_raw.isnull().sum() > 0].to_dict()
    raw_climate_missing = df_climate_raw.isnull().sum()[df_climate_raw.isnull().sum() > 0].to_dict()

    # Categorical cardinalities in cleaned data
    cat_cardinalities = {
        "route_type": int(df_clean["route_type"].nunique()),
        "park": int(df_clean["park"].nunique()),
        "state": int(df_clean["state"].nunique()),
    }

    # Duplicate check
    duplicate_trail_ids = int(df_trails_raw.duplicated(subset=["trail_id"]).sum())
    duplicate_trail_names = int(df_clean.duplicated(subset=["name", "park"]).sum())

    # Suspicious columns analysis
    suspicious_columns = [
        {
            "column": "visitor_usage",
            "issue": f"{df_trails_raw['visitor_usage'].isnull().sum()} missing values; post-hoc traffic estimation.",
            "action": "Excluded (Leakage & High Missingness)",
        },
        {
            "column": "avg_rating",
            "issue": "Post-hoc crowdsourced user rating reflecting trail satisfaction, not physical trail physics.",
            "action": "Excluded (Post-Hoc Leakage Risk)",
        },
        {
            "column": "popularity",
            "issue": "Search and click ranking influenced by user difficulty ratings.",
            "action": "Excluded (Post-Hoc Leakage Risk)",
        },
        {
            "column": "num_reviews",
            "issue": "Engagement count strongly correlated with easy/popular trails.",
            "action": "Excluded (Post-Hoc Leakage Risk)",
        },
        {
            "column": "units",
            "issue": "Arbitrary scrape unit parameter ('i' vs 'm') where length was already stored in meters.",
            "action": "Excluded (Artifact)",
        },
    ]

    report = {
        "summary": {
            "raw_trails_rows": int(len(df_trails_raw)),
            "raw_climate_rows": int(len(df_climate_raw)),
            "cleaned_hiking_rows": int(len(df_clean)),
            "derived_feature_matrix_shape": list(X_mat.shape),
            "final_feature_count": int(X_mat.shape[1]),
        },
        "target_distribution": {
            "column_name": TARGET_COLUMN,
            "classes": TARGET_NAMES,
            "raw_counts": target_counts,
            "percentages": target_percentages,
        },
        "missing_values": {
            "raw_trails_nulls": raw_trails_missing,
            "raw_climate_nulls": raw_climate_missing,
            "cleaned_features_nulls_after_preprocessing": int(np.isnan(X_mat).sum()),
        },
        "categorical_cardinalities": cat_cardinalities,
        "duplicates": {
            "duplicate_trail_ids": duplicate_trail_ids,
            "duplicate_trail_name_and_park": duplicate_trail_names,
        },
        "features_excluded_due_to_leakage": LEAKAGE_FEATURES + IDENTIFIER_COLUMNS,
        "suspicious_columns": suspicious_columns,
        "feature_list": feature_names,
    }

    # Save JSON report
    json_file = out_path / "data_quality_report.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Save Markdown report
    md_file = out_path / "data_quality_report.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# TerraPFN Data Quality & Integrity Report\n\n")
        f.write("## 1. Dataset Dimensions\n\n")
        f.write(f"- **Raw Trail Records:** {report['summary']['raw_trails_rows']:,}\n")
        f.write(f"- **Raw Climate Records:** {report['summary']['raw_climate_rows']:,}\n")
        f.write(f"- **Cleaned Hiking Trails:** {report['summary']['cleaned_hiking_rows']:,}\n")
        f.write(f"- **Final Modeling Feature Matrix:** {report['summary']['derived_feature_matrix_shape'][0]:,} rows × {report['summary']['derived_feature_matrix_shape'][1]} features\n\n")
        
        f.write("## 2. Target Variable Distribution (`difficulty_rating`)\n\n")
        f.write("| Difficulty Tier | Raw Value | Sample Count | Percentage |\n")
        f.write("| :--- | :---: | :---: | :---: |\n")
        for label, (val, count) in zip(TARGET_NAMES, target_counts.items()):
            pct = target_percentages[val]
            f.write(f"| **{label}** | {val} | {count:,} | {pct:.1f}% |\n")
        
        f.write("\n## 3. Features Excluded Due to Target Leakage\n\n")
        f.write("The following columns were strictly excluded to ensure scientific validity:\n\n")
        for item in suspicious_columns:
            f.write(f"- **`{item['column']}`**: {item['issue']} *(Status: {item['action']})*\n")
            
        f.write("\n## 4. Derived & Preprocessed Features\n\n")
        f.write(f"Total features generated: **{len(feature_names)}**\n\n")
        f.write("Features include continuous topography (`distance_km`, `elevation_gain`, `elevation_gradient`, `elevation_gain_per_km`), ")
        f.write("biophysical terrain flags (`forest`, `river`, `lake`, `waterfall`, `beach`, `cave`, `historic_site`, `hot_spring`, `backpacking`), ")
        f.write("10-year climate extremes (`summer_temp`, `winter_temp`, `annual_rain`, `annual_snow`), and one-hot route types and top park jurisdictions.\n")

    print(f"Data quality report saved to {json_file} and {md_file}")
    return report


if __name__ == "__main__":
    generate_report()
