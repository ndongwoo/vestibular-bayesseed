# Manuscript draft

This manuscript is under preparation for submission to SoftwareX.

# Vestibular-BayesSeed: An Open-Source Framework for Evidence-Anchored Logistic Bayesian Networks in Dizziness Diagnosis

**Manuscript type:** SoftwareX Original Software Publication  
**Status:** Draft skeleton for conversion into the official SoftwareX template  
**Version:** v0.2.2  
**Repository:** TBD: https://github.com/ndongwoo/vestibular-bayesseed  
**Archive DOI:** TBD after Zenodo release  

---

## Abstract

Vestibular-BayesSeed is an open-source Python framework for constructing evidence-anchored logistic Bayesian diagnostic networks using modular JSON disease definitions. The software separates disease-specific clinical knowledge from reusable inference logic: disease modules define input nodes, derived nodes, target disease nodes, coefficients, evidence metadata, and sensitivity ranges, whereas the Python package handles schema validation, derived-node evaluation, logistic conditional probability distribution inference, batch execution, visualization, and sensitivity analysis. The initial release includes transparent worked modules for benign paroxysmal positional vertigo, Ménière's disease, and presbyvestibulopathy with bilateral vestibulopathy as a threshold-based competing diagnosis. These modules represent positional/nystagmus-driven, episodic audio-vestibular, and chronic vestibular hypofunction phenotypes. The package includes a Python API, command-line interface, synthetic demonstration cases, unit tests, documentation, and an optional Streamlit interface for interactive educational use. Vestibular-BayesSeed is intended as a research and educational seed framework for clinical knowledge engineering, not as a validated clinical decision-support system or medical device. Future work will require disease-specific calibration, locked-model validation, and prospective evaluation before any clinical deployment.

**Keywords:** Bayesian network; logistic CPD; dizziness; vestibular disorders; knowledge engineering; clinical decision support; open-source software

---

## 1. Metadata

Use the table in `softwarex_metadata_table.md` or `tables/table1_software_metadata.md`.

Key fields to replace before submission:

- Permanent repository link
- Zenodo DOI or equivalent archive link
- Documentation URL
- Final release version
- Final dependency versions if locked

---

## 2. Motivation and significance

Dizziness and vertigo diagnosis requires integration of heterogeneous evidence, including symptom timing and triggers, positional nystagmus, audiometry, vestibular function tests, imaging, and exclusionary neurologic findings. Consensus diagnostic criteria are clinically useful, but a rule-based representation may be difficult to apply when information is incomplete, overlapping disease patterns coexist, or several correlated findings risk being counted repeatedly. Conversely, purely data-driven models may require large labeled datasets and may not expose how established clinical criteria and literature-derived evidence are used.

Bayesian-network modeling provides a transparent framework for representing uncertainty, missingness, dependencies, and competing diagnoses. However, full conditional probability tables become cumbersome as the number of parent nodes increases. Logistic conditional probability distributions offer a compact alternative by representing parent contributions as additive log-odds coefficients. This makes the parameters more interpretable and allows literature-derived odds ratios, likelihood ratios, criteria-level evidence, and expert-informed priors to be mapped into a common coefficient scale.

Vestibular-BayesSeed was developed to provide a reusable seed framework for this type of clinical knowledge engineering. The software allows users to define disease modules as JSON files, separating domain knowledge from the inference engine. The initial modules are not intended to constitute a validated dizziness CDSS. Instead, they serve as transparent worked examples showing how input nodes, derived nodes, target disease nodes, evidence metadata, and sensitivity ranges can be combined in an extensible framework.

The default modules focus on three representative vestibular diagnostic structures: benign paroxysmal positional vertigo (BPPV), Ménière's disease (MD), and presbyvestibulopathy (PVP) with bilateral vestibulopathy (BVP) as a competing threshold-based diagnosis. These examples were selected because they illustrate distinct diagnostic patterns: a positional/nystagmus-driven disorder, an episodic audio-vestibular disorder, and a chronic vestibular hypofunction syndrome.

---

