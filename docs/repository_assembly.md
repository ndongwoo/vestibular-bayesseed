# Repository assembly guide

This guide explains how to assemble the generated archives into a single GitHub-ready repository.

## Target repository structure

```text
vestibular-bayesseed/
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── default_modules/
├── docs/
├── src/
│   └── bayesseed/
├── examples/
├── app/
└── tests/
```

## Step 1. Create repository folder

```bash
mkdir vestibular-bayesseed
cd vestibular-bayesseed
```

## Step 2. Copy root files

Copy the contents of:

```text
vestibular-bayesseed_root_files/
```

into the repository root.

Required files:

- `README.md`
- `LICENSE`
- `pyproject.toml`
- `requirements.txt`
- `.gitignore`

## Step 3. Copy default modules

Copy:

```text
default_modules/
```

into the repository root.

Expected files:

- `bppv.json`
- `meniere_disease.json`
- `pvp_bvp.json`
- `sensitivity_ranges.json`
- `module_schema_draft.json`
- `README.md`

## Step 4. Copy core engine

Copy:

```text
src/bayesseed/
```

into:

```text
vestibular-bayesseed/src/bayesseed/
```

## Step 5. Copy examples

Copy:

```text
examples/
```

into the repository root.

Expected files:

- `synthetic_cases.csv`
- `run_examples.py`

## Step 6. Copy tests

Copy:

```text
tests/
```

into the repository root.

## Step 7. Copy Streamlit app

Copy:

```text
app/streamlit_app.py
```

into:

```text
vestibular-bayesseed/app/streamlit_app.py
```

## Step 8. Copy documentation

Copy:

```text
docs/
```

into the repository root.

## Step 9. Add evidence table

Place the edge-level evidence table in the repository root or a data/docs folder.

Recommended:

```text
edge_level_evidence_table_v0_1_0.csv
edge_level_evidence_table_v0_1_0.md
edge_level_evidence_table_v0_1_0.json
```

The Streamlit app can automatically detect the CSV if it is placed at the root.

## Step 10. Install and test

```bash
pip install -e .[app,dev]
pytest
python examples/run_examples.py
```

## Step 11. Run CLI smoke tests

```bash
bayesseed validate default_modules/
bayesseed list-modules --modules default_modules/
bayesseed mermaid default_modules/bppv.json
```

## Step 12. Run Streamlit

```bash
streamlit run app/streamlit_app.py
```

## Step 13. Create release

Before submission:

```bash
git init
git add .
git commit -m "Initial v0.2.1 release"
git tag v0.2.1
```

Then push to GitHub and create a release. Consider archiving the release with Zenodo to obtain a DOI.

## Pre-submission checklist

- [ ] repository installs with `pip install -e .[app,dev]`;
- [ ] `pytest` passes;
- [ ] examples run;
- [ ] Streamlit opens;
- [ ] README explains intended use and limitations;
- [ ] LICENSE is present;
- [ ] CITATION.cff is present or planned;
- [ ] no patient data are included;
- [ ] medical disclaimer is visible;
- [ ] GitHub release is tagged.
