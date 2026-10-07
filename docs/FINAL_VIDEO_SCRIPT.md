# TerraPFN — Final 60-Second Video Script

**Project:** TerraPFN (Outdoor Trail Intelligence via TabPFN)  
**Challenge:** Hacktoberfest 2026 Week 1  
**Category:** Best Use of TabPFN (Partner Sponsor)  
**Theme:** Touch Grass  
**Format:** 1080p 60fps Screen Recording + Voiceover Audio  
**Demonstration Trail:** Angels Landing Trail, Zion National Park (Class 5 · Hard)  
**Total Target Run Time:** 60.0 Seconds  

---

## Production Overview

This script defines the exact second-by-second narration, mouse actions, screen states, and visual cues for the official 60-second competition demonstration video. The focus is strictly on the user product journey: moving from screen time to trail preparation, and finally outdoors.

```
00:00 - 00:10 | Scene 1: The Problem & The Zero-Scroll Thesis
00:10 - 00:25 | Scene 2: Select Trail, Physical Specifications & Fast Preview
00:25 - 00:40 | Scene 3: TabPFN In-Context Foundation Inference & Calibrated Posteriors
00:40 - 00:50 | Scene 4: The Signature Grass Pass & Touch Grass Screenlock
00:50 - 01:00 | Scene 5: Post-Hike Reflection Loop & Empirical Benchmark Evidence
```

---

## Detailed Second-by-Second Cue Sheet

### Scene 1: The Problem & Zero-Scroll Thesis (00:00 – 00:10)
- **Time:** 00:00 – 00:10 (10 seconds)
- **Visual:** Full-screen capture of the TerraPFN landing page (`docs/screenshots/v2/01_landing.png`). Quiet dark editorial interface with header: *"Know the trail. Get outside."*
- **Action:** Cursor hovers gently over the header statement, then sweeps over the 4 curated benchmark reference cards without frantic movement.
- **On-Screen Text Overlay:** `TERRAPFN // ZERO-SCROLL OUTDOOR INTELLIGENCE`
- **Voiceover Narration:**  
  *"Traditional trail apps trap you in infinite reviews, star ratings, and photo feeds when all you want to do is go outside. TerraPFN is built on one simple rule: compute an objective biophysical preparation envelope in seconds, pocket your phone, and touch grass."*

---

### Scene 2: Trail Topography & Fast Preview (00:10 – 00:25)
- **Time:** 00:10 – 00:25 (15 seconds)
- **Visual:** Cursor moves to the curated card **Angels Landing Trail (Class 5 · Hard)** and clicks `Select Hard` (`docs/screenshots/v2/02_trail_selected.png`).
- **Action:**
  1. Selected trail specification smoothly populates:
     - Distance: `6.60 km`
     - Elevation Gain: `+493 m`
     - Average Slope: `7.5%`
     - Estimated Moving Time: `2h 25m – 3h 35m`
  2. Cursor scrolls down to show the environmental tags: `Summer Avg: 36.8°C`, `Winter Avg: -12.4°C`, `Precipitation: 248 mm/yr`.
  3. Cursor points to the `Quick Estimate (Instant Baseline)` panel displaying the sub-25ms HistGradientBoosting distribution.
- **On-Screen Text Overlay:** `SUB-25MS REAL-TIME PREVIEW`
- **Voiceover Narration:**  
  *"Select any trail across 3,104 National Parks hikes or synthesize a custom route. An instant baseline engine delivers sub-25ms responsive previews while you explore topographic physics."*

---

### Scene 3: TabPFN Foundation Assessment (00:25 – 00:40)
- **Time:** 00:25 – 00:40 (15 seconds)
- **Visual:** Cursor moves to the prominent green CTA button: `GENERATE GRASS PASS` and clicks (`docs/screenshots/v2/03_tabpfn_prediction.png` → `docs/screenshots/v2/04_grass_pass.png`).
- **Action:**
  1. Brief status indicator shows TabPFN executing in-context attention across reference trails.
  2. Success toast appears: `Grass Pass generated via TabPFN in 6.33s`.
  3. The calibrated posterior distribution renders cleanly:
     - Easy: `0.5%`
     - Moderate: `47.0%`
     - Hard: `48.5%`
     - Strenuous: `4.0%`
  4. Notice callout highlights the borderline split between Moderate and Hard.
