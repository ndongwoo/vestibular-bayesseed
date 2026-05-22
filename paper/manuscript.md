# Vestibular-BayesSeed: An Open-Source Framework for Evidence-Anchored Logistic Bayesian Networks in Dizziness Diagnosis

**Manuscript type:** SoftwareX Original Software Publication  
**Status:** Draft skeleton for conversion into the official SoftwareX template  
**Version:** v0.2.3  
**Repository:** https://github.com/ndongwoo/vestibular-bayesseed  
**Archive DOI:** 10.5281/zenodo.20325049  

---

## Abstract

Vestibular-BayesSeed is an open-source Python framework for constructing evidence-anchored logistic Bayesian diagnostic networks from modular JSON disease definitions. The software separates disease-specific clinical knowledge from reusable inference code. Disease modules define input nodes, derived nodes, target diagnosis nodes, coefficients, evidence metadata, and sensitivity ranges, while the Python package handles schema validation, derived-node evaluation, logistic conditional probability distribution inference, batch execution, visualization, and one-way sensitivity analysis. Version 0.2.3 includes transparent worked modules for benign paroxysmal positional vertigo, Ménière disease, and presbyvestibulopathy with bilateral vestibulopathy as a threshold-based competing diagnosis. The package is intended for research and education, not unvalidated clinical decision-making.

**Keywords:** Bayesian network; Logistic CPD; Vestibular disorders; Dizziness; Clinical decision support; Knowledge engineering

---

## Metadata


| **Nr** | **Code  metadata description**                               | **Metadata**                                                 |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| C1     | Current code version                                         | v0.2.3                                                       |
| C2     | Permanent link to  code/repository used for this code version | https://github.com/ndongwoo/vestibular-bayesseed; archived version: https://doi.org/10.5281/zenodo.20325049 |
| C3     | Legal code license                                           | Apache License 2.0                                           |
| C4     | Code versioning system used                                  | git                                                          |
| C5     | Software code languages,  tools and services used            | Python 3, JSON, YAML, NumPy,  pandas, Pydantic, jsonschema, NetworkX, matplotlib, Click, Rich, Streamlit,  Plotly, pytest, GitHub, Zenodo |
| C6     | Compilation requirements,  operating environments and dependencies | Python >=3.10. Runtime  dependencies: numpy>=1.24, pandas>=2.0, pydantic>=2.5,  jsonschema>=4.19, networkx>=3.1, matplotlib>=3.7, click>=8.1,  rich>=13.0, pyyaml>=6.0. Optional app dependencies: streamlit>=1.32,  plotly>=5.18. Development dependencies include pytest, pytest-cov, ruff,  black, mypy, and jupyter. |
| C7     | If available, link to  developer documentation/manual        | https://github.com/ndongwoo/vestibular-bayesseed/tree/main/docs |
| C8     | Support email for questions                                  | [ndongwoo@gmail.com](mailto:ndongwoo@gmail.com)              |

---

## 1. Motivation and significance

Dizziness and vertigo diagnosis requires the integration of heterogeneous clinical evidence, including symptom timing and triggers, positional nystagmus, audiometry, vestibular laboratory tests, imaging, and neurological exclusion findings. Consensus diagnostic criteria are clinically useful, but they can be difficult to operationalize when information is incomplete, when overlapping syndromes coexist, or when correlated findings may be counted more than once. Purely data-driven models can also be difficult to train in low-data clinical domains and may not clearly expose how formal criteria and literature-derived evidence are being used.

Bayesian network modeling provides a transparent framework for representing uncertainty, missing observations, dependencies, and competing diagnoses [2,3]. However, manually specifying full conditional probability tables becomes increasingly burdensome as the number of parent nodes increases. Logistic conditional probability distributions (CPDs) provide a compact alternative by representing parent-node contributions as additive log-odds coefficients. This parameterization keeps the model interpretable and allows odds ratios, likelihood ratios, diagnostic-criteria-level evidence, and expert priors to be mapped onto a common coefficient scale, without requiring deterministic criteria-fulfillment outputs to be used as parent nodes.

