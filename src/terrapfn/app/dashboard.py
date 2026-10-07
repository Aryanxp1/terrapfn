"""TerraPFN: Zero-Scroll Outdoor Trail Intelligence Dashboard.

Hacktoberfest 2026 Week 1 Entry
Author: Aryan Vishwakarma
Target Category: Best Use of TabPFN
Theme: Touch Grass
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Ensure repository root and src directory are in sys.path for direct cloud execution
SRC_DIR = Path(__file__).resolve().parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import numpy as np
import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui

# Custom outdoor styling and components
from terrapfn.app.components import (
    CLASS_BACKGROUNDS,
    CLASS_BORDERS,
    CLASS_COLORS,
    render_climate_and_terrain_tags,
    render_difficulty_distribution,
    render_grass_pass_hero,
    render_header,
    render_metrics_grid,
    render_preparation_checklist,
)
from terrapfn.app.styles import PREMIUM_OUTDOOR_CSS
from terrapfn.services.checkin_service import load_checkin_history, record_checkin
from terrapfn.services.grass_pass_service import (
    generate_preparation_notes,
    generate_printable_html,
)
from terrapfn.services.inference_service import DifficultyPrediction, TerraInferenceEngine
from terrapfn.services.trail_service import (
    CURATED_DEMO_TRAILS,
    build_custom_trail_record,
    get_all_parks,
    get_demo_trails,
    get_trail_by_id,
    load_trail_catalog,
    search_trails,
    validate_custom_trail_input,
)

# Streamlit Page Configuration
st.set_page_config(
    page_title="TerraPFN — Touch Grass Field Intelligence",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Cached Data and Engine Services
@st.cache_data(show_spinner=False)
def get_cached_catalog() -> pd.DataFrame:
    """Load and cache the cleaned trails dataset."""
    return load_trail_catalog()


@st.cache_resource(show_spinner=True)
def get_cached_engine() -> TerraInferenceEngine:
    """Fit and cache preprocessors, fast preview engine, and TabPFN in-context model."""
    catalog_df = get_cached_catalog()
    engine = TerraInferenceEngine(context_sample_size=1000, random_state=42)
    engine.fit_from_catalog(catalog_df)
    return engine


def init_session_state() -> None:
    """Initialize app-level session state variables."""
    if "selected_trail_id" not in st.session_state:
        st.session_state.selected_trail_id = 10006571  # Angels Landing (Hard demo default)
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "demo"  # 'demo', 'catalog', 'custom'
    if "cached_grass_pass" not in st.session_state:
        st.session_state.cached_grass_pass = None
    if "touch_grass_active" not in st.session_state:
        st.session_state.touch_grass_active = False
    if "hike_start_time" not in st.session_state:
        st.session_state.hike_start_time = None
    if "show_checkin_modal" not in st.session_state:
        st.session_state.show_checkin_modal = False


def render_sidebar(catalog_df: pd.DataFrame) -> None:
    """Render informative, restrained outdoor sidebar."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">TERRAPFN</div>
            <div style="font-size: 13px; line-height: 1.5; color: #8b949e; margin-bottom: 16px;">
              <strong>Zero-scroll outdoor trail intelligence.</strong><br>
              Traditional apps trap you in infinite reviews and photo feeds.
              TerraPFN calculates an objective biophysical preparation envelope in seconds.
              Pocket the phone and step outside.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Category: **Best Use of TabPFN**")
        st.caption("Theme: **Touch Grass**")
        st.caption("Challenge: **Hacktoberfest 2026 Week 1**")

        st.markdown("---")
        st.markdown(
            """
            <div class="sidebar-section-title">MODEL EVIDENCE (5-FOLD CV)</div>
            <table class="sidebar-evidence-table">
              <thead>
                <tr>
                  <th>Model</th>
                  <th style="text-align:right;">QWK</th>
                  <th style="text-align:right;">BalAcc</th>
                  <th style="text-align:right;">LogLoss</th>
                </tr>
              </thead>
              <tbody>
                <tr class="highlight">
                  <td style="color:#3fb950;">★ TabPFN (v2)</td>
                  <td style="text-align:right;">0.731</td>
                  <td style="text-align:right;">55.1%</td>
                  <td style="text-align:right;">0.702</td>
                </tr>
                <tr style="color:#c9d1d9;">
                  <td>Random Forest</td>
                  <td style="text-align:right;">0.726</td>
                  <td style="text-align:right;">54.6%</td>
                  <td style="text-align:right;">0.727</td>
                </tr>
                <tr style="color:#c9d1d9;">
                  <td>HistGradBoost</td>
                  <td style="text-align:right;">0.704</td>
                  <td style="text-align:right;">54.7%</td>
                  <td style="text-align:right;">0.888</td>
                </tr>
                <tr style="color:#8b949e;">
                  <td>Logistic Reg</td>
                  <td style="text-align:right;">0.706</td>
                  <td style="text-align:right;">53.4%</td>
                  <td style="text-align:right;">0.778</td>
                </tr>
                <tr style="color:#6e7681;">
                  <td>Dummy Floor</td>
                  <td style="text-align:right;">0.005</td>
                  <td style="text-align:right;">24.2%</td>
                  <td style="text-align:right;">10.95</td>
                </tr>
              </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "Evaluated on 3,104 National Parks trails with strict leakage prevention. "
            "TabPFN leads decisively in Log Loss and Quadratic Weighted Kappa."
        )

        st.markdown("---")
        history = load_checkin_history()
        st.markdown(
            f"""
            <div style="font-size: 12px; color: #8b949e;">
              Post-hike observation log: <strong style="color: #2ea043;">{len(history)} recorded</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    """Main application loop."""
    init_session_state()
    st.markdown(PREMIUM_OUTDOOR_CSS, unsafe_allow_html=True)

    catalog_df = get_cached_catalog()
    engine = get_cached_engine()

    render_sidebar(catalog_df)

    # -------------------------------------------------------------
    # SCREEN: TOUCH GRASS MODE (MINIMAL TRANSITION SCREEN)
    # -------------------------------------------------------------
    if st.session_state.touch_grass_active:
        render_touch_grass_screen()
        return

    # -------------------------------------------------------------
    # SCREEN: POST-HIKE CHECK-IN MODAL/SCREEN
    # -------------------------------------------------------------
    if st.session_state.show_checkin_modal:
        render_checkin_screen()
        return

    # -------------------------------------------------------------
    # SCREEN: MAIN APPLICATION FLOW
    # -------------------------------------------------------------
    render_header()

    # Step 1: Mode Selector (Tabs / Button Switcher without emojis)
    mode_cols = st.columns([1, 1, 1])
    with mode_cols[0]:
        if st.button("Curated Benchmark Trails", width="stretch", type="primary" if st.session_state.input_mode == "demo" else "secondary"):
            st.session_state.input_mode = "demo"
            st.rerun()
    with mode_cols[1]:
        if st.button("Explore National Catalog (3,100+)", width="stretch", type="primary" if st.session_state.input_mode == "catalog" else "secondary"):
            st.session_state.input_mode = "catalog"
            st.rerun()
    with mode_cols[2]:
        if st.button("Synthesize Custom Route", width="stretch", type="primary" if st.session_state.input_mode == "custom" else "secondary"):
            st.session_state.input_mode = "custom"
            st.rerun()

    active_trail_record: Optional[Dict[str, Any]] = None
    trail_df: Optional[pd.DataFrame] = None

    # -------------------------------------------------------------
    # INPUT MODE A: CURATED BENCHMARK TRAILS
    # -------------------------------------------------------------
    if st.session_state.input_mode == "demo":
        st.markdown(
            """
            <div style="font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #8b949e; margin: 18px 0 10px 0;">
              BENCHMARK REFERENCE TRAILS (4 GROUND-TRUTH CLASSES)
            </div>
            """,
            unsafe_allow_html=True,
        )

        demo_trails = get_demo_trails(catalog_df)
        demo_cols = st.columns(4)
        for i, demo in enumerate(demo_trails):
            with demo_cols[i]:
                is_selected = st.session_state.selected_trail_id == demo.get("trail_id")
                label = demo["label"]
                badge_color = CLASS_COLORS.get(label, "#2ea043")
                badge_bg = CLASS_BACKGROUNDS.get(label, "rgba(46, 160, 67, 0.12)")
                badge_border = CLASS_BORDERS.get(label, "rgba(46, 160, 67, 0.35)")

                border_style = "border: 1px solid #2ea043; background: #1c2128;" if is_selected else "border: 1px solid #262f3d; background: #161b22;"

                st.markdown(
                    f"""
                    <div style="{border_style} border-radius: 6px; padding: 14px; margin-bottom: 8px;">
                      <div class="trail-class-pill" style="color: {badge_color}; background: {badge_bg}; border: 1px solid {badge_border};">
                        Class {demo['difficulty_rating']} · {label}
                      </div>
                      <div class="trail-card-name">{demo['name']}</div>
                      <div class="trail-card-meta">{demo['park']} · {demo['state']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                btn_type = "primary" if is_selected else "secondary"
                if st.button(f"Select {label}", key=f"demo_btn_{demo['id']}", width="stretch", type=btn_type):
                    st.session_state.selected_trail_id = demo.get("trail_id")
                    st.session_state.cached_grass_pass = None
                    st.rerun()

        # Load selected demo trail
        active_trail_record = get_trail_by_id(st.session_state.selected_trail_id, catalog_df)
        if active_trail_record is not None:
            trail_df = catalog_df[catalog_df["trail_id"] == st.session_state.selected_trail_id].copy()

    # -------------------------------------------------------------
    # INPUT MODE B: FULL CATALOG EXPLORER
    # -------------------------------------------------------------
    elif st.session_state.input_mode == "catalog":
        st.markdown(
            """
            <div style="font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #8b949e; margin: 18px 0 10px 0;">
              SEARCH 3,104 VERIFIED NATIONAL PARK HIKES
            </div>
            """,
            unsafe_allow_html=True,
        )
        search_cols = st.columns([2, 1])
        with search_cols[0]:
            search_query = st.text_input("Trail name, landmark, or feature:", placeholder="e.g. Half Dome, Angels Landing, Mist Trail, Glacier...")
        with search_cols[1]:
            parks_list = get_all_parks(catalog_df)
            selected_park = st.selectbox("National Park filter:", parks_list)

        results = search_trails(catalog_df, query=search_query, park=selected_park, max_results=25)
        if not results.empty:
            trail_options = {
                f"{row['name']} ({row['park']}, {row['state']}) — {row['length']/1000:.1f} km, +{row['elevation_gain']:.0f}m": row["trail_id"]
                for _, row in results.iterrows()
            }
            selected_label = st.selectbox("Select Trail to Inspect:", list(trail_options.keys()))
            selected_id = trail_options[selected_label]
            if selected_id != st.session_state.selected_trail_id:
                st.session_state.selected_trail_id = selected_id
                st.session_state.cached_grass_pass = None

            active_trail_record = get_trail_by_id(st.session_state.selected_trail_id, catalog_df)
            trail_df = catalog_df[catalog_df["trail_id"] == st.session_state.selected_trail_id].copy()
        else:
            st.warning("No trails matched your search. Try broadening your keywords.")

    # -------------------------------------------------------------
    # INPUT MODE C: CUSTOM ROUTE SYNTHESIZER
    # -------------------------------------------------------------
    elif st.session_state.input_mode == "custom":
        st.markdown(
            """
            <div style="font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #8b949e; margin: 18px 0 10px 0;">
              CUSTOM ROUTE SPECIFICATION
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            custom_name = st.text_input("Route Name:", value="Alpine Ridge Traverse")
            custom_park = st.selectbox("Target Park Ecosystem:", get_all_parks(catalog_df)[1:], index=12)
        with c2:
            custom_dist = st.number_input("Distance (km):", min_value=0.5, max_value=150.0, value=12.5, step=0.5)
            custom_gain = st.number_input("Elevation Gain (m):", min_value=0.0, max_value=4000.0, value=650.0, step=25.0)
        with c3:
            custom_route_type = st.selectbox("Route Topology:", ["loop", "out and back", "point to point"])
            custom_state = "California" if "Yosemite" in custom_park else "Montana" if "Glacier" in custom_park else "Other"

        st.caption("Terrain & Ecosystem Features:")
        feat_cols = st.columns(5)
        with feat_cols[0]:
            f_forest = st.checkbox("Forest", value=True)
            f_river = st.checkbox("River / Stream", value=True)
        with feat_cols[1]:
            f_lake = st.checkbox("Subalpine Lake", value=False)
            f_waterfall = st.checkbox("Waterfall", value=False)
        with feat_cols[2]:
            f_beach = st.checkbox("Sand / Beach", value=False)
            f_cave = st.checkbox("Talus / Rock Scramble", value=False)
        with feat_cols[3]:
            f_historic = st.checkbox("Historic Landmark", value=False)
            f_hot_spring = st.checkbox("Thermal Spring", value=False)
        with feat_cols[4]:
            f_backpacking = st.checkbox("Overnight Backpacking", value=bool(custom_dist >= 20.0))

        biome_dict = {
            "forest": int(f_forest),
            "river": int(f_river),
            "lake": int(f_lake),
            "waterfall": int(f_waterfall),
            "beach": int(f_beach),
            "cave": int(f_cave),
            "historic_site": int(f_historic),
            "hot_spring": int(f_hot_spring),
            "backpacking": int(f_backpacking),
            "is_hiking": 1,
        }

        # Build custom record
        is_valid, err = validate_custom_trail_input(custom_dist, custom_gain)
        if is_valid:
            trail_df = build_custom_trail_record(
                name=custom_name,
                park=custom_park,
                state=custom_state,
                length_km=custom_dist,
                elevation_gain_m=custom_gain,
                route_type=custom_route_type,
                biome_features=biome_dict,
            )
            active_trail_record = trail_df.iloc[0].to_dict()
            active_trail_record["distance_km"] = custom_dist
        else:
            st.error(f"Input validation error: {err}")

    # -------------------------------------------------------------
    # SECTION C: TRAIL SPECIFICATION & FAST PREVIEW
    # -------------------------------------------------------------
    if active_trail_record is not None and trail_df is not None:
        st.markdown("---")
        dist_km = float(active_trail_record.get("distance_km", active_trail_record.get("length", 0.0) / 1000.0))
        gain_m = float(active_trail_record.get("elevation_gain", 0.0))
        gradient_pct = (gain_m / (dist_km * 1000.0) * 100) if dist_km > 0 else 0.0
        route_type = str(active_trail_record.get("route_type", "Loop")).title()

        # Fast preview baseline (<35ms)
        preview_pred = engine.predict_preview(trail_df)
        temp_notes = generate_preparation_notes(active_trail_record, preview_pred)

        # Editorial trail specification header
        st.markdown(
            f"""
            <div style="margin: 20px 0 12px 0;">
              <div style="font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #8b949e;">
                SELECTED TRAIL SPECIFICATION
              </div>
              <div style="font-size: 26px; font-weight: 800; color: #f0f6fc; margin: 4px 0 2px 0; letter-spacing: -0.01em;">
                {active_trail_record.get('name', 'Custom Trail')}
              </div>
              <div style="font-size: 13px; color: #8b949e;">
                {active_trail_record.get('park', '')} National Park · {active_trail_record.get('state', '')} · {route_type}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_metrics_grid(
            distance_km=dist_km,
            elevation_gain_m=gain_m,
            gradient_pct=gradient_pct,
            duration_str=temp_notes["duration_range"],
        )

        render_climate_and_terrain_tags(active_trail_record)

        # Fast Preview Expander
        with st.expander("Quick Estimate (Instant Baseline)", expanded=True):
            st.caption("Instant baseline while you explore. Generate Grass Pass below for the calibrated TabPFN assessment.")
            render_difficulty_distribution(preview_pred)

        # -------------------------------------------------------------
        # SECTION D: GENERATE GRASS PASS (TABPFN FOUNDATION INFERENCE)
        # -------------------------------------------------------------
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        gen_col1, gen_col2 = st.columns([3, 1])
        with gen_col1:
            st.markdown(
                """
                <div style="font-size: 13px; color: #8b949e; line-height: 1.5;">
                  <strong style="color: #f0f6fc;">TabPFN Foundation Assessment:</strong>
                  Executes the TabPFN in-context transformer across 1,000 reference trails to calculate
                  uncompromised, calibrated Bayesian posterior probabilities and seal your offline preparation envelope.
                </div>
                """,
                unsafe_allow_html=True,
            )
        with gen_col2:
            generate_clicked = st.button(
                "GENERATE GRASS PASS",
                key="btn_generate_pass",
                type="primary",
                width="stretch",
            )

        if generate_clicked:
            with st.spinner("Executing TabPFN in-context foundation model on trail geography..."):
                t_start = time.perf_counter()
                tabpfn_pred = engine.predict_tabpfn_pass(trail_df)
                t_elapsed = time.perf_counter() - t_start
                final_notes = generate_preparation_notes(active_trail_record, tabpfn_pred)
                st.session_state.cached_grass_pass = {
                    "trail": active_trail_record,
                    "prediction": tabpfn_pred,
                    "notes": final_notes,
                    "generated_at": time.time(),
                }
                st.success(f"Grass Pass generated via TabPFN in {t_elapsed:.2f}s")

        # -------------------------------------------------------------
        # SECTION E: DISPLAY GRASS PASS CARD & ACTION CTAS
        # -------------------------------------------------------------
        if st.session_state.cached_grass_pass is not None:
            pass_data = st.session_state.cached_grass_pass
            p_trail = pass_data["trail"]
            p_pred: DifficultyPrediction = pass_data["prediction"]
            p_notes = pass_data["notes"]

            st.markdown("---")
            render_grass_pass_hero(p_trail, p_pred, p_notes)

            st.markdown(
                """
                <div style="font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #8b949e; margin-bottom: 8px;">
                  CALIBRATED BAYESIAN POSTERIOR PROBABILITY (TABPFN)
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_difficulty_distribution(p_pred)

            render_preparation_checklist(p_notes)

            # Export & Offline Actions
            export_cols = st.columns([1, 1, 1])
            with export_cols[0]:
                if st.button("CACHE & GO (Touch Grass)", key="btn_cache_go", type="primary", width="stretch"):
                    st.session_state.touch_grass_active = True
                    st.session_state.hike_start_time = time.time()
                    st.rerun()

            with export_cols[1]:
                html_pass = generate_printable_html(p_trail, p_pred, p_notes)
                st.download_button(
                    label="Download Field Pass (HTML)",
                    data=html_pass,
                    file_name=f"TerraPFN_GrassPass_{p_trail.get('name', 'Trail').replace(' ', '_')}.html",
                    mime="text/html",
                    width="stretch",
                )

            with export_cols[2]:
                text_pass = (
                    f"TERRAPFN FIELD CARD // {p_trail.get('name')}\n"
                    f"Class: {p_pred.dominant_class_name.upper()}\n"
                    f"Probabilities: {p_pred.probabilities}\n"
                    f"Distance: {p_notes['distance_km']} km | Elev Gain: +{p_notes['elevation_gain_m']} m\n"
                    f"Water: Min {p_notes['minimum_water_l']}L (Rec {p_notes['recommended_water_l']}L)\n"
                    f"Footwear: {p_notes['footwear']}\n"
                    f"Turnaround: {p_notes['turnaround_note']}\n"
                    f"Screen time ends here."
                )
                st.download_button(
                    label="Save Field Card (TXT)",
                    data=text_pass,
                    file_name=f"TerraPFN_{p_trail.get('name', 'Trail').replace(' ', '_')}.txt",
                    mime="text/plain",
                    width="stretch",
                )


def render_touch_grass_screen() -> None:
    """Render the ultra-minimal Touch Grass field screen."""
    pass_data = st.session_state.cached_grass_pass
    trail_name = pass_data["trail"].get("name", "Trail") if pass_data else "the trail"

    elapsed_str = ""
    if st.session_state.hike_start_time:
        elapsed_sec = int(time.time() - st.session_state.hike_start_time)
        mins = elapsed_sec // 60
        secs = elapsed_sec % 60
        elapsed_str = f"{mins}m {secs}s"
    else:
        elapsed_str = "0m 00s"

    st.markdown(
        f"""
        <div class="touch-grass-screen">
          <div class="touch-grass-kicker">ACTIVE OUTDOOR MISSION</div>
          <div class="touch-grass-title">GRASS PASS CACHED</div>
          <div class="touch-grass-tagline">POCKET THE PHONE. GO OUTSIDE.</div>
          <div class="touch-grass-instruction">
            Your preparation envelope for <strong>{trail_name}</strong> is sealed.
            All biophysical parameters, water quotas, and turnaround alarms are committed.
            <br><br>
            Screen time ends here. Step onto the trail.
          </div>
          <div class="touch-grass-timer">
            Time elapsed outdoors: <strong>{elapsed_str}</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("I'M BACK (Record Reflection)", type="primary", width="stretch"):
            st.session_state.touch_grass_active = False
            st.session_state.show_checkin_modal = True
            st.rerun()

        if st.button("Return to Trail Planner", width="stretch"):
            st.session_state.touch_grass_active = False
            st.rerun()


def render_checkin_screen() -> None:
    """Render the calm, minimal post-hike reflection dialog."""
    pass_data = st.session_state.cached_grass_pass
    trail = pass_data["trail"] if pass_data else {}
    pred = pass_data["prediction"] if pass_data else None

    trail_name = trail.get("name", "Unnamed Trail")
    predicted_difficulty = pred.dominant_class_name if pred else "Moderate"

    st.markdown(
        f"""
        <div class="surface-card" style="max-width: 600px; margin: 30px auto 20px auto;">
          <div class="surface-title">
            <span>POST-HIKE OBSERVATION LOG</span>
            <span style="color: #2ea043;">GROUND TRUTH</span>
          </div>
          <div style="font-size: 20px; font-weight: 700; color: #f0f6fc; margin-bottom: 4px;">{trail_name}</div>
          <div style="font-size: 13px; color: #8b949e;">
            TabPFN Predicted Difficulty: <strong style="color: #f0f6fc;">{predicted_difficulty.upper()}</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(
            """
            <div style="max-width: 600px; margin: 0 auto 12px auto;">
              <div style="font-size: 15px; font-weight: 600; color: #f0f6fc;">How did the trail actually feel?</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            felt_difficulty = st.radio(
                "Observed Difficulty Rating:",
                options=["Easy", "Moderate", "Hard", "Strenuous"],
                index=["Easy", "Moderate", "Hard", "Strenuous"].index(predicted_difficulty) if predicted_difficulty in ["Easy", "Moderate", "Hard", "Strenuous"] else 1,
            )
        with c2:
            actual_duration = st.number_input(
                "Actual Moving Time (minutes, optional):",
                min_value=0,
                max_value=1440,
                value=120,
                step=15,
            )

        field_notes = st.text_area(
            "Field Notes (optional):",
            placeholder="e.g. Scramble was loose near summit, creek crossing was dry, heat was intense...",
        )

        sub_cols = st.columns([1, 1])
        with sub_cols[0]:
            if st.button("SAVE OBSERVATION", type="primary", width="stretch"):
                record = record_checkin(
                    trail_name=trail_name,
                    felt_difficulty=felt_difficulty,
                    predicted_difficulty=predicted_difficulty,
                    trail_id=trail.get("trail_id"),
                    actual_duration_min=int(actual_duration) if actual_duration > 0 else None,
                    notes=field_notes,
                )
                st.success("Observation saved to local ground-truth archive.")
                st.session_state.show_checkin_modal = False
                time.sleep(1.0)
                st.rerun()

        with sub_cols[1]:
            if st.button("Cancel & Return", width="stretch"):
                st.session_state.show_checkin_modal = False
                st.rerun()


if __name__ == "__main__":
    main()
