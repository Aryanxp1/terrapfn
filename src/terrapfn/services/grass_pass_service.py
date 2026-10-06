"""Grass Pass service for generating deterministic preparation envelopes and printable passes.

Converts trail geography and TabPFN calibrated posterior probabilities into
an actionable, offline-safe hiking preparation envelope.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from terrapfn.services.inference_service import DifficultyPrediction


def calculate_duration_range(distance_km: float, elevation_gain_m: float) -> Tuple[float, float, str]:
    """Calculate moving time range using Naismith's Rule with Langmuir corrections."""
    dist = max(distance_km, 0.1)
    gain = max(elevation_gain_m, 0.0)

    # Base rate: 4.5 km/h on flat + 1 hr per 350m vertical ascent
    t_flat = dist / 4.5
    t_vert = gain / 350.0

    steepness = (gain / (dist * 1000.0)) if dist > 0 else 0
    t_descent_penalty = t_flat * 0.10 if steepness > 0.12 else 0.0

    t_est = t_flat + t_vert + t_descent_penalty

    # Range: -15% for brisk pace, +25% for conservative/pack pace
    low_h = max(0.25, t_est * 0.85)
    high_h = max(0.5, t_est * 1.25)

    def _format_time(hours: float) -> str:
        h = int(hours)
        m = int(round((hours - h) * 60 / 5) * 5)
        if m == 60:
            h += 1
            m = 0
        if h == 0:
            return f"{m}m"
        return f"{h}h {m:02d}m" if m > 0 else f"{h}h"

    display_str = f"{_format_time(low_h)} – {_format_time(high_h)}"
    return low_h, high_h, display_str


def calculate_hydration_envelope(
    duration_high_hours: float,
    summer_temp_c: float,
    elevation_gradient: float,
) -> Dict[str, Any]:
    """Calculate deterministic water requirement based on metabolic load and heat."""
    # Baseline: 0.5 L per hour
    rate_l_hr = 0.5

    # Heat adjustment
    if summer_temp_c >= 30.0:
        rate_l_hr += 0.35
    elif summer_temp_c >= 24.0:
        rate_l_hr += 0.20
    elif summer_temp_c < 10.0:
        rate_l_hr -= 0.10

    # Gradient adjustment
    if elevation_gradient >= 0.08:
        rate_l_hr += 0.15

    total_liters = round(duration_high_hours * rate_l_hr * 1.15, 1)  # 15% safety reserve
    min_liters = max(1.0, round(total_liters * 0.75, 1))

    return {
        "recommended_liters": max(total_liters, 1.0),
        "minimum_liters": min_liters,
        "rate_l_hr": round(rate_l_hr, 2),
    }


