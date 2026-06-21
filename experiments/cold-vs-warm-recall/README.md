# Cold vs Warm Recall Experiment

This experiment compares two review runs on the same medical RCT draft:

- `cold/`: PaperSwarm without EvoMap recall injection.
- `warm/`: PaperSwarm with EvoMap recall injected before review.

The goal is to test whether one recalled medical RCT memory changes review
coverage on a new but similar RCT manuscript.

## Result

The honest result is negative for simple defect-count improvement:

| Metric | Cold | Warm |
| --- | ---: | ---: |
| Reviewer roles | 6 | 6 |
| Core planted issues hit | 5/5 | 5/5 |
| Total findings | 54 | 50 |
| EvoMap recall available | No | Yes |

Warm recall did not make PaperSwarm find more routine RCT defects. That is not
a failed integration. It shows that the existing specialist roles already cover
common RCT issues such as CI/p-value inconsistency, multiplicity, LOCF/dropout,
subgroup interaction, and missing registration/IRB evidence.

## Why This Still Matters

The experiment proves two useful things:

- PaperSwarm's multi-role review is strong even at cold start.
- EvoMap recall is wired into the workflow and can inject prior medical RCT
  review experience.

The current evidence does not justify claiming that one recalled memory
reliably improves every review. The realistic claim is narrower and stronger:
EvoMap provides a reusable memory path, and its quality impact should be tested
across more runs and less routine defects.

## Files

- `comparison.md`: Chinese experiment report.
- `cold/`: cold-start draft, role set, and six independent reviews.
- `warm/`: warm-start draft, role set, and six independent reviews.
- `examples/warm_recall.sanitized.json`: sanitized EvoMap recall evidence.

## Public Boundary

The original platform response is not published. This directory keeps only
review artifacts and a sanitized recall example. No OAuth tokens, account
state, live failure payloads, or node-local secrets are included.

