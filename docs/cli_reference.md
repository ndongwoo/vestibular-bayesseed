# Command-line interface reference

The package exposes the `bayesseed` command after installation.

Install from the repository root:

```bash
pip install -e .
```

For development and Streamlit features:

```bash
pip install -e .[app,dev]
```

## Validate modules

Validate one module:

```bash
bayesseed validate default_modules/bppv.json
```

Validate a directory of modules:

```bash
bayesseed validate default_modules/
```

Expected output:

```text
OK    default_modules/bppv.json
OK    default_modules/meniere_disease.json
OK    default_modules/pvp_bvp.json
```

## List modules

```bash
bayesseed list-modules --modules default_modules/
```

This lists module IDs, display names, and target disease nodes.

## Run a single case from JSON input

```bash
bayesseed run-one --modules default_modules/ '{"positional_trigger":1,"brief_duration_seconds_minutes":1,"dix_hallpike_torsional_upbeating_nystagmus":1}'
```

## Run a case file

```bash
bayesseed run --modules default_modules/ --case-file examples/synthetic_cases.csv
```

Save output:

```bash
bayesseed run \
  --modules default_modules/ \
  --case-file examples/synthetic_cases.csv \
  --output examples/output/results.json
```

## Derived-node propagation modes

The default mode is `threshold`.

```bash
bayesseed run \
  --modules default_modules/ \
  --case-file examples/synthetic_cases.csv \
  --derived-mode threshold
```

Available modes:

| Mode | Meaning |
|---|---|
| `threshold` | derived probability ≥ threshold becomes 1.0, otherwise 0.0 |
| `probability` | pass derived probability downstream directly |
| `centered_probability` | pass centered probability downstream; useful for experimental behavior |

Default threshold:

```text
0.5
```

## Export Mermaid network code

```bash
bayesseed mermaid default_modules/bppv.json
```

Save to a file:

```bash
bayesseed mermaid default_modules/bppv.json > docs/bppv_network.mmd
```

## Recommended smoke test

From a freshly assembled repository:

```bash
pip install -e .[app,dev]
bayesseed validate default_modules/
bayesseed list-modules --modules default_modules/
python examples/run_examples.py
pytest
```

If all commands work, the repository is ready for demonstration and software-paper preparation.
