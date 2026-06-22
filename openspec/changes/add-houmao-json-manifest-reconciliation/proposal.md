## Why

Milestone 5 gives Isomer a Houmao launch path, but users also need to operate Houmao directly through `houmao-mgr` without making Isomer blind to the resulting Agent Team Instance state. This change adds a durable JSON manifest and reconciliation contract so Isomer can understand, adopt, validate, and report Houmao-backed runtime state whether the launch started through Isomer quick launch or direct Houmao operation.

## What Changes

- Add adapter-scoped JSON manifests for Houmao-backed Agent Team Instance correlation, launch-material inventory, and observed runtime state.
- Define a reconciliation flow that reads Houmao runtime/project state, compares it with JSON manifests and Workspace Runtime records, then reports or records linked, adopted, drifted, conflicted, stale, or rejected outcomes.
- Keep Isomer quick launch supported by writing JSON manifests before and after `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <generated-profile>`.
- Support direct Houmao operation by allowing users to create or export a link manifest, edit Houmao project-profile material manually, launch with `houmao-mgr`, and then run an explicit Isomer reconcile or adopt command.
- Use JSON as the durable manifest format and the deterministic CLI/API interchange format, while keeping persisted manifests separate from command output payloads.
- Compute integrity from parsed canonical JSON plus raw referenced-file digests so whitespace and object field ordering do not create false drift.
- Preserve Houmao implementation details inside adapter manifests, adapter payload refs, and diagnostics rather than adding Houmao-specific fields to generic Isomer records.

## Capabilities

### New Capabilities
- `houmao-manifest-reconciliation`: Adapter-specific JSON manifest format, reconciliation states, direct-Houmao adoption, drift detection, and quick-launch manifest updates for Houmao-backed Agent Team Instances.

### Modified Capabilities
- `workspace-runtime-persistence`: Persist opaque refs to JSON adapter manifests, reconciliation records, manifest digest state, and adoption outcomes without promoting Houmao fields into generic runtime schema.
- `workspace-path-resolution`: Resolve durable JSON manifest paths and referenced launch-material paths under recorded Topic Workspace or Agent Workspace path plans, with explicit handling for referenced Houmao project overlay paths.
- `isomer-cli-project-discovery`: Add deterministic CLI contracts for exporting adapter links, reconciling direct Houmao state, adopting externally launched Houmao-backed Agent Team Instances, and inspecting integrity status.
- `research-execution-extension-contract`: Add provider-neutral command request behavior for adapter reconciliation and adoption alongside launch, inspect, and stop operations.
- `research-lifecycle-state`: Add lifecycle interpretation for linked, externally detected, adopted, drifted, conflicted, and stale Houmao-backed Agent Team Instance states.
- `research-recording-contracts`: Add Provenance Record, Artifact, and diagnostic obligations for manifest creation, reconciliation, direct adoption, drift decisions, and conflict outcomes.

## Impact

- Adds JSON parsing, rendering, canonicalization, and digest helpers for Houmao adapter manifests under `src/isomer_labs/`.
- Extends Houmao adapter launch, inspect, and recovery flows to write and read durable manifest refs.
- Adds CLI/API surfaces for adapter-link export, reconcile, adopt, and integrity inspection while keeping existing read-only inspection commands mutation-free unless the command explicitly records reconciliation.
- Adds unit tests for JSON round trip, canonical digest stability, raw launch-material digest detection, reconciliation state classification, CLI JSON output, and Workspace Runtime opaque-ref persistence.
- Adds live-gated or manual checks that compare Isomer quick launch with direct `houmao-mgr` launch followed by Isomer reconciliation.
