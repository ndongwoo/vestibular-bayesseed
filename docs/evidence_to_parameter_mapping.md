# Evidence-to-parameter mapping

This document describes how literature-derived evidence is converted into initial logistic coefficients for Vestibular-BayesSeed disease modules.

The default modules use conservative, literature-informed initialization values. These values are not clinically validated calibration parameters.

## Logistic CPD scale

Each node is calculated as:

```text
P(node = 1 | parents) = sigmoid(intercept + Σ beta_i × parent_i)
```

The coefficient `beta_i` lives on the log-odds scale.

## Base transformations

When quantitative diagnostic evidence is available, use the following transformations:

| Evidence source | Base coefficient |
|---|---|
| Odds ratio | `ln(OR)` |
| Positive likelihood ratio | `ln(LR+)` |
| Negative likelihood ratio | `ln(LR−)` |
| Sensitivity/specificity | convert to LR first, then use `ln(LR)` |
| Expected baseline prevalence | `logit(prevalence)` for an intercept |

For a binary diagnostic test:

```text
LR+ = sensitivity / (1 - specificity)
LR- = (1 - sensitivity) / specificity
```

Then:

```text
beta_plus  = ln(LR+)
beta_minus = ln(LR-)
```

## Conservative initialization rule

The recommended initialization rule is:

```text
beta_init = clip(q × p × beta_0, -2.5, +2.5)
```

where:

- `beta_0` is the base effect estimate;
- `q` is an evidence-quality discount;
- `p` is a placement discount;
- `clip` limits extreme coefficients in a seed framework.

The default coefficient cap is:

```text
-2.5 ≤ beta_init ≤ +2.5
```

## Qualitative evidence scale

When a paper provides criteria-level or consensus evidence but no stable quantitative LR or OR, use a capped qualitative prior.

| Evidence strength | Suggested uncapped range | Practical interpretation |
|---|---:|---|
| Very weak | ±0.2 to ±0.4 | nonspecific symptom or weak indirect pathophysiology |
| Weak | ±0.4 to ±0.7 | symptom-cluster component or soft competing evidence |
| Moderate | ±0.7 to ±1.2 | phenotype support or modest diagnostic LR |
| Strong | ±1.2 to ±1.8 | criteria-defining pattern or strong test support |
| Very strong | ±1.8 to ±2.5 | highly specific objective finding, still capped |

## Evidence-quality discount `q`

Recommended default values:

| Evidence source | Suggested `q` |
|---|---:|
| Official diagnostic criterion or major guideline | 0.7 to 0.9 |
| High-quality meta-analysis | 0.7 to 0.9 |
| Prospective cohort or multicenter diagnostic study | 0.5 to 0.8 |
| Retrospective cohort | 0.3 to 0.6 |
| Case-control diagnostic study | 0.3 to 0.5 |
| Expert consensus without quantitative estimate | 0.2 to 0.4 |
| Pure pathophysiologic plausibility | 0.1 to 0.3 |

## Placement discount `p`

Placement is critical because the same clinical construct may appear at more than one network layer.

| Edge placement | Suggested `p` | Rationale |
|---|---:|---|
| Raw input → derived pattern, when the source directly defines the pattern | 0.8 to 1.0 | best place to encode observable pattern |
| Derived pattern → diagnosis, when the same finding already built the pattern | 0.5 to 0.8 | avoids reusing the same evidence twice |
| Direct raw input → diagnosis despite an existing derived node | 0.2 to 0.5 | usually avoid unless the raw feature carries independent information |
| Negative or competing edge | 0.7 to 1.0 | appropriate when literature treats the finding as atypical, central, or alternative-diagnosis evidence |

## Prior uncertainty

For future Bayesian updating, coefficients may be treated as prior means with different uncertainties:

| Edge type | Suggested prior |
|---|---|
| Strong quantitative edge | `Normal(mu, SD 0.35–0.5)` |
| Moderate edge | `Normal(mu, SD 0.5–0.8)` |
| Weak or heterogeneous edge | `Normal(mu, SD 0.8–1.2)` |
| Expert-only edge | `Normal(mu, SD 1.0–1.3)` |

The v0.1.0 core engine uses fixed coefficients and sensitivity ranges rather than full Bayesian coefficient distributions.

## Intercepts

Diagnosis-node intercepts should not be set from general population prevalence.

Use the expected prevalence in the intended clinical pathway, such as:

- primary-care vertigo clinic;
- first-visit otology dizziness clinic;
- tertiary vestibular laboratory referral;
- emergency department acute vestibular syndrome pathway;
- stage-specific setting such as history-only versus test-confirmed stage.

Default intercepts in the worked modules are placeholders and should be reconfigured before formal validation.

## Example mapping

A diagnostic study reports sensitivity 0.82 and specificity 0.71 for a test.

```text
LR+ = 0.82 / (1 - 0.71) = 2.83
ln(LR+) = 1.04
```

If the test result is a broad test finding rather than a canal-specific defining pattern, beta around +1.0 may be reasonable. If the raw input encodes a specific pattern-defining finding, a stronger capped prior may be justified at the raw → derived layer, while the downstream derived → diagnosis edge should be moderated to avoid double counting.

## Implementation fields

Recommended edge fields:

```json
{
  "id": "edge_id",
  "from_node": "parent_node",
  "to_node": "child_node",
  "edge_direction": "supportive",
  "beta": 1.2,
  "beta_range": [0.7, 1.5],
  "evidence_strength": "moderate",
  "evidence_type": "criteria-based",
  "evidence_basis": "Brief rationale",
  "recommended_placement": "raw_to_derived",
  "applicability_concerns": "Potential transportability issue"
}
```

## Derived interaction nodes

Derived interaction nodes (`node_class: "derived_interaction"`) are deterministic engineered features, not logistic CPD derived nodes. Their parameters are set differently:

- **No intercept:** The node evaluates to 1 if (and only if) all parents are 1 (logical AND). There is no sigmoid function or intercept.
- **Downstream edge weight:** The edge from the interaction node to the target disease carries a single coefficient that represents *residual excess log-odds* — the additional log-odds gained when both (or all) parents co-occur, beyond what they contribute independently through their own edges.
- **Setting the coefficient:** This is not derived from a standard LR or OR. Instead, it reflects the extent to which the co-occurrence of two patterns is more informative than the sum of their parts. A conservative starting point is ±0.5 to ±1.5, with sensitivity analysis to explore robustness.
- **Not double-counting:** Because the parents already have their own edges to the downstream target, the interaction coefficient should be moderate. It captures synergy, not duplicated evidence.

Example from the BPPV module:

```text
pc_positional_concordance → dx_bppv    beta = 1.0   (range 0.5 - 1.5)
```

Both `brief_triggered_positional_syndrome` and `posterior_canal_positional_pattern` already have independent edges to `dx_bppv`. The concordance node adds a residual term for the case in which both fire together.

## Practical warning

Do not treat literature-derived ORs, LRs, or criteria-level evidence as universally transportable. Case mix, referral setting, test protocols, disease spectrum, and covariate adjustment all change the meaning of published estimates.