Vestibular-BayesSeed was developed to provide a reusable seed framework for this form of clinical knowledge engineering. Users define disease modules in JSON, while the core Python package provides module loading, validation, inference, visualization, and sensitivity analysis. The initial modules are not intended to constitute a validated dizziness clinical decision-support system. Instead, they show how input nodes, derived nodes, target diagnosis nodes, evidence metadata, and sensitivity ranges can be combined within an extensible framework.

The default modules focus on three representative vestibular diagnostic structures: benign paroxysmal positional vertigo (BPPV), Ménière disease (MD), and presbyvestibulopathy (PVP) with bilateral vestibulopathy (BVP) represented as a threshold-based competing diagnosis. These examples were selected because they illustrate different diagnostic patterns: a positional/nystagmus-driven disorder, an episodic audio-vestibular disorder, and a chronic vestibular hypofunction syndrome with quantitative threshold boundaries [5-8].

---

## 2. Software description

### 2.1 Software architecture

Vestibular-BayesSeed separates disease-specific knowledge from reusable inference logic. Disease modules are stored as JSON files, while the Python package handles loading, schema validation, derived-node evaluation, logistic CPD inference, one-way sensitivity analysis, and network visualization. The same disease module can be used through the Python API, command-line interface (CLI), tests, batch examples, or the optional Streamlit demonstration interface.

The core workflow is: (i) load one or more disease modules from JSON files; (ii) validate each module against the expected schema; (iii) accept a synthetic or user-defined case as input-node values; (iv) evaluate derived nodes from raw clinical observations; (v) calculate target-node probabilities using logistic CPDs; and (vi) return sorted posterior probabilities, contribution summaries, optional network exports, and sensitivity-analysis results. The overall architecture and information flow are summarized in Figure 1.

### 2.2 Node taxonomy and modeling pattern

The framework defines four main node classes:

• Input nodes: raw observations such as symptom duration, positional triggers, nystagmus patterns, audiometric findings, vestibular test thresholds, or red-flag findings.
• Derived nodes: intermediate clinical constructs such as posterior-canal positional pattern, auditory cluster, low-frequency cochlear pattern, hydrops evidence, or chronic vestibular hypofunction pattern.
• Target disease nodes: final diagnostic targets such as BPPV, MD, PVP, and BVP.
• Competing or negative evidence nodes: findings that reduce the probability of a target diagnosis or support an alternative disease process.

A subtype of derived node, termed a derived interaction node, is used to encode pre-specified non-additive relationships among observations. These nodes are deterministic engineered features rather than diagnostic outputs. In the current implementation, derived interaction nodes use an AND operator over two or more parent observations or intermediate derived nodes. They are evaluated as 1.0 when all component features are explicitly present, 0.0 when any component feature is explicitly absent, and unobserved when the available evidence is incomplete without an explicit negative component. When included in a target-node logistic CPD, the interaction coefficient is interpreted as residual excess log-odds beyond the additive main effects of the component variables, thereby avoiding interpretation as duplicated independent evidence.

To keep interaction terms interpretable and auditable, they are intended to be specified within a limited set of semantic roles. These include evidence-concordance interactions, in which multiple findings point to the same pathophysiologic process; temporal-phenotype interactions, in which symptom timing and symptom type are mutually coherent; syndrome-test or syndrome-laboratory concordance, in which a clinical syndrome is supported by an objective test pattern; antagonistic interactions, in which the joint presence of two findings lowers the plausibility of a target diagnosis; and red-flag suppression, in which central or otherwise incompatible features reduce confidence in peripheral target diagnoses. Version 0.2.3 implements this mechanism conservatively, with the BPPV module using evidence-concordance interaction nodes. Other roles provide a design vocabulary for future modules and should be pre-specified, documented, and validated before being used as model features.

The preferred modeling pattern places most literature-defined evidence on raw input-to-derived pattern edges, followed by moderated derived pattern-to-diagnosis edges. This helps reduce double counting when several raw observations define the same diagnostic construct. Figure 2 illustrates the relationship among raw input observations, derived clinical constructs, competing evidence, and target disease nodes.

