# Case Studies

This directory contains the public evidence behind PaperSwarm's project
description.

## Coverage

| Case | What it demonstrates | Main directory |
| --- | --- | --- |
| Medical RCT | Type-aware role expansion to statistician and ethicist, conflict adjudication, EvoMap GEP packaging | `medical-rct-lx204/` |
| CS ML benchmark | Type-aware role expansion to reproducibility reviewer, while statistician and ethicist are skipped | `cs-ml-benchmark/` |
| Education quasi-experiment | Base four-role review plus a real Worker/Verifier revision loop | `education-quasi-experiment/` |

These cases should be read together. The point is not that every paper uses the
same reviewers. The point is that `structure/reviewer_set.json` selects the
right reviewer swarm for the paper type.

## Public Boundary

The case studies exclude OAuth material, live platform failures, account state,
private registration notes, and raw submission logistics. They keep the review
chain, role-selection evidence, conflict reports, revision artifacts, and GEP
bundles that are needed to audit the project.

