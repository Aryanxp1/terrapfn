"""Leakage-free Stratified Cross-Validation Benchmark Runner for TerraPFN.

Conducts strict 5-fold stratified cross-validation.
Preprocessor is fitted solely on training folds.
Evaluates baselines vs TabPFN without test-set contamination.
"""

from __future__ import annotations

import copy
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from terrapfn.data.loader import load_and_merge_data
from terrapfn.data.preprocessor import TrailFeaturePreprocessor
from terrapfn.evaluation.metrics import evaluate_predictions
from terrapfn.models.baselines import get_baseline_models
from terrapfn.models.tabpfn_classifier import TabPFNClassifierWrapper

logger = logging.getLogger(__name__)


def run_benchmark(
    n_splits: int = 5,
    random_state: int = 42,
    output_dir: str | Path = "data/processed/benchmark_results",
    include_tabpfn: bool = True,
) -> Dict[str, Any]:
    """Execute the complete leak-free benchmark across all models.

    Args:
        n_splits: Number of stratified cross-validation folds.
        random_state: Master random seed.
        output_dir: Directory where benchmark results and figures will be stored.
        include_tabpfn: Whether to include TabPFN in the evaluation.

    Returns:
        Structured dictionary of overall results, fold metrics, and execution times.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print("Loading and cleaning datasets...")
    df = load_and_merge_data()
    y = df["target"].to_numpy()
    classes = sorted(list(np.unique(y)))
    n_samples = len(df)
    n_classes = len(classes)

    print(f"Dataset loaded: {n_samples} samples across classes {classes}.")
    print(f"Class distribution:\n{df['target'].value_counts().sort_index()}")
    import os
    os.environ["TABPFN_ALLOW_CPU_LARGE_DATASET"] = "1"

    # Build model pool
    models: Dict[str, Any] = get_baseline_models(random_state=random_state)
    if include_tabpfn:
        models["TabPFN (v2)"] = TabPFNClassifierWrapper(
            model_path="tabpfn-v2-classifier.ckpt",
            n_estimators=4,
            random_state=random_state,
            device="auto",
            ignore_pretraining_limits=True,
        )

    # Initialize storage for out-of-fold predictions and metrics
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    results: Dict[str, Any] = {
        model_name: {
            "fold_metrics": [],
            "oof_preds": np.zeros(n_samples, dtype=int),
            "oof_probs": np.zeros((n_samples, n_classes), dtype=np.float32),
            "fit_times": [],
            "inference_times": [],
        }
        for model_name in models
    }

    print(f"\nBeginning {n_splits}-fold Stratified Cross-Validation...")

    for fold_idx, (train_idx, val_idx) in enumerate(skf.split(df, y), start=1):
        print(f"\n--- Fold {fold_idx}/{n_splits} (Train: {len(train_idx)}, Val: {len(val_idx)}) ---")

        df_train = df.iloc[train_idx].copy()
        df_val = df.iloc[val_idx].copy()
        y_train = y[train_idx]
        y_val = y[val_idx]

        # 1. Leakage-free preprocessing: fit strictly on df_train
        preprocessor = TrailFeaturePreprocessor(scale_numeric=True)
        X_train = preprocessor.fit_transform(df_train)
        X_val = preprocessor.transform(df_val)

        # 2. Train and evaluate each model on this fold
        for model_name, model_template in models.items():
            print(f"  Training {model_name}...")
            # Create fresh instance for this fold
            if model_name == "TabPFN (v2)":
                model = TabPFNClassifierWrapper(
                    model_path="tabpfn-v2-classifier.ckpt",
                    n_estimators=4,
                    random_state=random_state + fold_idx,
                    device="auto",
                    ignore_pretraining_limits=True,
                )
            else:
                model = copy.deepcopy(model_template)

            # Fit with timing
            t0 = time.perf_counter()
            model.fit(X_train, y_train)
            fit_time = time.perf_counter() - t0

            # Inference with timing
            t1 = time.perf_counter()
            preds = model.predict(X_val)
            probs = model.predict_proba(X_val)
            inf_time = time.perf_counter() - t1

            # Store OOF predictions
            results[model_name]["oof_preds"][val_idx] = preds
            results[model_name]["oof_probs"][val_idx] = probs
            results[model_name]["fit_times"].append(fit_time)
            results[model_name]["inference_times"].append(inf_time)

            # Compute fold metrics
            fold_eval = evaluate_predictions(y_val, preds, probs, classes=classes)
            results[model_name]["fold_metrics"].append({
                "fold": fold_idx,
                "fit_time_sec": fit_time,
                "inference_time_sec": inf_time,
                **{k: v for k, v in fold_eval.items() if k not in ["confusion_matrix", "classification_report"]},
            })

            print(
                f"    -> Macro F1: {fold_eval['macro_f1']:.4f} | "
                f"Balanced Acc: {fold_eval['balanced_accuracy']:.4f} | "
                f"QWK: {fold_eval['quadratic_weighted_kappa']:.4f} | "
                f"Log Loss: {fold_eval['log_loss']:.4f} "
                f"(Fit: {fit_time:.2f}s, Inf: {inf_time:.2f}s)"
            )

    # Compute overall Out-Of-Fold (OOF) performance & summary statistics
    summary_rows = []
    detailed_output = {}

    print("\n================ BENCHMARK SUMMARY (OOF EVALUATION) ================")

    for model_name, res in results.items():
        oof_eval = evaluate_predictions(
            y, res["oof_preds"], res["oof_probs"], classes=classes
        )

        fold_f1s = [f["macro_f1"] for f in res["fold_metrics"]]
        fold_accs = [f["balanced_accuracy"] for f in res["fold_metrics"]]
        fold_qwks = [f["quadratic_weighted_kappa"] for f in res["fold_metrics"]]
        fold_losses = [f["log_loss"] for f in res["fold_metrics"]]

        total_fit_time = sum(res["fit_times"])
        total_inf_time = sum(res["inference_times"])
        mean_runtime = total_fit_time + total_inf_time

        summary_rows.append({
            "Model": model_name,
            "Macro F1": f"{oof_eval['macro_f1']:.4f} ± {np.std(fold_f1s):.4f}",
            "Balanced Acc": f"{oof_eval['balanced_accuracy']:.4f} ± {np.std(fold_accs):.4f}",
            "QWK": f"{oof_eval['quadratic_weighted_kappa']:.4f} ± {np.std(fold_qwks):.4f}",
            "Log Loss": f"{oof_eval['log_loss']:.4f} ± {np.std(fold_losses):.4f}",
            "Brier Score": f"{oof_eval['brier_score']:.4f}",
            "Total Runtime (s)": f"{mean_runtime:.2f}",
        })

        detailed_output[model_name] = {
            "oof_overall_metrics": oof_eval,
            "fold_metrics": res["fold_metrics"],
            "total_fit_time_sec": total_fit_time,
            "total_inf_time_sec": total_inf_time,
            "confusion_matrix": oof_eval["confusion_matrix"],
            "classification_report": oof_eval["classification_report"],
        }

    df_summary = pd.DataFrame(summary_rows)
    print(df_summary.to_string(index=False))

    # Save outputs
    summary_csv = out_path / "benchmark_summary.csv"
    df_summary.to_csv(summary_csv, index=False)

    summary_json = out_path / "benchmark_results.json"
    with open(summary_json, "w", encoding="utf-8") as f:
        json.dump(detailed_output, f, indent=2)

    # Save Markdown report
    summary_md = out_path / "benchmark_summary.md"
    with open(summary_md, "w", encoding="utf-8") as f:
        f.write("# TerraPFN Outdoor Trail Difficulty Benchmark Results\n\n")
        f.write("Evaluation Protocol: **Stratified 5-Fold Cross-Validation (Zero Test Leakage)**\n\n")
        f.write("Target: **4-Class Trail Difficulty (1=Easy, 3=Moderate, 5=Hard, 7=Strenuous)**\n\n")
        f.write(df_summary.to_markdown(index=False))
        f.write("\n\n## Per-Class Confusion Matrices\n\n")
        for m_name, det in detailed_output.items():
            f.write(f"### {m_name}\n\n")
            f.write("```\n")
            cm_arr = np.array(det["confusion_matrix"])
            f.write(f"Classes: {classes}\n")
            f.write(f"{cm_arr}\n")
            f.write("```\n\n")

    print(f"\nBenchmark artifacts written to {summary_csv}, {summary_json}, and {summary_md}")
    return detailed_output


if __name__ == "__main__":
    run_benchmark()
