"""Streamlit demonstration UI for Vestibular-BayesSeed.

This app is intentionally a frontend over the reusable ``bayesseed`` Python
package. It should not contain disease-specific inference logic. The disease
knowledge lives in JSON modules, and the inference engine lives under
``src/bayesseed``.

Run from the repository root with:

    streamlit run app/streamlit_app.py

The app is for research and educational demonstration only. It is not a
validated medical device and must not be used for diagnosis, treatment, or
patient management.
"""

from __future__ import annotations

import json
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

try:  # Plotly is an optional dependency declared in pyproject.toml [project.optional-dependencies].
    import plotly.express as px
except Exception:  # pragma: no cover - Streamlit app fallback
    px = None


# -----------------------------------------------------------------------------
# Robust local import handling
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent
SRC_DIR = REPO_ROOT / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bayesseed.inference import infer_modules  # noqa: E402
from bayesseed.module_loader import load_modules, load_sensitivity_config  # noqa: E402
from bayesseed.sensitivity import beta_grid, one_way_sensitivity  # noqa: E402
from bayesseed.visualization import edge_list, to_mermaid  # noqa: E402


# -----------------------------------------------------------------------------
# Streamlit configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Vestibular-BayesSeed",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Path discovery and cached loaders
# -----------------------------------------------------------------------------
def _candidate_paths(*relative_paths: str) -> list[Path]:
    roots = [Path.cwd(), REPO_ROOT, REPO_ROOT.parent, APP_DIR]
    out: list[Path] = []
    for root in roots:
        for rel in relative_paths:
            p = (root / rel).resolve()
            if p not in out:
                out.append(p)
    return out


def default_module_path() -> str:
    env_path = os.environ.get("BAYESSEED_MODULES")
    if env_path:
        return env_path
    for p in _candidate_paths("default_modules", "modules"):
        if p.exists() and p.is_dir():
            return str(p)
    return str((REPO_ROOT / "default_modules").resolve())


def default_case_file() -> str:
    env_path = os.environ.get("BAYESSEED_CASES")
    if env_path:
        return env_path
    for p in _candidate_paths("examples/synthetic_cases.csv"):
        if p.exists() and p.is_file():
            return str(p)
    return str((REPO_ROOT / "examples" / "synthetic_cases.csv").resolve())


def default_evidence_table_path() -> str | None:
    env_path = os.environ.get("BAYESSEED_EVIDENCE_TABLE")
    if env_path:
        return env_path
    candidates = _candidate_paths(
        "edge_level_evidence_table_v0_1_0.csv",
        "docs/edge_level_evidence_table.csv",
        "docs/evidence_table.csv",
        "edge_level_evidence_table.csv",
    )
    for p in candidates:
        if p.exists() and p.is_file():
            return str(p)
    return None


