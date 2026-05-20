#!/usr/bin/env python3
"""Run the Vestibular-BayesSeed synthetic example cases.

This script is intentionally small and dependency-light. It is designed for
SoftwareX reviewers and new users who want to verify that the default disease
modules can be loaded and executed in one command.

Example
-------
From the repository root::

    python examples/run_examples.py

Optional arguments::

    python examples/run_examples.py --modules default_modules --case-file examples/synthetic_cases.csv
    python examples/run_examples.py --derived-mode probability
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit("pandas is required. Install project dependencies first: pip install -e .") from exc

# Allow running directly from a source checkout without installation.
REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bayesseed.inference import infer_modules, read_case_file  # noqa: E402
from bayesseed.module_loader import load_modules  # noqa: E402


CASE_DESCRIPTIONS: list[dict[str, str]] = [
    {
        "case_id": "S01_typical_pc_bppv",
        "expected_pattern": "BPPV",
        "description": "Typical posterior-canal BPPV pattern with triggered brief vertigo and Dix-Hallpike torsional upbeating nystagmus.",
    },
    {
        "case_id": "S02_typical_hc_bppv",
        "expected_pattern": "BPPV",
        "description": "Horizontal-canal BPPV-like pattern with triggered brief vertigo and supine-roll geotropic/apogeotropic nystagmus.",
    },
    {
        "case_id": "S03_subjective_bppv",
        "expected_pattern": "BPPV, lower confidence",
        "description": "Subjective positional vertigo with negative objective positional testing; intended to show weakly positive subjective-BPPV behavior.",
    },
    {
        "case_id": "S04_central_positional_red_flag",
        "expected_pattern": "Low peripheral-disease confidence",
        "description": "Atypical positional nystagmus plus central neurologic/MRI evidence; intended to show competing red-flag behavior rather than a positive central diagnosis.",
    },
    {
        "case_id": "S05_definite_like_meniere",
        "expected_pattern": "Ménière disease",
        "description": "Definite-like Ménière disease pattern with recurrent 20 min–12 h episodes, auditory symptoms, low-frequency SNHL, and MRI hydrops.",
    },
    {
        "case_id": "S06_meniere_migraine_overlap",
        "expected_pattern": "Ménière disease with overlap penalty",
        "description": "Ménière-like episodic and auditory pattern with migraine features; intended to show weak competing rather than hard-exclusion behavior.",
    },
    {
        "case_id": "S07_typical_pvp",
        "expected_pattern": "Presbyvestibulopathy",
        "description": "Typical PVP-like pattern with age ≥60, chronic vestibular symptoms, gait burden, and mild bilateral vestibular hypofunction.",
    },
    {
        "case_id": "S08_bvp_competitor",
        "expected_pattern": "Bilateral vestibulopathy",
        "description": "BVP-like pattern with chronic gait burden, oscillopsia/darkness worsening, and severe bilateral vestibular hypofunction.",
    },
    {
        "case_id": "S09_mixed_md_pvp_evidence",
        "expected_pattern": "Mixed MD/PVP evidence",
        "description": "Mixed evidence case containing both chronic age-related vestibular hypofunction and partial Ménière-like episodic/cochlear evidence.",
    },
]


def _is_missing(value: Any) -> bool:
    """Return True for values that should not be treated as observed inputs."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def _case_inputs_only(case: dict[str, Any], input_node_ids: set[str]) -> dict[str, Any]:
    """Keep only model input nodes and drop missing cells for cleaner output."""
    return {key: value for key, value in case.items() if key in input_node_ids and not _is_missing(value)}


def _format_contributors(contributions: dict[str, float], *, limit: int = 5) -> str:
    """Format the largest absolute log-odds contributions for a table cell."""
    if not contributions:
        return ""
    items = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)[:limit]
    return "; ".join(f"{name}:{value:+.2f}" for name, value in items)


