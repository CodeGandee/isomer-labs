# Use a Read-Only Houmao Capability Gate

Milestone 5 needs a deterministic way to decide whether the local Houmao checkout is available for adapter work. Isomer will treat `extern/orphan/houmao` as adapter-available only after a lightweight read-only capability gate passes: resolve the checkout path, confirm `tmux -V`, run `pixi run houmao-mgr --version`, run `pixi run houmao-mgr --print-json system-skills list`, run `pixi run houmao-mgr --print-json project --project-dir <project> status`, and run `pixi run houmao-mgr --print-json agents global list`.

## Status

accepted

## Considered Options

- Read-only capability gate.
- Read-only capability gate plus Houmao `pixi run test-runtime`.
- Read-only capability gate plus temporary live launch smoke.

## Consequences

Default Isomer launch and handoff preflight stays fast and non-mutating. Houmao runtime tests, live launch smoke checks, and live handoff rounds remain part of live-gated integration or manual validation, not the baseline adapter availability check.
