"""Tests for evaluation metrics module."""

import numpy as np
import pytest
from terrapfn.evaluation.metrics import compute_multiclass_brier_score, evaluate_predictions


def test_perfect_predictions():
    y_true = np.array([0, 1, 2, 3, 0, 1, 2, 3])
    y_pred = np.array([0, 1, 2, 3, 0, 1, 2, 3])
    y_prob = np.eye(4)[y_true]

    metrics = evaluate_predictions(y_true, y_pred, y_prob, classes=[0, 1, 2, 3])

    assert np.isclose(metrics["macro_f1"], 1.0)
    assert np.isclose(metrics["balanced_accuracy"], 1.0)
    assert np.isclose(metrics["quadratic_weighted_kappa"], 1.0)
    assert np.isclose(metrics["brier_score"], 0.0)
    assert metrics["log_loss"] < 0.01


def test_quadratic_weighted_kappa_ordinal_penalty():
    # Misclassifying 0 as 1 should yield higher QWK than misclassifying 0 as 3
    y_true = np.array([0, 0, 1, 2, 3, 3])
    
    # Near mistakes (0 -> 1, 3 -> 2)
    y_pred_near = np.array([1, 1, 1, 2, 2, 2])
    metrics_near = evaluate_predictions(y_true, y_pred_near, classes=[0, 1, 2, 3])

    # Far mistakes (0 -> 3, 3 -> 0)
    y_pred_far = np.array([3, 3, 1, 2, 0, 0])
    metrics_far = evaluate_predictions(y_true, y_pred_far, classes=[0, 1, 2, 3])

    assert metrics_near["quadratic_weighted_kappa"] > metrics_far["quadratic_weighted_kappa"]


def test_multiclass_brier_score():
    y_true = np.array([0, 1])
    # Exact prediction: Brier = 0
    y_prob_exact = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert np.isclose(compute_multiclass_brier_score(y_true, y_prob_exact, n_classes=2), 0.0)

    # Worst prediction: Brier = 2.0 per sample
    y_prob_worst = np.array([[0.0, 1.0], [1.0, 0.0]])
    assert np.isclose(compute_multiclass_brier_score(y_true, y_prob_worst, n_classes=2), 2.0)