## 3. Software description

### 3.1 Software architecture

Vestibular-BayesSeed separates disease-specific knowledge from reusable inference logic. Disease modules are stored as JSON files, whereas the Python package handles module loading, schema validation, derived-node evaluation, logistic-CPD inference, sensitivity analysis, and visualization.

The core workflow is:

1. Load one or more disease modules from JSON files.
2. Validate each module against the expected schema.
3. Accept a synthetic or user-defined case as input-node values.
4. Evaluate derived nodes from raw input findings.
5. Compute target disease probabilities using logistic CPDs.
6. Return ranked posterior probabilities, contribution summaries, and optional diagnostic-network exports.
7. Optionally run one-way sensitivity analysis over predefined coefficient ranges.

See Figure 1 for the proposed architecture diagram.

### 3.2 Node taxonomy

The framework defines four main node classes:

- **Input nodes:** raw clinical observations such as symptom duration, positional triggers, nystagmus pattern, audiometric findings, vestibular-test thresholds, or red-flag findings.
- **Derived nodes:** intermediate clinical constructs such as posterior-canal positional pattern, auditory cluster, low-frequency cochlear pattern, hydrops evidence, or chronic vestibular hypofunction pattern.
- **Target disease nodes:** diagnostic target nodes such as `Dx.BPPV`, `Dx.MD`, `Dx.PVP`, and `Dx.BVP`.
- **Competing or negative evidence nodes:** findings that reduce the probability of a target diagnosis or suggest an alternative disease process.

The default modeling pattern places most literature-defined evidence on raw input → derived pattern edges, then uses moderated derived pattern → diagnosis edges to reduce double counting. Figure 2 summarizes this taxonomy.

### 3.3 Logistic CPD engine

For a node with binary or continuous parent features, the software computes:

```text
P(node = 1 | parents) = sigmoid(intercept + Σ beta_i × parent_i)
```

where `intercept` is the baseline log-odds and `beta_i` is the coefficient for parent `i`. Missing input values are treated as unobserved by default rather than imputed as absent, depending on module configuration.

The coefficient initialization concept is:

```text
beta_init = clip(q × p × beta_0, -2.5, +2.5)
```

where `beta_0` can be derived from `ln(OR)`, `ln(LR+)`, `ln(LR−)`, or a qualitative evidence-strength mapping; `q` is an evidence-quality discount; and `p` is a placement discount used to reduce double counting across network layers. These initialization values are provided as transparent starting values and should not be interpreted as universally calibrated diagnostic probabilities.

### 3.4 Interfaces

The software can be used through:

- a Python API for programmatic use;
- a command-line interface for reproducible batch execution;
- synthetic demonstration examples;
- an optional Streamlit interface for interactive module inspection, case simulation, evidence review, and sensitivity analysis.

The Streamlit interface is a frontend demonstration layer. The inference logic remains in the reusable Python package.

---

## 4. Software functionalities

Use `tables/table2_functionality.md` as the main functionality table.

Key functions include module loading, schema validation, derived-node evaluation, logistic CPD inference, synthetic batch execution, sensitivity analysis, Mermaid/NetworkX export, a command-line interface, and an optional Streamlit interface.

---

## 5. Illustrative examples

This release includes nine synthetic demonstration cases:

1. `S01_typical_pc_bppv`
2. `S02_typical_hc_bppv`
3. `S03_subjective_bppv`
4. `S04_central_positional_red_flag`
5. `S05_definite_like_meniere`
6. `S06_meniere_migraine_overlap`
7. `S07_typical_pvp`
8. `S08_bvp_competitor`
9. `S09_mixed_md_pvp_evidence`

These synthetic cases demonstrate model behavior, derived-node activation, competing diagnostic probabilities, and sensitivity to selected edge weights. They are not intended to estimate diagnostic accuracy, discrimination, calibration, or clinical utility.

### 5.1 BPPV worked example