### 2.3 Logistic CPD engine

For a binary or continuous parent-feature vector x = (x1, ..., xk), the software computes each logistic CPD as:

```
logit[P(D = 1 | x)] = alpha + sum_i beta_i x_i
```

or equivalently,

```
P(D = 1 | x) = 1 / {1 + exp[-(alpha + sum_i beta_i x_i)]}.
```

The intercept alpha represents the baseline log-odds, and beta_i represents the coefficient for parent node i. Missing input values are treated as unobserved by default rather than being imputed as absent, unless a module explicitly encodes a different behavior.

Default edge weights follow a conservative evidence-anchored initialization rule:

```
beta_init = clip(q × p × beta_0, -2.5, +2.5)
```

Here, beta_0 can be derived from ln(OR), ln(LR+), ln(LR−), or a qualitative evidence-strength mapping. The factor q is an evidence-quality discount, and p is a placement discount used to reduce double counting across network layers. These values are transparent starting points for research and sensitivity analysis; they should not be interpreted as universally calibrated diagnostic probabilities.

When clinically justified, the parent-feature vector may include pre-specified interaction features. For example, if A and B are component evidence variables, an engineered interaction feature A:B can be included as an additional parent:

```
logit[P(D = 1)] = alpha + beta_A A + beta_B B + beta_AB(A:B).
```

Here, beta_AB is not interpreted as a third independent finding. It represents the residual excess log-odds associated with the joint presence of A and B after accounting for their additive main effects.

Target-node probabilities are evaluated as binary conditional probabilities for each disease node and are used for ranking and inspection; they are not constrained to sum to one across mutually exclusive diagnoses.

### 2.4 Software functionalities

Vestibular-BayesSeed supports the complete workflow required to define, validate, execute, and inspect modular logistic Bayesian diagnostic networks. It loads vestibular disease modules encoded as JSON files and validates required fields, node references, edge definitions, coefficient metadata, and module consistency. Given raw clinical input values, the software evaluates derived clinical constructs and applies logistic conditional probability distribution inference to estimate derived-node and target-disease probabilities from intercepts and parent coefficients. For reproducible demonstrations, it can execute synthetic or user-supplied CSV case files in batch mode. It also provides one-way sensitivity analysis for selected coefficients and exports network structures for Mermaid- or NetworkX-based visualization. The package is accessible through a Python API, a command-line interface, example datasets, unit tests, documentation, and an optional Streamlit demonstration app.

### 2.5 Interfaces and sample usage

The package can be used programmatically, from the command line, or through the optional Streamlit demonstration layer. The Streamlit interface is a front-end demonstration tool; the reusable inference logic remains in the Python package. The optional Streamlit case-simulator interface is shown in Figure 3. The archived software version corresponding to this manuscript is cited according to software citation principles [1,4].

---

## 3. Illustrative examples

Version 0.2.3 includes nine synthetic demonstration cases:

1. S01_typical_pc_bppv: typical posterior-canal BPPV.
2. S02_typical_hc_bppv: typical horizontal-canal BPPV.
3. S03_subjective_bppv: subjective BPPV.
4. S04_central_positional_red_flag: central positional red-flag pattern.
5. S05_definite_like_meniere: definite-like Ménière disease pattern.
6. S06_meniere_migraine_overlap: Ménière-migraine overlap pattern.
7. S07_typical_pvp: typical presbyvestibulopathy pattern.
8. S08_bvp_competitor: bilateral vestibulopathy as a competing threshold-based diagnosis.
9. S09_mixed_md_pvp_evidence: mixed Ménière disease and presbyvestibulopathy evidence.

These synthetic cases demonstrate model behavior, derived-node activation, competing-diagnosis probabilities, and sensitivity to selected edge weights. They are not intended to estimate diagnostic accuracy, discrimination, calibration, or clinical utility. The top-ranked outputs for the nine synthetic cases are summarized in Table 1.

### 3.1. BPPV worked example
 
