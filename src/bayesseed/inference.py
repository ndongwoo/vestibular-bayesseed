"""Inference engine for JSON-defined logistic Bayesian network modules."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .derived_nodes import edge_weights_for_node, evaluate_derived_nodes
from .logistic_cpd import logistic_probability
from .module_loader import load_modules


@dataclass
class DiseaseResult:
    """Result for one target disease node."""

    disease_id: str
    display_name: str
    posterior: float
    intercept: float
    contributions: dict[str, float] = field(default_factory=dict)
    parents_observed: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "disease_id": self.disease_id,
            "display_name": self.display_name,
            "posterior": self.posterior,
            "intercept": self.intercept,
            "contributions": self.contributions,
            "parents_observed": self.parents_observed,
        }


@dataclass
class ModuleInferenceResult:
    """Inference result for one disease module."""

    module_id: str
    display_name: str
    disease_results: list[DiseaseResult]
    raw_inputs: dict[str, float | int | bool | None]
    derived_values: dict[str, float | None]
    derived_trace: dict[str, dict[str, Any]]

    def ranked(self) -> list[DiseaseResult]:
        return sorted(self.disease_results, key=lambda r: r.posterior, reverse=True)

    def to_dict(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "display_name": self.display_name,
            "raw_inputs": self.raw_inputs,
            "derived_values": self.derived_values,
            "derived_trace": self.derived_trace,
            "disease_results": [r.to_dict() for r in self.ranked()],
        }


def normalize_case_values(case: Mapping[str, Any]) -> dict[str, float | int | bool | None]:
    """Normalize case values for inference.

    Accepted truthy/falsy strings are converted to 1/0. Empty strings and common
    missing-value tokens are converted to ``None``.
    """
    missing_tokens = {"", "na", "n/a", "nan", "none", "null", "missing", "unknown"}
    truthy = {"1", "true", "yes", "y", "present", "positive", "pos"}
    falsy = {"0", "false", "no", "n", "absent", "negative", "neg"}
    out: dict[str, float | int | bool | None] = {}
    for key, value in case.items():
        if value is None:
            out[str(key)] = None
        elif isinstance(value, bool):
            out[str(key)] = int(value)
        elif isinstance(value, int | float):
            # Preserve numeric values, but convert NaN to missing.
            if isinstance(value, float) and value != value:
                out[str(key)] = None
            else:
                out[str(key)] = value
        elif isinstance(value, str):
            v = value.strip().lower()
            if v in missing_tokens:
                out[str(key)] = None
            elif v in truthy:
                out[str(key)] = 1
            elif v in falsy:
                out[str(key)] = 0
            else:
                try:
                    out[str(key)] = float(v)
                except ValueError as exc:
                    raise ValueError(f"Cannot interpret case value for '{key}': {value!r}") from exc
        else:
            raise ValueError(f"Unsupported case value type for '{key}': {type(value).__name__}")
    return out


def infer_module(
    module: Mapping[str, Any],
    case: Mapping[str, Any],
    *,
    derived_value_mode: str = "threshold",
    derived_threshold: float = 0.5,
) -> ModuleInferenceResult:
    """Run inference for a single disease module and one case.

    By default, derived nodes pass thresholded 0/1 activations downstream.
    Use ``derived_value_mode="probability"`` for fully soft propagation.
    """
    raw_inputs = normalize_case_values(case)
    derived_values, derived_trace = evaluate_derived_nodes(
        module, raw_inputs, value_mode=derived_value_mode, threshold=derived_threshold
    )
    all_values: dict[str, float | int | bool | None] = dict(raw_inputs)
    all_values.update(derived_values)

    disease_results: list[DiseaseResult] = []
    for target in module.get("target_diseases", []):
        disease_id = str(target["id"])
        weights = edge_weights_for_node(module, disease_id)
        posterior, contributions = logistic_probability(
            float(target.get("intercept", 0.0)),
            weights,
            all_values,
            require_observed_parent=False,
        )
        # posterior cannot be None when require_observed_parent is false.
        disease_results.append(
            DiseaseResult(
                disease_id=disease_id,
                display_name=str(target.get("display_name", disease_id)),
                posterior=float(posterior),
                intercept=float(target.get("intercept", 0.0)),
                contributions=contributions,
                parents_observed=sorted(contributions),
            )
        )

    return ModuleInferenceResult(
        module_id=str(module.get("module_id", "unknown_module")),
        display_name=str(module.get("display_name", module.get("module_id", "unknown_module"))),
        disease_results=disease_results,
        raw_inputs=raw_inputs,
        derived_values=derived_values,
        derived_trace=derived_trace,
    )


def infer_modules(
    modules: Sequence[Mapping[str, Any]],
    case: Mapping[str, Any],
    *,
    derived_value_mode: str = "threshold",
    derived_threshold: float = 0.5,
) -> list[ModuleInferenceResult]:
    """Run inference for multiple modules and one case."""
    return [
        infer_module(
            module,
            case,
            derived_value_mode=derived_value_mode,
            derived_threshold=derived_threshold,
        )
        for module in modules
    ]


def _sanitize_for_json(data: dict[str, Any]) -> dict[str, Any]:
    """Recursively convert NaN and other float NaN values to None for safe JSON output."""
    sanitized: dict[str, Any] = {}
    for k, v in data.items():
        if isinstance(v, float) and v != v:
            sanitized[k] = None
        elif isinstance(v, dict):
            sanitized[k] = _sanitize_for_json(v)
        else:
            sanitized[k] = v
    return sanitized


def infer_case(
    module_path: str | Path,
    case: Mapping[str, Any],
    *,
    derived_value_mode: str = "threshold",
    derived_threshold: float = 0.5,
) -> dict[str, Any]:
    """Convenience wrapper: load modules from *module_path* and infer one case."""
    modules = load_modules(module_path)
    results = infer_modules(
        modules, case, derived_value_mode=derived_value_mode, derived_threshold=derived_threshold
    )
    disease_rows: list[dict[str, Any]] = []
    for result in results:
        for disease in result.ranked():
            row = disease.to_dict()
            row["module_id"] = result.module_id
            row["module_display_name"] = result.display_name
            disease_rows.append(row)
    disease_rows.sort(key=lambda r: r["posterior"], reverse=True)
    return _sanitize_for_json(
        {
            "case": dict(case),
            "disease_results": disease_rows,
            "modules": [r.to_dict() for r in results],
        }
    )


def read_case_file(path: str | Path) -> list[dict[str, Any]]:
    """Read cases from JSON or CSV.

    JSON may be either a single object or a list of objects. CSV requires pandas.
    """
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".json":
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            return [dict(x) for x in data]
        raise ValueError("JSON case file must be an object or a list of objects.")
    if suffix == ".csv":
        import pandas as pd

        df = pd.read_csv(p)
        return df.to_dict(orient="records")
    raise ValueError("Case file must be .json or .csv")


def _clean_nan(value: Any) -> Any:
    """Convert float NaN to None so JSON serialization remains safe."""
    if isinstance(value, float) and value != value:
        return None
    return value


def batch_infer(
    module_path: str | Path,
    case_file: str | Path,
    *,
    derived_value_mode: str = "threshold",
    derived_threshold: float = 0.5,
) -> list[dict[str, Any]]:
    """Run inference for each case in a JSON/CSV case file."""
    modules = load_modules(module_path)
    cases = read_case_file(case_file)
    outputs: list[dict[str, Any]] = []
    for i, case in enumerate(cases, start=1):
        results = infer_modules(
            modules,
            case,
            derived_value_mode=derived_value_mode,
            derived_threshold=derived_threshold,
        )
        rows: list[dict[str, Any]] = []
        for result in results:
            for disease in result.ranked():
                row = disease.to_dict()
                row["module_id"] = result.module_id
                row["module_display_name"] = result.display_name
                rows.append(row)
        rows.sort(key=lambda r: r["posterior"], reverse=True)
        sanitized_case = {k: _clean_nan(v) for k, v in case.items()}
        outputs.append({"case_index": i, "case": sanitized_case, "disease_results": rows})
    return outputs
