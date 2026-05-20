# Vestibular-BayesSeed documentation

This folder contains user and developer documentation for **Vestibular-BayesSeed**, an open-source seed framework for building evidence-anchored logistic Bayesian diagnostic networks.

Vestibular-BayesSeed is designed as a transparent, extensible research framework. It is not a validated clinical decision-support system and must not be used for clinical diagnosis, treatment decisions, triage, or patient management.

## Documentation map

| File | Purpose |
|---|---|
| [`overview.md`](overview.md) | High-level project purpose, architecture, and intended use |
| [`node_taxonomy.md`](node_taxonomy.md) | Definitions of input nodes, derived nodes, target disease nodes, modifiers, and competing nodes |
| [`evidence_to_parameter_mapping.md`](evidence_to_parameter_mapping.md) | How literature-derived ORs, LRs, diagnostic criteria, and expert priors are mapped to logistic coefficients |
| [`default_modules.md`](default_modules.md) | Description of the BPPV, Ménière disease, and PVP/BVP default modules |
| [`adding_new_disease_module.md`](adding_new_disease_module.md) | Step-by-step guide for adding a new disease module |
| [`sensitivity_analysis.md`](sensitivity_analysis.md) | How and why to run one-way beta sensitivity analyses |
| [`cli_reference.md`](cli_reference.md) | Command-line usage examples |
| [`api_reference.md`](api_reference.md) | Minimal Python API usage examples |
| [`streamlit_demo.md`](streamlit_demo.md) | Guide to the optional Streamlit demonstration app |
| [`repository_assembly.md`](repository_assembly.md) | How to assemble the generated archives into one repository |
| [`softwarex_user_guide.md`](softwarex_user_guide.md) | SoftwareX-oriented usage, reproducibility, and submission notes |
| [`medical_disclaimer.md`](medical_disclaimer.md) | Research-use and non-clinical-use disclaimer |

## Minimal workflow

From the repository root:

```bash
pip install -e .[app,dev]
pytest
python examples/run_examples.py
streamlit run app/streamlit_app.py
```

## Recommended reader path

New users should read:

1. [`overview.md`](overview.md)
2. [`node_taxonomy.md`](node_taxonomy.md)
3. [`default_modules.md`](default_modules.md)
4. [`streamlit_demo.md`](streamlit_demo.md)

Developers extending the software should read:

1. [`evidence_to_parameter_mapping.md`](evidence_to_parameter_mapping.md)
2. [`adding_new_disease_module.md`](adding_new_disease_module.md)
3. [`cli_reference.md`](cli_reference.md)
4. [`api_reference.md`](api_reference.md)
5. [`sensitivity_analysis.md`](sensitivity_analysis.md)

Authors preparing a SoftwareX submission should also read:

1. [`repository_assembly.md`](repository_assembly.md)
2. [`softwarex_user_guide.md`](softwarex_user_guide.md)
3. [`medical_disclaimer.md`](medical_disclaimer.md)
