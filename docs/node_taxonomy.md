# Node taxonomy

Vestibular-BayesSeed uses a small set of node types so that disease modules remain transparent and extensible.

## 1. Input nodes

Input nodes are raw observations supplied by a user, case file, or future data-entry interface.

Examples:

- `positional_trigger`
- `brief_duration_seconds_minutes`
- `dix_hallpike_torsional_upbeating_nystagmus`
- `low_frequency_snhl`
- `mri_endolymphatic_hydrops`
- `mild_bilateral_vestibular_hypofunction`

Input nodes should be as close as possible to observable clinical facts. They should not already encode the final diagnosis.

### Recommended fields

```json
{
  "id": "positional_trigger",
  "type": "binary",
  "label": "Vertigo/dizziness triggered by head position change"
}
```

### Missingness policy

Unobserved inputs are treated as missing, not as negative evidence. If absence itself is clinically meaningful, define a separate explicit input node such as:

- `negative_positional_test`
- `no_objective_positional_nystagmus`
- `absence_of_central_signs`

This avoids confusing "not observed" with "observed to be absent."

## 2. Logistic derived nodes

Logistic derived nodes are intermediate clinical constructs calculated from input nodes or other derived nodes using a logistic conditional probability distribution (CPD).

Examples:

- `brief_triggered_positional_syndrome`
- `posterior_canal_positional_pattern`
- `auditory_cluster`
- `endolymphatic_hydrops_evidence`
- `gait_balance_symptom_burden`
- `non_central_chronic_vestibular_pattern`

Derived nodes are useful when multiple raw findings represent the same diagnostic construct. They make the network more interpretable and reduce double counting.

### Recommended fields

```json
{
  "id": "posterior_canal_positional_pattern",
  "display_name": "Posterior-canal positional pattern",
  "intercept": -2.0,
  "parents": [
    "dix_hallpike_torsional_upbeating_nystagmus"
  ]
}
```

## 2a. Derived interaction nodes

Derived interaction nodes are a special subclass of derived nodes. They are deterministic engineered features generated from primitive or derived observations, rather than probabilistic constructs with their own intercept and sigmoid CPD.

### Key properties

- **Deterministic activation:** The node evaluates to 1 only when all parent nodes are active (logical AND). Unlike logistic derived nodes, derived interaction nodes do not require an intercept.
- **Used only in the probabilistic ranking track:** They contribute to disease probability through a downstream edge weight, but they are not outputs of the deterministic criteria-audit track.
- **Residual excess log-odds:** The interaction coefficient on the edge from the derived interaction node to a target disease captures evidence *beyond* the additive main effects of the parents. This avoids double-counting evidence that is already represented by the parents' own edges.
- **Not diagnostic-criteria audit outputs:** The field `criteria_audit_output` is always `false`. These nodes do not signal that a formal diagnostic criterion has been met; they are probabilistic-engineering features used to model synergistic evidence patterns.

### Example

```json
{
  "id": "pc_positional_concordance",
  "node_class": "derived_interaction",
  "interaction_type": "evidence_concordance",
  "operator": "AND",
  "parents": [
    "brief_triggered_positional_syndrome",
    "posterior_canal_positional_pattern"
  ],
  "criteria_audit_output": false,
  "weight_interpretation": "residual_excess_log_odds",
  "missingness_policy": "unobserved_not_imputed",
  "description": "Residual evidence-concordance interaction between brief triggered positional syndrome and posterior-canal positional nystagmus. This is not a diagnostic-criteria audit output."
}
```

In the BPPV worked example, `pc_positional_concordance` and `hc_positional_concordance` capture the idea that concordance between a broad triggered positional syndrome and a canal-specific nystagmus pattern provides synergistic evidence beyond what either parent contributes independently.

## 3. Target disease nodes

Target disease nodes are final diagnostic probability nodes.

Examples:

- `dx_bppv`
- `dx_meniere_disease`
- `dx_presbyvestibulopathy`
- `dx_bilateral_vestibulopathy`

Each target disease node has an intercept. The intercept is a setting-specific baseline log-odds, not a universal disease prevalence.

### Recommended fields

```json
{
  "id": "dx_bppv",
  "display_name": "BPPV",
  "intercept": -2.2,
  "intercept_policy": "Placeholder specialty-clinic prior; configure by setting and stage before validation."
}
```

## 4. Modifier and competing nodes

Some inputs or derived nodes do not simply support a disease; they modify the interpretation or favor an alternative diagnosis.

Examples:

- `central_neurologic_sign_or_mri_lesion`
- `atypical_positional_red_flag`
- `migraine_overlap_pattern`
- `severe_bilateral_vestibular_hypofunction`

These nodes may have negative edges to one disease and positive edges to another.

For example:

```text
severe_bilateral_vestibular_hypofunction → dx_bilateral_vestibulopathy  positive
severe_bilateral_vestibular_hypofunction → dx_presbyvestibulopathy      negative
```

## 5. Edge types

Edges are stored separately from node definitions.

### Supportive edge

A supportive edge increases the log-odds of the child node when the parent is present.

```json
{
  "id": "bppv_e03",
  "from_node": "dix_hallpike_torsional_upbeating_nystagmus",
  "to_node": "posterior_canal_positional_pattern",
  "edge_direction": "supportive",
  "beta": 2.2
}
```

### Competing edge

A competing edge decreases the log-odds of the child node when the parent is present.

```json
{
  "id": "bppv_e15",
  "from_node": "central_neurologic_sign_or_mri_lesion",
  "to_node": "dx_bppv",
  "edge_direction": "competing",
  "beta": -1.8
}
```

## 6. Preferred modeling pattern

The preferred pattern is:

```text
raw clinical input → derived clinical pattern → target disease
```

Direct raw input → target disease edges should be used sparingly if an appropriate derived node already exists. When direct edges are used alongside derived nodes, the direct edge should usually be weak unless it represents independent information.
