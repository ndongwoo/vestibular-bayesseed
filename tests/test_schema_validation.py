from __future__ import annotations

import copy
from pathlib import Path

import pytest

from bayesseed.exceptions import ModuleValidationError
from bayesseed.module_loader import load_module, load_modules
from bayesseed.schema_validation import collect_node_ids, validate_module


def test_default_modules_are_valid(default_modules_dir: Path) -> None:
    for module in load_modules(default_modules_dir):
        assert validate_module(module)


def test_collect_node_ids_includes_input_derived_and_target(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    node_ids = collect_node_ids(module)
    assert "positional_trigger" in node_ids["input"]
    assert "posterior_canal_positional_pattern" in node_ids["derived"]
    assert "dx_bppv" in node_ids["target"]
    assert node_ids["input"] | node_ids["derived"] | node_ids["target"] == node_ids["all"]


def test_validation_rejects_missing_required_field(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    bad_module = copy.deepcopy(module)
    bad_module.pop("edges")
    with pytest.raises(ModuleValidationError, match="missing required"):
        validate_module(bad_module)


def test_validation_rejects_unknown_edge_node(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    bad_module = copy.deepcopy(module)
    bad_module["edges"][0]["from_node"] = "unknown_input_node"
    with pytest.raises(ModuleValidationError, match="unknown from_node"):
        validate_module(bad_module)


# --- Derived interaction node validation tests ---

# Engineered interaction features, not diagnostic-criteria audit outputs.


def test_derived_interaction_node_validates_successfully(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    module["derived_nodes"].append(
        {
            "id": "example_interaction",
            "node_class": "derived_interaction",
            "interaction_type": "evidence_concordance",
            "operator": "AND",
            "parents": ["positional_trigger", "brief_triggered_positional_syndrome"],
            "criteria_audit_output": False,
            "weight_interpretation": "residual_excess_log_odds",
            "missingness_policy": "unobserved_not_imputed",
            "description": "Engineered interaction feature. Not a criteria audit output.",
        }
    )
    assert validate_module(module)


def test_derived_interaction_rejects_missing_operator() -> None:
    module = {
        "schema_version": "0.1.0",
        "module_id": "test",
        "display_name": "Test",
        "version": "0.1.0",
        "target_diseases": [{"id": "dx", "display_name": "Dx", "intercept": -1.0}],
        "input_nodes": [],
        "derived_nodes": [
            {
                "id": "inter_x",
                "node_class": "derived_interaction",
                "parents": ["a"],
            }
        ],
        "edges": [],
    }
    with pytest.raises(ModuleValidationError, match="missing.*operator"):
        validate_module(module)


def test_derived_interaction_rejects_non_and_operator() -> None:
    module = {
        "schema_version": "0.1.0",
        "module_id": "test",
        "display_name": "Test",
        "version": "0.1.0",
        "target_diseases": [{"id": "dx", "display_name": "Dx", "intercept": -1.0}],
        "input_nodes": [],
        "derived_nodes": [
            {
                "id": "inter_x",
                "node_class": "derived_interaction",
                "operator": "OR",
                "parents": ["a"],
            }
        ],
        "edges": [],
    }
    with pytest.raises(ModuleValidationError, match="operator.*AND"):
        validate_module(module)


def test_derived_interaction_rejects_criteria_audit_output_true() -> None:
    module = {
        "schema_version": "0.1.0",
        "module_id": "test",
        "display_name": "Test",
        "version": "0.1.0",
        "target_diseases": [{"id": "dx", "display_name": "Dx", "intercept": -1.0}],
        "input_nodes": [
            {"id": "a", "type": "binary"},
            {"id": "b", "type": "binary"},
        ],
        "derived_nodes": [
            {
                "id": "inter_x",
                "node_class": "derived_interaction",
                "operator": "AND",
                "parents": ["a", "b"],
                "criteria_audit_output": True,
            }
        ],
        "edges": [],
    }
    with pytest.raises(ModuleValidationError, match="criteria_audit_output"):
        validate_module(module)


def test_derived_interaction_rejects_unknown_parent() -> None:
    module = {
        "schema_version": "0.1.0",
        "module_id": "test",
        "display_name": "Test",
        "version": "0.1.0",
        "target_diseases": [{"id": "dx", "display_name": "Dx", "intercept": -1.0}],
        "input_nodes": [
            {"id": "a", "type": "binary"},
            {"id": "b", "type": "binary"},
        ],
        "derived_nodes": [
            {
                "id": "inter_x",
                "node_class": "derived_interaction",
                "operator": "AND",
                "parents": ["a", "unknown_parent"],
            }
        ],
        "edges": [],
    }
    with pytest.raises(ModuleValidationError, match="unknown parent"):
        validate_module(module)


def test_derived_interaction_rejects_target_disease_parent() -> None:
    module = {
        "schema_version": "0.1.0",
        "module_id": "test",
        "display_name": "Test",
        "version": "0.1.0",
        "target_diseases": [{"id": "dx", "display_name": "Dx", "intercept": -1.0}],
        "input_nodes": [
            {"id": "a", "type": "binary"},
        ],
        "derived_nodes": [
            {
                "id": "inter_x",
                "node_class": "derived_interaction",
                "operator": "AND",
                "parents": ["a", "dx"],
            }
        ],
        "edges": [],
    }
    with pytest.raises(
        ModuleValidationError, match="target disease.*cannot be an interaction parent"
    ):
        validate_module(module)


def test_derived_interaction_rejects_self_parent() -> None:
    module = {
        "schema_version": "0.1.0",
        "module_id": "test",
        "display_name": "Test",
        "version": "0.1.0",
        "target_diseases": [{"id": "dx", "display_name": "Dx", "intercept": -1.0}],
        "input_nodes": [
            {"id": "a", "type": "binary"},
        ],
        "derived_nodes": [
            {
                "id": "inter_x",
                "node_class": "derived_interaction",
                "operator": "AND",
                "parents": ["a", "inter_x"],
            }
        ],
        "edges": [],
    }
    with pytest.raises(ModuleValidationError, match="self-parent"):
        validate_module(module)
