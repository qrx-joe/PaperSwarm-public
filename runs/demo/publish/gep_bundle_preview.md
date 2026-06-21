# GEP Bundle Preview

This is the human-readable public preview for
`runs/demo/publish/gep_bundle.json`.

## Bundle

- Bundle id: `paperswarm-run_20260618T031533Z_med`
- Protocol: `gep-a2a`
- Created at: `2026-06-18T03:20:00Z`
- Bundle hash: `sha256:6057be8ae52d99495b8acc2cd1aa4c1b99a867892984ce95157dd62d5154620b`

## Quality Gate

- Outcome score: `0.833`
- Blast radius files: `1`
- Blast radius lines: `200`
- Gate passed: `true`

## Assets

- `Gene`: pluggable PaperSwarm review strategy for Chinese academic drafts.
- `Capsule`: cached medical RCT demo case and its resolved review conflicts.
- `EvolutionEvent`: completed review event with conflict patterns, role
  reliability, and reusable lesson.

## Public Demo Note

This preview is sanitized for the public repository. It does not include private
credentials, OAuth material, registration notes, travel notes, planning logs, or
hackathon working notes.

The offline validation path is:

```powershell
uv run python steps\publish\scripts\gep_bundle.py validate runs\demo\publish\gep_bundle.json
```
