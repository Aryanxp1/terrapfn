# TerraPFN Development Roadmap

**Project Name:** TerraPFN  
**GitHub Repository:** [Aryanxp1/terrapfn](https://github.com/Aryanxp1/terrapfn)  
**Author & Lead Architect:** [Aryan Vishwakarma](https://github.com/Aryanxp1)  
**Hacktoberfest 2026 Category:** Best Use of TabPFN | **Theme:** Touch Grass  
**Positioning:** A TabPFN-powered zero-scroll outdoor trail intelligence system.

---

## Roadmap Overview: The 5 Project Phases

The development and delivery of TerraPFN is organized into **EXACTLY five major phases**. No additional numbered phases exist.

```mermaid
flowchart LR
    P1[Phase 1: Repository & Foundation] --> P2[Phase 2: ML & TabPFN]
    P2 --> P3[Phase 3: Product & UX]
    P3 --> P4[Phase 4: Polish & Judge Validation]
    P4 --> P5[Phase 5: Deployment & Submission]
    
    classDef complete fill:#238636,stroke:#2ea043,color:#fff;
    classDef inprogress fill:#d29922,stroke:#e3b341,color:#fff;
    classDef notstarted fill:#30363d,stroke:#8b949e,color:#8b949e;
    
    class P1,P2,P3 complete;
    class P4 inprogress;
    class P5 notstarted;
```

---

## Phase 1 — Repository & Foundation
**Status:** `COMPLETE`

- [x] **New Repository:** Fresh repository created and initialized with Aryan Vishwakarma as author.
- [x] **Project Structure:** Clean modular layout (`src/terrapfn/`, `tests/`, `data/`, `scripts/`, `docs/`).
- [x] **Provenance & Attribution:** Complete provenance record in `ATTRIBUTION.md` documenting open data sources (Jane's AllTrails, Open-Meteo CC BY 4.0) and reference architecture permissions.
- [x] **Licensing:** Standard MIT License in `LICENSE`.
- [x] **Clean Data Assets:** Sanitized raw CSVs in `data/raw/` (`national_parks_trails.csv`, `national_parks_climate.csv`, `hiker_benchmark_profiles.csv`, `candidate_routes.csv`).
- [x] **Engineering Foundation:** Declarative packaging via `pyproject.toml` with editable installation.

---

## Phase 2 — ML & TabPFN
**Status:** `COMPLETE`

- [x] **Data Preprocessing:** Leakage-free `TrailFeaturePreprocessor` with topographic physical feature derivation (`distance_km`, `elevation_gradient`, `elevation_gain_per_km`), fitted strictly on training folds.
- [x] **Baseline Models:** Implemented and standardized Stratified Dummy, Logistic Regression, Random Forest, and HistGradientBoosting classifiers.
- [x] **TabPFN Integration:** Created `TabPFNClassifierWrapper` isolating TabPFN v2 foundation model with CPU optimizations (`n_estimators=2`, `ignore_pretraining_limits=True`).
- [x] **Leakage-Free Evaluation:** Stratified 5-Fold cross-validation harness (`nested_cv.py`) with zero holdout test-set contamination.
- [x] **Benchmark Results:** Complete 5-fold evaluation executed and saved to `data/processed/benchmark_results/` showing TabPFN leads in QWK (0.7310), Balanced Accuracy (55.15%), Log Loss (0.7017), and Brier Score (0.4207).

---

## Phase 3 — Product & UX
**Status:** `COMPLETE`

- [x] **Trail Intelligence Interface:** Streamlit tactical outdoor dashboard (`src/terrapfn/app/dashboard.py`) with 3,104-trail catalog explorer and custom route synthesizer.
- [x] **Fast Preview:** Responsive `<10ms` preview engine powered by HistGradientBoosting for instantaneous slider feedback.
- [x] **TabPFN Grass Pass:** Deep Bayesian foundation model inference producing calibrated multi-class probability distributions, Shannon entropy diagnostics, and deterministic physical preparation envelopes (water quotas, footwear, poles, turnaround alarms).
- [x] **Touch Grass Mode:** Minimalist screen-lock transition screen encouraging hikers to pocket their phones, with an active offline hike timer.
- [x] **Post-Hike Observation:** Ground-truth post-hike check-in logging perceived exertion and notes to local structured storage (`data/processed/hike_checkins.json`).

---

## Phase 4 — Polish & Judge Validation
**Status:** `IN PROGRESS`

- [x] **Visual Polish:** Tactical dark outdoor design system (`src/terrapfn/app/styles.py`) with monospaced HUD typography, topo surface colors, and print-friendly export styling.
- [x] **Demo Optimization:** 4 curated ground-truth demo trails pre-configured for judges (Delicate Arch, Emerald Lake, Angels Landing, Half Dome).
- [x] **Performance:** Fast CPU inference caching via Streamlit `@st.cache_resource` and subsampled in-context reference embeddings.
- [x] **Test Verification:** Complete 23-test test suite passing (`pytest tests/`) covering data loading, feature engineering, models, services, and UI flows.
- [x] **Documentation Accuracy:** Factual `README.md` presenting empirical benchmark numbers without unsupported claims.
- [ ] **Screenshot / Demo Validation:** Capture high-resolution UI flow captures and judge walkthrough material.

---

## Phase 5 — Deployment & Submission
**Status:** `NOT STARTED`

- [ ] **Production Deployment:** Host live demo application on Streamlit Community Cloud or Hugging Face Spaces.
- [ ] **Final README:** Add live deployment links, status badges, and production URLs.
- [ ] **Demo Video:** Record concise 60-second judge demonstration emphasizing the "zero-scroll" loop.
- [ ] **DEV Write-Up:** Publish comprehensive technical submission article on DEV Community.
- [ ] **Hacktoberfest Submission Verification:** Submit project URL and verify Hacktoberfest 2026 Week 1 entry acceptance.
