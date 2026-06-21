# EvoMap Integration

PaperSwarm uses EvoMap as the evolution layer for academic review experience.
The review workflow itself runs locally and writes auditable Markdown/JSON
artifacts. EvoMap is used to turn those artifacts into reusable memory and
portable GEP assets.

## Integration Model

PaperSwarm connects to EvoMap in two directions:

1. PaperSwarm -> EvoMap
   - After a review run, `archive` extracts reusable lessons from the run.
   - `publish` packages the run as a GEP bundle.
   - The bundle is shaped as `Gene + Capsule + EvolutionEvent`.

2. EvoMap -> PaperSwarm
   - A later run can recall prior review experience using paper signals.
   - Signals include discipline, method, paper type, and selected reviewer
     roles.
   - The recalled lessons are injected as prior experience, not as a replacement
     for fresh review.

## Asset Mapping

| PaperSwarm artifact | EvoMap concept | Value |
| --- | --- | --- |
| `trace.json`, `steps/` | Gene | Reusable review strategy and role-selection protocol |
| `runs/<run_id>/` | Capsule | Concrete reviewed case with evidence and adjudication |
| `archive/review_archive.md` | EvolutionEvent | What the system learned from the run |
| `publish/gep_bundle.json` | GEP bundle | Portable package for validate/publish flows |
| `structure/evomap_recall.json` | Recall evidence | Prior memories returned for the current paper signals |

## Medical RCT Example

The public case study is:

`case-studies/medical-rct-lx204/`

It demonstrates the EvoMap integration value through a medical RCT run:

- `structure` classifies the manuscript as `medical-rct`.
- The role pool expands to include `statistician` and `ethicist`.
- Six independent reviewers produce separate reports.
- `conflict` detects cross-role agreement and disagreement.
- `archive` extracts reusable lessons.
- `publish` packages the review as a GEP bundle.

The key reusable lesson is that medical RCTs need both statistician and
ethicist roles. The statistician validates numeric consistency and missing-data
assumptions; the ethicist covers clinical registration, IRB, COI, data
protection, and participant-protection risks.

## Public Evidence

- Sanitized recall example:
  `integrations/evomap/examples/recall_medical_rct.sanitized.json`
- Public GEP bundle:
  `case-studies/medical-rct-lx204/run/gep_bundle.json`
- Cold vs warm recall experiment:
  `experiments/cold-vs-warm-recall/`
- Offline bundle validation:
  `uv run python steps/publish/scripts/gep_bundle.py validate case-studies/medical-rct-lx204/run/gep_bundle.json`

## Safety Boundary

This repository intentionally does not include:

- OAuth tokens or refresh tokens
- local node secrets or account identifiers
- private submission material
- live platform failure payloads
- raw account/billing state

The public materials show how PaperSwarm integrates with EvoMap without
publishing credentials or platform-private runtime traces.
