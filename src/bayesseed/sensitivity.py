"""One-way sensitivity utilities for edge beta coefficients."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from .inference import infer_module


def apply_beta_overrides(
    module: Mapping[str, Any], overrides: Mapping[str, float]
) -> dict[str, Any]:
    """Return a deep-copied module with edge beta overrides applied.

    Overrides are keyed by edge ID.
    """
    new_module = copy.deepcopy(dict(module))
    for edge in new_module.get("edges", []):
        edge_id = str(edge.get("id"))
        if edge_id in overrides:
            edge["suggested_beta"] = float(overrides[edge_id])
    return new_module


def one_way_sensitivity(
    module: Mapping[str, Any],
    case: Mapping[str, Any],
    edge_id: str,
    beta_values: list[float],
    *,
    derived_value_mode: str = "threshold",
    derived_threshold: float = 0.5,
) -> list[dict[str, Any]]:
    """Run one-way sensitivity analysis for one edge.

    Returns a long-form list with one row per beta value and target disease.
    """
    rows: list[dict[str, Any]] = []
    for beta in beta_values:
        altered = apply_beta_overrides(module, {edge_id: beta})
        result = infer_module(
            altered,
            case,
            derived_value_mode=derived_value_mode,
            derived_threshold=derived_threshold,
        )
        for disease in result.ranked():
            rows.append(
                {
                    "module_id": result.module_id,
                    "edge_id": edge_id,
                    "beta": beta,
                    "disease_id": disease.disease_id,
                    "display_name": disease.display_name,
                    "posterior": disease.posterior,
                }
            )
    return rows


def beta_grid(beta_min: float, beta_max: float, steps: int = 9) -> list[float]:
    """Return an evenly spaced beta grid including both endpoints."""
    if steps < 2:
        raise ValueError("steps must be >= 2")
    step = (float(beta_max) - float(beta_min)) / (steps - 1)
    return [float(beta_min) + i * step for i in range(steps)]
