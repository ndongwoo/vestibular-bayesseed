# Streamlit demonstration app

The optional Streamlit app provides an interactive interface for inspecting and running the default modules.

It is intended for demonstration, education, and software review. It is not a clinical diagnostic interface.

## Installation

From the repository root:

```bash
pip install -e .[app]
```

For development:

```bash
pip install -e .[app,dev]
```

## Launch

```bash
streamlit run app/streamlit_app.py
```

## App sections

### 1. Overview

Summarizes the project scope, intended use, and disclaimer.

### 2. Module viewer

Allows users to select a disease module and inspect:

- input nodes;
- derived nodes;
- target disease nodes;
- edge list;
- coefficients;
- evidence metadata if available.

### 3. Case simulator

Allows users to enter binary clinical findings and run posterior inference.

Recommended demonstration cases:

- typical posterior-canal BPPV;
- horizontal-canal BPPV;
- subjective BPPV;
- central positional red flag;
- definite-like Ménière disease;
- Ménière disease with migraine overlap;
- typical PVP;
- BVP competitor;
- mixed MD/PVP evidence.

### 4. Evidence table

Displays the edge-level evidence table when available.

Expected file:

```text
edge_level_evidence_table_v0_1_0.csv
```

### 5. Sensitivity analysis

Allows users to choose a sensitivity edge and vary beta values interactively.

Expected file:

```text
default_modules/sensitivity_ranges.json
```

### 6. Mermaid export

Displays Mermaid code for selected modules so users can copy network diagrams into documentation or manuscripts.

## Recommended screenshot for SoftwareX

A useful manuscript figure is a screenshot showing:

- selected module;
- input checklist;
- derived node activation;
- posterior table;
- edge contribution table.

Caption suggestion:

```text
Interactive Streamlit demonstration interface showing JSON-defined vestibular disease modules, case-level input, derived-node activation, and logistic-CPD posterior output. The interface is provided for research and educational demonstration only and does not represent a validated clinical decision-support system.
```

## Safety wording

The app should visibly display:

```text
Research and educational use only. Not a validated medical device or clinical decision-support system. Do not use for patient care.
```

## Recommended workflow for reviewers

```bash
pip install -e .[app,dev]
pytest
python examples/run_examples.py
streamlit run app/streamlit_app.py
```

After the app opens, test:

1. BPPV typical case;
2. MD typical case;
3. PVP/BVP competing case;
4. one sensitivity-analysis slider.
