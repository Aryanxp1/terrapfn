"""Baseline classifiers for TerraPFN trail difficulty benchmarking.

Implements standard scikit-learn baselines:
1. Stratified Dummy Classifier (baseline floor)
2. Multinomial Logistic Regression (linear baseline)
3. Random Forest Classifier (bagging ensemble)
4. HistGradientBoostingClassifier (gradient boosting ensemble)
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class BaselineModelWrapper(BaseEstimator, ClassifierMixin):
    """Standardized wrapper ensuring consistent fit/predict/predict_proba API."""

    def __init__(self, model_name: str, estimator: Any) -> None:
        self.model_name = model_name
        self.estimator = estimator

    def fit(self, X: np.ndarray, y: np.ndarray) -> BaselineModelWrapper:
        self.estimator.fit(X, y)
        self.classes_ = getattr(self.estimator, "classes_", np.unique(y))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.estimator.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.estimator.predict_proba(X)


def get_baseline_models(random_state: int = 42) -> Dict[str, BaselineModelWrapper]:
    """Instantiate the 4 standard baseline classifiers with reproducible seeds."""
    models = {
        "Dummy (Stratified)": BaselineModelWrapper(
            "Dummy (Stratified)",
            DummyClassifier(strategy="stratified", random_state=random_state),
        ),
        "Logistic Regression": BaselineModelWrapper(
            "Logistic Regression",
            LogisticRegression(
                max_iter=1000,
                C=1.0,
                solver="lbfgs",
                random_state=random_state,
            ),
        ),
        "Random Forest": BaselineModelWrapper(
            "Random Forest",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=12,
                min_samples_leaf=2,
                max_features="sqrt",
                n_jobs=-1,
                random_state=random_state,
            ),
        ),
        "HistGradientBoosting": BaselineModelWrapper(
            "HistGradientBoosting",
            HistGradientBoostingClassifier(
                max_iter=200,
                learning_rate=0.08,
                max_depth=6,
                min_samples_leaf=15,
                l2_regularization=0.1,
                random_state=random_state,
            ),
        ),
    }
    return models
