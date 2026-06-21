# Schema Gap Report for Medical RCT Demo Run

This note summarizes which audit fields can be recovered from the cached medical run, and which fields should only be claimed after the corresponding STEP implementations produce them natively.

The original report was written as a go/no-go audit for the event schema. This public version keeps the parts that are useful for reviewers and removes internal workspace details.

## 1. Run Provenance

| Item | Status |
|---|---|
| Reviewer judgments | Real cached outputs from six independent reviewer roles |
| Decision stage | AI-simulated author resolution in the cached medical run |
| Revision stage | Simplified in the historical medical run; full Worker/Verifier loop is demonstrated in the education case |
| Human-in-the-loop status | Interface and schema hooks are present, but the medical cached run should not be presented as a completed human decision run |

## 2. Event Recoverability

| Event type | Recoverability | Current state | Needs native STEP support |
|---|---|---|---|
| `reviewer_judgment` | Strong | Claims, evidence, and severity are present in reviewer reports | Stable finding IDs, target section ranges, and explicit confidence levels |
| `conflict` | Strong | Consensus and disagreements are explicit in the conflict report | Stable conflict IDs, tension categories, and finding references |
| `decision` | Partial | Resolution text exists, but the maker is AI-simulated | Human decision maker and structured `resolves` references |
| `revision` | Missing in the historical medical run | No revised paper artifact in that run | Full before/after revision objects and verifier state |
| `baseline_judgment` | Partial | Can be inferred from archived experience | Explicit linkage from recalled experience to current findings |

## 3. Lineage Breakpoints

- `judgment -> conflict`: soft break. The cached run links by semantics rather than stable `finding_id` and `conflict_id`.
- `conflict -> decision`: soft break. The run has numbered disagreements, but lacks machine-readable reference keys.
- `decision -> revision`: hard break in the historical medical run. The revision chain was intentionally simplified there.

This distinction matters because physical time order is not the same as causal lineage. A reviewer-facing audit trail needs explicit references such as `resolves`, `enacts`, and `derived_from`.

## 4. Honest Demo Boundary

The medical RCT run is strong evidence for multi-role review depth, especially the CI/p-value inconsistency found independently by two roles. It should not be described as a full human-in-the-loop revision run.

For a full Worker/Verifier correction loop, use the education quasi-experiment case. For EvoMap memory recall behavior, use the cold-vs-warm recall experiment.

## 5. Production Fixes

| Missing field or behavior | Production-side fix |
|---|---|
| `confidence_level` | Add explicit low/medium/high confidence output to reviewer STEP files |
| `finding_id` and `conflict_id` | Emit stable IDs from review and conflict stages |
| `tension_type` | Classify conflict types inside the conflict STEP |
| Human `decision_maker` | Require an explicit human confirmation gate for gold runs |
| `decision.resolves` | Reference conflict IDs from decision objects |
| Revision lineage | Run Worker/Verifier and persist before/after revision records |

The discipline is simple: missing fields should be marked as gaps, not backfilled as if they were produced by the original agents.
