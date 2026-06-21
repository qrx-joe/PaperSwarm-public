# Medical RCT Case Study: LX-204

This case study shows the full public PaperSwarm review chain for a synthetic
medical RCT manuscript about LX-204, a GLP-1 analogue for T2DM.

The goal is to make the EvoMap integration and PaperSwarm's review value
auditable: reviewers can inspect the input draft, role selection, independent
review outputs, conflict resolution, revision plan, archive, GEP bundle, and
P1 audit events.

## Why This Case Matters

Medical RCTs need specialized reviewers. A generic academic reviewer may notice
style and logic issues, but the most dangerous flaws are often role-specific:

- statistician: CI/p-value consistency, LOCF assumptions, multiplicity, sample
  size, model choice
- ethicist: registration, IRB approval, COI, data protection, participant
  protection
- methodologist: randomization, blinding, dropout, CONSORT reporting
- domain expert: clinical positioning against existing GLP-1 evidence
- devil's advocate: adversarial checks and alternative explanations
- editor: publication threshold and author-facing priority

In this run, `structure` classifies the paper as `medical-rct`, so the reviewer
pool expands beyond the base four roles and adds `statistician` and `ethicist`.

## Directory Map

```text
case-studies/medical-rct-lx204/
|-- input/paper_draft.medical.md
|-- run/structure/
|-- run/review_editor/
|-- run/review_method/
|-- run/review_domain/
|-- run/review_devil/
|-- run/review_statistician/
|-- run/review_ethicist/
|-- run/conflict/
|-- run/advice/
|-- run/revise/
|-- run/archive_review_archive.md
|-- run/gep_bundle.json
`-- p1-audit/
```

## Reading Path

1. Start with `input/paper_draft.medical.md`.
2. Read `run/structure/reviewer_set.json` to see why six roles were selected.
3. Compare independent reviews in `run/review_*`.
4. Read `run/conflict/conflict_report.md` for cross-role consensus and
   disagreements.
5. Read `run/advice/revision_plan.md` for P0/P1/P2 actions.
6. Read `run/revise/revise_report.md` for the simplified verification boundary.
7. Read `run/gep_bundle.json` to see how the case is packaged for EvoMap.
8. Inspect `p1-audit/events.demo.json` for the event-model audit sample.

## Main Findings

- The primary endpoint reports a 1.1% HbA1c difference with 95% CI 0.6-1.6% and
  p=0.02. The statistician and devil's advocate independently flag that the
  reported CI and p-value are mathematically inconsistent.
- Eight secondary endpoints are compared without multiplicity control, making
  nominal p=0.03 or p=0.04 claims fragile.
- LOCF is used despite asymmetric dropout. The devil's advocate initially
  argues it inflates treatment effect; the statistician corrects that the bias
  direction depends on dropout mechanism and needs sensitivity analysis.
- The ethicist uniquely flags missing clinical registration, IRB approval
  number, COI/funding disclosure, data protection, and participant-protection
  language.

## EvoMap Value

This run is packaged into a GEP bundle:

`run/gep_bundle.json`

The bundle turns a one-off review into reusable EvoMap assets:

- `Gene`: type-aware medical RCT review strategy
- `Capsule`: the LX-204 case and resolved conflicts
- `EvolutionEvent`: reusable lessons from this review

The matching recall example is published at:

`integrations/evomap/examples/recall_medical_rct.sanitized.json`

## Public Boundary

This case is a sanitized public artifact. It does not include private
credentials, OAuth files, account state, registration material, or platform
failure payloads.

The revised manuscript is intentionally not treated as the core public asset.
The evidence focus is the auditable review chain and EvoMap packaging path.

