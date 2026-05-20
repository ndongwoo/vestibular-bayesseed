# Adding a new disease module

This guide describes how to add a new disease module to Vestibular-BayesSeed.

A disease module is a JSON file that defines:

1. target disease node or nodes;
2. input nodes;
3. derived nodes;
4. edges and coefficients;
5. evidence metadata and sensitivity ranges.

## Step 1. Define the module scope

Start with a narrow, clinically interpretable module.

Good initial scope:

```text
AUVP module for acute unilateral vestibulopathy
```

Too broad:

```text
All acute dizziness diagnoses
```

The best module is small enough that each input, derived node, and edge can be justified.

## Step 2. Define the target disease node

Create a target disease node with a placeholder intercept.

```json
{
  "id": "dx_auvp",
  "display_name": "Acute unilateral vestibulopathy",
  "intercept": -3.0,
  "intercept_policy": "Placeholder; adjust by target clinical setting before validation."
}
```

The intercept is not a universal disease prevalence. It should be adjusted to the expected baseline probability in the target clinic, referral pathway, and diagnostic stage.

## Step 3. List raw input nodes

Input nodes should represent observable findings.

Examples:

```json
{
  "id": "acute_continuous_vertigo",
  "type": "binary",
  "label": "Acute continuous vertigo lasting at least 24 hours"
}
```

```json
{
  "id": "abnormal_head_impulse_unilateral",
  "type": "binary",
  "label": "Unilateral abnormal head impulse test"
}
```

Avoid input nodes that already encode the final diagnosis, such as:

```text
meets_auvp_criteria
```

Instead, represent the criteria components separately.

## Step 4. Create derived nodes

Derived nodes should represent clinically meaningful intermediate constructs.

Examples:

```json
{
  "id": "acute_unilateral_vestibular_syndrome_pattern",
  "display_name": "Acute unilateral vestibular syndrome pattern",
  "intercept": -2.0,
  "parents": [
    "acute_continuous_vertigo",
    "spontaneous_unidirectional_nystagmus",
    "abnormal_head_impulse_unilateral"
  ]
}
```

Use derived nodes when several raw findings represent a single construct. This reduces double counting and improves explainability.

## Step 5. Add edges

Each edge should have:

- `id`
- `from_node`
- `to_node`
- `edge_direction`
- `beta`
- optional evidence metadata

Example:

```json
{
  "id": "auvp_e01",
  "from_node": "acute_continuous_vertigo",
  "to_node": "acute_unilateral_vestibular_syndrome_pattern",
  "edge_direction": "supportive",
  "beta": 1.0,
  "evidence_strength": "moderate",
  "evidence_type": "criteria-based",
  "recommended_placement": "raw_to_derived",
  "comments": "Syndromic feature; not specific by itself."
}
```

## Step 6. Add negative and competing evidence

Do not ignore red flags or alternative-diagnosis signs.

Examples:

```json
{
  "id": "auvp_e20",
  "from_node": "new_unilateral_hearing_loss",
  "to_node": "dx_auvp",
  "edge_direction": "competing",
  "beta": -0.8,
  "comments": "New hearing loss is atypical for isolated AUVP and should raise alternative diagnoses."
}
```

```json
{
  "id": "auvp_e21",
  "from_node": "central_neurologic_sign_or_mri_lesion",
  "to_node": "dx_auvp",
  "edge_direction": "competing",
  "beta": -1.8,
  "comments": "Central findings favor non-peripheral causes."
}
```

## Step 7. Validate the JSON file

From the repository root:

```bash
bayesseed validate default_modules/auvp.json
```

or validate all modules:

```bash
bayesseed validate default_modules/
```

## Step 8. Add synthetic cases

Add representative rows to `examples/synthetic_cases.csv` or create a new example CSV.

Use synthetic cases to demonstrate behavior, not to claim diagnostic accuracy.

Suggested cases:

- typical disease-positive case;
- atypical case with missing evidence;
- red-flag case;
- competing diagnosis case;
- mixed-evidence case.

## Step 9. Add sensitivity ranges

Uncertain edges should be entered in `default_modules/sensitivity_ranges.json`.

Example:

```json
{
  "module_id": "auvp",
  "edge_id": "auvp_e20",
  "from_node": "new_unilateral_hearing_loss",
  "to_node": "dx_auvp",
  "default_beta": -0.8,
  "beta_range": [-1.3, -0.3],
  "reason": "Atypical for isolated AUVP, but exact magnitude is uncertain."
}
```

## Step 10. Run examples and tests

```bash
python examples/run_examples.py
pytest
```

If the new module is meant for publication, add at least one test that confirms expected behavior.

## Checklist for a new module

Before committing a new disease module, verify:

- [ ] target disease node is defined;
- [ ] raw input nodes are observable and not final diagnoses;
- [ ] derived nodes are clinically meaningful;
- [ ] edge IDs are unique;
- [ ] all edge endpoints exist;
- [ ] coefficient signs are clinically plausible;
- [ ] negative/competing evidence is modeled when relevant;
- [ ] uncertain edges have sensitivity ranges;
- [ ] JSON validation passes;
- [ ] at least one synthetic case runs;
- [ ] module documentation includes intended use and limitations.
