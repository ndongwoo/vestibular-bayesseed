# Table 2. Major software functionalities

| Functionality | Implementation | Purpose |
|---|---|---|
| Disease module loading | `module_loader.py` reads JSON modules from `default_modules/` | Separates clinical domain knowledge from reusable inference code |
| Schema validation | `schema_validation.py` | Checks required fields and internal consistency before inference |
| Logistic CPD calculation | `logistic_cpd.py` | Computes node probabilities from intercepts and weighted parent states |
| Derived-node evaluation | `derived_nodes.py` | Converts raw clinical observations into intermediate clinical constructs |
| Inference orchestration | `inference.py` | Runs multi-module posterior calculations for one case or a batch of cases |
| Sensitivity analysis | `sensitivity.py` | Varies selected coefficients within predefined ranges |
| Visualization export | `visualization.py` | Generates edge lists, NetworkX objects, and Mermaid diagrams |
| Command-line interface | `cli.py` and `bayesseed` entry point | Enables reproducible validation, inference, and graph export |
| Synthetic demonstrations | `examples/synthetic_cases.csv`, `examples/run_examples.py` | Demonstrates model behavior without patient data |
| Interactive demonstration | `app/streamlit_app.py` | Provides an educational UI for module viewing, case simulation, evidence inspection, and sensitivity analysis |
| Documentation | `docs/` | Guides installation, usage, module extension, evidence mapping, and clinical limitations |
| Tests | `tests/` | Verifies core functions, default modules, CLI behavior, and examples |

