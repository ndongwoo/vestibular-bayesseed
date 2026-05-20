# Figure plan for SoftwareX manuscript

## Figure 1. Software architecture

**Purpose:** Show that Vestibular-BayesSeed is a reusable framework rather than a disease-specific app.

**Core message:** Disease-specific knowledge is stored in JSON modules, while the Python engine handles validation, derived-node evaluation, logistic CPD inference, sensitivity analysis, and output through CLI/API/Streamlit.

**Suggested panels:**

- Panel A: Repository components
- Panel B: Runtime workflow
- Panel C: Available interfaces

**Draft caption:**

> Figure 1. Architecture of Vestibular-BayesSeed. Disease-specific knowledge is encoded in modular JSON files, whereas reusable Python components handle schema validation, derived-node evaluation, logistic-CPD inference, sensitivity analysis, and visualization. The same inference engine can be accessed through the Python API, command-line interface, batch examples, or the optional Streamlit demonstration interface.

**Source file:** `fig1_architecture.mmd`

---

## Figure 2. Node taxonomy and modeling pattern

**Purpose:** Explain input nodes, derived nodes, target disease nodes, competing/negative edges, and evidence metadata.

**Core message:** Most literature-defined evidence is placed on raw input → derived pattern edges; derived pattern → diagnosis edges are kept moderate to reduce double counting.

**Draft caption:**

> Figure 2. Node taxonomy used in the default disease modules. Raw input nodes represent observations, derived nodes represent intermediate clinical constructs, and target disease nodes estimate posterior diagnostic probabilities using logistic CPDs. Competing edges reduce the probability of target disease nodes when evidence suggests an alternative diagnosis or a red-flag condition.

**Source file:** `fig2_node_taxonomy.mmd`

---

## Figure 3. Streamlit demonstration interface

**Purpose:** Show the optional interactive UI.

**Needed before submission:** Run `streamlit run app/streamlit_app.py`, capture a screenshot of the Module Viewer or Case Simulator, and save it as `fig3_streamlit_demo.png`.

**Important:** The screenshot should visibly include the research/educational disclaimer.

**Draft caption:**

> Figure 3. Optional Streamlit demonstration interface. The interface allows users to inspect default modules, enter synthetic clinical findings, view derived-node activation, examine edge-level evidence metadata, and perform one-way sensitivity analysis. The interface is intended for research and educational demonstration only.

---

## Figure 4. Synthetic case output

**Purpose:** Demonstrate model behavior without clinical validation claims.

**Recommended source:** Run `python examples/run_examples.py` and use the resulting summary table or posterior plot.

**Suggested panels:**

- Panel A: BPPV synthetic cases and posterior ranking
- Panel B: Ménière's disease synthetic cases and posterior ranking
- Panel C: PVP/BVP synthetic cases and competing posterior behavior

**Draft caption:**

> Figure 4. Output from synthetic demonstration cases. The examples demonstrate posterior ranking behavior, competing diagnostic probabilities, and the effect of derived-node activation. They are not intended to estimate diagnostic accuracy or clinical performance.