The BPPV module demonstrates how positional triggers, brief symptom duration, Dix-Hallpike torsional upbeating nystagmus, supine-roll horizontal nystagmus, subjective positional vertigo, and atypical positional red flags can be represented as a network. Canal-specific positional findings primarily contribute to derived nodes, which then support the BPPV target node with moderated coefficients.

### 5.2 Ménière's disease worked example

The MD module demonstrates integration of recurrent episodic vestibular symptoms, the 20 min–12 h duration window, fluctuating auditory symptoms, low-frequency sensorineural hearing loss, supportive hydrops evidence, and migraine overlap. Migraine features are modeled as weak competing or overlap evidence rather than a hard exclusion.

### 5.3 Presbyvestibulopathy/BVP worked example

The PVP/BVP module demonstrates a chronic vestibular hypofunction phenotype. Mild bilateral vestibular hypofunction supports PVP, whereas severe bilateral vestibular hypofunction strongly supports BVP and negatively competes against PVP. This module shows how objective threshold-defined nodes can be used to represent competing disease boundaries.

---

## 6. Impact

Vestibular-BayesSeed is designed to support reproducible clinical knowledge engineering. Its main contribution is not a validated diagnostic model, but an extensible software framework for constructing transparent logistic Bayesian diagnostic networks.

The framework has several potential impacts:

1. **Transparency:** Each module exposes input nodes, derived nodes, target disease nodes, coefficients, evidence basis, comments, and sensitivity ranges.
2. **Extensibility:** Users can add new disease modules by editing JSON definitions rather than modifying inference code.
3. **Reproducibility:** The repository includes synthetic cases, command-line examples, documentation, and pytest-based tests.
4. **Educational utility:** The software can demonstrate Bayesian reasoning, derived-node construction, competing evidence, and double-counting prevention.
5. **Cross-domain potential:** Although the initial examples focus on vestibular disorders, the same architecture could be adapted to other low-data but knowledge-rich clinical domains.

The repository therefore provides a seed framework for future research in evidence-anchored diagnostic modeling, local calibration, and prospective validation.

---

## 7. Limitations

The default disease modules are worked examples and are not validated diagnostic tools. The coefficients are literature-informed initialization values rather than universally calibrated parameters. The synthetic cases demonstrate software behavior only and do not estimate diagnostic accuracy or clinical utility. Real-world use would require locked-model validation, calibration assessment, external validation, governance review, and regulatory assessment. The current release also focuses on a small number of vestibular modules and should be expanded cautiously with disease-specific evidence review and sensitivity analysis.

---

## 8. Conclusions

Vestibular-BayesSeed provides an open-source software framework for building evidence-anchored logistic Bayesian diagnostic networks using modular JSON disease definitions. The initial release includes reusable inference code, schema validation, synthetic examples, tests, documentation, an optional Streamlit demonstration interface, and transparent worked modules for BPPV, Ménière's disease, and PVP/BVP. The software is intended for research and education as a seed framework for future clinical knowledge-engineering studies, not as a validated clinical decision-support system.

---

## 9. Acknowledgments

TBD.

---

## 10. Funding

TBD.

---

## 11. Conflict of interest

TBD.

---

## 12. Data availability

No patient-level data are included. Synthetic cases are provided in `examples/synthetic_cases.csv`. Source code, documentation, default modules, evidence metadata, and tests will be made available in the project repository and archived with a permanent DOI before submission.

---

## 13. Code availability

TBD: GitHub repository URL and Zenodo DOI.

---

## 14. References to verify before final submission

The final reference list should include, at minimum:

1. SoftwareX author guidelines and software citation guidance.
2. A general reference on Bayesian networks in medicine.
3. A methodological reference on logistic CPDs or logistic-regression local probability models in Bayesian networks.
4. BPPV diagnostic criteria and/or AAO-HNS BPPV guideline.
5. Ménière's disease diagnostic criteria.
6. Presbyvestibulopathy diagnostic criteria.
7. Bilateral vestibulopathy diagnostic criteria.
8. The key evidence sources used in the edge-level evidence table, including hydrops MRI, VEMP/ECoG, and central positional nystagmus literature where relevant.

