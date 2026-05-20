from __future__ import annotations

import math

import pytest

from bayesseed.logistic_cpd import clip, logit, logistic_probability, sigmoid


def test_sigmoid_and_logit_are_inverse_for_common_probabilities() -> None:
    for p in [0.01, 0.1, 0.5, 0.9, 0.99]:
        assert sigmoid(logit(p)) == pytest.approx(p)


def test_sigmoid_has_overflow_protection() -> None:
    assert sigmoid(1000.0) == pytest.approx(1.0)
    assert sigmoid(-1000.0) == pytest.approx(0.0)


def test_logit_rejects_invalid_probabilities() -> None:
    for p in [0.0, 1.0, -0.1, 1.1]:
        with pytest.raises(ValueError):
            logit(p)


def test_clip_limits_beta_range() -> None:
    assert clip(3.7) == 2.5
    assert clip(-3.7) == -2.5
    assert clip(1.2) == 1.2


def test_logistic_probability_ignores_missing_parent_values() -> None:
    probability, contributions = logistic_probability(
        intercept=-2.0,
        weights={"a": 1.0, "b": 2.0, "c": -1.0},
        values={"a": 1, "b": None},
    )
    assert probability == pytest.approx(sigmoid(-1.0))
    assert contributions == {"a": 1.0}


def test_logistic_probability_can_require_an_observed_parent() -> None:
    probability, contributions = logistic_probability(
        intercept=-1.0,
        weights={"a": 1.0},
        values={},
        require_observed_parent=True,
    )
    assert probability is None
    assert contributions == {}


def test_logistic_probability_accepts_soft_parent_values() -> None:
    probability, contributions = logistic_probability(
        intercept=0.0,
        weights={"soft_node": 2.0},
        values={"soft_node": 0.25},
    )
    assert probability == pytest.approx(sigmoid(0.5))
    assert contributions["soft_node"] == pytest.approx(0.5)
