"""Inference service for TerraPFN dual-engine trail difficulty classification.

Orchestrates:
1. Fast Preview Engine (HistGradientBoosting, <10ms) for interactive UI exploration.
2. Deep Foundation Engine (TabPFN v2, ~2-4s) for calibrated Bayesian posterior distributions.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

# Ensure CPU large dataset allowance for TabPFN
os.environ["TABPFN_ALLOW_CPU_LARGE_DATASET"] = "1"

from terrapfn.data.loader import TARGET_NAMES
from terrapfn.data.preprocessor import TrailFeaturePreprocessor
from terrapfn.models.baselines import get_baseline_models
from terrapfn.models.tabpfn_classifier import TabPFNClassifierWrapper

CLASS_LABELS = ["Easy", "Moderate", "Hard", "Strenuous"]


@dataclass
class DifficultyPrediction:
    """Structured container for difficulty classification inference results."""
    model_name: str
    dominant_class_idx: int
    dominant_class_name: str
    probabilities: Dict[str, float]
    raw_probabilities: np.ndarray
    entropy: float
    confidence_margin: float
    is_borderline: bool
    borderline_details: Optional[str]
    inference_time_ms: float


class TerraInferenceEngine:
    """Manages preprocessors and fitted model instances for interactive inference."""

    def __init__(self, context_sample_size: int = 1000, random_state: int = 42) -> None:
        self.context_sample_size = context_sample_size
        self.random_state = random_state

        self.preprocessor_ = TrailFeaturePreprocessor(scale_numeric=True)
        self.preview_model_ = None
        self.tabpfn_model_ = None
        self.is_fitted_ = False

    def fit_from_catalog(self, catalog_df: pd.DataFrame) -> TerraInferenceEngine:
        """Fit preprocessor, fast preview baseline, and TabPFN in-context representation."""
        df = catalog_df.copy()

        # 1. Fit preprocessor
        X_all = self.preprocessor_.fit_transform(df)
        y_all = df["target"].to_numpy()

        # 2. Fit Fast Preview Engine (HistGradientBoosting on full dataset)
        baseline_models = get_baseline_models(random_state=self.random_state)
        self.preview_model_ = baseline_models["HistGradientBoosting"]
        self.preview_model_.fit(X_all, y_all)

        # 3. Prepare balanced stratified context for TabPFN v2
        if len(df) > self.context_sample_size:
            splitter = StratifiedShuffleSplit(
                n_splits=1,
                train_size=self.context_sample_size,
                random_state=self.random_state,
            )
            context_idx, _ = next(splitter.split(X_all, y_all))
            X_context = X_all[context_idx]
            y_context = y_all[context_idx]
        else:
            X_context = X_all
            y_context = y_all

        # Initialize and fit TabPFN v2 wrapper (n_estimators=2 for high quality + low CPU latency)
        self.tabpfn_model_ = TabPFNClassifierWrapper(
            n_estimators=2,
            random_state=self.random_state,
        )
        self.tabpfn_model_.fit(X_context, y_context)

        self.is_fitted_ = True
        return self

    def _transform_single_trail(self, trail_df: pd.DataFrame) -> np.ndarray:
        """Transform a single trail record into feature array."""
        if not self.is_fitted_:
            raise RuntimeError("Inference engine must be fitted before transforming features.")
        return self.preprocessor_.transform(trail_df)

    def _build_prediction_result(
        self,
        model_name: str,
        probs: np.ndarray,
        elapsed_ms: float,
    ) -> DifficultyPrediction:
        """Calculate entropy, margins, and borderline states from probability distribution."""
        probs = np.asarray(probs, dtype=np.float64).flatten()
        # Ensure proper normalization
        prob_sum = np.sum(probs)
        if prob_sum > 0:
            probs = probs / prob_sum
        else:
            probs = np.ones(4) / 4.0

        dominant_idx = int(np.argmax(probs))
        dominant_name = CLASS_LABELS[dominant_idx]

        # Normalized Shannon Entropy H / log2(4)
        safe_p = np.clip(probs, 1e-12, 1.0)
        entropy = float(-np.sum(safe_p * np.log2(safe_p)) / 2.0)

        # Confidence margin (difference between top 2 classes)
        sorted_indices = np.argsort(probs)[::-1]
        top1 = probs[sorted_indices[0]]
        top2 = probs[sorted_indices[1]]
        margin = float(top1 - top2)

        # Borderline threshold detection: top 2 classes separated by < 15%
        is_borderline = margin < 0.15
        borderline_details = None
        if is_borderline:
            c1 = CLASS_LABELS[sorted_indices[0]]
            c2 = CLASS_LABELS[sorted_indices[1]]
            borderline_details = (
                f"Split decision between {c1} ({top1*100:.1f}%) and {c2} ({top2*100:.1f}%). "
                f"Environmental exposure or personal fatigue will likely shift perceived difficulty to {c2}."
            )

        prob_dict = {label: float(p) for label, p in zip(CLASS_LABELS, probs)}

        return DifficultyPrediction(
            model_name=model_name,
            dominant_class_idx=dominant_idx,
            dominant_class_name=dominant_name,
            probabilities=prob_dict,
            raw_probabilities=probs,
            entropy=entropy,
            confidence_margin=margin,
            is_borderline=is_borderline,
            borderline_details=borderline_details,
            inference_time_ms=elapsed_ms,
        )

    def predict_preview(self, trail_df: pd.DataFrame) -> DifficultyPrediction:
        """Generate fast preview prediction via HistGradientBoosting (<10ms)."""
        if not self.is_fitted_ or self.preview_model_ is None:
            raise RuntimeError("Engine not fitted.")

        X = self._transform_single_trail(trail_df)
        t0 = time.perf_counter()
        probs = self.preview_model_.predict_proba(X)[0]
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return self._build_prediction_result(
            model_name="HistGradientBoosting (Fast Preview)",
            probs=probs,
            elapsed_ms=elapsed_ms,
        )

    def predict_tabpfn_pass(self, trail_df: pd.DataFrame) -> DifficultyPrediction:
        """Generate deep calibrated prediction via TabPFN v2 Foundation Model (~2-4s)."""
        if not self.is_fitted_ or self.tabpfn_model_ is None:
            raise RuntimeError("Engine not fitted.")

        X = self._transform_single_trail(trail_df)
        t0 = time.perf_counter()
        probs = self.tabpfn_model_.predict_proba(X)[0]
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return self._build_prediction_result(
            model_name="TabPFN v2 (Prior-Data Transformer)",
            probs=probs,
            elapsed_ms=elapsed_ms,
        )
