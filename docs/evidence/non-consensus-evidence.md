# PaperSwarm Non-Consensus Evidence Card

Source case: the cached medical RCT run for GLP-1 analog LX-204 in type 2 diabetes. The case uses six independent reviewer contexts and a fan-in conflict stage.

This note records the strongest public-facing evidence for PaperSwarm's core claim: some rejection-level defects are only visible when the right specialist role is present, and some claims become more reliable when two independent roles reach the same finding.

## Card 1: Primary Endpoint CI and p Value Are Inconsistent

Human reviewer blind spot: many reviews check whether a confidence interval crosses zero and whether `p < 0.05`, but do not recompute the standard error implied by the confidence interval.

PaperSwarm finding, independently identified by the statistician and devil's advocate:

- The paper reports a between-group difference of `1.1%`, `95% CI [0.6%, 1.6%]`, and `p = 0.02`.
- The CI width implies `SE ~= 0.255%`.
- But with approximately `n = 120` per arm and `SD ~= 0.85`, the standard error is roughly `sqrt(0.85^2 / 120 * 2) ~= 0.110`.
- That implies `z ~= 10`, so the p value should be far smaller than `0.02`.

Why it matters: this is not a stylistic issue. It suggests the primary endpoint table needs to be reconciled against the original statistical output before the result can be trusted.

## Card 2: Eight Secondary Endpoints Without Multiplicity Control

PaperSwarm finding, identified by the statistician:

- Eight secondary endpoints are reported using nominal `p < 0.05`.
- No Holm, Hochberg, hierarchical gatekeeping, or other multiplicity strategy is documented.
- With eight tests at alpha `0.05`, the family-wise probability of at least one false positive is about `1 - 0.95^8 ~= 34%`.
- A Holm-style first threshold would be `0.05 / 8 = 0.00625`, making reported values such as `p = 0.03` or `p = 0.04` insufficient as standalone confirmatory evidence.

Why it matters: the issue is not merely "add a sentence about limitations"; it changes how secondary efficacy claims should be interpreted.

## Card 3: LOCF and Asymmetric Dropout Need Sensitivity Analysis

PaperSwarm finding, captured as a useful disagreement between the devil's advocate and statistician:

- The devil's advocate argued that LOCF plus asymmetric dropout likely inflated the treatment effect.
- The statistician corrected the directionality claim: the bias direction depends on the missingness mechanism and must be tested rather than asserted.
- The conflict stage kept the practical concern while tightening the claim into an executable requirement: run sensitivity analyses such as MMRM and tipping-point analysis.

Why it matters: the swarm did not just average opinions. It preserved a sharp objection, checked its statistical overreach, and turned it into a concrete revision requirement.

## Summary

| Blind spot | Detecting role(s) | Why it matters |
|---|---|---|
| CI/p-value inconsistency | Statistician + devil's advocate | Requires active recomputation, not checklist reading |
| Multiplicity inflation | Statistician | Changes the evidential status of secondary endpoints |
| Missing-data bias direction | Devil's advocate + statistician | Converts an intuitive objection into a testable analysis |
| Ethics and registration gaps | Ethicist | Trial registration, IRB approval, and COI statements are domain-specific rejection risks |
| Reproducibility gaps | Reproducibility reviewer in CS runs | Benchmark comparability depends on shared code, data, and environment |

The useful pattern is not "more reviewers are always better." The useful pattern is type-aware reviewer selection: medical RCTs need statistical and ethics review; CS benchmark papers need reproducibility review; other paper types should not pay for irrelevant roles.