def default_sensitivity_path(module_path: str) -> str | None:
    env_path = os.environ.get("BAYESSEED_SENSITIVITY")
    if env_path:
        return env_path
    candidates = [
        Path(module_path) / "sensitivity_ranges.json",
        *_candidate_paths("default_modules/sensitivity_ranges.json", "modules/sensitivity_ranges.json"),
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            return str(p)
    return None


@st.cache_data(show_spinner=False)
def cached_load_modules(path: str) -> list[dict[str, Any]]:
    return load_modules(path)


@st.cache_data(show_spinner=False)
def cached_load_cases(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    if p.suffix.lower() == ".csv":
        return pd.read_csv(p)
    if p.suffix.lower() == ".json":
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = [data]
        return pd.DataFrame(data)
    return pd.DataFrame()


@st.cache_data(show_spinner=False)
def cached_load_evidence_table(path: str | None, modules_json: str) -> pd.DataFrame:
    if path:
        p = Path(path)
        if p.exists() and p.suffix.lower() == ".csv":
            return pd.read_csv(p)
        if p.exists() and p.suffix.lower() == ".json":
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return pd.DataFrame(data)
            if isinstance(data, dict):
                return pd.DataFrame(data.get("items", data.get("edges", [])))
    modules = json.loads(modules_json)
    rows: list[dict[str, Any]] = []
    for module in modules:
        for edge in module.get("edges", []):
            rows.append(
                {
                    "module_id": module.get("module_id"),
                    "module_display_name": module.get("display_name"),
                    "edge_id": edge.get("id"),
                    "from_node": edge.get("from_node"),
                    "to_node": edge.get("to_node"),
                    "edge_direction": edge.get("edge_direction", "supportive"),
                    "suggested_beta": edge.get("suggested_beta"),
                    "beta_min": (edge.get("suggested_beta_range") or [None, None])[0],
                    "beta_max": (edge.get("suggested_beta_range") or [None, None])[1],
                    "evidence_strength": edge.get("evidence_strength"),
                    "evidence_basis": edge.get("evidence_basis"),
                    "placement": edge.get("placement"),
                    "sensitivity_analysis": edge.get("sensitivity_analysis"),
                    "comments": edge.get("comments"),
                }
            )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def cached_load_sensitivity(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    return load_sensitivity_config(p)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def module_to_display_name(module: dict[str, Any]) -> str:
    return f"{module.get('display_name', module.get('module_id'))} ({module.get('module_id')})"


def modules_as_json(modules: list[dict[str, Any]]) -> str:
    # cache_data needs hashable input; JSON string is stable enough for this app.
    return json.dumps(modules, sort_keys=True, ensure_ascii=False)


def node_label_map(module: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for n in module.get("input_nodes", []):
        mapping[str(n.get("id"))] = str(n.get("label", n.get("id")))
    for n in module.get("derived_nodes", []):
        mapping[str(n.get("id"))] = str(n.get("label", n.get("description", n.get("id"))))
    for n in module.get("target_diseases", []):
        mapping[str(n.get("id"))] = str(n.get("display_name", n.get("id")))
    return mapping


def node_summary(module: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for n in module.get("input_nodes", []):
        rows.append(
            {
                "node_id": n.get("id"),
                "node_type": "input",
                "label": n.get("label", n.get("id")),
                "intercept": None,
                "description": n.get("description", ""),
            }
        )
    for n in module.get("derived_nodes", []):
        rows.append(
            {
                "node_id": n.get("id"),
                "node_type": "derived",
                "label": n.get("label", n.get("id")),
                "intercept": n.get("intercept"),
                "description": n.get("description", ""),
            }
        )
    for n in module.get("target_diseases", []):
        rows.append(
            {
                "node_id": n.get("id"),
                "node_type": "target_disease",
                "label": n.get("display_name", n.get("id")),
                "intercept": n.get("intercept"),
                "description": n.get("intercept_policy", ""),
            }
        )
    return pd.DataFrame(rows)


def input_nodes_for_modules(modules: list[dict[str, Any]]) -> pd.DataFrame:
    seen: dict[str, dict[str, Any]] = {}
    for module in modules:
        module_id = module.get("module_id")
        for n in module.get("input_nodes", []):
            node_id = str(n.get("id"))
            if node_id not in seen:
                seen[node_id] = {
                    "node_id": node_id,
                    "label": n.get("label", node_id),
                    "type": n.get("type", "binary"),
                    "modules": [module_id],
                }
            else:
                if module_id not in seen[node_id]["modules"]:
                    seen[node_id]["modules"].append(module_id)
    rows = list(seen.values())
    for row in rows:
        row["modules"] = ", ".join(str(x) for x in row["modules"])
    return pd.DataFrame(rows).sort_values(["modules", "node_id"]).reset_index(drop=True)


def normalize_case_from_ui(values: dict[str, str]) -> dict[str, int | None]:
    translated: dict[str, int | None] = {}
    for key, value in values.items():
        if value == "Present / positive":
            translated[key] = 1
        elif value == "Absent / negative":
            translated[key] = 0
        else:
            translated[key] = None
    return translated


def case_from_preset(cases_df: pd.DataFrame, preset_label: str) -> dict[str, Any]:
    if cases_df.empty:
        return {}
    id_cols = [c for c in ["case_id", "id", "name", "label"] if c in cases_df.columns]
    if id_cols:
        id_col = id_cols[0]
        row = cases_df.loc[cases_df[id_col].astype(str) == preset_label]
        if row.empty:
            row = cases_df.iloc[[0]]
    else:
        row = cases_df.iloc[[int(preset_label.split()[1]) - 1]]
    series = row.iloc[0]
    out: dict[str, Any] = {}
    metadata_cols = {"case_id", "id", "name", "label", "expected_top", "description", "notes"}
    for key, value in series.items():
        if key in metadata_cols:
            continue
        if pd.isna(value):
            out[str(key)] = None
        else:
            out[str(key)] = value
    return out


def flatten_inference_results(results: list[Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for result in results:
        for rank, disease in enumerate(result.ranked(), start=1):
            rows.append(
                {
                    "rank_within_module": rank,
                    "module_id": result.module_id,
                    "module": result.display_name,
                    "disease_id": disease.disease_id,
                    "disease": disease.display_name,
                    "posterior": disease.posterior,
                    "intercept": disease.intercept,
                    "observed_parent_count": len(disease.parents_observed),
                }
            )
    return pd.DataFrame(rows).sort_values("posterior", ascending=False).reset_index(drop=True)


def contribution_dataframe(result: Any) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    label_maps = {}
    for disease in result.ranked():
        for parent, contribution in disease.contributions.items():
            rows.append(
                {
                    "disease_id": disease.disease_id,
                    "disease": disease.display_name,
                    "parent_node": parent,
                    "contribution": contribution,
                }
            )
    return pd.DataFrame(rows).sort_values("contribution", ascending=False) if rows else pd.DataFrame()


def derived_trace_dataframe(result: Any) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for node_id, trace in result.derived_trace.items():
        rows.append(
            {
                "derived_node": node_id,
                "probability": trace.get("probability"),
                "downstream_value": trace.get("value"),
                "parents_observed": ", ".join(trace.get("parents_observed", [])),
                "description": trace.get("description", ""),
            }
        )
    return pd.DataFrame(rows).sort_values("derived_node") if rows else pd.DataFrame()


def st_dataframe(df: pd.DataFrame, *, height: int | None = None) -> None:
    if df.empty:
        st.info("No rows to display.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True, height=height)


def download_json_button(label: str, data: Any, file_name: str) -> None:
    st.download_button(
        label,
        data=json.dumps(data, indent=2, ensure_ascii=False),
        file_name=file_name,
        mime="application/json",
    )


# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
st.sidebar.title("Vestibular-BayesSeed")
st.sidebar.caption("Interactive research demonstration UI")

module_path = st.sidebar.text_input("Module directory", value=default_module_path())
case_file = st.sidebar.text_input("Synthetic case CSV/JSON", value=default_case_file())
evidence_table_path = st.sidebar.text_input(
    "Evidence table CSV/JSON", value=default_evidence_table_path() or ""
)
sensitivity_path = st.sidebar.text_input(
    "Sensitivity config JSON", value=default_sensitivity_path(module_path) or ""
)

st.sidebar.divider()
derived_value_mode = st.sidebar.selectbox(
    "Derived-node propagation mode",
    options=["threshold", "probability", "centered_probability"],
    index=0,
    help=(
        "threshold passes 0/1 activations downstream; probability passes soft probabilities; "
        "centered_probability passes only probability above the activation threshold."
    ),
)
derived_threshold = st.sidebar.slider("Derived activation threshold", 0.10, 0.90, 0.50, 0.05)

st.sidebar.divider()
st.sidebar.warning(
    "Research/educational demonstration only. This is not a validated medical device and must not be used for patient care.",
    icon="⚠️",
)


# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
try:
    modules = cached_load_modules(module_path)
except Exception as exc:
    st.error(f"Could not load disease modules from `{module_path}`: {exc}")
    st.stop()

cases_df = cached_load_cases(case_file)
modules_json = modules_as_json(modules)
evidence_df = cached_load_evidence_table(evidence_table_path or None, modules_json)
sensitivity_items = cached_load_sensitivity(sensitivity_path or None)

module_options = {module_to_display_name(m): m for m in modules}
module_ids = {str(m.get("module_id")): m for m in modules}


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.title("Vestibular-BayesSeed")
st.subheader("Open-source seed framework for evidence-anchored logistic Bayesian diagnostic networks")

with st.expander("Intended use and scope", expanded=False):
    st.markdown(
        """
        This Streamlit app demonstrates how JSON-defined vestibular disease modules can be
        inspected, simulated, and sensitivity-tested. It is designed to support a SoftwareX-style
        open-source research software submission.

        **It is not a validated clinical decision-support system.** The included BPPV, Ménière's
        disease, and presbyvestibulopathy/bilateral vestibulopathy modules are transparent worked
        examples, not deployment-ready diagnostic models.
        """
    )


# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------
tab_overview, tab_module, tab_case, tab_evidence, tab_sensitivity = st.tabs(
    ["Overview", "Module viewer", "Case simulator", "Evidence table", "Sensitivity analysis"]
)


# -----------------------------------------------------------------------------
# Overview tab
# -----------------------------------------------------------------------------
with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Loaded modules", len(modules))
    c2.metric("Target diseases", sum(len(m.get("target_diseases", [])) for m in modules))
    c3.metric("Input nodes", len(input_nodes_for_modules(modules)))
    c4.metric("Edges", sum(len(m.get("edges", [])) for m in modules))

    st.markdown("### Architecture")
    st.markdown(
        """
        The software separates **domain knowledge** from **inference logic**:

        1. Disease-specific knowledge is stored in JSON modules.
        2. The Python package validates modules, evaluates derived nodes, and computes logistic-CPD posteriors.
        3. This Streamlit app provides an optional interactive frontend for demonstration and education.
        """
    )

    arch_df = pd.DataFrame(
        [
            {"Layer": "JSON disease modules", "Responsibility": "Input nodes, derived nodes, target diseases, edges, beta values, evidence metadata"},
            {"Layer": "bayesseed core engine", "Responsibility": "Schema validation, derived-node evaluation, logistic CPD inference, sensitivity analysis"},
            {"Layer": "CLI / examples", "Responsibility": "Reproducible batch execution for SoftwareX reviewers and users"},
            {"Layer": "Streamlit app", "Responsibility": "Interactive module inspection, case simulation, evidence review, sensitivity testing"},
        ]
    )
    st_dataframe(arch_df)

    st.markdown("### Loaded module summary")
    summary_rows = []
    for module in modules:
        summary_rows.append(
            {
                "module_id": module.get("module_id"),
                "display_name": module.get("display_name"),
                "role": module.get("module_role", ""),
                "version": module.get("version", ""),
                "input_nodes": len(module.get("input_nodes", [])),
                "derived_nodes": len(module.get("derived_nodes", [])),
                "target_diseases": len(module.get("target_diseases", [])),
                "edges": len(module.get("edges", [])),
            }
        )
    st_dataframe(pd.DataFrame(summary_rows))


# -----------------------------------------------------------------------------
# Module viewer tab
# -----------------------------------------------------------------------------
with tab_module:
    st.markdown("### Disease module viewer")
    selected_label = st.selectbox("Select module", list(module_options), key="module_viewer_select")
    selected_module = module_options[selected_label]

    st.markdown(f"#### {selected_module.get('display_name', selected_module.get('module_id'))}")
    st.caption(selected_module.get("module_role", ""))

    meta_cols = st.columns(4)
    meta_cols[0].metric("Inputs", len(selected_module.get("input_nodes", [])))
    meta_cols[1].metric("Derived nodes", len(selected_module.get("derived_nodes", [])))
    meta_cols[2].metric("Targets", len(selected_module.get("target_diseases", [])))
    meta_cols[3].metric("Edges", len(selected_module.get("edges", [])))

    st.markdown("#### Nodes")
    st_dataframe(node_summary(selected_module), height=320)

    st.markdown("#### Edges")
    edge_df = pd.DataFrame(edge_list(selected_module))
    st_dataframe(edge_df, height=360)

    st.markdown("#### Mermaid network code")
    st.caption("Copy this block into a Mermaid-enabled Markdown viewer to render the module diagram.")
    st.code(to_mermaid(selected_module), language="mermaid")

    st.markdown("#### Raw JSON module")
    with st.expander("Show JSON", expanded=False):
        st.json(selected_module)
    download_json_button(
        "Download selected module JSON",
        selected_module,
        f"{selected_module.get('module_id', 'module')}.json",
    )


# -----------------------------------------------------------------------------
# Case simulator tab
# -----------------------------------------------------------------------------
with tab_case:
    st.markdown("### Case simulator")
    st.caption("Missing inputs are treated as unobserved, not as negative evidence.")

    run_all = st.checkbox("Run all loaded modules", value=True)
    if run_all:
        sim_modules = modules
    else:
        selected_sim_labels = st.multiselect(
            "Select modules to run",
            list(module_options),
            default=list(module_options)[:1],
        )
        sim_modules = [module_options[x] for x in selected_sim_labels]

    use_preset = st.checkbox("Use a synthetic preset case", value=not cases_df.empty)
    case: dict[str, Any]

    if use_preset and not cases_df.empty:
        if "case_id" in cases_df.columns:
            preset_options = [str(x) for x in cases_df["case_id"].tolist()]
        else:
            preset_options = [f"Case {i}" for i in range(1, len(cases_df) + 1)]
        preset_label = st.selectbox("Preset case", preset_options)
        case = case_from_preset(cases_df, preset_label)
        st.markdown("#### Preset input values")
        preset_view = pd.DataFrame(
            [{"node_id": k, "value": v} for k, v in case.items() if v is not None]
        ).sort_values("node_id")
        st_dataframe(preset_view, height=280)
    else:
        input_df = input_nodes_for_modules(sim_modules)
        st.markdown("#### Manual input")
        st.caption("Choose Missing unless the finding is explicitly observed as present or absent.")
        ui_values: dict[str, str] = {}
        cols = st.columns(2)
        for i, row in input_df.iterrows():
            col = cols[i % 2]
            label = f"{row['label']}  ·  `{row['node_id']}`"
            ui_values[row["node_id"]] = col.selectbox(
                label,
                options=["Missing / unobserved", "Present / positive", "Absent / negative"],
                index=0,
                key=f"manual_{row['node_id']}",
            )
        case = normalize_case_from_ui(ui_values)

    if st.button("Run inference", type="primary"):
        if not sim_modules:
            st.error("No modules selected.")
        else:
            try:
                results = infer_modules(
                    sim_modules,
                    case,
                    derived_value_mode=derived_value_mode,
                    derived_threshold=derived_threshold,
                )
            except Exception as exc:
                st.error(f"Inference failed: {exc}")
            else:
                result_df = flatten_inference_results(results)
                st.markdown("#### Ranked target disease posteriors")
                st_dataframe(result_df, height=260)

                if not result_df.empty and px is not None:
                    fig = px.bar(
                        result_df,
                        x="disease",
                        y="posterior",
                        hover_data=["module_id", "disease_id", "intercept", "observed_parent_count"],
                        title="Posterior probabilities",
                    )
                    fig.update_yaxes(range=[0, 1])
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("#### Module-level explanations")
                for result in results:
                    with st.expander(f"{result.display_name} ({result.module_id})", expanded=False):
                        st.markdown("**Derived-node trace**")
                        st_dataframe(derived_trace_dataframe(result), height=260)

                        st.markdown("**Target-node contributions**")
                        st_dataframe(contribution_dataframe(result), height=260)

                st.markdown("#### Download results")
                download_json_button(
                    "Download detailed inference JSON",
                    [r.to_dict() for r in results],
                    "inference_results.json",
                )


# -----------------------------------------------------------------------------
# Evidence table tab
# -----------------------------------------------------------------------------
with tab_evidence:
    st.markdown("### Edge-level evidence table")
    st.caption("This table is loaded from the evidence CSV/JSON when available; otherwise it is reconstructed from module edge metadata.")

    if evidence_df.empty:
        st.info("No evidence table found.")
    else:
        filtered = evidence_df.copy()
        cols = st.columns(4)
        module_col = "disease_module" if "disease_module" in filtered.columns else "module_id"
        strength_col = "evidence_strength" if "evidence_strength" in filtered.columns else None
        placement_col = "recommended_placement" if "recommended_placement" in filtered.columns else "placement" if "placement" in filtered.columns else None
        direction_col = "edge_direction" if "edge_direction" in filtered.columns else None

        if module_col in filtered.columns:
            module_values = ["All"] + sorted(filtered[module_col].dropna().astype(str).unique().tolist())
            selected_module_filter = cols[0].selectbox("Module", module_values)
            if selected_module_filter != "All":
                filtered = filtered[filtered[module_col].astype(str) == selected_module_filter]

        if strength_col:
            strength_values = ["All"] + sorted(filtered[strength_col].dropna().astype(str).unique().tolist())
            selected_strength = cols[1].selectbox("Evidence strength", strength_values)
            if selected_strength != "All":
                filtered = filtered[filtered[strength_col].astype(str) == selected_strength]

        if placement_col:
            placement_values = ["All"] + sorted(filtered[placement_col].dropna().astype(str).unique().tolist())
            selected_placement = cols[2].selectbox("Placement", placement_values)
            if selected_placement != "All":
                filtered = filtered[filtered[placement_col].astype(str) == selected_placement]

        if direction_col:
            direction_values = ["All"] + sorted(filtered[direction_col].dropna().astype(str).unique().tolist())
            selected_direction = cols[3].selectbox("Direction", direction_values)
            if selected_direction != "All":
                filtered = filtered[filtered[direction_col].astype(str) == selected_direction]

        query = st.text_input("Search evidence text or node IDs", value="")
        if query.strip():
            q = query.strip().lower()
            mask = filtered.apply(lambda row: q in " ".join(row.astype(str).str.lower().tolist()), axis=1)
            filtered = filtered[mask]

        st_dataframe(filtered, height=520)
        st.download_button(
            "Download filtered evidence table CSV",
            filtered.to_csv(index=False),
            "filtered_edge_evidence_table.csv",
            mime="text/csv",
        )


# -----------------------------------------------------------------------------
# Sensitivity tab
# -----------------------------------------------------------------------------
with tab_sensitivity:
    st.markdown("### One-way sensitivity analysis")
    st.caption("Change one beta coefficient over its configured range and inspect posterior changes.")

    if not sensitivity_items:
        st.info("No sensitivity configuration found. Provide `default_modules/sensitivity_ranges.json` or set BAYESSEED_SENSITIVITY.")
    else:
        sensitivity_df = pd.DataFrame(sensitivity_items)
        available_module_ids = sorted(sensitivity_df["module_id"].dropna().astype(str).unique().tolist())
        selected_sens_module_id = st.selectbox("Module", available_module_ids)
        sens_module = module_ids.get(selected_sens_module_id)
        if sens_module is None:
            st.error(f"Loaded modules do not include `{selected_sens_module_id}`.")
        else:
            module_items = [x for x in sensitivity_items if str(x.get("module_id")) == selected_sens_module_id]
            edge_labels = {
                f"{item.get('edge_id')} · {item.get('from_node')} → {item.get('to_node')}": item
                for item in module_items
            }
            selected_edge_label = st.selectbox("Edge", list(edge_labels))
            selected_item = edge_labels[selected_edge_label]

            st.markdown("#### Sensitivity edge metadata")
            st.json(selected_item)

            # Case selection for sensitivity analysis.
            if not cases_df.empty:
                if "case_id" in cases_df.columns:
                    preset_options = [str(x) for x in cases_df["case_id"].tolist()]
                else:
                    preset_options = [f"Case {i}" for i in range(1, len(cases_df) + 1)]
                sens_preset = st.selectbox("Case for sensitivity analysis", preset_options, key="sens_preset")
                sens_case = case_from_preset(cases_df, sens_preset)
            else:
                st.warning("No synthetic case file found; using an empty case.")
                sens_case = {}

            beta_min, beta_max = selected_item.get("beta_range", [None, None])
            if beta_min is None or beta_max is None:
                st.error("Selected sensitivity item does not contain a beta_range.")
            else:
                steps = st.slider("Grid steps", 3, 21, 9, 2)
                grid = beta_grid(float(beta_min), float(beta_max), steps=steps)
                try:
                    rows = one_way_sensitivity(
                        sens_module,
                        sens_case,
                        str(selected_item.get("edge_id")),
                        grid,
                        derived_value_mode=derived_value_mode,
                        derived_threshold=derived_threshold,
                    )
                except Exception as exc:
                    st.error(f"Sensitivity analysis failed: {exc}")
                else:
                    sens_out_df = pd.DataFrame(rows)
                    st_dataframe(sens_out_df, height=300)
                    if not sens_out_df.empty and px is not None:
                        fig = px.line(
                            sens_out_df,
                            x="beta",
                            y="posterior",
                            color="display_name",
                            markers=True,
                            title="Posterior probability across beta values",
                        )
                        fig.update_yaxes(range=[0, 1])
                        st.plotly_chart(fig, use_container_width=True)
                    st.download_button(
                        "Download sensitivity results CSV",
                        sens_out_df.to_csv(index=False),
                        "sensitivity_results.csv",
                        mime="text/csv",
                    )
