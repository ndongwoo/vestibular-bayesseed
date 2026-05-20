"""Utilities for binary logistic conditional probability distributions."""

from __future__ import annotations

import math
from collections.abc import Mapping


def sigmoid(x: float) -> float:
    """Return the logistic sigmoid of *x* with overflow protection."""
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def logit(p: float) -> float:
    """Return log(p / (1 - p)).

    Parameters
    ----------
    p:
        Probability in the open interval (0, 1).
    """
    if not 0 < p < 1:
        raise ValueError("p must be in the open interval (0, 1).")
    return math.log(p / (1.0 - p))


def clip(value: float, lower: float = -2.5, upper: float = 2.5) -> float:
    """Clip *value* to the closed interval [lower, upper]."""
    if lower > upper:
        raise ValueError("lower must be <= upper")
    return max(lower, min(upper, value))


def contribution(beta: float, value: float | int | bool | None) -> float | None:
    """Return beta * value, preserving missing values as ``None``.

    Missingness policy follows the project convention: unobserved inputs are not
    interpreted as negative evidence. A missing parent therefore contributes
    nothing and is represented as ``None`` rather than beta * 0.
    """
    if value is None:
        return None
    return float(beta) * float(value)


def logistic_probability(
    intercept: float,
    weights: Mapping[str, float],
    values: Mapping[str, float | int | bool | None],
    *,
    require_observed_parent: bool = False,
) -> tuple[float | None, dict[str, float]]:
    """Compute a logistic-CPD probability.

    Parameters
    ----------
    intercept:
        Baseline log-odds.
    weights:
        Mapping from parent-node ID to beta coefficient.
    values:
        Mapping from parent-node ID to observed value. Values may be binary,
        continuous, or soft probabilities. Missing parents should be absent or
        set to ``None``.
    require_observed_parent:
        If true, return ``(None, {})`` when none of the weighted parents is
        observed. This is useful for derived nodes, where a baseline probability
        should not become downstream evidence when no defining inputs are known.

    Returns
    -------
    tuple
        ``(probability, contributions)`` where contributions is a mapping from
        parent-node ID to beta * value for observed parents.
    """
    linear = float(intercept)
    contributions: dict[str, float] = {}

    for parent, beta in weights.items():
        if parent not in values or values[parent] is None:
            continue
        c = float(beta) * float(values[parent])
        contributions[parent] = c
        linear += c

    if require_observed_parent and not contributions:
        return None, {}

    return sigmoid(linear), contributions
