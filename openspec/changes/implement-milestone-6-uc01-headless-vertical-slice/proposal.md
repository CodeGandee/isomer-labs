## Why

Milestone 5 proves Isomer can launch, inspect, stop, dispatch, observe, and normalize one Houmao-backed Agent Team Instance, but the platform still lacks a repeatable research workflow that turns those mechanics into durable research state. Milestone 6 should make UC-01, Explore a New Research Direction, the first headless vertical slice that starts from a fixture Project and ends with recorded Artifacts, Evidence Items, a follow-up Research Inquiry Gate, and a Decision Record.

## What Changes

- Add a UC-01 fixture Project and repeatable headless workflow that initializes Workspace Runtime, prepares readiness, creates a `deepsci-mini` Agent Team Instance, launches or simulates the team through the Houmao Execution Adapter, dispatches bounded scouting and synthesis-review handoffs, and normalizes their outputs.
- Add host-facing recording paths for the minimal UC-01 research records: seed-source summaries, literature notes, claim candidates, Evidence Items, review notes, inquiry options, follow-up Gate, selected Research Inquiry, Decision Record, and Provenance Records.
- Add or extend Workspace Runtime persistence and validation for Artifact, Evidence Item, Finding or claim-candidate, Gate, Decision Record, View Manifest, and Provenance refs needed by the UC-01 path.
- Add a CLI or manual-test runner that executes the UC-01 path with root-level `--print-json`, supports adapter-simulated mode for deterministic tests, and can be live-gated for real Houmao.
- Add minimal View Manifest records for literature matrix, claim graph, and inquiry comparison as durable CLI-readable records without requiring a GUI renderer.
- Keep Houmao-specific refs inside adapter payloads, manifests, or adapter tables; generic UC-01 records should use Isomer domain terms.

## Capabilities

### New Capabilities

- `uc01-headless-vertical-slice`: Defines the end-to-end UC-01 acceptance workflow, fixture shape, required durable records, simulated/live adapter modes, and completion criteria for the headless vertical slice.

### Modified Capabilities

- `research-lifecycle-state`: Add UC-01 lifecycle expectations for Research Inquiry creation, Research Task routing, Run closeout, follow-up inquiry selection, Gate resolution, and Decision Record linkage.
- `research-recording-contracts`: Add minimal recording requirements for UC-01 Artifacts, Evidence Items, Findings or claim candidates, Decision Records, Gates, View Manifest refs, and Provenance Records.
- `workspace-runtime-persistence`: Persist and validate the runtime-visible research records needed by UC-01 and include them in Agent Team Instance and runtime inspection summaries.
- `isomer-cli-project-discovery`: Expose the UC-01 headless runner or manual validation surface through the modular CLI/test command shape with root-level `--print-json` output.
- `houmao-cli-adapter-layer`: Require UC-01 to use the Houmao adapter boundary and live-gated or simulated execution without leaking Houmao native fields into generic research records.

## Impact

- Affected code: `src/isomer_labs/runtime/`, `src/isomer_labs/cli/`, `src/isomer_labs/houmao/`, fixture setup under `tests/fixtures/`, and manual or integration tests under `tests/manual/` or `tests/integration/`.
- Affected docs: README or workflow docs for running the UC-01 headless path, troubleshooting for incomplete Gates or missing research records, and ROADMAP Milestone 6 checklist updates after validation.
- Affected runtime: Workspace Runtime schema and validation may add or expose minimal durable research-record tables or lifecycle records for Artifacts, Evidence Items, Findings, Decision Records, Gates, View Manifests, and Provenance Records.
- Dependencies: Milestone 6 assumes the Milestone 5 Houmao Execution Adapter launch, handoff dispatch, Signal Observation, and normalization foundation is available or applied before implementation.
