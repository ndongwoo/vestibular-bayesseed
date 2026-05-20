# Vestibular-BayesSeed core engine v0.1.0

This archive contains the initial `src/bayesseed/` Python core engine.

## Included modules

- `logistic_cpd.py`: sigmoid/logit/logistic-CPD calculation utilities
- `module_loader.py`: JSON disease-module and sensitivity-config loaders
- `schema_validation.py`: lightweight validation for default module structure
- `derived_nodes.py`: derived/intermediate node evaluation
- `inference.py`: single-case and batch inference functions
- `sensitivity.py`: one-way beta sensitivity utilities
- `visualization.py`: edge-list, NetworkX, and Mermaid export helpers
- `cli.py`: command-line interface registered as `bayesseed`

## Quick smoke test

From the repository root after copying `src/` into the project:

```bash
pip install -e .
bayesseed validate default_modules/bppv.json
bayesseed list-modules --modules default_modules/
bayesseed run-one --modules default_modules/ '{"positional_trigger":1,"brief_duration_seconds_minutes":1,"dix_hallpike_torsional_upbeating_nystagmus":1}'
```

## Derived node propagation

The default inference mode is `derived_value_mode="threshold"`, meaning derived-node probabilities are passed downstream as 1.0 if they are ≥0.5 and 0.0 otherwise. This avoids unintended weak downstream evidence from low baseline probabilities when a derived construct is only partially observed. Soft propagation remains available with `derived_value_mode="probability"`.

This software is for research and educational demonstrations only. It is not a validated medical device or clinical decision-support system.
