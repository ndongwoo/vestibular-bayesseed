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
