# CS ML Benchmark Case Study

This case shows how PaperSwarm changes reviewer composition for a computer
science benchmark paper.

Unlike the medical RCT case, this run selects `reproducibility` and skips
`statistician` and `ethicist`. That is the key evidence for type-aware reviewer
selection: a CS benchmark paper needs code/data/baseline scrutiny more than
clinical-trial statistics or medical ethics review.

## Reading Path

1. `run/structure/reviewer_set.json`
2. `run/review_reproducibility/review_reproducibility.md`
3. `run/review_devil/review_devil.md`
4. `run/conflict/conflict_report.md`
5. `run/advice/revision_plan.md`
6. `run/gep_bundle.json`

## What It Demonstrates

- `structure` classifies the paper as `cs-ml-benchmark`.
- `reproducibility` is included to check baseline fairness, data/code
  availability, run variance, and experimental comparability.
- `statistician` and `ethicist` produce sentinel skip files because this is not
  a clinical RCT or human-subject medical study.
- The conflict report shows that role severity depends on defect type, not a
  fixed "strict" or "lenient" persona.

## EvoMap Relevance

The GEP bundle records the case as a reusable CS benchmark review lesson:

`run/gep_bundle.json`

It complements the medical RCT case by proving that PaperSwarm's role-selection
signals are bidirectional: medical adds statistician/ethicist, CS adds
reproducibility.

