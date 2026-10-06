"""Integration test for Streamlit dashboard flow using Streamlit AppTest."""

from __future__ import annotations

import pytest
from streamlit.testing.v1 import AppTest


def test_dashboard_initial_render():
    """Verify that the dashboard initializes without exceptions."""
    at = AppTest.from_file("src/terrapfn/app/dashboard.py", default_timeout=35)
    at.run()
    assert not at.exception
    # Check that main buttons are present
    button_labels = [b.label for b in at.button]
    assert any("Curated" in label for label in button_labels)
    assert any("GENERATE GRASS PASS" in label for label in button_labels)


def test_dashboard_select_demo_and_generate_pass():
    """Test switching demo trails and generating Grass Pass."""
    at = AppTest.from_file("src/terrapfn/app/dashboard.py", default_timeout=35)
    at.run()
    assert not at.exception

    # Find the 'Select Hard' button
    hard_btn = next((b for b in at.button if "Hard" in b.label and "Select" in b.label), None)
    assert hard_btn is not None
    hard_btn.click().run()
    assert not at.exception

    # Click Generate Grass Pass
    gen_btn = next((b for b in at.button if "GENERATE GRASS PASS" in b.label), None)
    assert gen_btn is not None
    gen_btn.click().run()
    assert not at.exception

    # Verify Grass Pass is cached and Cache & Go button is rendered
    cache_go_btn = next((b for b in at.button if "CACHE & GO" in b.label), None)
    assert cache_go_btn is not None

    # Click Cache & Go to trigger Touch Grass mode
    cache_go_btn.click().run()
    assert not at.exception

    # In Touch Grass Mode, back button should be available
    back_btn = next((b for b in at.button if "I'M BACK" in b.label), None)
    assert back_btn is not None

    # Click back button to trigger post-hike checkin
    back_btn.click().run()
    assert not at.exception
    save_btn = next((b for b in at.button if "SAVE OBSERVATION" in b.label), None)
    assert save_btn is not None