- **On-Screen Text Overlay:** `TABPFN V2 CALIBRATED BAYESIAN POSTERIOR`
- **Voiceover Narration:**  
  *"Now click Generate Grass Pass. TabPFN evaluates in-context transformer attention across our national trail corpus. Instead of an overconfident label, TabPFN calculates calibrated Bayesian posterior probabilities: 48.5% Hard, 47.0% Moderate, detecting the borderline ridge scramble. From this distribution, TerraPFN derives your physical safety envelope: a minimum 2.6 liters of water, lugged footwear, and a 2-hour turnaround watch alarm."*

---

### Scene 4: Cache & Go — Touch Grass Mode (00:40 – 00:50)
- **Time:** 00:40 – 00:50 (10 seconds)
- **Visual:** Cursor moves to the primary action: `CACHE & GO (Touch Grass)` and clicks (`docs/screenshots/v2/05_touch_grass_mode.png`).
- **Action:**
  1. The interface transitions immediately into the minimalist outdoor screenlock.
  2. Centered message:
     - `GRASS PASS CACHED`
     - `POCKET THE PHONE. GO OUTSIDE.`
     - `"Screen time ends here. Step onto the trail."`
  3. Outdoor elapsed timer ticks: `0m 00s` → `0m 04s`.
- **On-Screen Text Overlay:** `SCREEN TIME ENDS HERE. POCKET THE PHONE.`
- **Voiceover Narration:**  
  *"Click Cache & Go. Your preparation envelope is sealed. Screen time ends right here. Pocket the phone, step onto the trail, and hike."*

---

### Scene 5: Post-Hike Reflection & Model Evidence (00:50 – 01:00)
- **Time:** 00:50 – 01:00 (10 seconds)
- **Visual:** Cursor clicks `I'M BACK (Record Reflection)` (`docs/screenshots/v2/06_post_hike_checkin.png`).
- **Action:**
  1. Shows the calm post-hike observation log: *"How did the trail actually feel?"*
  2. Selects observed rating, inputs moving time, clicks `SAVE OBSERVATION`.
  3. Cursor shifts to the sidebar table showing the verified 5-fold cross-validation evidence:
     - TabPFN (v2): `QWK 0.731` | `BalAcc 55.1%` | `LogLoss 0.702`
     - Random Forest: `QWK 0.726` | `BalAcc 54.6%` | `LogLoss 0.727`
     - HistGradBoost: `QWK 0.704` | `BalAcc 54.7%` | `LogLoss 0.888`
- **On-Screen Text Overlay:** `5-FOLD CV: TABPFN LEADS IN LOG LOSS (0.702) & QWK (0.731)`
- **Voiceover Narration:**  
  *"When you return, record an honest observation to complete the ground-truth loop. In 5-fold cross-validation across 3,104 trails, TabPFN led in Quadratic Weighted Kappa and Log Loss. TerraPFN: intelligence that gets you outside."*
- **Final Closing Frame:**  
  `TERRAPFN`  
  `Know the trail. Get outside.`  
  `https://github.com/Aryanxp1/terrapfn`  

---

## Technical Specifications for Recording

1. **Resolution:** 1920 × 1080 (1080p, 16:9).
2. **Frame Rate:** 60 FPS.
3. **Audio:** High-quality voiceover narration, normalized to -14 LUFS, subtle ambient nature soundtrack at -26 dB.
4. **Tooling:** OBS Studio / Screen Studio / Playwright screen capture.
5. **Color Profile:** Clean sRGB, verified against dark mode palette (`#0D1117` background).
