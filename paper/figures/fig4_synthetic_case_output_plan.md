# Figure 4 plan: Synthetic case output

Generate outputs with:

```bash
python examples/run_examples.py
```

Recommended source files:

```text
examples/output/synthetic_case_results_summary.csv
examples/output/synthetic_case_results_detailed.json
```

Suggested figure format:

- A table-like panel showing the top-ranked diagnosis for each synthetic case
- Or three small posterior probability plots for representative BPPV, MD, and PVP/BVP cases

Important language:

> These synthetic examples demonstrate model behavior and are not intended to estimate clinical diagnostic accuracy.

Draft caption:

> Figure 4. Output from synthetic demonstration cases. The examples demonstrate posterior ranking behavior, competing diagnostic probabilities, and the effect of derived-node activation. They are not intended to estimate diagnostic accuracy or clinical performance.

