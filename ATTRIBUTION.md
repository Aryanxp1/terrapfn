# Data Provenance & Attribution Notice

**Project:** TerraPFN  
**Author & Maintainer:** Aryan Vishwakarma  
**Competition Entry:** Hacktoberfest 2026 (Category: *Best Use of TabPFN* | Theme: *Touch Grass*)

---

## 1. Research Scaffold & Exploration Reference
TerraPFN was independently conceived, architected, and built by Aryan Vishwakarma during the Hacktoberfest 2026 challenge window. 

The original domain problem exploration and preliminary backpacking log structure were referenced with permission from:
- **Project:** *MyTrails* (formerly *TrailGenie*)
- **Original Author:** Jamie Breault (`jgbreault`)
- **Repository Reference:** [https://github.com/jgbreault/MyTrails](https://github.com/jgbreault/MyTrails)
- **Status:** Used as a reference scaffold and historical test case with explicit permission from the original author.

---

## 2. Dataset Sources & Licenses

### A. US National Park Trail Records
- **Source:** Compiled AllTrails records for USA National Parks.
- **Curated By:** Jane (`j-ane/trail-data`)
- **Repository:** [https://github.com/j-ane/trail-data](https://github.com/j-ane/trail-data)
- **Usage:** Contains 3,313 trail topographic records (distance, elevation gain, coordinates, feature tags, and catalog difficulty ratings).

### B. Climate & Meteorological Reanalysis Data
- **Source:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- **Provider:** Open-Meteo.com under Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Usage:** 10-year historical weather climatology (summer maximum temperature 98th percentile, winter minimum temperature 2nd percentile, annual precipitation, and annual snowfall).

### C. Foundation Tabular Model
- **Model:** TabPFN (Prior-Data Fitted Networks for Tabular Data)
- **Authors:** Prior Labs / Frank Hutter, Noah Hollmann, Samuel Müller et al.
- **Repository:** [https://github.com/priorlabs/TabPFN](https://github.com/priorlabs/TabPFN)
- **License:** Apache 2.0 / Custom Research License as provided by Prior Labs.

---

## 3. Independent Intellectual Property
All application code, modular Python packages (`src/terrapfn/`), probabilistic uncertainty calibration routines, in-context few-shot adaptation mechanisms, unit tests, and interactive user interfaces in this repository are original implementations by **Aryan Vishwakarma**.
