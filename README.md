# PaperSwarm

[Chinese README](README.zh-CN.md)

PaperSwarm is a multi-role academic review workflow for Chinese research
drafts. It turns one paper into a traceable review swarm: structure parsing,
role selection, independent expert reviews, conflict detection, revision
planning, verification, archival, and optional EvoMap asset packaging.

The project is designed as a clean public artifact. It contains the workflow
definition, role prompts, schema/rubric resources, a static replay viewer, and
one sanitized cached demo run. It does not include private credentials,
registration material, travel notes, planning logs, or hackathon working notes.

This repository is a public demo subset, not the full private working folder.
The private workspace may contain extra draft papers, additional runs, local
experience stores, roadmap notes, OAuth experiments, and event logs. Those files
are intentionally excluded when they are private, process-heavy, unrelated to
the public demo, or unnecessary for offline validation.

## What It Does

- Selects reviewers by paper type instead of using one fixed agent chain.
- Runs independent review roles such as editor, methodologist, domain expert,
  devil's advocate, statistician, reproducibility reviewer, and ethicist.
- Compares reviewer outputs to find conflicts, overlapping evidence, and
  priority disagreements.
- Produces a P0/P1/P2 revision plan and a verification report.
- Packages the run as a portable trace and optional EvoMap GEP bundle.

## EvoMap Integration

PaperSwarm uses EvoMap as the evolution layer for review experience. A review
run can be archived as reusable memory, recalled by paper signals, and packaged
as a GEP bundle containing `Gene`, `Capsule`, and `EvolutionEvent` assets.

Start here:

- `integrations/evomap/README.md`
- `integrations/evomap/workflow.md`
- `integrations/evomap/examples/recall_medical_rct.sanitized.json`

The main public integration cases are:

- `case-studies/medical-rct-lx204/`
- `case-studies/cs-ml-benchmark/`
- `case-studies/education-quasi-experiment/`

## Repository Layout

```text
.
|-- trace.json                  # Workflow declaration
|-- resources/                  # Example paper, schemas, rubrics, reusable knowledge
|-- steps/                      # Step-level instructions and helper scripts
|-- runs/demo/                  # Sanitized cached demo output
|-- case-studies/               # Public end-to-end case studies
|-- integrations/               # EvoMap integration notes and sanitized examples
|-- replay/                     # Static replay viewer
|-- scripts/demo-smoke.ps1      # Offline public smoke check
|-- docs/DEMO.md                # Demo walkthrough
|-- .env.example                # Credential variable names only
`-- pyproject.toml              # Minimal uv project metadata
```

## Quick Check

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\demo-smoke.ps1
```

The smoke check validates the local public demo files, JSON assets, declared
`trace.json` demo assets, the review reports, and the GEP bundle. It does not
call LLMs, EvoMap, or any external service.

If you use Python helpers, create the project-local virtual environment with
uv:

```powershell
uv venv
uv run python --version
```

If PowerShell prints Chinese text as mojibake, switch the console to UTF-8
before viewing files:

```powershell
chcp 65001
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
```

## Demo Run

The included demo is under `runs/demo/`. It shows a medical RCT draft being
routed to editor, method, domain, devil, ethicist, and statistician reviewers.
The reviewers independently surface statistical consistency issues and
publication-compliance gaps, then the workflow merges them into a conflict
report and revision plan.

Start reading from:

- `runs/demo/structure/reviewer_set.json`
- `runs/demo/conflict/conflict_report.md`
- `runs/demo/advice/revision_plan.md`
- `runs/demo/revise/revise_report.md`
- `runs/demo/archive/review_archive.md`
- `runs/demo/publish/gep_bundle.json`

The public demo includes a placeholder `runs/demo/revise/paper_revised.md`
rather than a full revised manuscript. That keeps the package focused on the
workflow trace and avoids redistributing unnecessary manuscript text.

## Medical RCT Case Study

The full public medical chain is under `case-studies/medical-rct-lx204/`. It
includes the synthetic medical manuscript, six role reviews, conflict
adjudication, a revision plan, an archive summary, a P1 audit sample, and the
GEP bundle used to show the EvoMap integration path.

Additional public cases are under `case-studies/`: the CS benchmark case shows
why reproducibility review is selected for computational experiments, and the
education quasi-experiment case shows the real Worker/Verifier revision loop.

## Credentials

No secrets are committed. EvoMap integration scripts expect credentials from
the user's local environment or home directory. For public demos, use
`validate`/offline paths first and never commit generated token files.

## Contributors

- [qrx-joe](https://github.com/qrx-joe)
- [Joe-rq](https://github.com/Joe-rq)

## License

MIT. See `LICENSE`.
