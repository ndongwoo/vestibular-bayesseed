"""Network export helpers for diagrams and Streamlit displays."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def edge_list(module: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return module edges in a display-friendly format."""
    rows: list[dict[str, Any]] = []
    for edge in module.get("edges", []):
        rows.append(
            {
                "from": edge.get("from_node"),
                "to": edge.get("to_node"),
                "beta": edge.get("suggested_beta"),
                "direction": edge.get("edge_direction", "supportive"),
                "placement": edge.get("placement", ""),
                "evidence_strength": edge.get("evidence_strength", ""),
            }
        )
    return rows


def to_networkx(module: Mapping[str, Any]):
    """Convert a module to a networkx.DiGraph.

    networkx is imported lazily so the core inference engine remains lightweight.
    """
    import networkx as nx

    graph = nx.DiGraph(module_id=module.get("module_id"), display_name=module.get("display_name"))
    for node in module.get("input_nodes", []):
        graph.add_node(node["id"], node_type="input", label=node.get("label", node["id"]))
    for node in module.get("derived_nodes", []):
        graph.add_node(node["id"], node_type="derived", label=node.get("label", node["id"]))
    for node in module.get("target_diseases", []):
        graph.add_node(node["id"], node_type="target", label=node.get("display_name", node["id"]))
    for edge in module.get("edges", []):
        graph.add_edge(
            edge["from_node"],
            edge["to_node"],
            beta=float(edge["suggested_beta"]),
            edge_id=edge.get("id"),
            direction=edge.get("edge_direction", "supportive"),
            placement=edge.get("placement", ""),
        )
    return graph


def to_mermaid(module: Mapping[str, Any]) -> str:
    """Export a module as a simple Mermaid flowchart."""
    lines = ["flowchart LR"]
    for node in module.get("input_nodes", []):
        node_id = str(node["id"])
        label = str(node.get("label", node_id)).replace('"', "'")
        lines.append(f'  {node_id}["{label}"]')
    for node in module.get("derived_nodes", []):
        node_id = str(node["id"])
        label = str(node.get("description", node_id)).replace('"', "'")
        label = label[:60] + ("..." if len(label) > 60 else "")
        lines.append(f'  {node_id}(("{node_id}"))')
    for node in module.get("target_diseases", []):
        node_id = str(node["id"])
        label = str(node.get("display_name", node_id)).replace('"', "'")
        lines.append(f'  {node_id}{{"{label}"}}')
    for edge in module.get("edges", []):
        beta = float(edge.get("suggested_beta", 0.0))
        sign = "+" if beta >= 0 else "−"
        label = f"{sign}{abs(beta):.2f}"
        lines.append(f'  {edge["from_node"]} -- "{label}" --> {edge["to_node"]}')
    return "\n".join(lines) + "\n"
