# P1 Tiny Audit Chain

This folder is the smallest honest upgrade from "good demo" to "auditable demo".

## What Is Here

- `events.demo.json`
  A valid manual-demo event chain for one conflict: `finding -> conflict -> ai_simulated decision`.

- `events.human-template.json`
  A tiny gold-run template. It must not be submitted as truth until the human operator fills every `REPLACE_*` placeholder and confirms the decision.

- `index.html`
  Offline static audit table. Open directly in a browser. It intentionally shows `decision_maker = ai_simulated` so the demo does not fake human-in-loop.

## How To Upgrade To Human Gold

1. Ask the human operator to confirm the C2 decision:
   - adopt / reject / partial / request_reargument
   - one-sentence rationale
2. Copy `events.human-template.json` to `events.human.json`.
3. Replace:
   - `REPLACE_WITH_ISO_TIMESTAMP`
   - `REPLACE_WITH_HUMAN_DECISION_TIME`
   - `REPLACE_WITH_HUMAN_RATIONALE`
   - `REPLACE_WITH_REVISION_TIME`
   - `REPLACE_WITH_SCOPED_REVISION_ACTION`
4. Validate JSON:
   ```powershell
   node -e "JSON.parse(require('fs').readFileSync('events.human.json','utf8'))"
   ```
5. Load `events.human.json` in `1-do/flowtrace/papertrace-review/replay/index.html`.

## Discipline

Do not set `decision_maker=human` without real human confirmation. A fake gold run is worse than no gold run.
