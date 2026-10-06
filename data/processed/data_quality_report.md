# TerraPFN Data Quality & Integrity Report

## 1. Dataset Dimensions

- **Raw Trail Records:** 3,313
- **Raw Climate Records:** 3,313
- **Cleaned Hiking Trails:** 3,104
- **Final Modeling Feature Matrix:** 3,104 rows × 58 features

## 2. Target Variable Distribution (`difficulty_rating`)

| Difficulty Tier | Raw Value | Sample Count | Percentage |
| :--- | :---: | :---: | :---: |
| **Easy (1)** | 1 | 778 | 25.1% |
| **Moderate (3)** | 3 | 1,379 | 44.4% |
| **Hard (5)** | 5 | 763 | 24.6% |
| **Strenuous (7)** | 7 | 184 | 5.9% |

## 3. Features Excluded Due to Target Leakage

The following columns were strictly excluded to ensure scientific validity:

- **`visitor_usage`**: 253 missing values; post-hoc traffic estimation. *(Status: Excluded (Leakage & High Missingness))*
- **`avg_rating`**: Post-hoc crowdsourced user rating reflecting trail satisfaction, not physical trail physics. *(Status: Excluded (Post-Hoc Leakage Risk))*
- **`popularity`**: Search and click ranking influenced by user difficulty ratings. *(Status: Excluded (Post-Hoc Leakage Risk))*
- **`num_reviews`**: Engagement count strongly correlated with easy/popular trails. *(Status: Excluded (Post-Hoc Leakage Risk))*
- **`units`**: Arbitrary scrape unit parameter ('i' vs 'm') where length was already stored in meters. *(Status: Excluded (Artifact))*

## 4. Derived & Preprocessed Features

Total features generated: **58**

Features include continuous topography (`distance_km`, `elevation_gain`, `elevation_gradient`, `elevation_gain_per_km`), biophysical terrain flags (`forest`, `river`, `lake`, `waterfall`, `beach`, `cave`, `historic_site`, `hot_spring`, `backpacking`), 10-year climate extremes (`summer_temp`, `winter_temp`, `annual_rain`, `annual_snow`), and one-hot route types and top park jurisdictions.
