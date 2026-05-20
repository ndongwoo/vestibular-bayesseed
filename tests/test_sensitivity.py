from __future__ import annotations

from pathlib import Path

import pytest

from bayesseed.module_loader import load_module
from bayesseed.sensitivity import apply_beta_overrides, beta_grid, one_way_sensitivity


def test_beta_grid_includes_endpoints() -> None:
    grid = beta_grid(-0.7, 0.0, steps=4)
    assert grid[0] == pytest.approx(-0.7)
    assert grid[-1] == pytest.approx(0.0)
    assert len(grid) == 4


def test_apply_beta_overrides_changes_only_selected_edge(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    altered = apply_beta_overrides(module, {"bppv_e10": -0.7})
    original_edge = next(edge for edge in module["edges"] if edge["id"] == "bppv_e10")
    altered_edge = next(edge for edge in altered["edges"] if edge["id"] == "bppv_e10")
    assert original_edge["suggested_beta"] != altered_edge["suggested_beta"]
    assert altered_edge["suggested_beta"] == pytest.approx(-0.7)


def test_one_way_sensitivity_returns_rows_for_each_beta_and_target(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    rows = one_way_sensitivity(
        module,
        {"positional_trigger": 1, "brief_duration_seconds_minutes": 1, "negative_positional_test": 1},
        edge_id="bppv_e10",
        beta_values=[0.0, -0.3, -0.7],
    )
    assert len(rows) == 3  # BPPV module has one target disease.
    assert {row["beta"] for row in rows} == {0.0, -0.3, -0.7}
    assert all(row["disease_id"] == "dx_bppv" for row in rows)
