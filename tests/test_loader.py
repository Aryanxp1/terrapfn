"""Tests for dataset loader module."""

import pytest
import pandas as pd
from terrapfn.data.loader import (
    load_and_merge_data,
    load_raw_datasets,
    LEAKAGE_FEATURES,
    TARGET_COLUMN,
    TARGET_MAPPING,
)


def test_load_raw_datasets():
    df_trails, df_climate = load_raw_datasets()
    assert len(df_trails) == 3313
    assert len(df_climate) == 3313
    assert "trail_id" in df_trails.columns
    assert "trail_id" in df_climate.columns


def test_load_and_merge_data_structure():
    df = load_and_merge_data()
    assert len(df) > 3000
    assert "target" in df.columns
    assert TARGET_COLUMN in df.columns
    assert set(df["target"].unique()) == {0, 1, 2, 3}


def test_no_zero_length_trails():
    df = load_and_merge_data()
    assert (df["length"] <= 0).sum() == 0


def test_target_mapping_integrity():
    df = load_and_merge_data()
    for raw_val, mapped_val in TARGET_MAPPING.items():
        subset = df[df[TARGET_COLUMN] == raw_val]
        if len(subset) > 0:
            assert (subset["target"] == mapped_val).all()
