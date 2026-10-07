"""Reusable UI components for the TerraPFN outdoor intelligence interface.

Follows a restrained, editorial design system inspired by expedition field cards,
modern topographical specifications, and technical trail navigation.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
import streamlit as st

from terrapfn.services.inference_service import DifficultyPrediction

# Restrained semantic colors
CLASS_COLORS = {
    "Easy": "#2ea043",        # Natural Forest
    "Moderate": "#d29922",    # Topo Amber
    "Hard": "#c95d22",        # Terracotta Rust
    "Strenuous": "#cf4a43",   # Deep Crimson
}

CLASS_BACKGROUNDS = {
    "Easy": "rgba(46, 160, 67, 0.12)",
    "Moderate": "rgba(210, 153, 34, 0.12)",
    "Hard": "rgba(201, 93, 34, 0.12)",
    "Strenuous": "rgba(207, 74, 67, 0.12)",
}

CLASS_BORDERS = {
    "Easy": "rgba(46, 160, 67, 0.35)",
    "Moderate": "rgba(210, 153, 34, 0.35)",
    "Hard": "rgba(201, 93, 34, 0.35)",
    "Strenuous": "rgba(207, 74, 67, 0.35)",
}


def render_header() -> None:
    """Render top editorial header communicating the product purpose."""
    st.markdown(
        """
        <div class="editorial-header">
          <div class="brand-kicker">
            <span>TERRAPFN</span>
            <span class="kicker-tag">BEST USE OF TABPFN · TOUCH GRASS</span>
          </div>
          <h1 class="editorial-title">Know the trail. Get outside.</h1>
          <div class="editorial-lead">
            TabPFN-powered trail difficulty intelligence that turns a few seconds of planning
            into an offline field pass. Compute your biophysical envelope, pocket your phone, and hike.
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
    """Render clean 4-column topographic specification grid."""
    st.markdown(
        f"""
        <div class="spec-grid">
          <div class="spec-tile">
            <div class="spec-label">Distance</div>
            <div class="spec-value">{distance_km:.2f} <span class="spec-unit">km</span></div>
          </div>
          <div class="spec-tile">
            <div class="spec-label">Elevation Gain</div>
            <div class="spec-value">+{elevation_gain_m:.0f} <span class="spec-unit">m</span></div>
          </div>
          <div class="spec-tile">
            <div class="spec-label">Average Slope</div>
            <div class="spec-value">{gradient_pct:.1f}<span class="spec-unit">%</span></div>
          </div>
          <div class="spec-tile">
            <div class="spec-label">Estimated Moving Time</div>
            <div class="spec-value" style="font-size: 16px; padding-top: 4px;">{duration_str}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_difficulty_distribution(prediction: DifficultyPrediction) -> None:
    """Render scientific posterior probability distribution with restrained tones."""
    probs = prediction.probabilities
    p_easy = probs.get("Easy", 0.0)
    p_mod = probs.get("Moderate", 0.0)
    p_hard = probs.get("Hard", 0.0)
    p_stren = probs.get("Strenuous", 0.0)

    classes_data = [
        ("Easy", p_easy),
        ("Moderate", p_mod),
        ("Hard", p_hard),
        ("Strenuous", p_stren),
    ]

    # Clean multi-row scientific probability gauge
    rows_html = []
    for cls_name, cls_prob in classes_data:
        is_dom = cls_name == prediction.dominant_class_name
        bar_fill_color = CLASS_COLORS[cls_name] if is_dom else "#30363d"
        text_weight = "600" if is_dom else "400"
        text_color = "#f0f6fc" if is_dom else "#8b949e"
        pct_color = CLASS_COLORS[cls_name] if is_dom else "#8b949e"

        rows_html.append(
            f'<div class="posterior-row">'
            f'<div class="posterior-label" style="font-weight:{text_weight}; color:{text_color};">{cls_name}</div>'
            f'<div class="posterior-track">'
            f'<div class="posterior-fill" style="width: {cls_prob * 100:.1f}%; background: {bar_fill_color};"></div>'
            f'</div>'
            f'<div class="posterior-pct" style="color: {pct_color};">{cls_prob * 100:.1f}%</div>'
            f'</div>'
        )

    all_rows = "".join(rows_html)
    st.markdown(f'<div class="posterior-container">{all_rows}</div>', unsafe_allow_html=True)

    # Statistical metadata line
    meta_cols = st.columns([2, 1, 1])
    with meta_cols[0]:
        st.caption(f"Engine: **{prediction.model_name}** ({prediction.inference_time_ms:.1f} ms)")
    with meta_cols[1]:
        st.caption(f"Shannon Entropy: **{prediction.entropy:.2f}** / 1.00")
    with meta_cols[2]:
        st.caption(f"Confidence Margin: **{prediction.confidence_margin * 100:.1f}%**")

    # Borderline notification if applicable
    if prediction.is_borderline and prediction.borderline_details:
        st.markdown(
            f"""
            <div style="background: rgba(210, 153, 34, 0.1); border: 1px solid rgba(210, 153, 34, 0.3); border-radius: 6px; padding: 10px 14px; font-size: 13px; color: #d29922; margin-top: 8px;">
              <strong>Notice:</strong> {prediction.borderline_details} Preparation guidance is calibrated to the higher difficulty envelope.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_climate_and_terrain_tags(trail: Dict[str, Any]) -> None:
    """Render environmental climate tags and biome indicators without emojis."""
    summer = trail.get("summer_temp", 22.0)
    winter = trail.get("winter_temp", -2.0)
    rain = trail.get("annual_rain", 600.0)
    snow = trail.get("annual_snow", 100.0)

    st.markdown(
        f"""
        <div style="display:flex; flex-wrap:wrap; gap:8px; margin: 12px 0 10px 0;">
          <span style="background:#161b22; border:1px solid #30363d; padding:4px 10px; border-radius:4px; font-size:12px; color:#8b949e;">Summer Avg: <strong style="color:#f0f6fc;">{summer:.1f}°C</strong></span>
          <span style="background:#161b22; border:1px solid #30363d; padding:4px 10px; border-radius:4px; font-size:12px; color:#8b949e;">Winter Avg: <strong style="color:#f0f6fc;">{winter:.1f}°C</strong></span>
          <span style="background:#161b22; border:1px solid #30363d; padding:4px 10px; border-radius:4px; font-size:12px; color:#8b949e;">Precipitation: <strong style="color:#f0f6fc;">{rain:.0f} mm/yr</strong></span>
          <span style="background:#161b22; border:1px solid #30363d; padding:4px 10px; border-radius:4px; font-size:12px; color:#8b949e;">Snowfall: <strong style="color:#f0f6fc;">{snow:.0f} mm/yr</strong></span>
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
        tags_html = " ".join([
            f"<span style='background:rgba(46, 160, 67, 0.08); border:1px solid rgba(46, 160, 67, 0.25); color:#7ee787; padding:3px 9px; border-radius:4px; font-size:11px;'>{b}</span>"
            for b in biomes
        ])
        st.markdown(f"<div style='margin-bottom:14px;'>{tags_html}</div>", unsafe_allow_html=True)


def render_grass_pass_hero(
    trail: Dict[str, Any],
    prediction: DifficultyPrediction,
    notes: Dict[str, Any],
) -> None:
    """Render the Grass Pass signature field card header."""
    trail_name = trail.get("name", "Custom Route")
    park_name = trail.get("park", "National Park")
    state_name = trail.get("state", "USA")
    route_type = str(trail.get("route_type", "Loop")).title()
    dom_class = prediction.dominant_class_name
    badge_color = CLASS_COLORS.get(dom_class, "#2ea043")
    badge_bg = CLASS_BACKGROUNDS.get(dom_class, "rgba(46, 160, 67, 0.12)")
    badge_border = CLASS_BORDERS.get(dom_class, "rgba(46, 160, 67, 0.35)")

    st.markdown(
        f"""
        <div class="field-pass-card">
          <div class="field-pass-header">
            <div>
              <div class="field-pass-kicker">TABPFN IN-CONTEXT ASSESSMENT</div>
              <div class="field-pass-trail-name">{trail_name}</div>
              <div class="field-pass-trail-loc">{park_name} · {state_name} · {route_type}</div>
            </div>
            <div class="field-pass-badge" style="background:{badge_bg}; color:{badge_color}; border-color:{badge_border};">
              {dom_class.upper()}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_preparation_checklist(notes: Dict[str, Any]) -> None:
    """Render the deterministic physical preparation envelope as a clean field document."""
    st.markdown(
        f"""
        <div class="surface-card">
          <div class="surface-title">
            <span>Offline Preparation Envelope</span>
            <span style="color:#2ea043; font-size:11px; font-weight:600;">CALIBRATED GUIDANCE</span>
          </div>
          <div class="field-prep-list">
            <div class="field-prep-row">
              <div class="field-prep-key">Hydration</div>
              <div class="field-prep-value">
                Carry minimum <strong>{notes['minimum_water_l']} L</strong> (Recommended: <strong>{notes['recommended_water_l']} L</strong> based on duration and metabolic thermal load).
              </div>
            </div>
            <div class="field-prep-row">
              <div class="field-prep-key">Footwear</div>
              <div class="field-prep-value">{notes['footwear']}</div>
            </div>
            <div class="field-prep-row">
              <div class="field-prep-key">Trekking Poles</div>
              <div class="field-prep-value">{notes['poles_note']}</div>
            </div>
            <div class="field-prep-row">
              <div class="field-prep-key">Pack & Layers</div>
              <div class="field-prep-value">{notes['layer_notes']}</div>
            </div>
            <div class="field-prep-row">
              <div class="field-prep-key">Turnaround</div>
              <div class="field-prep-value">{notes['turnaround_note']}</div>
            </div>
            <div class="field-prep-row">
              <div class="field-prep-key">Model Insight</div>
              <div class="field-prep-value" style="color:#8b949e;">{notes['model_insight']}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
