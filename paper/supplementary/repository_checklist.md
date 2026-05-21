# Repository readiness checklist for SoftwareX submission

Use this checklist before submission.

## Required repository files

- [ ] `README.md` is complete and includes installation, quick start, default modules, and disclaimer.
- [ ] `LICENSE` is present and matches the metadata table.
- [ ] `CITATION.cff` is present or planned before release.
- [ ] `pyproject.toml` defines package metadata and dependencies.
- [ ] `requirements.txt` is present for users who prefer pip requirements.
- [ ] `.gitignore` is present.
- [ ] `src/bayesseed/` contains the reusable core engine.
- [ ] `default_modules/` contains BPPV, MD, PVP/BVP modules.
- [ ] `examples/synthetic_cases.csv` is present.
- [ ] `examples/run_examples.py` runs without errors.
- [ ] `tests/` exists and `pytest` passes.
- [ ] `docs/` includes module extension and evidence mapping guides.
- [ ] `app/streamlit_app.py` launches with `streamlit run app/streamlit_app.py`.

## Reproducibility checks

Run from the repository root:

```bash
pip install -e .[app,dev]
pytest
python examples/run_examples.py
bayesseed validate default_modules/bppv.json
bayesseed validate default_modules/meniere_disease.json
bayesseed validate default_modules/pvp_bvp.json
streamlit run app/streamlit_app.py
```

## Release checks

- [ ] Create GitHub repository.
- [ ] Push all files.
- [ ] Open and close at least one test issue or run GitHub Actions if available.
- [ ] Create release `v0.2.1`.
- [ ] Archive release in Zenodo.
- [ ] Replace all `TBD` placeholders in manuscript.
- [ ] Capture Streamlit screenshot for Figure 3.
- [ ] Generate synthetic output figure/table for Figure 4.

## Scope-control checks

- [ ] README clearly states research/educational use only.
- [ ] Manuscript does not claim clinical validation.
- [ ] Streamlit UI includes disclaimer.
- [ ] No patient-level data are included.
- [ ] Synthetic cases are clearly labeled as synthetic.
- [ ] Limitations state that clinical deployment requires validation and regulatory review.

