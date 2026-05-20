from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from bayesseed.cli import main


def test_cli_list_modules(default_modules_dir: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["list-modules", "--modules", str(default_modules_dir)])
    assert result.exit_code == 0
    assert "bppv" in result.output
    assert "meniere_disease" in result.output
    assert "presbyvestibulopathy_with_bvp_competitor" in result.output


def test_cli_validate_module(bppv_module_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(bppv_module_path)])
    assert result.exit_code == 0
    assert "OK" in result.output


def test_cli_run_one(default_modules_dir: Path) -> None:
    runner = CliRunner()
    case_json = '{"positional_trigger": 1, "brief_duration_seconds_minutes": 1, "dix_hallpike_torsional_upbeating_nystagmus": 1}'
    result = runner.invoke(main, ["run-one", "--modules", str(default_modules_dir), case_json])
    assert result.exit_code == 0
    assert '"disease_id": "dx_bppv"' in result.output


def test_cli_mermaid(bppv_module_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["mermaid", str(bppv_module_path)])
    assert result.exit_code == 0
    assert result.output.startswith("flowchart LR")
