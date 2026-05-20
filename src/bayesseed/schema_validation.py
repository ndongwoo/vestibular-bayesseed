"""Lightweight disease-module validation.

The validator intentionally stays permissive. It checks the structural fields
required by the current default modules while allowing additional metadata used
for documentation, evidence tracking, and Streamlit displays.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .exceptions import ModuleValidationError

REQUIRED_MODULE_FIELDS = {
    "schema_version",
    "module_id",
    "display_name",
    "version",
    "target_diseases",
    "input_nodes",
    "derived_nodes",
    "edges",
}

REQUIRED_EDGE_FIELDS = {"id", "from_node", "to_node", "suggested_beta"}
REQUIRED_TARGET_FIELDS = {"id", "intercept"}
REQUIRED_NODE_FIELDS = {"id"}


def _ensure_list(module: Mapping[str, Any], key: str) -> list[Any]:
    value = module.get(key)
    if not isinstance(value, list):
        raise ModuleValidationError(f"'{key}' must be a list.")
    return value


def _ids(items: list[Mapping[str, Any]], label: str) -> set[str]:
    out: set[str] = set()
    for item in items:
        if not isinstance(item, Mapping):
            raise ModuleValidationError(f"Every {label} entry must be an object.")
        missing = REQUIRED_NODE_FIELDS - set(item)
        if missing:
            raise ModuleValidationError(
                f"{label} entry is missing required field(s): {sorted(missing)}"
            )
        node_id = str(item["id"])
        if node_id in out:
            raise ModuleValidationError(f"Duplicate {label} id: {node_id}")
        out.add(node_id)
    return out


def validate_module(module: Mapping[str, Any], *, strict_edges: bool = True) -> bool:
    """Validate a disease module and return ``True`` when valid.

    The function raises :class:`ModuleValidationError` with a human-readable
    message when validation fails.
    """
    missing = REQUIRED_MODULE_FIELDS - set(module)
    if missing:
        raise ModuleValidationError(f"Module is missing required field(s): {sorted(missing)}")

    if not isinstance(module.get("module_id"), str) or not module["module_id"]:
        raise ModuleValidationError("'module_id' must be a non-empty string.")

    input_nodes = _ensure_list(module, "input_nodes")
    derived_nodes = _ensure_list(module, "derived_nodes")
    target_diseases = _ensure_list(module, "target_diseases")
    edges = _ensure_list(module, "edges")

    input_ids = _ids(input_nodes, "input_nodes")
    derived_ids = _ids(derived_nodes, "derived_nodes")

    target_ids: set[str] = set()
    for target in target_diseases:
        if not isinstance(target, Mapping):
            raise ModuleValidationError("Every target_diseases entry must be an object.")
        missing_target = REQUIRED_TARGET_FIELDS - set(target)
        if missing_target:
            raise ModuleValidationError(
                f"target_diseases entry is missing required field(s): {sorted(missing_target)}"
            )
        target_id = str(target["id"])
        if target_id in target_ids:
            raise ModuleValidationError(f"Duplicate target disease id: {target_id}")
        float(target["intercept"])
        target_ids.add(target_id)

    all_node_ids = input_ids | derived_ids | target_ids

    for derived in derived_nodes:
        if "intercept" not in derived:
            raise ModuleValidationError(f"Derived node '{derived['id']}' is missing 'intercept'.")
        float(derived["intercept"])
        parents = derived.get("parents", [])
        if not isinstance(parents, list):
            raise ModuleValidationError(f"Derived node '{derived['id']}' parents must be a list.")

    edge_ids: set[str] = set()
    for edge in edges:
        if not isinstance(edge, Mapping):
            raise ModuleValidationError("Every edge entry must be an object.")
        missing_edge = REQUIRED_EDGE_FIELDS - set(edge)
        if missing_edge:
            raise ModuleValidationError(
                f"Edge is missing required field(s): {sorted(missing_edge)}"
            )
        edge_id = str(edge["id"])
        if edge_id in edge_ids:
            raise ModuleValidationError(f"Duplicate edge id: {edge_id}")
        edge_ids.add(edge_id)
        float(edge["suggested_beta"])
        if strict_edges:
            from_node = str(edge["from_node"])
            to_node = str(edge["to_node"])
            if from_node not in all_node_ids:
                raise ModuleValidationError(
                    f"Edge '{edge_id}' has unknown from_node '{from_node}'."
                )
            if to_node not in all_node_ids:
                raise ModuleValidationError(f"Edge '{edge_id}' has unknown to_node '{to_node}'.")

    return True


def collect_node_ids(module: Mapping[str, Any]) -> dict[str, set[str]]:
    """Return input, derived, target, and all node ID sets for a module."""
    input_ids = {str(n["id"]) for n in module.get("input_nodes", [])}
    derived_ids = {str(n["id"]) for n in module.get("derived_nodes", [])}
    target_ids = {str(n["id"]) for n in module.get("target_diseases", [])}
    return {
        "input": input_ids,
        "derived": derived_ids,
        "target": target_ids,
        "all": input_ids | derived_ids | target_ids,
    }
