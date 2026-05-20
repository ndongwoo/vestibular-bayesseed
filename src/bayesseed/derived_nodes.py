"""Evaluation of derived/intermediate nodes."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from .exceptions import InferenceError
from .logistic_cpd import logistic_probability
from .schema_validation import collect_node_ids


def incoming_edges(module: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Return edges grouped by their ``to_node``."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in module.get("edges", []):
        grouped[str(edge["to_node"])].append(dict(edge))
    return dict(grouped)


def edge_weights_for_node(module: Mapping[str, Any], node_id: str) -> dict[str, float]:
    """Return parent beta coefficients for one node."""
    weights: dict[str, float] = {}
    for edge in module.get("edges", []):
        if str(edge.get("to_node")) == node_id:
            weights[str(edge["from_node"])] = float(edge["suggested_beta"])
    return weights


def _derived_node_map(module: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(node["id"]): dict(node) for node in module.get("derived_nodes", [])}


def evaluate_derived_nodes(
    module: Mapping[str, Any],
    raw_values: Mapping[str, float | int | bool | None],
    *,
    max_passes: int = 100,
    value_mode: str = "threshold",
    threshold: float = 0.5,
) -> tuple[dict[str, float | None], dict[str, dict[str, Any]]]:
    """Evaluate all derived nodes in dependency order.

    Missing raw inputs stay missing. A derived node is returned as ``None`` when
    none of its parents is observed or computed; this prevents a default baseline
    probability from becoming evidence downstream when there is no information
    for that construct.

    ``value_mode`` controls what is passed downstream:

    - ``"threshold"``: pass 1.0 if probability >= threshold, else 0.0.
      This is the default because it prevents low baseline probabilities in
      partially observed derived nodes from acting as unintended weak evidence.
    - ``"probability"``: pass the soft probability itself.
    - ``"centered_probability"``: pass max(0, probability - threshold) /
      (1 - threshold), preserving only probability above the activation point.

    Returns
    -------
    tuple
        ``(derived_values, trace)`` where trace contains probability and
        contribution details for each derived node.
    """
    node_sets = collect_node_ids(module)
    derived_ids = node_sets["derived"]
    derived_map = _derived_node_map(module)
    values: dict[str, float | int | bool | None] = dict(raw_values)
    derived_values: dict[str, float | None] = {}
    trace: dict[str, dict[str, Any]] = {}

    unresolved = set(derived_ids)
    passes = 0
    while unresolved and passes < max_passes:
        progressed = False
        passes += 1
        for node_id in list(unresolved):
            weights = edge_weights_for_node(module, node_id)
            # Parent is available when it is raw/present or a derived node already resolved.
            parent_ids = set(weights)
            unresolved_derived_parents = (parent_ids & derived_ids) - set(derived_values)
            if unresolved_derived_parents:
                continue

            node = derived_map[node_id]
            probability, contributions = logistic_probability(
                float(node.get("intercept", 0.0)),
                weights,
                values,
                require_observed_parent=True,
            )
            if probability is None:
                downstream_value = None
            elif value_mode == "probability":
                downstream_value = probability
            elif value_mode == "threshold":
                downstream_value = 1.0 if probability >= threshold else 0.0
            elif value_mode == "centered_probability":
                downstream_value = max(0.0, probability - threshold) / max(1e-12, 1.0 - threshold)
            else:
                raise InferenceError("value_mode must be one of: threshold, probability, centered_probability")

            derived_values[node_id] = downstream_value
            values[node_id] = downstream_value
            trace[node_id] = {
                "node_id": node_id,
                "probability": probability,
                "value": downstream_value,
                "value_mode": value_mode,
                "threshold": threshold,
                "intercept": float(node.get("intercept", 0.0)),
                "contributions": contributions,
                "parents_observed": sorted(contributions),
                "description": node.get("description", ""),
            }
            unresolved.remove(node_id)
            progressed = True
        if not progressed:
            raise InferenceError(
                "Could not resolve derived-node dependencies. Check for cycles or missing node IDs: "
                + ", ".join(sorted(unresolved))
            )
    if unresolved:
        raise InferenceError("Derived-node evaluation exceeded maximum passes.")

    return derived_values, trace
