## Why
The manifest reconciliation work leaves quick-launch completion blocked because Isomer Labs does not yet have a concrete Houmao adapter layer that can materialize launch material, invoke Houmao, and feed observed runtime state back into Workspace Runtime. Houmao’s supported surface is currently CLI-first: its project, profile, specialist, agent, mailbox, and gateway operations are Click commands with `--print-json` output and runtime setup behavior that is not available through a stable Python SDK. Isomer should therefore integrate live Houmao lifecycle work through the public `houmao-mgr --print-json` boundary instead of importing Houmao internals.

This change narrows Milestone 5 to the missing adapter layer. It gives users both launch paths Isomer needs to support: a quick Isomer command for the common case, and a prepare-only/manual path where users can inspect or edit Houmao launch material and then run `houmao-mgr` directly. Both paths must leave enough JSON runtime manifest state for Isomer to reconcile what happened later.

## What Changes
- Add a CLI-backed Houmao Execution Adapter facade that resolves the local Houmao checkout or configured Houmao command, runs capability/preflight checks, invokes `houmao-mgr --print-json`, parses structured output, and records command payload references without requiring `import houmao`.
- Add shared launch material generation for quick launch and prepare-only workflows, including deterministic Houmao project material, per-Agent Instance launch inputs, `adapter-link.json`, and `launch-material-manifest.json`.
- Add quick launch orchestration that launches one Houmao managed-agent per Isomer Agent Instance, records command attempts and adapter refs, writes `adapter-runtime-manifest.json`, and drives manifest reconciliation to the `launched_by_isomer` path.
- Add a direct/manual lane that writes launch material and manifests without starting Houmao agents, so users can inspect, edit, or launch with `houmao-mgr` and later reconcile the resulting live state through Isomer.
- Add live inspect and stop adapter operations that call Houmao CLI JSON commands, preserve opaque Houmao refs in Workspace Runtime, and keep mutation boundaries explicit.
- Add focused unit and integration tests for command-runner behavior, no-runtime-Houmao-import guarantees, materialization, quick launch, partial launch recovery, manual adoption, inspection, stop, and path persistence.

## Capabilities
### New Capabilities
- `houmao-cli-adapter-layer`: CLI-backed Houmao adapter facade, command runner, shared launch materialization, quick launch, prepare-only/manual launch material, live inspect, stop, and manifest reconciliation hooks.

### Modified Capabilities
- `isomer-cli-project-discovery`: expose and document the adapter-backed `team-instances` launch, prepare-only, inspect-live, and stop command contracts with deterministic JSON output and clear mutation boundaries.
- `workspace-runtime-persistence`: persist adapter command runs, launch attempts, inspection snapshots, stop outcomes, payload references, and manifest links as Workspace Runtime records tied to Agent Team Instances and Agent Instances.
- `workspace-path-resolution`: define durable path plans for Houmao adapter material, command payloads, logs, and per-agent launch material inside the Topic Workspace runtime area.
- `research-execution-extension-contract`: require the Houmao Execution Adapter to use Houmao’s public CLI JSON boundary for live lifecycle work unless Houmao later exposes an accepted stable SDK.

## Impact
This change completes the missing adapter layer needed by the JSON manifest reconciliation change and de-risks the broader Milestone 5 execution adapter plan. It keeps Houmao terms behind adapter records and CLI internals, while allowing Isomer’s domain commands to quick-launch teams, prepare editable Houmao materials, inspect live state, stop managed agents, and reconcile direct Houmao activity. The main implementation risk is partial launch failure: the adapter must record every attempted command and preserve enough per-agent state for follow-up inspect, stop, or adoption commands to recover cleanly.
