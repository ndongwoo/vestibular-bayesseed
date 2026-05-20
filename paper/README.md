# Paper package for SoftwareX submission

This folder contains draft manuscript materials for submitting **Vestibular-BayesSeed** as an Original Software Publication to **SoftwareX**.

The intended positioning is:

> Vestibular-BayesSeed is an open-source research software framework for constructing evidence-anchored logistic Bayesian diagnostic networks using modular JSON disease definitions. It is not a validated clinical decision-support system or medical device.

## Contents

```text
paper/
├── softwarex_manuscript_skeleton.md
├── softwarex_metadata_table.md
├── cover_letter_draft.md
├── highlights.md
├── graphical_abstract_caption.md
├── figures/
│   ├── figure_plan.md
│   ├── fig1_architecture.mmd
│   ├── fig2_node_taxonomy.mmd
│   ├── fig3_streamlit_demo_caption.md
│   └── fig4_synthetic_case_output_plan.md
├── tables/
│   ├── table1_software_metadata.md
│   ├── table2_functionality.md
│   └── table3_default_modules.md
└── supplementary/
    ├── repository_checklist.md
    ├── evidence_table_description.md
    └── softwarex_submission_notes.md
```

## Recommended next steps

1. Assemble the full GitHub repository.
2. Run `pytest` and `python examples/run_examples.py` from the repository root.
3. Create a tagged release, for example `v0.1.0`.
4. Archive the release in Zenodo and obtain a DOI.
5. Replace all `TBD` placeholders in the manuscript and metadata table.
6. Convert `softwarex_manuscript_skeleton.md` into the official SoftwareX Word/LaTeX template.
7. Capture an actual Streamlit screenshot for Figure 3.
8. Generate actual synthetic output tables or plots for Figure 4.

