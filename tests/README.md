# Tests for Vestibular-BayesSeed

This folder contains the initial pytest suite for the Vestibular-BayesSeed
repository. Copy the `tests/` directory into the project root after combining the
root files, `src/bayesseed/`, `default_modules/`, and `examples/` folders.

Run:

```bash
pip install -e .[dev]
pytest
```

The suite checks:

- logistic-CPD utilities and missingness behavior
- module loading and schema validation
- derived-node evaluation
- synthetic case inference
- one-way sensitivity utilities
- Mermaid/NetworkX exports
- basic CLI commands

These tests are intended to verify software behavior only. They do not establish
clinical diagnostic accuracy.
