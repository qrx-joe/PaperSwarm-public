# PaperSwarm

PaperSwarm is a multi-role academic review workflow for Chinese research drafts. It turns one paper into a traceable review swarm: structure parsing, role selection, independent expert reviews, conflict detection, revision planning, verification, archival, and optional EvoMap asset packaging.

The project is designed as a clean public artifact. It contains the workflow definition, role prompts, schema/rubric resources, and one sanitized cached demo run. It does not include private credentials, registration material, travel notes, planning logs, or hackathon working notes.

## What It Does

- Selects reviewers by paper type instead of using one fixed agent chain.
- Runs independent review roles such as editor, methodologist, domain expert, devil's advocate, statistician, reproducibility reviewer, and ethicist.
- Compares reviewer outputs to find conflicts, overlapping evidence, and priority disagreements.
- Produces a P0/P1/P2 revision plan and a verification report.
- Packages the run as a portable trace and optional EvoMap GEP bundle.

## Repository Layout

```text
.
├─ trace.json                  # Workflow declaration
├─ resources/                  # Example paper, schemas, rubrics, reusable knowledge
├─ steps/                      # Step-level instructions and helper scripts
├─ runs/demo/                  # Sanitized cached demo output
├─ replay/                     # Static replay viewer
├─ scripts/demo-smoke.ps1      # Offline public smoke check
├─ docs/DEMO.md                # Demo walkthrough
├─ .env.example                # Credential variable names only
└─ pyproject.toml              # Minimal uv project metadata
```

## Quick Check

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\demo-smoke.ps1
```

The smoke check only validates local files and JSON. It does not call LLMs, EvoMap, or any external service.

If you use Python helpers, create the project-local virtual environment with uv:

```powershell
uv venv
uv run python --version
```

## Demo Run

The included demo is under `runs/demo/`. It shows a medical RCT draft being routed to editor, method, domain, devil, ethicist, and statistician reviewers. The reviewers independently surface statistical consistency issues and publication-compliance gaps, then the workflow merges them into a conflict report and revision plan.

Start reading from:

- `runs/demo/structure/reviewer_set.json`
- `runs/demo/conflict/conflict_report.md`
- `runs/demo/advice/revision_plan.md`
- `runs/demo/revise/revise_report.md`
- `runs/demo/publish/gep_bundle.json`

## Credentials

No secrets are committed. EvoMap integration scripts expect credentials from the user's local environment or home directory. For public demos, use `validate`/offline paths first and never commit generated token files.

## License

MIT. See `LICENSE`.
