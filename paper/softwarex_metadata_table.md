# Software metadata table

| Metadata field | Value |
|---|---|
| Current code version | v0.2.3 |
| Permanent link to code/repository used for this code version | https://doi.org/10.5281/zenodo.20339056 |
| Permanent link to reproducible capsule | Not applicable / TBD if Code Ocean or Binder is added |
| Legal code license | Apache License 2.0 |
| Code versioning system used | git |
| Software code languages, tools, and services used | Python, JSON, JSON Schema/Pydantic-style validation, NumPy, pandas, NetworkX, matplotlib, Click, Rich, Streamlit, pytest |
| Compilation requirements, operating environments, and dependencies | Python >=3.10; operating-system independent; dependencies listed in `pyproject.toml` and `requirements.txt` |
| Installation | `pip install -e .` from repository root; optional app dependencies with `pip install -e .[app]` |
| Example execution | `python examples/run_examples.py`; `bayesseed validate default_modules/bppv.json`; `streamlit run app/streamlit_app.py` |
| Link to developer documentation/manual | TBD: GitHub `docs/` URL |
| Support email for questions | ndongwoo@gmail.com |
| Repository URL | https://github.com/ndongwoo/vestibular-bayesseed |
| Issue tracker | https://github.com/ndongwoo/vestibular-bayesseed/issues |
| Documentation URL | https://github.com/ndongwoo/vestibular-bayesseed/tree/main/docs |
| Example data availability | Synthetic cases included in `examples/synthetic_cases.csv`; no patient-level data included |
| Intended use | Research, education, and methodological demonstration |
| Explicit non-intended use | Not for clinical diagnosis, triage, treatment decisions, or patient management without validation and regulatory review |

