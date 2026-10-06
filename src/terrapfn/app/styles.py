"""Custom tactical outdoor CSS styling for TerraPFN Streamlit interface.

Inspired by topographic charts, field compasses, and minimalist HUD instruments.
"""

TACTICAL_CSS = """
<style>
/* Base Streamlit theme overrides */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg-primary: #0a0d12;
  --bg-surface: #121721;
  --bg-card: #181f2c;
  --border-muted: #263042;
  --border-focus: #3d4d68;
  --text-main: #f0f6fc;
  --text-muted: #8b949e;
  --text-dim: #656d76;
  --pine-green: #2ea043;
  --topo-amber: #d29922;
  --mesa-rust: #db6d28;
  --alpine-crimson: #f85149;
  --cyan-accent: #38bdf8;
}

/* Overall container */
.stApp {
  background-color: var(--bg-primary);
  color: var(--text-main);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header & Brand HUD */
.hud-header {
  border-bottom: 2px solid var(--border-muted);
  padding-bottom: 16px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 2px;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  background: rgba(46, 160, 67, 0.15);
  color: var(--pine-green);
  border: 1px solid var(--pine-green);
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 1px;
  font-weight: 700;
}

.brand-subtitle {
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 4px;
  line-height: 1.4;
}

/* Tactical cards */
.tactical-card {
  background: var(--bg-card);
  border: 1px solid var(--border-muted);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.tactical-card-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-muted);
  margin-bottom: 14px;
  border-bottom: 1px solid var(--border-muted);
  padding-bottom: 6px;
  display: flex;
  justify-content: space-between;
}

/* Metrics grid */
.metric-tile {
  background: var(--bg-surface);
  border: 1px solid var(--border-muted);
  border-radius: 6px;
  padding: 12px 14px;
  text-align: center;
}

.metric-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  font-weight: 600;
}

.metric-number {
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  font-weight: 800;
  color: #ffffff;
  margin-top: 4px;
}

.metric-unit {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: normal;
}

/* Difficulty distribution meter */
.dist-meter-container {
  margin: 16px 0;
}

.dist-bar-wrapper {
  display: flex;
  height: 18px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid var(--border-muted);
  background: #000;
}

.dist-seg {
  height: 100%;
  transition: width 0.4s ease;
}

.dist-seg-easy { background: var(--pine-green); }
.dist-seg-mod { background: var(--topo-amber); }
.dist-seg-hard { background: var(--mesa-rust); }
.dist-seg-stren { background: var(--alpine-crimson); }

.dist-labels-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-top: 10px;
}

.dist-chip {
  background: var(--bg-surface);
  border: 1px solid var(--border-muted);
  border-radius: 6px;
  padding: 8px;
  text-align: center;
}

.chip-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.chip-pct {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 800;
  margin-top: 2px;
}

/* Grass Pass Hero Card */
.grass-pass-hero {
  background: #0d121c;
  border: 2px solid var(--border-focus);
  border-left: 6px solid var(--pine-green);
  border-radius: 10px;
  padding: 24px;
  margin: 20px 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.pass-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--border-muted);
  padding-bottom: 14px;
}

.pass-trail-name {
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.2;
}

.pass-trail-sub {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 4px;
  font-family: 'JetBrains Mono', monospace;
}

.pass-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 800;
  padding: 6px 14px;
  border-radius: 6px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #fff;
}

/* Preparation Notes */
.prep-item {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 14px;
  line-height: 1.5;
}

.prep-icon {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--pine-green);
  font-weight: bold;
}

/* Touch Grass Mode Screen */
.touch-grass-screen {
  text-align: center;
  padding: 60px 20px;
  background: radial-gradient(circle at center, #131d16 0%, #0a0d12 70%);
  border: 2px solid var(--pine-green);
  border-radius: 12px;
  margin: 30px 0;
}

.touch-grass-title {
  font-size: 32px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 1px;
}

.touch-grass-tagline {
  font-size: 18px;
  color: var(--pine-green);
  font-weight: 600;
  margin: 12px 0 24px 0;
  font-family: 'JetBrains Mono', monospace;
}

.touch-grass-instruction {
  font-size: 15px;
  color: var(--text-muted);
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Custom buttons */
.stButton > button {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  letter-spacing: 1px;
  border-radius: 6px;
  transition: all 0.2s ease;
}
</style>
"""
