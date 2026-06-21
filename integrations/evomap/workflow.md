# PaperSwarm x EvoMap Workflow

```text
paper_draft.md
  -> structure
      -> reviewer_set.json
      -> EvoMap recall by paper signals
  -> independent review roles
  -> conflict detection and adjudication
  -> revision plan
  -> archive reusable lessons
  -> publish GEP bundle
```

## 1. Signal Encoding

PaperSwarm converts the paper into EvoMap-friendly signals:

- `paper-review`
- `discipline-medical`
- `method-rct`
- `type-medical-rct`
- `role-editor`
- `role-method`
- `role-domain`
- `role-devil`
- `role-statistician`
- `role-ethicist`

These signals let a later run recall prior cases with similar review structure.

## 2. Recall Injection

Recall is treated as prior experience. It can remind the reviewers of common
risks, but each reviewer still has to inspect the current manuscript. This
keeps the workflow from blindly copying old findings.

For the medical RCT case, recalled lessons include:

- LOCF plus asymmetric dropout needs sensitivity analysis.
- CI and p-value consistency should be recalculated.
- Multiple secondary endpoints need multiplicity control.
- Clinical registration, IRB, COI, and participant protection require ethicist
  review.

## 3. GEP Bundle

The publish step packages the run into:

- `Gene`: the reusable review strategy.
- `Capsule`: the LX-204 medical RCT case and its resolved conflicts.
- `EvolutionEvent`: the lessons extracted from this run.

The public bundle can be validated offline without external credentials:

```powershell
uv run python steps\publish\scripts\gep_bundle.py validate case-studies\medical-rct-lx204\run\gep_bundle.json
```

## 4. Honest Boundary

The public repository proves the integration path, the asset format, the
medical RCT case, and offline validation. It does not claim that every future
review is automatically improved by one recalled memory. In current evidence,
EvoMap is most valuable as a reusable memory and packaging layer; quality gains
need more runs and harder cross-case tests.

