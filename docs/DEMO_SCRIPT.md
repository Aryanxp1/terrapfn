# TerraPFN — Judge Demo Walkthrough

**Hacktoberfest 2026 Week 1 · Best Use of TabPFN · Touch Grass**
**Author:** Aryan Vishwakarma
**Repository:** https://github.com/Aryanxp1/terrapfn

---

## 60-Second Judge Narrative

> The following script is the canonical walkthrough for evaluating TerraPFN.
> Follow it step-by-step to experience the complete zero-scroll product thesis.

---

### T+00s — Open the App

```
streamlit run src/terrapfn/app/dashboard.py
-> Browser opens at http://localhost:8501
```

**What the judge sees:**
- Dark tactical HUD landing page
- Three mode selectors across the top
- Sidebar showing the verified **5-fold benchmark table** (no fabricated numbers)
- Sidebar philosophy: *"ZERO-SCROLL"*

**First-impression proof points:**
- TabPFN leads on Log Loss (0.7017 vs. 0.8880 for HistGradBoost)
- QWK: 0.7310 (TabPFN) vs. 0.7260 (Random Forest)
- Dummy floor: 0.0055 — confirms our models genuinely solve the task

---

### T+05s — The Problem Statement

The sidebar explains **the real-world pain**:

> *"Traditional outdoor apps trap you in infinite reviews, star-ratings, and social feeds. TerraPFN computes an objective biophysical preparation envelope in seconds."*

No opinion aggregation. No social noise. **One prediction. One printable card. Get outside.**

---

### T+10s — Select a Benchmark Trail

Click **"Curated Benchmark Demos"** (active by default).

Four cards appear — one per difficulty class:

| Card | Trail | Class |
|------|-------|-------|
| Easy | Cascade Falls Trail | Class 1 |
| Moderate | Emerald Lake | Class 3 |
| Hard | Angels Landing (Zion) | Class 5 |
| Strenuous | Half Dome Cables | Class 7 |

**Recommended demo trail: Angels Landing, Zion NP (Hard / Class 5)**

Click **"Select Hard"** -> trail profile loads instantly.

---

### T+15s — Trail Physics Metrics Grid

The four metric tiles update immediately (no spinner):

```
DISTANCE        ELEV. GAIN      AVG GRADE       DURATION EST.
  7.7 km         +488 m           6.3%           2h 45m - 4h 00m
```

Climate and terrain tags render below:
Summer: 28.0C | Winter: 3.0C | Annual Rain: 330mm | Forest | Exposed Ridge

---

### T+20s — Fast Preview (HistGradientBoosting, <10ms)

The **interactive fast preview** expander is open by default.

A live probability bar renders — this is the **<10ms HistGradientBoosting** baseline.
It allows zero-lag browsing across 3,100+ trails while the heavier TabPFN inference
stays reserved for the final Grass Pass.

---

### T+30s — Generate the Grass Pass (TabPFN v2)

Click **"GENERATE GRASS PASS"** (green primary button).

Spinner: "Executing TabPFN v2 in-context foundation model on trail geography..."

**~2.5-3.5 seconds on CPU** — this is real TabPFN v2 in-context inference, not a cached lookup.

Success banner: "Grass Pass generated via TabPFN in 2.83s!"

---

### T+35s — Read the Grass Pass Card

The Grass Pass hero card renders with:

- TabPFN calibrated posterior probability bar (all 4 classes)
- HARD difficulty badge
- HYDRATION ENVELOPE: Min 2.3L / Recommended 3.1L
- FOOTWEAR: Stiff trail boots or alpine runners with rock plate
- TURNAROUND ALARM: Set watch at 2.2h from trailhead

**Why this matters for the judge:**
- TabPFN provides calibrated posterior probabilities — not a single point estimate
- The preparation envelope derives from prediction entropy
- Borderline terrain triggers conservative-side gear escalation automatically

---

### T+45s — Export / Cache and Go

Three action buttons:

| Button | Action |
|--------|--------|
| CACHE AND GO (TOUCH GRASS) | Enters Touch Grass Mode |
| Download Printable Card (HTML) | Self-contained HTML with @media print rules |
| Save Field Card (TXT) | Plain-text card for offline use |

Click **"CACHE AND GO (TOUCH GRASS)"**

---

### T+48s — Touch Grass Mode

The entire screen switches to the zero-distraction lockscreen:

```
TERRAPFN // ACTIVE FIELD MISSION

GRASS PASS CACHED
POCKET THE PHONE. GO OUTSIDE.

Your preparation envelope for Angels Landing is sealed.
Screen time ends right here. Step onto the dirt.

Time elapsed since phone pocketed: 0m 04s
```

This is the core product thesis demonstrated:
> **TabPFN computes. The phone goes away. The human goes hiking.**

---

### T+55s — Post-Hike Check-In (Ground Truth Loop)

Click **"I'M BACK FROM THE HIKE"**

The ground-truth check-in screen appears:
- Select observed difficulty (Easy / Moderate / Hard / Strenuous)
- Enter actual moving time (optional)
- Add field notes

Click **"SAVE OBSERVATION"** -> saved to local JSONL archive.

This creates a persistent ground-truth feedback loop where actual felt difficulty
is compared against TabPFN's prediction over time.

---

### T+60s — Summary for the Judge

| Dimension | TerraPFN |
|-----------|----------|
| **Best Use of TabPFN** | TabPFN v2 calibrated Bayesian posteriors for 4-class trail difficulty; verified superior Log Loss 0.7017 vs next-best 0.7266 |
| **Touch Grass** | Product explicitly terminates screen engagement; zero-scroll philosophy on every screen |
| **Technical Novelty** | Dual-engine: fast preview (<10ms) for browsing + TabPFN foundation inference for final pass |
| **Real Data** | 3,104 US National Parks trails + historical climate data; no synthetic benchmarks |
| **Honest Claims** | All metrics verified 5-fold CV; raw results in data/processed/benchmark_results/ |
| **Product Completeness** | Full export (HTML, TXT), offline-capable, post-hike ground-truth loop |

---

## Printable HTML Card — Regression Verification

The download button produces a self-contained HTML file with:
- @media print stylesheet -> black-on-white for paper/PDF
- Probability bar with all four class segments
- Topographic physics grid (distance, gain, grade, duration)
- Full preparation checklist
- Print / Save PDF button embedded

Verified: no external fonts, no CDN dependencies, fully offline-safe.

---

## Screenshot Reference

| Screenshot | Description |
|------------|-------------|
| 01_landing.png | App landing with benchmark sidebar |
| 02_trail_selected.png | Trail profile with metrics grid |
| 03_tabpfn_prediction.png | TabPFN spinner + success banner |
| 04_grass_pass.png | Full Grass Pass hero card |
| 05_touch_grass_mode.png | Touch Grass lockscreen |
| 06_post_hike_checkin.png | Post-hike ground-truth form |
| 07_benchmark_evidence.png | Sidebar benchmark table close-up |

---

## Running the Full Demo Locally

```bash
# 1. Clone and install
git clone https://github.com/Aryanxp1/terrapfn
cd terrapfn
pip install -e ".[dev]"

# 2. Run all tests (23/23 expected)
pytest tests/ -v

# 3. Launch the app
streamlit run src/terrapfn/app/dashboard.py
```

> **Preparation Guidance Disclaimer:** TerraPFN provides planning guidance derived from
> publicly available trail and climate data. It is not a substitute for professional
> safety assessment. Always hike within your own abilities.

---

*Generated for Phase 4 -- Polish and Judge Validation*
*TerraPFN - Hacktoberfest 2026 Week 1*
