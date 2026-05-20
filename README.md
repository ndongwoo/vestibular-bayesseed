# Vestibular-BayesSeed

**Vestibular-BayesSeed** is an open-source seed framework for constructing **evidence-anchored logistic Bayesian diagnostic networks** for vestibular disorders.

The project is designed as a transparent, extensible starting point for clinical knowledge engineering rather than as a validated medical diagnostic system. The initial default modules are intended to demonstrate the framework using three representative vestibular diagnostic phenotypes:

- **Benign paroxysmal positional vertigo (BPPV)**: a positional/nystagmus-driven disorder
- **Ménière's disease (MD)**: an audio-vestibular episodic disorder
- **Presbyvestibulopathy (PVP)** with **bilateral vestibulopathy (BVP)** as a competing threshold-based diagnosis

The software separates disease-specific knowledge from the inference engine. Disease modules are stored in JSON files, while the Python package handles schema validation, derived-node evaluation, logistic-CPD inference, sensitivity analysis, and optional interactive visualization.

---

## Important medical disclaimer

This software is intended for **research, education, and methodological demonstration only**.

It is **not** a validated clinical decision-support system, **not** a medical device, and **must not** be used for clinical diagnosis, treatment decisions, triage, or patient management without appropriate clinical validation, governance, and regulatory review.

The example coefficients are literature-informed initialization values, not universally calibrated diagnostic probabilities. They should be treated as transparent starting values for research and sensitivity analysis.

---

## Why this project exists

Vestibular diagnosis often requires the integration of heterogeneous evidence:

- symptom timing and triggers
- positional nystagmus patterns
- audiometry
- vestibular testing
- imaging or exclusionary findings
- competing and overlapping syndromes

Rule-based criteria are clinically useful but can be difficult to apply when information is incomplete or when multiple disease patterns overlap. Purely data-driven models may be difficult to train in low-data clinical domains and may not clearly expose how diagnostic criteria and literature-derived evidence are being used.

Vestibular-BayesSeed provides a modular framework for representing this reasoning as a logistic Bayesian network with:

- **input nodes** for raw clinical observations
- **derived nodes** for intermediate clinical constructs
- **target disease nodes** for posterior diagnostic probabilities
- **edge-level evidence metadata** for transparency
- **sensitivity ranges** for uncertain or heterogeneous evidence

---

## Core modeling idea

Each target or derived node can be represented using a logistic conditional probability distribution:

```text
P(node = 1 | parents) = sigmoid(intercept + Σ beta_i × parent_i)
```

Default edge weights follow a conservative evidence-anchored initialization rule:

```text
beta_init = clip(q × p × beta_0, -2.5, +2.5)
```

where:

- `beta_0` is a base effect estimate such as `ln(LR+)`, `ln(LR−)`, `ln(OR)`, or a qualitative prior weight
- `q` is an evidence-quality discount
- `p` is a placement discount used to reduce double counting across network layers
- `clip` prevents unrealistically large coefficients in the seed model

The framework emphasizes placing most of the evidence weight on **raw input → derived pattern** edges when the literature directly defines the pattern, and using more moderate **derived pattern → diagnosis** weights to avoid double counting.

---

## Planned repository structure

```text
vestibular-bayesseed/
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── requirements.txt
├── default_modules/
│   ├── bppv.json
│   ├── meniere_disease.json
│   ├── pvp_bvp.json
│   ├── sensitivity_ranges.json
│   └── module_schema_draft.json
├── docs/
│   ├── overview.md
│   ├── node_taxonomy.md
│   ├── evidence_to_parameter_mapping.md
│   ├── adding_new_disease_module.md
│   ├── default_modules.md
│   ├── sensitivity_analysis.md
│   └── medical_disclaimer.md
├── src/
│   └── bayesseed/
│       ├── __init__.py
│       ├── logistic_cpd.py
│       ├── module_loader.py
│       ├── derived_nodes.py
│       ├── inference.py
│       ├── schema_validation.py
│       ├── sensitivity.py
│       ├── visualization.py
│       └── cli.py
├── examples/
│   ├── synthetic_cases.csv
│   ├── run_examples.py
│   ├── example_bppv_case.json
│   ├── example_md_case.json
│   └── example_pvp_case.json
├── app/
│   └── streamlit_app.py
└── tests/
    ├── test_logistic_cpd.py
    ├── test_module_loader.py
    ├── test_schema_validation.py
    ├── test_derived_nodes.py
    └── test_inference_examples.py
```

