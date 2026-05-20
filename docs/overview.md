# Overview

**Vestibular-BayesSeed** is an open-source seed framework for constructing evidence-anchored logistic Bayesian diagnostic networks. The initial distribution provides transparent worked examples for three vestibular diagnostic phenotypes:

- benign paroxysmal positional vertigo (**BPPV**)
- Ménière disease (**MD**)
- presbyvestibulopathy (**PVP**) with bilateral vestibulopathy (**BVP**) as a competing threshold-based diagnosis

The project is intended to demonstrate how clinical diagnostic knowledge can be represented as a modular Bayesian-network-like model using input nodes, derived nodes, target disease nodes, and logistic conditional probability distributions.

## What the software does

Vestibular-BayesSeed provides:

- JSON-defined disease modules
- schema validation for module files
- logistic-CPD inference
- derived-node evaluation
- batch execution on synthetic cases
- one-way sensitivity analysis for uncertain coefficients
- Mermaid network export
- optional Streamlit demonstration interface

## What the software does not do

Vestibular-BayesSeed does **not** provide a clinically validated diagnosis. It is not a medical device. It is not intended for direct patient care.

The default coefficients are literature-informed initialization values. They are not universally calibrated diagnostic probabilities. Clinical deployment would require locked-model validation, calibration assessment, clinical governance, and regulatory review.

## Architecture

The framework separates disease-specific knowledge from general inference logic.

```text
JSON disease modules
        ↓
Schema validation
        ↓
Input-node parsing
        ↓
Derived-node evaluation
        ↓
Logistic CPD inference
        ↓
Posterior probabilities, edge contributions, visual output
```

The disease modules define the clinical knowledge. The Python package implements the generic inference engine.

## Core modeling idea

Each derived or target node can be represented as a binary logistic conditional probability distribution:

```text
P(node = 1 | parents) = sigmoid(intercept + Σ beta_i × parent_i)
```

where each parent is a raw input node or a derived node. Missing raw inputs are treated as unobserved, not automatically as negative evidence.

## Why derived nodes are used

Derived nodes serve three purposes:

1. **Represent clinical constructs** such as posterior-canal positional pattern, auditory cluster, hydropic evidence, or mild bilateral vestibular hypofunction.
2. **Reduce double counting** by aggregating correlated findings before sending a more moderate weight to the diagnosis node.
3. **Make the network explainable** by showing which intermediate patterns are activated by the input evidence.

## Default module philosophy

The default modules intentionally use a conservative approach:

- strong evidence is placed mainly on raw input → derived pattern edges;
- derived pattern → diagnosis edges are kept moderate when the same evidence has already been used upstream;
- uncertain or heterogeneous evidence is assigned wider sensitivity ranges;
- central or competing-diagnosis signs are modeled as negative or competing evidence rather than as silent omissions.

## Intended use cases

The framework can be used for:

- education in probabilistic clinical reasoning;
- transparent demonstration of clinical knowledge engineering;
- development of disease-specific Bayesian diagnostic modules;
- sensitivity analysis of uncertain diagnostic weights;
- research software accompanying a methodology or software paper.

It should not be used for clinical decision-making without appropriate validation.
