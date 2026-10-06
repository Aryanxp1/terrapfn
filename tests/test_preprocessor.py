"""Tests for feature preprocessor module."""

import numpy as np
import pandas as pd
import pytest
from terrapfn.data.loader import load_and_merge_data, TARGET_COLUMN
from terrapfn.data.preprocessor import TrailFeaturePreprocessor


@pytest.fixture
def clean_data():
    return load_and_merge_data()


def test_derived_topographic_features(clean_data):
    prep = TrailFeaturePreprocessor(scale_numeric=False)
    X = prep.fit_transform(clean_data)
    feature_names = prep.get_feature_names_out()

    assert "distance_km" in feature_names
    assert "elevation_gain" in feature_names
    assert "elevation_gradient" in feature_names
    assert "elevation_gain_per_km" in feature_names

    # Check physics calculation on first row
    row0 = clean_data.iloc[0]
    expected_dist_km = row0["length"] / 1000.0
    dist_idx = feature_names.index("distance_km")
    assert np.isclose(X[0, dist_idx], expected_dist_km, rtol=1e-3)


def test_no_target_in_features(clean_data):
    prep = TrailFeaturePreprocessor()
    prep.fit(clean_data)
    feature_names = prep.get_feature_names_out()

    assert TARGET_COLUMN not in feature_names
    assert "target" not in feature_names
    assert "avg_rating" not in feature_names
    assert "popularity" not in feature_names


def test_no_nans_in_transformed_output(clean_data):
    prep = TrailFeaturePreprocessor(scale_numeric=True)
    X = prep.fit_transform(clean_data)
    assert not np.isnan(X).any()


def test_train_test_split_isolation(clean_data):
    train_df = clean_data.iloc[:2000].copy()
    test_df = clean_data.iloc[2000:].copy()

    prep = TrailFeaturePreprocessor()
    X_train = prep.fit_transform(train_df)
    X_test = prep.transform(test_df)

    assert X_train.shape[1] == X_test.shape[1]
    assert not np.isnan(X_test).any()
