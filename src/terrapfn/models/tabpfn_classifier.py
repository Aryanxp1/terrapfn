"""TabPFNClassifier wrapper for TerraPFN trail difficulty classification.

Wraps the official TabPFN foundation model interface (tabpfn v2).
Ensures deterministic seeds, input dimension validation, and scikit-learn API compatibility.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

logger = logging.getLogger(__name__)


class TabPFNClassifierWrapper(BaseEstimator, ClassifierMixin):
    """Clean scikit-learn compatible wrapper for TabPFNClassifier."""

    def __init__(
        self,
        model_path: str = "tabpfn-v2-classifier.ckpt",
        n_estimators: Any = 4,
        random_state: int = 42,
        device: str = "auto",
        ignore_pretraining_limits: bool = True,
    ) -> None:
        self.model_path = model_path
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.device = device
        self.ignore_pretraining_limits = ignore_pretraining_limits
        self.model_: Optional[Any] = None
        self.classes_: Optional[np.ndarray] = None
        self.n_features_in_: Optional[int] = None

    def _init_underlying_model(self) -> None:
        """Lazily initialize the underlying TabPFN model."""
        try:
            from tabpfn import TabPFNClassifier
        except ImportError as e:
            raise ImportError(
                "tabpfn package is required to use TabPFNClassifierWrapper. "
                "Install it via `pip install tabpfn`."
            ) from e

        self.model_ = TabPFNClassifier(
            model_path=self.model_path,
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            device=self.device,
            ignore_pretraining_limits=self.ignore_pretraining_limits,
        )

    def fit(self, X: np.ndarray, y: np.ndarray) -> TabPFNClassifierWrapper:
        """Fit TabPFN in-context representation on training data."""
        X_arr = np.asarray(X, dtype=np.float32)
        y_arr = np.asarray(y)

        if X_arr.ndim != 2:
            raise ValueError(f"Expected 2D array for X, got shape {X_arr.shape}")
        if len(X_arr) != len(y_arr):
            raise ValueError(f"Length mismatch: X has {len(X_arr)} rows, y has {len(y_arr)}")

        self.n_features_in_ = X_arr.shape[1]
        self.classes_ = np.unique(y_arr)

        if self.model_ is None:
            self._init_underlying_model()

        self.model_.fit(X_arr, y_arr)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels for X."""
        if self.model_ is None:
            raise RuntimeError("Model has not been fitted yet. Call fit() before predict().")

        X_arr = np.asarray(X, dtype=np.float32)
        return self.model_.predict(X_arr)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict calibrated class probabilities for X."""
        if self.model_ is None:
            raise RuntimeError("Model has not been fitted yet. Call fit() before predict_proba().")

        X_arr = np.asarray(X, dtype=np.float32)
        return self.model_.predict_proba(X_arr)
