from __future__ import annotations

from pathlib import Path

from bayesseed.module_loader import load_module, load_modules, load_sensitivity_config


def test_load_one_default_module(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    assert module["module_id"] == "bppv"
    assert module["target_diseases"][0]["id"] == "dx_bppv"
    assert module["_source_path"].endswith("bppv.json")


def test_load_modules_skips_schema_and_sensitivity_files(default_modules_dir: Path) -> None:
    modules = load_modules(default_modules_dir)
    module_ids = {module["module_id"] for module in modules}
    assert module_ids == {"bppv", "meniere_disease", "presbyvestibulopathy_with_bvp_competitor"}


def test_load_sensitivity_config(default_modules_dir: Path) -> None:
    items = load_sensitivity_config(default_modules_dir / "sensitivity_ranges.json")
    assert len(items) >= 1
    assert all("edge_id" in item for item in items)
    assert any(item["edge_id"] == "bppv_e05" for item in items)
