from __future__ import annotations

from pathlib import Path

from bayesseed.module_loader import load_module
from bayesseed.visualization import edge_list, to_mermaid, to_networkx


def test_edge_list_contains_display_fields(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    rows = edge_list(module)
    assert rows
    assert {"from", "to", "beta", "direction", "placement", "evidence_strength"}.issubset(rows[0])


def test_to_mermaid_exports_flowchart(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    text = to_mermaid(module)
    assert text.startswith("flowchart LR")
    assert "dx_bppv" in text
    assert "posterior_canal_positional_pattern" in text


def test_to_networkx_contains_expected_nodes_and_edges(bppv_module_path: Path) -> None:
    module = load_module(bppv_module_path)
    graph = to_networkx(module)
    assert graph.has_node("positional_trigger")
    assert graph.has_node("dx_bppv")
    assert graph.has_edge("posterior_canal_positional_pattern", "dx_bppv")
