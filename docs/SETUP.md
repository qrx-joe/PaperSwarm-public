# Setup

This repository is designed to be reviewable offline. A fresh clone can validate
the public demo without LLM keys, EvoMap credentials, or access to the original
private workspace.

## Dependency Matrix

| Capability | Required tools | Required? |
|---|---|---|
| Read Markdown/JSON artifacts | Git, a text editor | Yes |
| Run offline smoke check | PowerShell 5.1+, Node.js, uv, Python 3.11+ | Recommended |
| Validate GEP bundles | uv, Python 3.11+ | Recommended |
| Validate review roles and JSON | Node.js | Recommended |
| Open replay page | Any modern browser | Optional |
| Open Flowtrace DAG UI | Flowtrace CLI | Optional |
| Call EvoMap live APIs | EvoMap credentials | Optional, not needed for public demo |
| Call LLMs live | Model/API credentials | Optional, not needed for public demo |

## Windows Quick Start

1. Clone the repository:

   ```powershell
   git clone https://github.com/qrx-joe/PaperSwarm-public.git
   cd PaperSwarm-public
   ```

2. Install the general-purpose tools if they are missing:

   ```powershell
   winget install Git.Git
   winget install Python.Python.3.12
   winget install astral-sh.uv
   winget install OpenJS.NodeJS.LTS
   ```

3. Create the project-local Python environment:

   ```powershell
   uv venv
   uv run python --version
   ```

4. Run the offline smoke check:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\demo-smoke.ps1
   ```

   Expected result:

   ```text
   PaperSwarm public demo smoke: PASS
   ```

The smoke check does not call LLMs, EvoMap, or any external API. It validates
local files, JSON assets, reviewer role coverage, and GEP bundle structure.

## Static Replay Page

The route-level replay page is self-contained:

```powershell
uv run python -m http.server 8765 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8765/replay/index.html
```

You can also open `replay/index.html` directly in a browser because it embeds a
demo event stream.

## Flowtrace DAG UI

The Flowtrace DAG viewer is optional and external. This repository contains the
PaperSwarm `trace.json` and a launcher script, but it does not bundle the
Flowtrace CLI binary or Web UI source.

To use it, install Flowtrace so that one of these works:

```powershell
flowtrace --help
```

or:

```powershell
Test-Path "$env:USERPROFILE\.cargo\bin\flowtrace.exe"
```

Then start the DAG viewer:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\serve-flowtrace.ps1
```

Open:

```text
http://127.0.0.1:3001
```

Important: Flowtrace's `--scope` argument points to the directory that contains
trace project folders, not the folder that directly contains `trace.json`.
`scripts/serve-flowtrace.ps1` handles this automatically.

## Credentials

No credentials are required for the public demo.

Do not commit:

- `.env`
- `node_id`
- `node_secret`
- OAuth token files
- raw live EvoMap responses
- local run state or account/balance payloads

The repository includes `.env.example` only to document variable names.

## Troubleshooting

If PowerShell prints Chinese text as mojibake, switch to UTF-8 first:

```powershell
chcp 65001
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
```

If `demo-smoke.ps1` fails with `node not on PATH`, install Node.js LTS and open
a new terminal.

If it fails with `uv not on PATH`, install uv and open a new terminal.

If `serve-flowtrace.ps1` says Flowtrace is missing, the offline demo is still
usable; only the optional DAG UI is unavailable.
