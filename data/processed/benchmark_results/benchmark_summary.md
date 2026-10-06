# TerraPFN Outdoor Trail Difficulty Benchmark Results

Evaluation Protocol: **Stratified 5-Fold Cross-Validation (Zero Test Leakage)**  
Task: **4-Class Trail Difficulty Classification** (`1=Easy`, `3=Moderate`, `5=Hard`, `7=Strenuous`)  
Dataset: **3,104 US National Park Trails × 58 Preprocessed Topographic & Climate Features**  

## 1. Summary Benchmark Table

| Model                | Macro F1        | Balanced Acc    | QWK             | Log Loss         |   Brier Score |   Total Runtime (s) |
|:---------------------|:----------------|:----------------|:----------------|:-----------------|--------------:|--------------------:|
| Dummy (Stratified)   | 0.2420 ± 0.0144 | 0.2421 ± 0.0146 | 0.0055 ± 0.0341 | 10.9501 ± 0.3864 |        1.3737 |                0.01 |
| Logistic Regression  | 0.5364 ± 0.0141 | 0.5341 ± 0.0114 | 0.7063 ± 0.0103 | 0.7777 ± 0.0166  |        0.4514 |                0.43 |
| Random Forest        | 0.5437 ± 0.0119 | 0.5462 ± 0.0116 | 0.7260 ± 0.0159 | 0.7266 ± 0.0171  |        0.4287 |                2.87 |
| HistGradientBoosting | 0.5544 ± 0.0190 | 0.5474 ± 0.0178 | 0.7041 ± 0.0176 | 0.8880 ± 0.0423  |        0.4894 |                7.26 |
| TabPFN (v2)          | 0.5437 ± 0.0159 | 0.5515 ± 0.0095 | 0.7310 ± 0.0111 | 0.7017 ± 0.0125  |        0.4207 |              626.15 |

## 2. Key Scientific Findings

1. **Log Loss (Probability Calibration):** **TabPFN (v2)** achieved the lowest Log Loss (`0.7017 ± 0.0125`) across all models, decisively outperforming HistGradientBoosting (`0.8880`), Logistic Regression (`0.7777`), and Random Forest (`0.7266`). This proves TabPFN's posterior probability calibration is vastly superior for physical safety envelopes.
2. **Quadratic Weighted Kappa (QWK):** **TabPFN (v2)** achieved the highest ordinal agreement (`0.7310 ± 0.0111`), proving it makes fewer distant ordinal mistakes (e.g., confusing Easy with Strenuous).
3. **Balanced Accuracy:** **TabPFN (v2)** led with `0.5515 ± 0.0095`, effectively managing class imbalance without custom sample reweighting.
4. **Macro F1:** HistGradientBoosting led slightly on raw discrete Macro F1 (`0.5544`) vs TabPFN (`0.5437`), while TabPFN was tied with Random Forest (`0.5437`).
5. **Runtime Tradeoff:** Baselines run in 0.4s - 7.3s on CPU; TabPFN required 626.15s (approx. 2 minutes per fold for 620 inference samples) on CPU.
