# SoftwareX user guide and submission notes

This document summarizes how Vestibular-BayesSeed should be positioned for a SoftwareX submission.

## Recommended SoftwareX framing

Vestibular-BayesSeed should be presented as:

```text
an open-source research software framework for constructing evidence-anchored logistic Bayesian diagnostic networks, demonstrated with vestibular disease modules.
```

It should not be presented as:

```text
a validated clinical decision-support system for diagnosing dizziness.
```

## Core contribution

The core software contribution is the separation of:

1. disease-specific knowledge stored in JSON modules;
2. generic logistic-CPD inference implemented in Python;
3. evidence metadata and sensitivity ranges for transparency;
4. optional Streamlit UI for interactive demonstration.

## Suggested manuscript title

```text
Vestibular-BayesSeed: An open-source framework for evidence-anchored logistic Bayesian networks in dizziness diagnosis
```

Alternative more general title:

```text
Vestibular-BayesSeed: An open-source seed framework for constructing logistic Bayesian diagnostic networks
```

## Suggested abstract structure

Include:

- one sentence about the diagnostic modeling problem;
- one sentence about the software architecture;
- one sentence about the default modules;
- one sentence about reproducible examples and sensitivity analysis;
- one sentence stating that it is research software, not a validated CDSS.

Avoid claiming clinical accuracy.

## Required repository features

A SoftwareX submission should include:

- public GitHub repository;
- open-source license;
- installation instructions;
- command-line examples;
- synthetic examples;
- tests;
- documentation;
- citation information;
- release tag.

## Suggested figures

### Figure 1. Software architecture

```text
JSON modules → schema validation → derived-node evaluation → logistic CPD inference → CLI/Streamlit/API outputs
```

### Figure 2. Node taxonomy

Show input nodes, derived nodes, target disease nodes, modifiers, and competing edges.

### Figure 3. Worked modules

Compare BPPV, MD, and PVP/BVP modules.

### Figure 4. Streamlit demonstration

Show a typical case and posterior output.

## Suggested tables

### Table 1. Software functionality

| Function | Description |
|---|---|
| Module loading | Loads JSON disease modules |
| Schema validation | Checks node and edge consistency |
| Derived-node evaluation | Computes intermediate constructs |
| Logistic CPD inference | Calculates posterior probabilities |
| Sensitivity analysis | Varies selected beta coefficients |
| Visualization | Exports Mermaid diagrams |
| Streamlit demo | Interactive demonstration interface |

### Table 2. Default modules

| Module | Diagnostic pattern | Key derived nodes |
|---|---|---|
| BPPV | positional/nystagmus-driven | posterior-canal pattern, horizontal-canal pattern, subjective positional pattern |
| MD | audio-vestibular episodic | episodic vestibular syndrome, auditory cluster, hydropic evidence |
| PVP/BVP | chronic vestibular hypofunction | mild bilateral hypofunction, severe bilateral hypofunction, non-central chronic pattern |

## Demonstration commands

SoftwareX reviewers should be able to run:

```bash
pip install -e .[app,dev]
pytest
python examples/run_examples.py
bayesseed validate default_modules/
streamlit run app/streamlit_app.py
```

## Claims that are appropriate

Appropriate:

- transparent research software;
- extensible disease modules;
- evidence-anchored coefficients;
- worked examples;
- synthetic case demonstrations;
- sensitivity-analysis support.

Not appropriate:

- validated diagnostic accuracy;
- real-world clinical deployment;
- regulatory-grade CDSS;
- superiority over physicians or machine-learning models.

## Impact statement points

Potential impact:

- lowers the barrier to building interpretable diagnostic Bayesian networks;
- allows clinical experts to inspect and edit disease knowledge in JSON form;
- supports reproducible educational demonstrations;
- provides an extensible template for future validated CDSS development;
- can be adapted to other symptom-based diagnostic domains.

## Limitations to state explicitly

- default coefficients are initialization values;
- target-disease intercepts are placeholders;
- synthetic cases do not estimate diagnostic accuracy;
- clinical validation is required before use in patient care;
- literature-derived coefficients may not transport across settings.

## Recommended release workflow

1. Clean repository.
2. Run tests.
3. Run examples.
4. Capture Streamlit screenshot.
5. Tag `v0.1.0`.
6. Archive release with Zenodo.
7. Submit SoftwareX manuscript with repository link and release DOI.
