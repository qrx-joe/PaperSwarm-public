# PaperSwarm Demo

This demo is cached and offline. It is meant to show the workflow shape and the quality of the produced artifacts without requiring live model calls.

## Walkthrough

1. Open `trace.json` to see the full workflow DAG.
2. Open `runs/demo/structure/reviewer_set.json` to see how the paper type selected the reviewer swarm.
3. Compare independent reviews:
   - `runs/demo/review_editor/review_editor.md`
   - `runs/demo/review_method/review_method.md`
   - `runs/demo/review_domain/review_domain.md`
   - `runs/demo/review_devil/review_devil.md`
   - `runs/demo/review_ethicist/review_ethicist.md`
   - `runs/demo/review_statistician/review_statistician.md`
4. Read `runs/demo/conflict/conflict_report.md` to see how cross-reviewer conflicts and convergences were merged.
5. Read `runs/demo/advice/revision_plan.md` for the P0/P1/P2 repair plan.
6. Read `runs/demo/revise/revise_report.md` for the verification summary.

## Offline Smoke Test

```powershell
powershell -ExecutionPolicy Bypass -File scripts\demo-smoke.ps1
```

The script checks expected files and validates JSON syntax. It does not send network requests.
