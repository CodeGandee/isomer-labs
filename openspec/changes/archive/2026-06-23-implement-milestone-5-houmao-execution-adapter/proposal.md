## Why

Recent Houmao adapter work already added the modular CLI-backed adapter foundation, launch material preparation, quick launch, inspect-live, stop, manifest reconciliation, adoption, and the root-level `--print-json` output switch. The remaining Milestone 5 gap is narrower: Isomer still needs a public handoff/control layer that can dispatch one manual Houmao-backed handoff, observe candidate results as Signal Observations, and normalize accepted or rejected results back into Workspace Runtime without treating Houmao signals as authoritative research completion.

This revision keeps the recent module boundaries and avoids reintroducing compatibility shims or duplicate launch requirements. Milestone 5 now builds on the current `isomer_labs.houmao`, `isomer_labs.runtime`, and modular `isomer_labs.cli.commands` packages.

## What Changes

- Add a focused Houmao Execution Adapter extension for manual handoff dispatch, adapter observation, and Operator Agent normalization on top of the existing CLI-backed launch/inspect/stop adapter layer.
- Add a top-level `isomer-cli handoffs` command group with `dispatch`, `observe`, and `normalize` subcommands that use structured human-readable output by default and root-level `isomer-cli --print-json ...` for deterministic JSON.
- Persist handoff dispatch records, Signal Observations, normalization outcomes, Run refs, Artifact refs, adapter payload refs, and Provenance refs in Workspace Runtime while keeping Houmao terms inside adapter-scoped payloads or records.
- Audit the existing `team-instances launch`, `launch-material prepare`, `inspect-live`, `stop`, `reconcile`, and `adopt` implementation against the current main specs instead of rebuilding those surfaces in this change.
- Keep `extern/orphan/houmao` as the ignored local Houmao source and live-test boundary; defects discovered in Houmao remain separate Houmao repository work validated with Houmao commands before Isomer depends on them.
- Add mocked unit coverage and live-gated integration or manual validation for one manual-mode `deepsci-org` handoff round after a Houmao-backed Agent Team Instance has been launched or adopted.

## Capabilities

### New Capabilities
- `houmao-execution-adapter`: Follow-on Milestone 5 handoff/control extension for Houmao-backed Agent Team Instances, covering manual dispatch, Signal Observation ingestion, normalization, live-gated validation, and compatibility with the existing CLI-backed adapter layer.

### Modified Capabilities
- `isomer-cli-project-discovery`: Add the top-level `handoffs` CLI command surface and root-level `--print-json` contracts for handoff dispatch, observation, and normalization while preserving existing read-only and mutation boundaries.
- `research-execution-extension-contract`: Add concrete manual handoff dispatch behavior through provider-neutral Execution Adapter Command Requests and adapter preflight, with adapter observations treated as non-authoritative signals.
- `workspace-runtime-persistence`: Extend Workspace Runtime records for handoff dispatch, Signal Observation refs, normalization outcomes, and adapter-linked Provenance without adding Houmao-specific generic fields.
- `research-lifecycle-state`: Add lifecycle transition expectations for manual handoff dispatch, observing, candidate completion, accepted completion, rejection, repair, and stale states.
- `research-recording-contracts`: Add recording obligations for Signal Observations, handoff result normalization, output Artifact refs, corrective Service Request refs, and Provenance Records.
- `workspace-path-resolution`: Add adapter observation, mailbox/gateway snapshot, handoff payload, normalization artifact, and log path-plan requirements under recorded Topic Workspace or Agent Workspace paths.

## Impact

- Adds or updates modular code under `src/isomer_labs/cli/commands/`, `src/isomer_labs/houmao/`, and `src/isomer_labs/runtime/` without restoring removed shim modules.
- Depends on the existing Houmao adapter launch/inspect/stop foundation and verifies that those surfaces still satisfy current main specs before adding handoff behavior.
- Adds Workspace Runtime persistence and validation for handoff dispatch, Signal Observations, normalization outcomes, and adapter-linked Provenance refs.
- Adds unit and live-gated coverage for one manual-mode `deepsci-org` handoff round, including skipped or unavailable status when the local Houmao checkout is absent.
