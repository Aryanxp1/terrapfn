"""Unit tests for TerraPFN application services and Grass Pass generation."""

from __future__ import annotations

import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from terrapfn.services.trail_service import (
    CURATED_DEMO_TRAILS,
    build_custom_trail_record,
    get_demo_trails,
    get_trail_by_id,
    load_trail_catalog,
    search_trails,
    validate_custom_trail_input,
)
from terrapfn.services.inference_service import TerraInferenceEngine
from terrapfn.services.grass_pass_service import (
    calculate_duration_range,
    calculate_hydration_envelope,
    generate_preparation_notes,
    generate_printable_html,
)
from terrapfn.services.checkin_service import load_checkin_history, record_checkin


@pytest.fixture(scope="module")
def catalog_df():
    """Load cached test catalog."""
    return load_trail_catalog()


@pytest.fixture(scope="module")
def inference_engine(catalog_df):
    """Instantiate and fit inference engine on small subset for fast testing."""
    engine = TerraInferenceEngine(context_sample_size=200, random_state=42)
    # Fit with subset to keep test under a few seconds
    engine.fit_from_catalog(catalog_df.iloc[:400])
    return engine


def test_demo_trails_structure(catalog_df):
    """Verify curated demo trails contain all 4 difficulty classes and valid attributes."""
    demos = get_demo_trails(catalog_df)
    assert len(demos) == 4
    labels = [d["label"] for d in demos]
    assert set(labels) == {"Easy", "Moderate", "Hard", "Strenuous"}
    for demo in demos:
        assert demo["distance_km"] > 0
        assert "name" in demo
        assert "park" in demo


def test_trail_search(catalog_df):
    """Verify search filtering by text and park."""
    results = search_trails(catalog_df, query="Angels", max_results=10)
    assert not results.empty
    assert any("Angels" in name for name in results["name"])

    # Park filter
    yosemite_results = search_trails(catalog_df, query="", park="Yosemite", max_results=10)
    assert not yosemite_results.empty
    assert all(p.lower() == "yosemite" for p in yosemite_results["park"])


def test_custom_trail_validation():
    """Verify physical bounds validation for user-entered trails."""
    # Valid
    ok, err = validate_custom_trail_input(10.0, 500.0)
    assert ok and err is None

    # Invalid: 0 distance
    ok, err = validate_custom_trail_input(0.0, 500.0)
    assert not ok and "greater than 0" in err

    # Invalid: negative gain
    ok, err = validate_custom_trail_input(5.0, -100.0)
    assert not ok and "negative" in err

    # Invalid: vertical cliff (gain > distance)
    ok, err = validate_custom_trail_input(0.5, 800.0)
    assert not ok and "horizontal route distance" in err


def test_custom_trail_builder_and_features():
    """Verify building custom route produces correct schema."""
    df_custom = build_custom_trail_record(
        name="Test Ridge Trail",
        park="Glacier",
        state="Montana",
        length_km=14.0,
        elevation_gain_m=750.0,
        route_type="out and back",
        biome_features={"forest": 1, "river": 1},
    )
    assert len(df_custom) == 1
    assert df_custom.iloc[0]["length"] == 14000.0
    assert df_custom.iloc[0]["elevation_gain"] == 750.0
    assert df_custom.iloc[0]["forest"] == 1
    assert df_custom.iloc[0]["river"] == 1


def test_inference_engine_predictions(catalog_df, inference_engine):
    """Verify preview and TabPFN predictions satisfy all probabilistic and dimensional constraints."""
    sample_trail = catalog_df.iloc[0:1].copy()

    # Fast Preview
    preview_pred = inference_engine.predict_preview(sample_trail)
    assert preview_pred.dominant_class_name in ["Easy", "Moderate", "Hard", "Strenuous"]
    assert np.isclose(sum(preview_pred.probabilities.values()), 1.0, atol=1e-4)
    assert 0.0 <= preview_pred.entropy <= 1.0
    assert preview_pred.inference_time_ms >= 0.0

    # TabPFN Pass
    tabpfn_pred = inference_engine.predict_tabpfn_pass(sample_trail)
    assert tabpfn_pred.dominant_class_name in ["Easy", "Moderate", "Hard", "Strenuous"]
    assert np.isclose(sum(tabpfn_pred.probabilities.values()), 1.0, atol=1e-4)
    assert 0.0 <= tabpfn_pred.entropy <= 1.0
    assert 0.0 <= tabpfn_pred.confidence_margin <= 1.0


def test_grass_pass_generation_and_html(catalog_df, inference_engine):
    """Verify preparation notes calculation and HTML export generation."""
    sample_trail = catalog_df.iloc[0].to_dict()
    sample_df = catalog_df.iloc[0:1].copy()

    pred = inference_engine.predict_preview(sample_df)
    notes = generate_preparation_notes(sample_trail, pred)

    assert "duration_range" in notes
    assert "recommended_water_l" in notes
    assert notes["recommended_water_l"] >= notes["minimum_water_l"]
    assert "footwear" in notes
    assert "turnaround_note" in notes

    html = generate_printable_html(sample_trail, pred, notes)
    assert "TERRAPFN" in html
    assert sample_trail["name"] in html
    assert "CALIBRATED DIFFICULTY PROBABILITY" in html
    assert "window.print()" in html


def test_checkin_service_roundtrip():
    """Verify post-hike check-in logging to local JSON file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "checkins.json"

        rec = record_checkin(
            trail_name="Half Dome",
            felt_difficulty="Strenuous",
            predicted_difficulty="Strenuous",
            trail_id=10008302,
            actual_duration_min=480,
            notes="Cables were steep and intense.",
            file_path=test_file,
        )

        assert rec["trail_name"] == "Half Dome"
        assert rec["agreement"] == 1

        history = load_checkin_history(test_file)
        assert len(history) == 1
        assert history[0]["actual_duration_min"] == 480
