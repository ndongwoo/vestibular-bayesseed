# default_modules v0.1.0

This folder contains literature-informed default disease modules for the proposed
Vestibular-BayesSeed software.

## Files

- `bppv.json`: BPPV worked example module.
- `meniere_disease.json`: Ménière disease worked example module.
- `pvp_bvp.json`: Presbyvestibulopathy module with bilateral vestibulopathy as a competing target.
- `sensitivity_ranges.json`: priority edges and beta ranges for sensitivity analysis.
- `module_schema_draft.json`: draft JSON schema for module validation.

## Design principle

The modules follow a raw-input -> derived-pattern -> diagnosis structure.
Most strongly supported objective or criteria-defining evidence is placed on
raw-input -> derived-pattern edges. The downstream derived-pattern -> diagnosis
edges are kept moderate when the same clinical construct has already been used
upstream, to reduce double counting.

## Disclaimer

These coefficients are literature-informed initialization values, not validated
clinical calibration parameters. The files are intended for research and
educational demonstration only and should not be used for patient management.

## Intercepts

Diagnosis-node intercepts are placeholders. Before any validation study, replace
them with priors appropriate for the intended clinic, stage, and referral pathway.