def generate_preparation_notes(
    trail: Dict[str, Any],
    prediction: DifficultyPrediction,
) -> Dict[str, Any]:
    """Derive deterministic physical guidance from trail and prediction state."""
    dist_km = float(trail.get("length", 0.0)) / 1000.0 if "length" in trail else float(trail.get("distance_km", 1.0))
    dist_km = max(dist_km, 0.1)
    gain_m = float(trail.get("elevation_gain", 0.0))
    gradient = gain_m / (dist_km * 1000.0) if dist_km > 0 else 0.0
    gain_per_km = gain_m / dist_km if dist_km > 0 else 0.0

    summer_temp = float(trail.get("summer_temp", 22.0))
    winter_temp = float(trail.get("winter_temp", -2.0))
    rain_mm = float(trail.get("annual_rain", 600.0))
    snow_mm = float(trail.get("annual_snow", 100.0))

    # 1. Duration
    low_h, high_h, duration_str = calculate_duration_range(dist_km, gain_m)

    # 2. Hydration
    hydration = calculate_hydration_envelope(high_h, summer_temp, gradient)

    # 3. Footwear & Traction
    if gradient > 0.14 or gain_per_km > 100:
        footwear = "Stiff trail boots or alpine runners with deep multidirectional lugs and rock plate."
    elif gradient > 0.07 or gain_per_km > 50:
        footwear = "Lugged trail running shoes or light hiking shoes with toe cap protection."
    else:
        footwear = "Standard cushioned trail runners or supportive walking shoes."

    # 4. Trekking Poles
    poles_needed = (gain_per_km >= 60.0 or gain_m >= 400.0 or dist_km >= 12.0)
    poles_note = (
        "Strongly advised: Trekking poles to reduce knee shear stress and stabilize steep descent."
        if poles_needed else
        "Optional: Moderate terrain; poles not strictly necessary."
    )

    # 5. Pack / Layer Strategy
    layers = []
    if summer_temp > 28.0:
        layers.append("Sun protection: UPF long-sleeve, wide-brim hat, electrolytes.")
    if winter_temp < 2.0 or snow_mm > 150:
        layers.append("Insulation layer: Wind/thermal shell in pack even if base is mild.")
    if rain_mm > 900.0:
        layers.append("Moisture management: Packable taped waterproof shell.")
    if not layers:
        layers.append("Standard 3-layer system: Breathable base layer + light windbreaker.")

    # 6. Daylight & Turnaround Strategy
    daylight_hours = high_h + 1.5  # 90m buffer
    turnaround_note = (
        f"Hard turnaround buffer: Allow {daylight_hours:.1f} hours of total daylight before official sunset. "
        f"Set an uncompromised turnaround watch alarm at {high_h * 0.55:.1f} hours from trailhead."
    )

    # 7. Uncertainty & Bayesian Envelope Explanation
    if prediction.is_borderline and prediction.borderline_details:
        model_insight = (
            f"BORDERLINE TERRAIN: {prediction.borderline_details} "
            f"Equip gear and hydration as if tackling the higher rating."
        )
    else:
        dom_prob = prediction.probabilities.get(prediction.dominant_class_name, 0.0)
        entropy_level = "High Certainty" if prediction.entropy < 0.45 else "Moderate Ambiguity" if prediction.entropy < 0.75 else "High Variance"
        model_insight = (
            f"TabPFN assigns {dom_prob*100:.1f}% posterior probability to '{prediction.dominant_class_name}' "
            f"(Entropy: {prediction.entropy:.2f} — {entropy_level}). "
            f"This profile reflects pure biophysical demand independent of subjective review bias."
        )

    return {
        "distance_km": round(dist_km, 2),
        "elevation_gain_m": round(gain_m, 1),
        "gradient_pct": round(gradient * 100, 1),
        "gain_per_km": round(gain_per_km, 1),
        "duration_range": duration_str,
        "recommended_water_l": hydration["recommended_liters"],
        "minimum_water_l": hydration["minimum_liters"],
        "footwear": footwear,
        "poles_note": poles_note,
        "layer_notes": " • ".join(layers),
        "turnaround_note": turnaround_note,
        "model_insight": model_insight,
        "summer_temp": round(summer_temp, 1),
        "winter_temp": round(winter_temp, 1),
        "annual_rain": round(rain_mm, 0),
        "annual_snow": round(snow_mm, 0),
    }


def generate_printable_html(
    trail: Dict[str, Any],
    prediction: DifficultyPrediction,
    notes: Dict[str, Any],
) -> str:
    """Generate self-contained, print-friendly HTML document for Grass Pass."""
    trail_name = trail.get("name", "Custom Route")
    park_name = trail.get("park", "National Park")
    state_name = trail.get("state", "USA")
    route_type = str(trail.get("route_type", "Loop")).title()

    probs = prediction.probabilities
    p_easy = f"{probs.get('Easy', 0.0)*100:.1f}%"
    p_mod = f"{probs.get('Moderate', 0.0)*100:.1f}%"
    p_hard = f"{probs.get('Hard', 0.0)*100:.1f}%"
    p_stren = f"{probs.get('Strenuous', 0.0)*100:.1f}%"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>TerraPFN Grass Pass — {trail_name}</title>