---

## Installation

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/ndongwoo/vestibular-bayesseed.git
cd vestibular-bayesseed
pip install -e .
```

For the optional Streamlit demonstration interface and development tools:

```bash
pip install -e ".[app,dev]"
```

Alternatively, install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Quick start

Run the example synthetic cases:

```bash
python examples/run_examples.py
```

Validate a disease module:

```bash
bayesseed validate default_modules/bppv.json
```

Run inference from a CSV file of synthetic cases:

```bash
bayesseed run examples/synthetic_cases.csv --modules default_modules/
```

Launch the optional Streamlit demonstration app:

```bash
streamlit run app/streamlit_app.py
```

---

## Default modules

### BPPV module

The BPPV module demonstrates a positional/nystagmus-driven diagnostic network. It includes raw findings such as positional triggers, brief vertigo duration, Dix-Hallpike torsional upbeating nystagmus, supine-roll geotropic or apogeotropic nystagmus, subjective positional vertigo, and atypical positional red flags.

The main derived constructs include:

- brief triggered positional syndrome
- posterior-canal positional pattern
- horizontal-canal positional pattern
- subjective positional pattern
- atypical positional red flag
- no objective positional nystagmus

### Ménière's disease module

The MD module demonstrates an audio-vestibular episodic diagnostic network. It integrates episode duration, recurrent spontaneous vertigo, fluctuating auditory symptoms, low-frequency sensorineural hearing loss, hydropic evidence, and migraine overlap.

The main derived constructs include:

- episodic vestibular syndrome
- auditory cluster
- objective low-frequency cochlear pattern
- endolymphatic hydrops evidence
- migraine overlap pattern

### PVP/BVP module

The PVP/BVP module demonstrates a chronic vestibular hypofunction network with a threshold-based competing diagnosis. It separates mild bilateral vestibular hypofunction supporting PVP from severe bilateral vestibular hypofunction supporting BVP and competing against PVP.

The main derived constructs include:

- chronic vestibular course
- gait/balance symptom burden
- mild bilateral vestibular hypofunction
- severe bilateral vestibular hypofunction
- non-central chronic vestibular pattern

---

## Adding a new disease module

A new module should define:

1. `disease_id` and human-readable disease name
2. input nodes
3. derived nodes
4. target disease node or nodes
5. logistic intercepts and edge weights
6. evidence metadata for each edge
7. sensitivity-analysis ranges for uncertain edges
8. applicability concerns and limitations

A future disease module may be added without modifying the inference engine if it follows the JSON schema.

Example template:

```json
{
  "disease_id": "new_disease",
  "display_name": "New Disease",
  "version": "0.1.0",
  "intended_use": "research and educational demonstration only",
  "input_nodes": [],
  "derived_nodes": [],
  "target_nodes": [],
  "edges": [],
  "evidence_notes": []
}
```

---

## Streamlit demonstration interface

The optional Streamlit interface is intended to make the framework easier to inspect. It is not the core software engine.

Planned app sections:

- **Module Viewer**: inspect BPPV, MD, and PVP/BVP module structure
- **Case Simulator**: enter synthetic clinical features and observe posterior changes
- **Derived Node Explanation**: view which intermediate constructs are activated
- **Evidence Table**: inspect coefficient rationale and evidence strength
- **Sensitivity Analysis**: vary selected uncertain coefficients and visualize posterior changes

---

## Development

Run tests:

```bash
pytest
```

Format code:

```bash
black src tests examples app
ruff check src tests examples app
```

Type checking:

```bash
mypy src
```

---

## Citation

A `CITATION.cff` file should be included in the repository once the first release is created. If the software is archived through Zenodo, cite the versioned DOI in addition to the related paper.

---

## License

This project is released under the Apache License 2.0. See `LICENSE` for details.

---

## Status

This project is currently an early-stage research software seed framework. The default disease modules and coefficients are intended for transparent demonstration and future validation, not for clinical deployment.
