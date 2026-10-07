"""Premium outdoor design system and styling for TerraPFN Streamlit interface.

Inspired by modern trail cartography, editorial expedition documentation,
and minimal, high-contrast technical instrumentation.
"""

from __future__ import annotations

PREMIUM_OUTDOOR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
  --bg-canvas: #0d1117;
  --bg-surface: #161b22;
  --bg-surface-elevated: #1c2128;
  --border-subtle: #272d37;
  --border-rule: #30363d;
  --text-primary: #f0f6fc;
  --text-secondary: #8b949e;
  --text-muted: #6e7681;
  --forest-green: #2ea043;
  --forest-green-muted: rgba(46, 160, 67, 0.12);
  --forest-green-border: rgba(46, 160, 67, 0.35);
  --amber-caution: #d29922;
  --amber-caution-muted: rgba(210, 153, 34, 0.12);
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace;
}

/* Base application styling */
.stApp {
  background-color: var(--bg-canvas);
  color: var(--text-primary);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
}

/* Header & Editorial Hero */
.editorial-header {
  padding: 12px 0 24px 0;
  border-bottom: 1px solid var(--border-rule);
  margin-bottom: 24px;
}

.brand-kicker {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--forest-green);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-kicker span.kicker-tag {
  background: var(--forest-green-muted);
  border: 1px solid var(--forest-green-border);
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 10px;
}

.editorial-title {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.2;
}

.editorial-lead {
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin-top: 6px;
  max-width: 680px;
}

/* Specification Grid */
.spec-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin: 16px 0;
}

@media (max-width: 768px) {
  .spec-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.spec-tile {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  padding: 14px 16px;
  transition: border-color 0.15s ease;
}

.spec-tile:hover {
  border-color: var(--border-rule);
}

.spec-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: 4px;
}

.spec-value {
  font-family: var(--font-mono);
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.spec-unit {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 400;
  margin-left: 2px;
}

/* Surface containers */
.surface-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.surface-title {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-bottom: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Curated Demo Trail Cards */
.trail-card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin: 14px 0 20px 0;
}

@media (max-width: 768px) {
  .trail-card-grid {
    grid-template-columns: 1fr;
  }
}

.trail-selection-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  padding: 14px;
  transition: all 0.15s ease;
  cursor: pointer;
}

.trail-selection-card.active {
  background: var(--bg-surface-elevated);
  border-color: var(--forest-green);
  box-shadow: 0 0 0 1px var(--forest-green);
}

.trail-class-pill {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 6px;
}

.trail-card-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.3;
  margin-bottom: 4px;
}

.trail-card-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

/* Scientific Posterior Distribution */
.posterior-container {
  margin: 16px 0;
}

.posterior-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 13px;
}

.posterior-label {
  width: 90px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  text-align: right;
}

.posterior-track {
  flex: 1;
  height: 8px;
  background: #21262d;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.posterior-fill {
  height: 100%;
  border-radius: 4px;
  background: #38414e;
  transition: width 0.3s ease;
}

.posterior-fill.dominant {
  background: var(--forest-green);
}

.posterior-pct {
  width: 50px;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
}

/* Grass Pass Signature Field Card */
.field-pass-card {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-rule);
  border-radius: 8px;
  padding: 24px;
  margin: 20px 0;
}

.field-pass-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-rule);
  margin-bottom: 18px;
}

.field-pass-kicker {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--forest-green);
  margin-bottom: 4px;
}

.field-pass-trail-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.field-pass-trail-loc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.field-pass-badge {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 6px;
  border: 1px solid transparent;
}

/* Field Preparation Rows */
.field-prep-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 16px 0;
}

.field-prep-row {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 10px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
}

.field-prep-key {
  min-width: 110px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  color: var(--text-secondary);
  padding-top: 1px;
}

.field-prep-value {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-primary);
  flex: 1;
}

/* Touch Grass Field Screenlock */
.touch-grass-screen {
  text-align: center;
  padding: 70px 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border-rule);
  border-radius: 12px;
  margin: 40px auto;
  max-width: 640px;
}

.touch-grass-kicker {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--forest-green);
  margin-bottom: 12px;
}

.touch-grass-title {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  line-height: 1.15;
}

.touch-grass-tagline {
  font-size: 20px;
  color: var(--text-primary);
  font-weight: 700;
  margin: 12px 0 20px 0;
  letter-spacing: -0.01em;
}

.touch-grass-instruction {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
  max-width: 480px;
  margin: 0 auto 28px auto;
}

.touch-grass-timer {
  font-family: var(--font-mono);
  font-size: 14px;
  color: var(--text-muted);
  padding: 8px 16px;
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 28px;
}

/* Streamlit button customization */
button[data-testid="stBaseButton-secondary"],
div[data-testid="stButton"] > button {
  font-family: var(--font-sans) !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.2px !important;
  border-radius: 6px !important;
  transition: all 0.15s ease !important;
  background-color: #21262d !important;
  color: #f0f6fc !important;
  border: 1px solid #30363d !important;
  padding: 8px 16px !important;
}

button[data-testid="stBaseButton-secondary"]:hover,
div[data-testid="stButton"] > button:hover {
  background-color: #30363d !important;
  border-color: #484f58 !important;
  color: #ffffff !important;
}

button[data-testid="stBaseButton-primary"],
div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"] {
  background-color: #238636 !important;
  color: #ffffff !important;
  border: 1px solid #2ea043 !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  box-shadow: none !important;
}

button[data-testid="stBaseButton-primary"]:hover,
div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"]:hover {
  background-color: #2ea043 !important;
  border-color: #3fb950 !important;
  color: #ffffff !important;
}

/* Download button */
div[data-testid="stDownloadButton"] > button {
  font-family: var(--font-sans) !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  background-color: #161b22 !important;
  border: 1px solid #30363d !important;
  color: #f0f6fc !important;
  border-radius: 6px !important;
}

div[data-testid="stDownloadButton"] > button:hover {
  background-color: #21262d !important;
  border-color: #484f58 !important;
}

/* Streamlit Header chrome */
header[data-testid="stHeader"] {
  background-color: transparent !important;
}

/* Sidebar refined styling */
section[data-testid="stSidebar"] {
  background-color: #0b0f14 !important;
  border-right: 1px solid #21262d !important;
}

.sidebar-title {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #f0f6fc;
  padding-bottom: 8px;
  border-bottom: 1px solid #21262d;
  margin-bottom: 12px;
}

.sidebar-section-title {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #8b949e;
  margin-bottom: 8px;
}

.sidebar-evidence-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
  margin: 8px 0;
}

.sidebar-evidence-table th {
  padding: 4px 2px;
  text-align: left;
  color: #8b949e;
  border-bottom: 1px solid #21262d;
  font-weight: 500;
}

.sidebar-evidence-table td {
  padding: 5px 2px;
  border-bottom: 1px solid #161b22;
  font-family: var(--font-mono);
}

.sidebar-evidence-table tr.highlight {
  color: #3fb950;
  font-weight: 600;
}
</style>
"""

# Backwards compatibility alias
TACTICAL_CSS = PREMIUM_OUTDOOR_CSS