The BPPV module shows how positional triggers, brief symptom duration, torsional upbeating nystagmus on Dix-Hallpike testing, horizontal nystagmus on supine-roll testing, subjective positional vertigo, and atypical central red flags can be represented in a diagnostic network. Canal-specific positional findings primarily activate derived nodes, which then support the BPPV target node through moderated coefficients. Atypical positional red flags provide competing or negative evidence rather than direct support for the BPPV target.

In version 0.2.3, the BPPV module also includes two derived interaction nodes: pc_positional_concordance and hc_positional_concordance. The first is activated when brief_triggered_positional_syndrome and posterior_canal_positional_pattern are both explicitly present, and the second is activated when brief_triggered_positional_syndrome and horizontal_canal_positional_pattern are both explicitly present. These nodes represent residual evidence concordance between symptom timing and canal-specific positional nystagmus. They are not diagnostic-criteria fulfillment nodes and are not outputs of a deterministic criteria-audit algorithm. Each contributes a moderate residual coefficient to the BPPV target node, improving the calibration of typical canal-specific BPPV examples while leaving subjective BPPV and central red-flag cases comparatively low-confidence.

In the synthetic examples, this design yields BPPV posterior probabilities of 0.818 for typical posterior-canal BPPV and 0.802 for typical horizontal-canal BPPV, while subjective BPPV remains lower confidence at 0.142 and the central positional red-flag case suppresses BPPV to 0.005.

### 3.2. Ménière disease worked example

The MD module integrates recurrent episodic vestibular symptoms, a 20 min to 12 h duration window, fluctuating auditory symptoms, low-frequency sensorineural hearing loss, supportive hydrops evidence, and migraine overlap. Migraine features are modeled as weak competing or overlap evidence rather than as an absolute exclusion rule, reflecting the practical difficulty of distinguishing audio-vestibular overlap syndromes in partially observed clinical settings.

### 3.3. Presbyvestibulopathy/BVP worked example

The PVP/BVP module represents a chronic vestibular hypofunction phenotype. Mild bilateral vestibular hypofunction supports PVP, whereas severe bilateral vestibular hypofunction strongly supports BVP and competes against PVP. This module demonstrates how objectively threshold-defined nodes can encode boundaries between related diagnoses within the same network.

---

## 4. Impact

Vestibular-BayesSeed is designed to support reproducible clinical knowledge engineering rather than to provide a finished diagnostic model. Its main contribution is a transparent and extensible software framework for building logistic Bayesian diagnostic networks that can expose assumptions, coefficients, evidence sources, and sensitivity ranges.

The software can improve the pursuit of existing research questions in several ways. First, it makes expert-derived diagnostic logic executable and inspectable. Second, it allows investigators to separate disease-module design from inference code, so new disease modules can be added without rewriting the engine. Future modules could further extend this pattern by adding pre-specified concordance features, such as temporal-phenotype or syndrome-test concordance, when these relationships are clinically justified. Third, it encourages reporting of edge-level evidence metadata and sensitivity ranges, which may make knowledge-engineered diagnostic models easier to audit than black-box models. Fourth, it provides a reproducible environment with synthetic cases, a CLI, documentation, and pytest-based tests.

The framework also creates new research opportunities. Investigators can study how different evidence-mapping rules affect posterior probabilities, how derived-node placement changes double-counting behavior, and how local calibration modifies seed coefficients. It may also serve as an educational platform for teaching Bayesian reasoning, diagnostic overlap, missing-evidence handling, and competing-diagnosis modeling in vestibular medicine.

The current public release is early-stage research software. There are no patient-level datasets or claims of clinical performance. Before any real clinical deployment, disease-specific calibration, fixed-model validation, external validation, prospective evaluation, governance review, and regulatory assessment would be necessary.

• Transparency: modules disclose input nodes, derived nodes, target nodes, coefficients, evidence bases, annotations, and sensitivity ranges.
• Extensibility: new disease modules can be defined by editing JSON without changing the inference engine.
• Reproducibility: the repository contains synthetic cases, command-line examples, documentation, and automated tests.
• Educational utility: the network structure and sensitivity analyses can be used to demonstrate Bayesian inference and competing evidence.
• Cross-domain potential: although the examples are vestibular, the same architecture could be adapted to other knowledge-rich but data-limited clinical domains.

