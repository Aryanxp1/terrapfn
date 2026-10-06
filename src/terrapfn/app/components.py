"""Reusable UI components for the TerraPFN tactical dashboard."""

from __future__ import annotations

from typing import Any, Dict, Optional
import streamlit as st

from terrapfn.services.inference_service import DifficultyPrediction

CLASS_COLORS = {
    "Easy": "#2ea043",        # Pine Green
    "Moderate": "#d29922",    # Topo Amber
    "Hard": "#db6d28",        # Mesa Rust
    "Strenuous": "#f85149",   # Alpine Crimson
}


def render_header() -> None:
    """Render top tactical HUD header with brand identity."""
    st.markdown(
        """
        <div class="hud-header">
          <div>
            <div class="brand-title">
              <span>TERRAPFN</span>
              <span class="brand-badge">TOUCH GRASS // WEEK 1</span>
            </div>
            <div class="brand-subtitle">
              Zero-scroll outdoor trail intelligence powered by TabPFN foundation models.
              Get your evidence-based preparation envelope and get off your screen.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics_grid(
    distance_km: float,
    elevation_gain_m: float,
    gradient_pct: float,
    duration_str: str,
) -> None:
    """Render 4-column topographic physical metric grid."""
    cols = st.columns(4)
    with cols[0]:
        st.markdown(
            f"""
            <div class="metric-tile">
              <div class="metric-label">DISTANCE</div>
              <div class="metric-number">{distance_km:.2f} <span class="metric-unit">km</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            f"""
            <div class="metric-tile">
              <div class="metric-label">ELEV GAIN</div>
              <div class="metric-number">+{elevation_gain_m:.0f} <span class="metric-unit">m</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            f"""
            <div class="metric-tile">
              <div class="metric-label">AVG SLOPE</div>
              <div class="metric-number">{gradient_pct:.1f}<span class="metric-unit">%</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[3]:
        st.markdown(
            f"""
            <div class="metric-tile">
              <div class="metric-label">MOVING TIME</div>
              <div class="metric-number" style="font-size: 16px; margin-top:8px;">{duration_str}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_difficulty_distribution(prediction: DifficultyPrediction) -> None:
    """Render calibrated multi-class difficulty posterior distribution."""
    probs = prediction.probabilities
    p_easy = probs.get("Easy", 0.0)
    p_mod = probs.get("Moderate", 0.0)
    p_hard = probs.get("Hard", 0.0)
    p_stren = probs.get("Strenuous", 0.0)

    # Meter HTML
    st.markdown(
        f"""
        <div class="dist-meter-container">
          <div class="dist-bar-wrapper">
            <div class="dist-seg dist-seg-easy" style="width: {p_easy * 100:.1f}%;" title="Easy: {p_easy * 100:.1f}%"></div>
            <div class="dist-seg dist-seg-mod" style="width: {p_mod * 100:.1f}%;" title="Moderate: {p_mod * 100:.1f}%"></div>
            <div class="dist-seg dist-seg-hard" style="width: {p_hard * 100:.1f}%;" title="Hard: {p_hard * 100:.1f}%"></div>
            <div class="dist-seg dist-seg-stren" style="width: {p_stren * 100:.1f}%;" title="Strenuous: {p_stren * 100:.1f}%"></div>
          </div>
          <div class="dist-labels-grid">
            <div class="dist-chip">
              <div class="chip-name" style="color: {CLASS_COLORS['Easy']};">Easy</div>
              <div class="chip-pct">{p_easy * 100:.1f}%</div>
            </div>
            <div class="dist-chip">
              <div class="chip-name" style="color: {CLASS_COLORS['Moderate']};">Moderate</div>
              <div class="chip-pct">{p_mod * 100:.1f}%</div>
            </div>
            <div class="dist-chip">
              <div class="chip-name" style="color: {CLASS_COLORS['Hard']};">Hard</div>
              <div class="chip-pct">{p_hard * 100:.1f}%</div>
            </div>
            <div class="dist-chip">
              <div class="chip-name" style="color: {CLASS_COLORS['Strenuous']};">Strenuous</div>
              <div class="chip-pct">{p_stren * 100:.1f}%</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Statistical metadata badge
    subcols = st.columns([2, 1, 1])
    with subcols[0]:
        st.caption(f"🧠 Engine: **{prediction.model_name}** ({prediction.inference_time_ms:.1f} ms)")
    with subcols[1]:
        st.caption(f"Entropy: **{prediction.entropy:.2f}** / 1.00")
    with subcols[2]:
        st.caption(f"Margin: **{prediction.confidence_margin * 100:.1f}%**")

    if prediction.is_borderline and prediction.borderline_details:
        st.warning(f"⚠️ {prediction.borderline_details}")


def render_climate_and_terrain_tags(trail: Dict[str, Any]) -> None:
    """Render environmental reanalysis badges and biome flags."""
    summer = trail.get("summer_temp", 22.0)
    winter = trail.get("winter_temp", -2.0)
    rain = trail.get("annual_rain", 600.0)
    snow = trail.get("annual_snow", 100.0)

    st.markdown(
        f"""
        <div style="display:flex; flex-wrap:wrap; gap:8px; margin: 10px 0;">
          <span style="background:#161f2e; border:1px solid #2b3952; padding:4px 10px; border-radius:4px; font-size:12px; font-family:monospace;">☀️ Summer: {summer:.1f}°C</span>
          <span style="background:#161f2e; border:1px solid #2b3952; padding:4px 10px; border-radius:4px; font-size:12px; font-family:monospace;">❄️ Winter: {winter:.1f}°C</span>
          <span style="background:#161f2e; border:1px solid #2b3952; padding:4px 10px; border-radius:4px; font-size:12px; font-family:monospace;">🌧️ Rain: {rain:.0f} mm/yr</span>
          <span style="background:#161f2e; border:1px solid #2b3952; padding:4px 10px; border-radius:4px; font-size:12px; font-family:monospace;">🌨️ Snow: {snow:.0f} mm/yr</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Biome tags
    biomes = []
    for k in ["forest", "river", "lake", "waterfall", "beach", "cave", "historic_site", "hot_spring"]:
        if trail.get(k) == 1:
            biomes.append(k.replace("_", " ").title())
    if trail.get("backpacking") == 1:
        biomes.append("Backpacking")

    if biomes:
        tags_html = " ".join([f"<span style='background:#1b241e; border:1px solid #2ea043; color:#7ee787; padding:2px 8px; border-radius:4px; font-size:11px; font-family:monospace;'>{b}</span>" for b in biomes])
        st.markdown(f"<div style='margin-bottom:12px;'>{tags_html}</div>", unsafe_allow_html=True)


def render_grass_pass_hero(
    trail: Dict[str, Any],
    prediction: DifficultyPrediction,
    notes: Dict[str, Any],
) -> None:
    """Render the full Grass Pass hero block on the dashboard."""
    trail_name = trail.get("name", "Custom Route")
    park_name = trail.get("park", "National Park")
    state_name = trail.get("state", "USA")
    route_type = str(trail.get("route_type", "Loop")).title()
    dom_class = prediction.dominant_class_name
    badge_color = CLASS_COLORS.get(dom_class, "#2ea043")

    st.markdown(
        f"""
        <div class="grass-pass-hero" style="border-left: 6px solid {badge_color};">
          <div class="pass-header">
            <div>
              <div style="font-family:monospace; font-size:11px; letter-spacing:2px; color:{badge_color}; font-weight:700;">
                GRASS PASS // VERIFIED FIELD CARD
              </div>
              <div class="pass-trail-name">{trail_name}</div>
              <div class="pass-trail-sub">{park_name} • {state_name} • {route_type}</div>
            </div>
            <div class="pass-badge" style="background:{badge_color};">{dom_class.upper()}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_preparation_checklist(notes: Dict[str, Any]) -> None:
    """Render the deterministic physical preparation points."""
    st.markdown(
        f"""
        <div class="tactical-card">
          <div class="tactical-card-title">
            <span>OFFLINE PREPARATION ENVELOPE</span>
            <span style="color:#2ea043;">FIELD-READY</span>
          </div>
          <div class="prep-item">
            <div class="prep-icon">💧</div>
            <div><strong>Hydration Requirement:</strong> Carry at least <strong>{notes['minimum_water_l']} Liters</strong> (Recommended <strong>{notes['recommended_water_l']} Liters</strong> based on duration and heat load).</div>
          </div>
          <div class="prep-item">
            <div class="prep-icon">🥾</div>
            <div><strong>Footwear & Traction:</strong> {notes['footwear']}</div>
          </div>
          <div class="prep-item">
            <div class="prep-icon">🥢</div>
            <div><strong>Trekking Poles:</strong> {notes['poles_note']}</div>
          </div>
          <div class="prep-item">
            <div class="prep-icon">🎒</div>
            <div><strong>Layer System:</strong> {notes['layer_notes']}</div>
          </div>
          <div class="prep-item">
            <div class="prep-icon">⏱️</div>
            <div><strong>Turnaround Watch Alarm:</strong> {notes['turnaround_note']}</div>
          </div>
          <div class="prep-item">
            <div class="prep-icon">📊</div>
            <div><strong>Model Rationalization:</strong> {notes['model_insight']}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
