"""Tests for baseline models and TabPFN classifier wrapper."""

import numpy as np
import pytest
from terrapfn.models.baselines import get_baseline_models
from terrapfn.models.tabpfn_classifier import TabPFNClassifierWrapper


@pytest.fixture
def toy_data():
    X = np.array([
        [1.0, 2.0, 0.5],
        [2.0, 1.0, 0.2],
        [5.0, 6.0, 1.2],
        [6.0, 5.0, 1.5],
        [8.0, 9.0, 2.0],
        [9.0, 8.0, 2.2],
        [12.0, 15.0, 3.5],
        [14.0, 16.0, 4.0],
    ], dtype=np.float32)
    y = np.array([0, 0, 1, 1, 2, 2, 3, 3])
    return X, y


def test_baseline_models(toy_data):
    X, y = toy_data
    models = get_baseline_models(random_state=42)

    for name, model in models.items():
        model.fit(X, y)
        preds = model.predict(X)
        probs = model.predict_proba(X)

        assert len(preds) == len(X)
        assert probs.shape == (len(X), 4)
        assert np.allclose(probs.sum(axis=1), 1.0)


def test_tabpfn_classifier_wrapper(toy_data):
    X, y = toy_data
    clf = TabPFNClassifierWrapper(
        model_path="tabpfn-v2-classifier.ckpt",
        random_state=42,
    )
    clf.fit(X, y)
    preds = clf.predict(X)
    probs = clf.predict_proba(X)

    assert len(preds) == len(X)
    assert probs.shape == (len(X), 4)
    assert np.allclose(probs.sum(axis=1), 1.0, atol=1e-3)
    assert set(preds).issubset({0, 1, 2, 3})


def test_tabpfn_dimension_validation():
    clf = TabPFNClassifierWrapper()
    with pytest.raises(ValueError):
        # 1D array should fail
        clf.fit(np.array([1.0, 2.0]), np.array([0, 1]))