---

## 5. Conclusions

Vestibular-BayesSeed provides an open-source framework for constructing evidence-anchored logistic Bayesian diagnostic networks using modular JSON disease definitions. Version 0.2.3 includes reusable inference code, schema validation, synthetic examples, tests, documentation, an optional Streamlit demonstration interface, and transparent worked modules for BPPV, Ménière disease, and PVP/BVP. The software is intended as a research and educational seed framework for clinical knowledge engineering and should not be used as an unvalidated clinical decision-support system.

---

## Acknowledgments

This manuscript was adapted from the doctoral dissertation of Dong Woo Nam submitted to Chungbuk National University Graduate School in partial fulfillment of the requirements for the Doctor of Philosophy degree.

---

## Funding

This work was supported by research grants from Seoul National University Bundang Hospital (Grant No. 06-2021-0482, 14-2022-0043, 02-2025-0039, and 13-2025-0008). The funder had no role in study design, data collection, analysis, interpretation, or manuscript preparation.

---

## Declaration of competing interest

The author declares that he has no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## Data availability

No patient-level or clinical research dataset was used in this article. Synthetic cases are provided in `examples/synthetic_cases.csv`. The demonstration cases are synthetic and are included in the archived software repository together with the source code.

---

## Code availability

Source code is available at https://github.com/ndongwoo/vestibular-bayesseed. The archived version for this release is https://doi.org/10.5281/zenodo.20325049.

---

## CRediT authorship contribution statement

Dong Woo Nam: Conceptualization, Methodology, Software, Validation, Visualization, Investigation, Writing – original draft, Writing – review & editing, Project administration, Funding acquisition.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work and the associated software, the author used OpenCode with a locally served Qwen3.6:27B large language model to assist with code drafting, refactoring suggestions, debugging, and documentation consistency checks. The author also used OpenAI ChatGPT to assist with manuscript proofreading, language editing, and consistency checking. After using this tool/service, the author reviewed and edited the content as needed and takes full responsibility for the content of the published article.

## References

[1] Nam D. Vestibular-BayesSeed: An open-source framework for evidence-anchored logistic Bayesian networks in dizziness diagnosis. Version v0.2.3. Zenodo; 2026. doi:10.5281/zenodo.20325049.
[2] Pearl J. Probabilistic reasoning in intelligent systems: networks of plausible inference. San Francisco: Morgan Kaufmann; 1988.
[3] Koller D, Friedman N. Probabilistic graphical models: principles and techniques. Cambridge, MA: MIT Press; 2009.
[4] Smith AM, Katz DS, Niemeyer KE, Chue Hong N, FORCE11 Software Citation Working Group. Software citation principles. PeerJ Computer Science. 2016;2:e86. doi:10.7717/peerj-cs.86.
[5] Bhattacharyya N, Gubbels SP, Schwartz SR, Edlow JA, El-Kashlan H, Fife T, et al. Clinical practice guideline: benign paroxysmal positional vertigo (update). Otolaryngology-Head and Neck Surgery. 2017;156(3_suppl):S1-S47. doi:10.1177/0194599816689667.
[6] Lopez-Escamez JA, Carey J, Chung WH, Goebel JA, Magnusson M, Mandalà M, et al. Diagnostic criteria for Menière's disease. Journal of Vestibular Research. 2015;25(1):1-7. doi:10.3233/VES-150549.
[7] Agrawal Y, Van de Berg R, Wuyts F, Walther L, Magnusson M, Oh E, et al. Presbyvestibulopathy: diagnostic criteria. Consensus document of the Classification Committee of the Bárány Society. Journal of Vestibular Research. 2019;29(4):161-170. doi:10.3233/VES-190672.
[8] Strupp M, Kim JS, Murofushi T, Straumann D, Jen JC, Rosengren SM, et al. Bilateral vestibulopathy: diagnostic criteria. Consensus document of the Classification Committee of the Bárány Society. Journal of Vestibular Research. 2017;27(4):177-189. doi:10.3233/VES-170619.