<style>
  :root {{
    --bg: #0d1117;
    --card: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #2ea043;
    --amber: #d29922;
    --rust: #db6d28;
    --crimson: #f85149;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 24px;
    display: flex;
    justify-content: center;
  }}
  .pass-card {{
    max-width: 680px;
    width: 100%;
    background: var(--card);
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.4);
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 20px;
  }}
  .brand {{
    font-size: 13px;
    font-family: "SF Mono", Consolas, Monaco, monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    font-weight: 700;
  }}
  .trail-title {{
    font-size: 26px;
    font-weight: 800;
    margin-top: 4px;
    color: #ffffff;
    line-height: 1.2;
  }}
  .trail-sub {{
    font-size: 13px;
    color: var(--muted);
    margin-top: 4px;
  }}
  .badge {{
    font-family: monospace;
    font-size: 14px;
    padding: 6px 14px;
    border-radius: 6px;
    font-weight: bold;
    text-transform: uppercase;
    background: #21262d;
    border: 1px solid var(--border);
  }}
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 20px;
  }}
  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 20px;
  }}
  .metric-box {{
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
  }}
  .metric-label {{
    font-size: 10px;
    text-transform: uppercase;
    color: var(--muted);
    letter-spacing: 1px;
    font-weight: 600;
  }}
  .metric-val {{
    font-size: 18px;
    font-weight: 700;
    margin-top: 4px;
    font-family: monospace;
  }}
  .prob-bar {{
    display: flex;
    height: 14px;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 12px;
    border: 1px solid var(--border);
  }}
  .prob-seg {{ height: 100%; transition: width 0.3s; }}
  .seg-easy {{ background: var(--accent); }}
  .seg-mod {{ background: var(--amber); }}
  .seg-hard {{ background: var(--rust); }}
  .seg-stren {{ background: var(--crimson); }}
  .section-title {{
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    font-weight: 700;
    margin-bottom: 8px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 4px;
  }}
  .notes-list {{
    list-style: none;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 20px;
  }}
  .notes-list li {{
    margin-bottom: 8px;
    padding-left: 14px;
    position: relative;
  }}
  .notes-list li::before {{
    content: "■";
    position: absolute;
    left: 0;
    color: var(--accent);
    font-size: 8px;
    top: 5px;
  }}
  .footer {{
    text-align: center;
    border-top: 2px solid var(--border);
    padding-top: 20px;
    margin-top: 10px;
  }}
  .footer-cta {{
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #ffffff;
    text-transform: uppercase;
  }}
  .footer-sub {{
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
    font-style: italic;
  }}
  .print-btn {{
    background: #238636;
    color: #fff;
    border: none;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 14px;
  }}
  .print-btn:hover {{ background: #2ea043; }}
  @media print {{
    body {{ background: #fff; color: #000; padding: 0; }}
    .pass-card {{ border: 2px solid #000; box-shadow: none; background: #fff; color: #000; }}
    .trail-title {{ color: #000; }}
    .metric-box {{ background: #f6f8fa; border: 1px solid #d0d7de; color: #000; }}
    .print-btn {{ display: none; }}
    .brand {{ color: #000; }}
    .footer-cta {{ color: #000; }}
  }}
</style>
</head>
<body>
<div class="pass-card">
  <div class="header">
    <div>
      <div class="brand">TERRAPFN OUTDOOR INTELLIGENCE</div>
      <h1 class="trail-title">{trail_name}</h1>
      <div class="trail-sub">{park_name} • {state_name} • {route_type}</div>
    </div>
    <div class="badge">{prediction.dominant_class_name.upper()}</div>
  </div>

  <div class="section-title">CALIBRATED DIFFICULTY PROBABILITY (TABPFN V2)</div>
  <div class="prob-bar">
    <div class="prob-seg seg-easy" style="width: {p_easy};" title="Easy: {p_easy}"></div>
    <div class="prob-seg seg-mod" style="width: {p_mod};" title="Moderate: {p_mod}"></div>
    <div class="prob-seg seg-hard" style="width: {p_hard};" title="Hard: {p_hard}"></div>
    <div class="prob-seg seg-stren" style="width: {p_stren};" title="Strenuous: {p_stren}"></div>
  </div>
  <div class="grid-4">
    <div class="metric-box">
      <div class="metric-label">Easy</div>
      <div class="metric-val" style="color: var(--accent);">{p_easy}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Moderate</div>
      <div class="metric-val" style="color: var(--amber);">{p_mod}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Hard</div>
      <div class="metric-val" style="color: var(--rust);">{p_hard}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Strenuous</div>
      <div class="metric-val" style="color: var(--crimson);">{p_stren}</div>
    </div>
  </div>

  <div class="section-title">TOPOGRAPHIC PHYSICS</div>
  <div class="grid-4">
    <div class="metric-box">
      <div class="metric-label">Distance</div>
      <div class="metric-val">{notes['distance_km']} km</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Elev Gain</div>
      <div class="metric-val">+{notes['elevation_gain_m']} m</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Avg Grade</div>
      <div class="metric-val">{notes['gradient_pct']}%</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Est Moving Time</div>
      <div class="metric-val" style="font-size:14px;">{notes['duration_range']}</div>
    </div>
  </div>

  <div class="section-title">PREPARATION ENVELOPE</div>
  <ul class="notes-list">
    <li><strong>Hydration Envelope:</strong> Carry minimum <strong>{notes['minimum_water_l']} L</strong> (Recommended: <strong>{notes['recommended_water_l']} L</strong> total fluids).</li>
    <li><strong>Footwear:</strong> {notes['footwear']}</li>
    <li><strong>Trekking Poles:</strong> {notes['poles_note']}</li>
    <li><strong>Pack System:</strong> {notes['layer_notes']}</li>
    <li><strong>Turnaround Protocol:</strong> {notes['turnaround_note']}</li>
    <li><strong>Biophysical Insight:</strong> {notes['model_insight']}</li>
  </ul>

  <div class="footer">
    <div class="footer-cta">CACHE & GO</div>
    <div class="footer-sub">Your screen time ends here. Pocket the phone and hike.</div>
    <button class="print-btn" onclick="window.print()">Print / Save PDF</button>
  </div>
</div>
</body>
</html>"""
    return html
