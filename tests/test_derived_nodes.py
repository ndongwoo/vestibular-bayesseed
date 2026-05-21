from __future__ import annotations

from pathlib import Path

import pytest

from bayesseed.derived_nodes import (
    _evaluate_and_interaction,
    edge_weights_for_node,
    evaluate_derived_nodes,
)
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


# --------------- AND interaction unit tests ---------------

# Engineered interaction features, not diagnostic-criteria audit outputs.


def test_and_interaction_all_true_returns_one() -> None:
    result = _evaluate_and_interaction({"a": 1, "b": 1})
    assert result == 1.0


def test_and_interaction_bool_true_returns_one() -> None:
    result = _evaluate_and_interaction({"a": True, "b": 1.0})
    assert result == 1.0


def test_and_interaction_any_false_returns_zero() -> None:
    result = _evaluate_and_interaction({"a": 1, "b": 0})
    assert result == 0.0


def test_and_interaction_any_bool_false_returns_zero() -> None:
    result = _evaluate_and_interaction({"a": False, "b": 0})
    assert result == 0.0


def test_and_interaction_zero_and_none_returns_zero() -> None:
    # Any explicit false wins over missing.
    result = _evaluate_and_interaction({"a": 0, "b": None})
    assert result == 0.0


def test_and_interaction_one_and_none_returns_none() -> None:
    # One true, one missing → missing, not imputed as false.
    result = _evaluate_and_interaction({"a": 1, "b": None})
    assert result is None


def test_and_interaction_all_none_returns_none() -> None:
    result = _evaluate_and_interaction({"a": None, "b": None})
    assert result is None


def test_and_interaction_soft_float_not_treated_as_true() -> None:
    # Non-binary floats such as 0.7 must NOT be silently thresholded to true.
    result = _evaluate_and_interaction({"a": 0.7, "b": 1})
    assert result is None


def test_and_interaction_single_parent_true() -> None:
    # Single parent that is explicitly true.
    result = _evaluate_and_interaction({"a": 1})
    assert result == 1.0


def test_and_interaction_single_parent_none() -> None:
    # Single parent that is missing.
    result = _evaluate_and_interaction({"a": None})
    assert result is None


def test_and_interaction_empty_parent_values_returns_none() -> None:
    result = _evaluate_and_interaction({})
    assert result is None


# --- Integration: interaction node through evaluation engine ---


def _make_module_with_interaction() -> dict:
    """Build an ad-hoc module with one interaction derived node for testing."""
    return {
        "module_id": "interaction_test",
        "display_name": "Interaction Test",
        "version": "0.1.0",
        "schema_version": "0.1.0",
        "target_diseases": [
            {
                "id": "dx_test",
                "display_name": "Test Dx",
                "intercept": -2.0,
            }
        ],
        "input_nodes": [
            {"id": "feature_a", "type": "binary"},
            {"id": "feature_b", "type": "binary"},
        ],
        "derived_nodes": [
            {
                "id": "ab_concordance",
                "node_class": "derived_interaction",
                "interaction_type": "evidence_concordance",
                "operator": "AND",
                "parents": ["feature_a", "feature_b"],
                "description": "Engineered AND interaction. Not a criteria audit output.",
            }
        ],
        "edges": [
            {
                "id": "e1",
                "from_node": "ab_concordance",
                "to_node": "dx_test",
                "suggested_beta": 1.0,
            }
        ],
    }


def test_interaction_node_activates_when_both_parents_true() -> None:
    module = _make_module_with_interaction()
    values, trace = evaluate_derived_nodes(
        module,
        {"feature_a": 1, "feature_b": 1},
        value_mode="threshold",
    )
    assert values["ab_concordance"] == 1.0
    assert trace["ab_concordance"]["node_class"] == "derived_interaction"
    assert trace["ab_concordance"]["operator"] == "AND"


def test_interaction_node_is_zero_when_one_parent_false() -> None:
    module = _make_module_with_interaction()
    values, _ = evaluate_derived_nodes(
        module,
        {"feature_a": 1, "feature_b": 0},
        value_mode="threshold",
    )
    assert values["ab_concordance"] == 0.0


def test_interaction_node_is_none_when_parent_missing() -> None:
    module = _make_module_with_interaction()
    values, _ = evaluate_derived_nodes(
        module,
        {"feature_a": 1},
        value_mode="threshold",
    )
    assert values["ab_concordance"] is None


def test_interaction_node_trace_marks_interaction_mode() -> None:
    module = _make_module_with_interaction()
    _, trace = evaluate_derived_nodes(
        module,
        {"feature_a": 1, "feature_b": 1},
        value_mode="threshold",
    )
    t = trace["ab_concordance"]
    assert t["value_mode"] == "interaction"
    assert t["node_class"] == "derived_interaction"
    assert t["probability"] is None


# --- BPPV concordance integration tests ---


def test_pc_concordance_activates_with_typical_pc_bppv(bppv_module_path: Path) -> None:
    """pc_positional_concordance fires when both syndrome and PC pattern are true (S01)."""
    module = load_module(bppv_module_path)
    values, trace = evaluate_derived_nodes(
        module,
        {
            "positional_trigger": 1,
            "brief_duration_seconds_minutes": 1,
            "dix_hallpike_torsional_upbeating_nystagmus": 1,
        },
        value_mode="threshold",
    )
    assert values.get("pc_positional_concordance") == 1.0
    assert trace.get("pc_positional_concordance", {}).get("node_class") == "derived_interaction"


def test_hc_concordance_activates_with_typical_hc_bppv(bppv_module_path: Path) -> None:
    """hc_positional_concordance fires when both syndrome and HC pattern are true (S02)."""
    module = load_module(bppv_module_path)
    values, trace = evaluate_derived_nodes(
        module,
        {
            "positional_trigger": 1,
            "brief_duration_seconds_minutes": 1,
            "supine_roll_geotropic_or_apogeotropic_nystagmus": 1,
        },
        value_mode="threshold",
    )
    assert values.get("hc_positional_concordance") == 1.0
    assert trace.get("hc_positional_concordance", {}).get("node_class") == "derived_interaction"


def test_s03_subjective_bppv_no_concordance_boost(bppv_module_path: Path) -> None:
    """Subjective BPPV (S03) should not activate PC or HC concordance."""
    module = load_module(bppv_module_path)
    values, _ = evaluate_derived_nodes(
        module,
        {
            "positional_trigger": 1,
            "subjective_positional_vertigo_only": 1,
            "negative_positional_test": 1,
        },
        value_mode="threshold",
    )
    assert values.get("pc_positional_concordance") is not True
    assert values.get("hc_positional_concordance") is not True


def test_bppv_no_criteria_met_node(bppv_module_path: Path) -> None:
    """Derived nodes should not include any criteria-met / criteria_audit_output node."""
    module = load_module(bppv_module_path)
    for node in module.get("derived_nodes", []):
        assert node.get("criteria_audit_output", False) is not True
