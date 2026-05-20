# Edge-level evidence table description

The repository includes an edge-level evidence table derived from the literature-informed coefficient-initialization document. The table is intended to make the default disease modules transparent and inspectable.

## Recommended file locations

```text
edge_level_evidence_table_v0_1_0.csv
edge_level_evidence_table_v0_1_0.xlsx
edge_level_evidence_table_v0_1_0.json
edge_level_evidence_table_v0_1_0.md
```

## Intended use in the software

The evidence table supports:

1. module inspection in the Streamlit interface;
2. reviewer-readable explanation of default coefficients;
3. sensitivity analysis range definitions;
4. future updates when users add or revise disease modules.

## Main fields

| Field | Meaning |
|---|---|
| `edge_id` | Unique identifier for an edge |
| `disease_module` | Disease module in which the edge appears |
| `from_node` | Parent node |
| `to_node` | Child node |
| `edge_direction` | Supportive, competing, or negative effect |
| `suggested_beta` | Default coefficient used in the worked module |
| `beta_min`, `beta_max` | Plausible sensitivity range |
| `evidence_strength` | Qualitative strength category |
| `evidence_source` | Diagnostic criterion, meta-analysis, cohort, expert rationale, or other source type |
| `evidence_type` | How the evidence was interpreted |
| `recommended_placement` | Raw-to-derived, derived-to-diagnosis, or competing edge placement |
| `sensitivity_analysis` | Whether the edge is prioritized for sensitivity testing |
| `applicability_concerns` | Notes about transportability, heterogeneity, or protocol dependence |

## Manuscript language

Suggested wording for the SoftwareX manuscript:

> The default modules are accompanied by an edge-level evidence table. For each edge, the table records the parent and child nodes, coefficient, plausible sensitivity range, evidence type, recommended network placement, and applicability concerns. These metadata are used by the Streamlit interface and are intended to make the worked modules inspectable rather than to claim universal calibration.

