"""Evaluation metrics for TerraPFN trail difficulty classification.

Implements primary and secondary metrics:
Primary:
- Macro F1
- Balanced Accuracy
- Quadratic Weighted Kappa (QWK)
- Multi-class Log Loss
Secondary:
- Multi-class Brier Score
- Confusion Matrix
- Per-class Precision, Recall, and Support
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.metrics import (
    balanced_accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    log_loss,
)


def compute_multiclass_brier_score(
    y_true: np.ndarray, y_prob: np.ndarray, n_classes: int
) -> float:
    """Compute the multi-class Brier score: mean squared difference between one-hot true labels and predicted probabilities."""
    y_true_arr = np.asarray(y_true)
    y_prob_arr = np.asarray(y_prob)

    # One-hot encode true labels
    n_samples = len(y_true_arr)
    one_hot = np.zeros((n_samples, n_classes), dtype=np.float64)
    for i, label in enumerate(y_true_arr):
        if 0 <= label < n_classes:
            one_hot[i, label] = 1.0

    brier = np.mean(np.sum((y_prob_arr - one_hot) ** 2, axis=1))
    return float(brier)


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
    classes: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """Compute all benchmark evaluation metrics for a set of predictions.

    Args:
        y_true: Ground truth integer class labels (0 to K-1).
        y_pred: Predicted integer class labels.
        y_prob: Predicted class probability distribution (N x K).
        classes: Ordered list of all class integers (e.g. [0, 1, 2, 3]).

    Returns:
        Dictionary containing all primary and secondary evaluation metrics.
    """
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)

    if classes is None:
        classes = sorted(list(np.unique(np.concatenate([y_true_arr, y_pred_arr]))))

    n_classes = len(classes)

    # Primary metrics
    macro_f1 = float(f1_score(y_true_arr, y_pred_arr, average="macro", zero_division=0))
    balanced_acc = float(balanced_accuracy_score(y_true_arr, y_pred_arr))
    qwk = float(cohen_kappa_score(y_true_arr, y_pred_arr, labels=classes, weights="quadratic"))

    # Log Loss & Brier Score
    if y_prob is not None:
        y_prob_arr = np.asarray(y_prob)
        # Clip probabilities slightly to avoid log(0)
        eps = 1e-15
        y_prob_safe = np.clip(y_prob_arr, eps, 1 - eps)
        # Re-normalize rows to sum to 1
        y_prob_safe = y_prob_safe / y_prob_safe.sum(axis=1, keepdims=True)

        try:
            loss = float(log_loss(y_true_arr, y_prob_safe, labels=classes))
        except Exception:
            loss = float("nan")

        brier = compute_multiclass_brier_score(y_true_arr, y_prob_safe, n_classes)
    else:
        loss = float("nan")
        brier = float("nan")

    # Confusion matrix
    cm = confusion_matrix(y_true_arr, y_pred_arr, labels=classes).tolist()

    # Per-class metrics
    class_report = classification_report(
        y_true_arr,
        y_pred_arr,
        labels=classes,
        output_dict=True,
        zero_division=0,
    )

    return {
        "macro_f1": macro_f1,
        "balanced_accuracy": balanced_acc,
        "quadratic_weighted_kappa": qwk,
        "log_loss": loss,
        "brier_score": brier,
        "confusion_matrix": cm,
        "classification_report": class_report,
    }
