"""Feature preprocessor for TerraPFN trail difficulty classification.

Implements leakage-free feature derivation, categorical encoding, and scaling.
Strictly fits statistics only on training data folds.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Core feature definitions
CONTINUOUS_RAW_FEATURES = [
    "length",
    "elevation_gain",
    "summer_temp",
    "winter_temp",
    "annual_rain",
    "annual_snow",
]

BINARY_FEATURES = [
    "forest",
    "river",
    "lake",
    "waterfall",
    "beach",
    "cave",
    "historic_site",
    "hot_spring",
    "backpacking",
]

CATEGORICAL_FEATURES = [
    "route_type",
]


class TrailFeaturePreprocessor(BaseEstimator, TransformerMixin):
    """Leakage-free Scikit-Learn transformer for trail features.

    Derives topographic physical indicators, encodes categoricals,
    imputes missing values, and optionally scales continuous variables.
    """

    def __init__(
        self,
        scale_numeric: bool = True,
        min_park_frequency: int = 15,
        include_park: bool = True,
    ) -> None:
        self.scale_numeric = scale_numeric
        self.min_park_frequency = min_park_frequency
        self.include_park = include_park

        self.num_imputer_ = SimpleImputer(strategy="median")
        self.scaler_ = StandardScaler() if scale_numeric else None
        self.cat_encoder_ = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        self.frequent_parks_: set[str] = set()
        self.feature_names_out_: List[str] = []

    def _derive_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Compute derived features and segment into continuous, binary, and categorical."""
        df_copy = df.copy()

        # Derived topographic physics
        length_m = df_copy["length"].clip(lower=1.0)
        dist_km = length_m / 1000.0
        elev_gain = df_copy["elevation_gain"].clip(lower=0.0)

        # Elevation gradient (m gain per m distance, dimensionless slope)
        elev_gradient = elev_gain / length_m
        # Elevation gain per km (m/km, typical hiking effort metric)
        gain_per_km = elev_gain / dist_km

        continuous_dict = {
            "distance_km": dist_km,
            "elevation_gain": elev_gain,
            "elevation_gradient": elev_gradient,
            "elevation_gain_per_km": gain_per_km,
            "summer_temp": df_copy["summer_temp"],
            "winter_temp": df_copy["winter_temp"],
            "annual_rain": df_copy["annual_rain"],
            "annual_snow": df_copy["annual_snow"],
        }
        df_continuous = pd.DataFrame(continuous_dict, index=df.index)

        # Binary features (guaranteed 0/1)
        binary_dict = {}
        for col in BINARY_FEATURES:
            if col in df_copy.columns:
                binary_dict[col] = df_copy[col].fillna(0).astype(int)
            else:
                binary_dict[col] = pd.Series(0, index=df.index, dtype=int)
        df_binary = pd.DataFrame(binary_dict, index=df.index)

        # Categorical features
        cat_dict = {
            "route_type": df_copy["route_type"].fillna("unknown").astype(str),
        }
        if self.include_park:
            cat_dict["park"] = df_copy["park"].fillna("Other").astype(str)
        df_cat = pd.DataFrame(cat_dict, index=df.index)

        return df_continuous, df_binary, df_cat

    def fit(self, X: pd.DataFrame, y=None) -> TrailFeaturePreprocessor:
        """Fit feature statistics strictly on training data."""
        df_continuous, df_binary, df_cat = self._derive_features(X)

        # 1. Fit continuous imputer and scaler
        imputed_cont = self.num_imputer_.fit_transform(df_continuous)
        if self.scaler_ is not None:
            self.scaler_.fit(imputed_cont)

        # 2. Learn frequent parks from training set only
        if self.include_park and "park" in df_cat.columns:
            park_counts = df_cat["park"].value_counts()
            self.frequent_parks_ = set(
                park_counts[park_counts >= self.min_park_frequency].index
            )
            df_cat["park"] = df_cat["park"].apply(
                lambda p: p if p in self.frequent_parks_ else "Other"
            )

        # 3. Fit categorical encoder
        self.cat_encoder_.fit(df_cat)

        # 4. Construct feature names
        cont_names = list(df_continuous.columns)
        bin_names = list(df_binary.columns)
        cat_names = list(self.cat_encoder_.get_feature_names_out(df_cat.columns))
        self.feature_names_out_ = cont_names + bin_names + cat_names

        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform input features using fitted statistics."""
        df_continuous, df_binary, df_cat = self._derive_features(X)

        # 1. Transform continuous
        imputed_cont = self.num_imputer_.transform(df_continuous)
        if self.scaler_ is not None:
            cont_vals = self.scaler_.transform(imputed_cont)
        else:
            cont_vals = imputed_cont

        # 2. Transform binary
        bin_vals = df_binary.to_numpy(dtype=np.float32)

        # 3. Transform categorical with learned park categories
        if self.include_park and "park" in df_cat.columns:
            df_cat["park"] = df_cat["park"].apply(
                lambda p: p if p in self.frequent_parks_ else "Other"
            )
        cat_vals = self.cat_encoder_.transform(df_cat)

        # Concatenate horizontally
        return np.hstack([cont_vals, bin_vals, cat_vals]).astype(np.float32)

    def get_feature_names_out(self) -> List[str]:
        """Return the output feature names."""
        return self.feature_names_out_
