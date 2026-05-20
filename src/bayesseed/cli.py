"""Command-line interface for Vestibular-BayesSeed."""

from __future__ import annotations

import json
from pathlib import Path

import click

from .inference import batch_infer, infer_case, read_case_file
from .module_loader import load_module, load_modules
from .schema_validation import validate_module
from .visualization import to_mermaid


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    """Run and inspect logistic Bayesian diagnostic modules."""


@main.command("validate")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
def validate_cmd(paths: tuple[Path, ...]) -> None:
    """Validate one or more module JSON files or directories."""
    if not paths:
        raise click.UsageError("Provide at least one module file or directory.")
    ok = 0
    failed = 0
    for path in paths:
        candidates = sorted(path.glob("*.json")) if path.is_dir() else [path]
        for candidate in candidates:
            try:
                module = load_module(candidate, validate=False)
                validate_module(module)
                click.echo(f"OK    {candidate}")
                ok += 1
            except Exception as exc:
                click.echo(f"FAIL  {candidate}: {exc}", err=True)
                failed += 1
    if failed:
        raise click.ClickException(f"{failed} file(s) failed validation; {ok} passed.")


@main.command("list-modules")
@click.option("--modules", "module_path", required=True, type=click.Path(exists=True, path_type=Path))
def list_modules_cmd(module_path: Path) -> None:
    """List loadable disease modules in a directory."""
    modules = load_modules(module_path)
    for module in modules:
        targets = ", ".join(t.get("id", "") for t in module.get("target_diseases", []))
        click.echo(f"{module.get('module_id')}\t{module.get('display_name')}\t{targets}")


@main.command("run")
@click.option("--modules", "module_path", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--case-file", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path), help="Optional JSON output path.")
@click.option("--pretty/--compact", default=True, help="Pretty-print JSON to stdout.")
@click.option(
    "--derived-mode",
    type=click.Choice(["threshold", "probability", "centered_probability"]),
    default="threshold",
    show_default=True,
    help="How derived-node probabilities are passed downstream.",
)
@click.option("--derived-threshold", default=0.5, show_default=True, type=float)
def run_cmd(
    module_path: Path,
    case_file: Path,
    output: Path | None,
    pretty: bool,
    derived_mode: str,
    derived_threshold: float,
) -> None:
    """Run inference for a JSON or CSV case file."""
    # Use batch_infer for both single and multiple cases.
    results = batch_infer(
        module_path,
        case_file,
        derived_value_mode=derived_mode,
        derived_threshold=derived_threshold,
    )
    text = json.dumps(results, ensure_ascii=False, indent=2 if pretty else None)
    if output:
        output.write_text(text, encoding="utf-8")
        click.echo(f"Wrote {output}")
    else:
        click.echo(text)


@main.command("run-one")
@click.option("--modules", "module_path", required=True, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--derived-mode",
    type=click.Choice(["threshold", "probability", "centered_probability"]),
    default="threshold",
    show_default=True,
)
@click.option("--derived-threshold", default=0.5, show_default=True, type=float)
@click.argument("case_json", type=str)
def run_one_cmd(module_path: Path, case_json: str, derived_mode: str, derived_threshold: float) -> None:
    """Run one inline JSON case, e.g. '{"positional_trigger": 1}'."""
    case = json.loads(case_json)
    result = infer_case(
        module_path,
        case,
        derived_value_mode=derived_mode,
        derived_threshold=derived_threshold,
    )
    click.echo(json.dumps(result, ensure_ascii=False, indent=2))


@main.command("mermaid")
@click.argument("module_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path), help="Optional .mmd output path.")
def mermaid_cmd(module_file: Path, output: Path | None) -> None:
    """Export a module as Mermaid flowchart text."""
    module = load_module(module_file)
    text = to_mermaid(module)
    if output:
        output.write_text(text, encoding="utf-8")
        click.echo(f"Wrote {output}")
    else:
        click.echo(text)


if __name__ == "__main__":  # pragma: no cover
    main()
