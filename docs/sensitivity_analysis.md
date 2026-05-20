# Sensitivity analysis

Sensitivity analysis is essential because the default coefficients are literature-informed starting values, not validated calibration parameters.

The v0.1.0 framework supports one-way beta sensitivity analysis: one edge coefficient is varied across a range while all other coefficients are held constant.

## Why sensitivity analysis matters

Many diagnostic edges are supported by heterogeneous or indirect evidence. Sensitivity analysis helps identify whether posterior probabilities are overly dependent on uncertain coefficients.

High-priority sensitivity edges include:

- subjective positional pattern → BPPV;
- no objective positional nystagmus → BPPV;
- migraine overlap → MD;
- hydrops evidence → MD;
- mild bilateral vestibular hypofunction → PVP;
- severe bilateral vestibular hypofunction → BVP and against PVP;
- central neurologic sign edges.

## Sensitivity configuration

Sensitivity ranges are stored in:

```text
default_modules/sensitivity_ranges.json
```

Example item:

```json
{
  "module_id": "bppv",
  "edge_id": "bppv_e12",
  "from_node": "subjective_positional_pattern",
  "to_node": "dx_bppv",
  "default_beta": 0.7,
  "beta_range": [0.2, 1.0],
  "reason": "Sensitivity-analysis edge."
}
```

## Running sensitivity analysis in Python

```python
from bayesseed.module_loader import load_modules, load_sensitivity_config
from bayesseed.sensitivity import one_way_sensitivity

modules = load_modules("default_modules")
config = load_sensitivity_config("default_modules/sensitivity_ranges.json")

case = {
    "positional_trigger": 1,
    "brief_duration_seconds_minutes": 1,
    "subjective_positional_vertigo_only": 1,
}

result = one_way_sensitivity(
    modules=modules,
    case=case,
    edge_id="bppv_e12",
    beta_values=[0.2, 0.4, 0.7, 1.0],
)

print(result)
```

## Streamlit sensitivity tab

The Streamlit app provides an interactive sensitivity tab. Users can:

1. choose a module;
2. choose a target edge from the sensitivity configuration;
3. move a beta slider;
4. observe changes in posterior probability.

Run:

```bash
streamlit run app/streamlit_app.py
```

## Interpreting results

A robust module should not flip diagnostic ranking from a clinically typical case due to a small coefficient perturbation. Ranking instability may be acceptable in intentionally borderline or mixed-evidence cases.

Interpret results as follows:

| Pattern | Interpretation |
|---|---|
| Posterior changes modestly, ranking stable | coefficient is not driving the module alone |
| Posterior changes substantially, ranking stable | coefficient affects calibration but not ranking |
| Ranking flips across plausible range | edge is structurally important and should be documented |
| Ranking flips in typical cases | module may be over-dependent on that coefficient |

## Recommended reporting

For a manuscript or software paper, report:

- which edges were varied;
- default beta and range;
- rationale for the range;
- representative case used;
- posterior change in target disease;
- whether disease ranking changed.

## Important limitation

One-way sensitivity analysis does not capture interactions among multiple uncertain edges. Future versions may support multi-parameter or probabilistic sensitivity analysis.
