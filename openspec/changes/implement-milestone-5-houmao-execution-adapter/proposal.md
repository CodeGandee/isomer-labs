## Why

Milestone 4 can create and validate pre-launch Agent Team Instance records, but Isomer still cannot start, inspect, stop, or normalize real `deepsci-org` work through the local Houmao build. Milestone 5 closes that gap by adding the first Execution Adapter slice while keeping Houmao launch details inside adapter-specific records rather than promoting them into core Isomer schema or UI language.

## What Changes

- Add a Houmao Execution Adapter implementation plan that maps an Isomer Domain Agent Team Template, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Agent Workspace, Run, handoff, and Artifact refs onto local Houmao launch, mailbox, gateway, notifier, inspection, and stop surfaces.
- Add explicit launch, inspect, stop, and manual handoff flows for one manual-mode `deepsci-org` Agent Team Instance created from an existing Topic Agent Team Profile and Workspace Runtime.
- Materialize Houmao launch material from `teams/deepsci-org/execplan/agents/`, generated skills, notifier prompts, topology, and communication templates under adapter-owned Topic Workspace paths.
- Persist adapter refs, launch material refs, inspection snapshots, Signal Observations, handoff normalization records, Run refs, and Provenance refs in Workspace Runtime without storing Houmao terms as generic Agent Team Instance fields.
- Use `extern/orphan/houmao` as the local Houmao source and build target, and document that defects discovered in Houmao must be fixed and validated in the Houmao checkout as separate local work before Isomer depends on them.
- Add CLI and API surfaces for launch, inspect, stop, and one manual handoff round, plus tests that prove no launch can happen without readiness, runtime state, a valid Topic Agent Team Profile, and adapter preflight.

## Capabilities

### New Capabilities
- `houmao-execution-adapter`: Adapter-specific launch, inspection, stop, mailbox or gateway observation, launch-material generation, local Houmao build boundary, and adapter ref recording for Houmao-backed Agent Team Instances.

### Modified Capabilities
- `isomer-cli-project-discovery`: Add Milestone 5 launch, inspect, stop, and handoff command-surface contracts while preserving deterministic JSON and read-only command boundaries.
- `research-execution-extension-contract`: Add concrete `agent_launch`, `agent_inspect`, `agent_stop`, and manual handoff dispatch behavior through Execution Adapter Command Requests and adapter preflight.
- `workspace-runtime-persistence`: Extend Workspace Runtime records to store opaque Execution Adapter refs, launch material refs, inspection snapshots, Signal Observations, Run linkage, and Houmao-backed launch status without making Houmao fields generic runtime schema.
- `research-lifecycle-state`: Add lifecycle transition expectations for launched, inspected, stopped, failed, stale, and normalized handoff states for Agent Team Instances, Agent Instances, Runs, and handoffs.
- `research-recording-contracts`: Add recording obligations for launch Provenance Records, adapter inspection Artifacts or snapshots, Signal Observations, handoff result normalization, and corrective records for adapter failures.
- `workspace-path-resolution`: Add adapter launch-material path-plan requirements so generated Houmao launch files, notifier prompts, mailbox metadata, gateway metadata, and adapter logs are materialized under recorded Topic Workspace or Agent Workspace paths.

## Impact

- Adds runtime adapter modules under `src/isomer_labs/` and CLI wiring for Houmao-backed Agent Team Instance launch, inspection, stop, and manual handoff operations.
- Depends on the ignored local Houmao checkout at `extern/orphan/houmao` and its own validation commands; Isomer tests should skip or clearly report adapter-live checks when the local Houmao build is unavailable.
- Updates Workspace Runtime persistence and validation to include opaque adapter refs, launch-material path plans, launch status, Signal Observations, and adapter Provenance refs.
- Adds unit and integration coverage for one manual-mode `deepsci-org` launch path, stop/recovery behavior, and the repository-boundary rule for Houmao fixes.
