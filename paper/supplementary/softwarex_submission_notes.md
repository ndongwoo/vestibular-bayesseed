# SoftwareX submission notes

## Main positioning

Submit as an **Original Software Publication**.

Primary claim:

> Vestibular-BayesSeed is reusable open-source research software for building evidence-anchored logistic Bayesian diagnostic networks from modular JSON disease definitions.

Do not claim:

- validated CDSS;
- clinical diagnostic accuracy;
- superiority over clinician diagnosis or ML models;
- readiness for patient management.

## Recommended manuscript length

Aim for a concise SoftwareX-style manuscript. Keep clinical background short and place most details in repository documentation.

## Must-have elements before submission

- Working repository
- Open-source license
- Versioned release
- Permanent archive DOI
- Installation instructions
- Reproducible example
- Tests
- Documentation
- Medical disclaimer

## Common reviewer risks and planned responses

| Possible reviewer concern | Preventive response in manuscript/repository |
|---|---|
| “This is a disease-specific prototype, not reusable software.” | Emphasize modular JSON disease definitions and `adding_new_disease_module.md`. |
| “Clinical claims are not validated.” | Explicitly state research/education only and avoid diagnostic accuracy claims. |
| “The default coefficients are arbitrary.” | Provide edge-level evidence table and sensitivity ranges. |
| “The app is not enough as software.” | Emphasize Python package, CLI, tests, and API; Streamlit is optional frontend only. |
| “Can others run it?” | Provide one-command examples, tests, and complete installation instructions. |

## Final conversion step

After content approval, convert `softwarex_manuscript_skeleton.md` into the current official SoftwareX template and verify formatting requirements directly from the journal website before submission.

