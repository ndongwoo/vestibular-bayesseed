from __future__ import annotations

from pathlib import Path

import pytest

from bayesseed.derived_nodes import edge_weights_for_node, evaluate_derived_nodes
from bayesseed.module_loader import load_module


def test_edge_weights_for_node_returns_parent_betas(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    weights = edge_weights_for_node(module, "posterior_canal_positional_pattern")
    assert weights["dix_hallpike_torsional_upbeating_nystagmus"] == pytest.approx(2.2)


def test_bppv_posterior_canal_pattern_activates_with_typical_nystagmus(
    bppv_module_path: Path,
) -> None:
    module = load_module(bppv_module_path)
    values, trace = evaluate_derived_nodes(
        module,
        {"dix_hallpike_torsional_upbeating_nystagmus": 1},
        value_mode="threshold",
    )
    assert values["posterior_canal_positional_pattern"] == 1.0
    assert trace["posterior_canal_positional_pattern"]["probability"] > 0.5


def test_unobserved_derived_node_does_not_contribute_baseline(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    values, trace = evaluate_derived_nodes(module, {}, value_mode="threshold")
    assert all(value is None for value in values.values())
    assert all(item["probability"] is None for item in trace.values())


def test_probability_mode_passes_soft_derived_value(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    values, trace = evaluate_derived_nodes(
        module,
        {"dix_hallpike_torsional_upbeating_nystagmus": 1},
        value_mode="probability",
    )
    probability = trace["posterior_canal_positional_pattern"]["probability"]
    assert values["posterior_canal_positional_pattern"] == pytest.approx(probability)
    assert 0.5 < probability < 1.0