def run_examples(
    module_path: Path,
    case_file: Path,
    output_dir: Path,
    *,
    derived_mode: str = "threshold",
    derived_threshold: float = 0.5,
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    """Load modules and cases, run inference, and write summary outputs."""
    modules = load_modules(module_path)
    cases = read_case_file(case_file)
    input_node_ids = {node["id"] for module in modules for node in module.get("input_nodes", [])}

    if len(cases) != len(CASE_DESCRIPTIONS):
        print(
            f"Warning: {case_file} contains {len(cases)} cases but the built-in manifest contains "
            f"{len(CASE_DESCRIPTIONS)} descriptions. Generic labels will be used for unmatched rows.",
            file=sys.stderr,
        )

    summary_rows: list[dict[str, Any]] = []
    detailed_outputs: list[dict[str, Any]] = []

    for idx, raw_case in enumerate(cases, start=1):
        manifest = CASE_DESCRIPTIONS[idx - 1] if idx <= len(CASE_DESCRIPTIONS) else {
            "case_id": f"case_{idx:02d}",
            "expected_pattern": "not specified",
            "description": "No built-in description available.",
        }
        case = _case_inputs_only(raw_case, input_node_ids)
        module_results = infer_modules(
            modules,
            case,
            derived_value_mode=derived_mode,
            derived_threshold=derived_threshold,
        )

        disease_rows: list[dict[str, Any]] = []
        for module_result in module_results:
            for disease in module_result.ranked():
                row = disease.to_dict()
                row["module_id"] = module_result.module_id
                row["module_display_name"] = module_result.display_name
                disease_rows.append(row)
        disease_rows.sort(key=lambda r: r["posterior"], reverse=True)

        detailed_outputs.append(
            {
                "case_index": idx,
                "case_id": manifest["case_id"],
                "expected_pattern": manifest["expected_pattern"],
                "description": manifest["description"],
                "observed_inputs": case,
                "disease_results": disease_rows,
                "modules": [module_result.to_dict() for module_result in module_results],
            }
        )

        for rank, disease_row in enumerate(disease_rows, start=1):
            summary_rows.append(
                {
                    "case_index": idx,
                    "case_id": manifest["case_id"],
                    "expected_pattern": manifest["expected_pattern"],
                    "rank": rank,
                    "disease_id": disease_row["disease_id"],
                    "disease_name": disease_row["display_name"],
                    "posterior": round(float(disease_row["posterior"]), 6),
                    "module_id": disease_row["module_id"],
                    "parents_observed": ";".join(disease_row.get("parents_observed", [])),
                    "top_log_odds_contributors": _format_contributors(disease_row.get("contributions", {})),
                }
            )

    summary_df = pd.DataFrame(summary_rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_csv = output_dir / "synthetic_case_results_summary.csv"
    details_json = output_dir / "synthetic_case_results_detailed.json"
    summary_df.to_csv(summary_csv, index=False)
    details_json.write_text(json.dumps(detailed_outputs, ensure_ascii=False, indent=2), encoding="utf-8")

    return summary_df, detailed_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Vestibular-BayesSeed synthetic example cases.")
    parser.add_argument(
        "--modules",
        type=Path,
        default=REPO_ROOT / "default_modules",
        help="Path to a module JSON file or directory. Default: default_modules/",
    )
    parser.add_argument(
        "--case-file",
        type=Path,
        default=Path(__file__).resolve().parent / "synthetic_cases.csv",
        help="CSV or JSON case file. Default: examples/synthetic_cases.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "output",
        help="Directory for summary CSV and detailed JSON outputs. Default: examples/output/",
    )
    parser.add_argument(
        "--derived-mode",
        choices=["threshold", "probability", "centered_probability"],
        default="threshold",
        help="How derived-node probabilities are passed downstream. Default: threshold.",
    )
    parser.add_argument(
        "--derived-threshold",
        type=float,
        default=0.5,
        help="Activation threshold for derived nodes when --derived-mode=threshold. Default: 0.5.",
    )
    args = parser.parse_args()

    summary_df, _ = run_examples(
        module_path=args.modules,
        case_file=args.case_file,
        output_dir=args.output_dir,
        derived_mode=args.derived_mode,
        derived_threshold=args.derived_threshold,
    )

    # Show top-ranked result for each synthetic case in the terminal.
    top1 = summary_df[summary_df["rank"] == 1][
        ["case_index", "case_id", "expected_pattern", "disease_name", "posterior", "top_log_odds_contributors"]
    ]
    print("\nTop-ranked disease for each synthetic case")
    print(top1.to_string(index=False))
    print(f"\nWrote: {args.output_dir / 'synthetic_case_results_summary.csv'}")
    print(f"Wrote: {args.output_dir / 'synthetic_case_results_detailed.json'}")


if __name__ == "__main__":
    main()
