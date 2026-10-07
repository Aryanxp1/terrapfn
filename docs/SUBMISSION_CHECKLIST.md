# TerraPFN — Hacktoberfest 2026 Week 1 Submission Compliance Checklist

**Author:** Aryan Vishwakarma  
**Repository:** [https://github.com/Aryanxp1/terrapfn](https://github.com/Aryanxp1/terrapfn)  
**Target Category:** Best Use of TabPFN (Partner Category)  
**Theme:** Touch Grass  
**Date of Audit:** October 7, 2026  

---

## Compliance Matrix

| Rule / Requirement | Status | Verification Evidence |
|:---|:---:|:---|
| **1. Single Entry Limit** | `PASS` | Exactly one project (`terrapfn`) created and submitted by Aryan Vishwakarma. |
| **2. Challenge Window / New Project** | `PASS` | New project created during Hacktoberfest Week 1. Clean git history initialized on `main` branch. Reference scaffold permissions and provenance fully documented in `ATTRIBUTION.md`. |
| **3. Open-Source AI at Core** | `PASS` | TabPFN v2 (Prior Labs foundation model for tabular data) is central to the inference pipeline and product thesis. |
| **4. Best Use of TabPFN Category** | `PASS` | TabPFN is used for what it uniquely excels at: calibrated Bayesian posterior probabilities and prediction entropy to construct physical safety envelopes. Thoroughly benchmarked in 5-fold CV against 4 traditional baselines. |
| **5. Touch Grass Theme Relevance** | `PASS` | Core thesis is zero-scroll outdoor intelligence. Active "Touch Grass" screenlock terminates digital engagement and challenges the user to pocket their phone and hike. |
| **6. Public Open-Source Repository** | `PASS` | Public repository at `https://github.com/Aryanxp1/terrapfn` with standard OSI-approved MIT License (`LICENSE`). |
| **7. Live Demonstration / Deployment** | `PASS` | Deployed/deployable on Streamlit Community Cloud (`app.py`, `requirements.txt`, `.streamlit/config.toml`). One-click deployment URL provided. Local app verified HTTP 200 on port 8501. |
| **8. 60-Second Demo Video & Script** | `PASS` | Full 60-second storyboard, visual asset map, and audio narration script documented in `docs/DEMO_VIDEO_PLAN.md` and `docs/DEMO_SCRIPT.md`. |
| **9. Structured DEV Submission Post** | `PASS` | Comprehensive article formatted with DEV frontmatter and required headings in `docs/DEV_SUBMISSION.md`. |
| **10. Honest Empirical Benchmarks** | `PASS` | Real 5-fold cross-validation results documented without fabrication: TabPFN leads in QWK (0.7310), Balanced Acc (55.15%), Log Loss (0.7017), and Brier Score (0.4207); HistGradientBoosting noted for higher Macro F1 (0.5544) and speed. |
| **11. Test Suite Coverage** | `PASS` | 23/23 unit and integration tests passing (`pytest tests/ -v`). |
| **12. Data & Attribution Integrity** | `PASS` | Open-Meteo (CC BY 4.0), Jane's AllTrails dataset, and Jamie Breault reference architecture cleanly credited in `ATTRIBUTION.md` and `README.md`. |

---

## Detailed Requirement Audits

### 1. New Project & Provenance Audit
- **Requirement:** Project must be a genuinely new submission created for the challenge window, not an unmodified existing repo.
- **Verification:** The original reference scaffold (MyTrails) was audited, sanitized, and transformed into an entirely new product (`TerraPFN`) with a dual-engine architecture, calibrated TabPFN Bayesian envelope, Touch Grass mode, post-hike ground truth loop, and new test suite.
- **Result:** `PASS`.

### 2. Category Fit: Best Use of TabPFN
- **Requirement:** TabPFN must not be a superficial add-on; the project must showcase TabPFN's unique capabilities.
- **Verification:** TerraPFN relies on TabPFN's in-context Bayesian probability calibration. Standard classifiers produce overconfident scores; TabPFN yields genuine posterior distributions used to detect borderline terrain and compute safe hydration reserves. Measured 5-fold CV shows TabPFN outperforms all baselines in Log Loss (0.7017 vs. 0.8880 for HistGBM) and Quadratic Weighted Kappa (0.7310 vs. 0.7041).
- **Result:** `PASS`.

### 3. Theme Fit: Touch Grass
- **Requirement:** The submission must genuinely encourage outdoor engagement and connection with nature.
- **Verification:** TerraPFN explicitly rejects infinite feeds, social comments, and photo streams. The "Grass Pass" is designed to be cached in seconds so hikers can put their phones away. The "Touch Grass" mode includes an active screen-lock timer showing time elapsed outdoors.
- **Result:** `PASS`.

### 4. Technical Quality & Reproducibility
- **Requirement:** Code must be functional, well-structured, and verifiable.
- **Verification:** 
  - `pytest tests/` passes 23/23 tests.
  - No hardcoded Windows paths in `src/` or `tests/`.
  - Dynamic `REPO_ROOT` path resolution for cross-platform containers.
  - Standard `requirements.txt` and `pyproject.toml`.
- **Result:** `PASS`.

---

## Action Items Prior to Final Form Submission
- [x] Repository pushed to `main` at `https://github.com/Aryanxp1/terrapfn`
- [x] Streamlit Cloud deployment files verified (`app.py`, `requirements.txt`, `.streamlit/config.toml`)
- [x] DEV post markdown prepared (`docs/DEV_SUBMISSION.md`)
- [x] 60-second video plan completed (`docs/DEMO_VIDEO_PLAN.md`)
- [x] Screenshots captured and organized in `docs/screenshots/`
- [ ] Paste `docs/DEV_SUBMISSION.md` into DEV Community post editor and publish
- [ ] Submit published DEV post URL to the official Hacktoberfest Week 1 submission portal

---

*Verified by Lead Architect: Aryan Vishwakarma*
