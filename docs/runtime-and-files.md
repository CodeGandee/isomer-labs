# Runtime and Files

This page describes durable runtime files, generated adapter files, manifests, payload refs, and the boundary between durable records and cache. It covers Project files, Topic Workspace files, Workspace Runtime records, path plans, Agent Workspaces, adapter material, manifests, and command payloads.

## Project Files

A Project is a user-owned directory tree. After `isomer-cli init`, the Project Config Directory `.isomer-labs/` contains:

- `manifest.toml` — the Project Manifest, the discovery authority for Research Topics, Topic Workspaces, and Pixi environment bindings.
- `research-topics/<topic-id>.toml` — Research Topic Config files with topic defaults and refs.
- `team-profiles/<profile-id>.toml` — optional Topic Agent Team Profile definitions.
- `team-instances/<instance-id>.toml` — optional Agent Team Instance refs or configuration.
- `local.toml` — optional untracked user-local active context.

The Project Config Directory should not contain default cache, temporary files, or schema directories. System-owned schemas are Isomer built-in artifacts queried through `isomer-cli schemas list`.

## Topic Workspace Files

A Topic Workspace is a project-local directory declared by the Project Manifest, usually under `topic-workspaces/<topic-workspace-id>/`. It owns:

- `state.sqlite` — the Workspace Runtime database.
- `artifacts/` — workspace-level research Artifacts.
- `agents/` — Agent Workspace directories, one per Agent Instance.
- `tasks/` — Research Task records and supporting files.
- `runs/` — Run records and supporting files.
- `views/` — generated View Manifests and GUI view material.
- `logs/` — workspace-level logs.
- `runtime/adapters/houmao/<agent-team-instance-id>/` — Houmao adapter-generated manifests, launch material, command payloads, snapshots, stop outcomes, handoff payloads, Signal Observation payloads, and normalization payloads.

The path plan for each surface is recorded in Workspace Runtime so that commands can resolve paths consistently.

## Workspace Runtime Records

Workspace Runtime stores records in `state.sqlite`. Major record kinds include:

- `WorkspaceRuntimeMetadata` — schema version, Project root, Project Manifest path, Research Topic id, Topic Workspace id, Topic Workspace path, timestamps, and provenance refs.
- `PathPlanRecord` — id, Topic Workspace id, surface, path, source, source detail, and created timestamp.
- `TopicEnvironmentReadinessRecord` — readiness status, project Pixi environment refs, standalone Pixi manifest refs, diagnostics, checked timestamp, actor ref, and optional repair Service Request hint.
- `AgentTeamInstanceRecord` — id, Research Topic id, Topic Workspace id, Topic Agent Team Profile id, Domain Agent Team Template id, status, agent instance ids, agent workspace ids, run ids, workflow stage cursor ids, blocker refs, handoff ids, and provenance refs.
- `AgentInstanceRecord` — id, Agent Team Instance id, Agent Role id, Research Topic id, Topic Workspace id, Agent Profile ref, status, and provenance refs.
- `AgentWorkspaceRecord` — id, Agent Instance id, Topic Workspace id, Path Plan id, status, and provenance refs.
- `RuntimeLifecycleRecord` — generic lifecycle records for Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Topic Workspace, Topic Agent Team Profile, Artifact, Gate, Research Claim, Evidence Item, Decision Record, and Provenance Record.
- `HandoffRecord` — source actor, target actor, status, Research Task id, Run id, Agent Team Instance id, Completion Watcher Contract refs, expected output refs, staleness rules, and provenance refs.
- `ValidationIssueRecord` — severity, code, concept, message, record ref, and provenance refs.
- `AdapterManifestRefRecord` — manifest kind, manifest path, manifest digest, source, path plan id, and agent instance ids.
- `AdapterReconciliationRecord` — reconciliation state, mapping confidence, manifest digest summary, live observation summary, diagnostics, and actor ref.
- `AdapterPayloadRefRecord` — payload kind, payload path, payload digest, source, agent instance id, command run id, and path plan id.
- `AdapterCommandRunRecord` — operation kind, argv, cwd, env hints, status, returncode, timestamps, duration, payload refs, diagnostics, and actor ref.
- `AdapterMaterializationRecord` — materialization status, material ref ids, manifest ref ids, path plan ids, diagnostics, and actor ref.
- `AdapterLaunchAttemptRecord` — launch attempt status, agent instance ids, command run ids, manifest ref ids, payload ref ids, adapter refs, diagnostics, and timestamps.
- `AdapterInspectionSnapshotRecord` — inspection status, command run ids, manifest ref ids, snapshot payload ref id, live observation summary, diagnostics, and actor ref.
- `AdapterStopOutcomeRecord` — stop outcome status, target agent instance ids, command run ids, payload ref ids, remaining live refs, diagnostics, and actor ref.
- `AdapterHandoffDispatchRecord` — handoff dispatch status, source and target Agent Instance ids, Run and Research Task refs, command run ids, payload refs, expected output refs, Completion Watcher Contract refs, diagnostics, and provenance refs.
- `SignalObservationRecord` — non-authoritative adapter observation status, observation kind, summary, command run ids, payload refs, source and target Agent Instance ids, Run ref, diagnostics, and provenance refs.
- `HandoffNormalizationRecord` — Operator Agent normalization status, rationale, Signal Observation ids, output Artifact refs, corrective refs, payload refs, diagnostics, and provenance refs.

## Path Plans

Path Plan records map a named surface to a concrete filesystem path. Surfaces include `workspace_runtime_db`, `artifacts`, `agents`, `tasks`, `runs`, `views`, `logs`, and adapter-specific surfaces such as `adapter_manifest:houmao:<agent-team-instance-id>:<kind>`.

Commands use Path Plan records to locate durable files without recomputing layout from configuration. `isomer-cli paths preview` prints the path plan without creating files.

## Agent Workspaces

Agent Workspaces live under `<topic-workspace>/agents/<agent-instance-id>/`. Each Agent Workspace belongs to one globally unique Agent Instance. The directory contains:

- owned scratch files and local runtime state;
- Agent Artifacts produced or curated by the agent;
- local logs and recovery files;
- a Workspace Boundary declaration (README or manifest) documenting write ownership and Peer Read Access rules.

Agent Workspace boundaries are advisory. Isomer records expected access, but it does not provide filesystem-grade access control. Agents with system tools may still modify files outside their declared boundaries.

## Adapter Material and Manifests

The Houmao Execution Adapter generates material under `<topic-workspace>/runtime/adapters/houmao/<agent-team-instance-id>/`:

- `adapter-link.json` — durable link manifest that binds the Agent Team Instance to Houmao launch context, including project refs, agent bindings, and the Houmao project overlay directory.
- `launch-material-manifest.json` — manifest of generated launch material files, their digests, editable policy, and agent instance mapping.
- `adapter-runtime-manifest.json` — runtime reconciliation state, agent bindings, live observation summary, and diagnostics.
- `command-payloads/` — JSON payloads for Houmao CLI invocations. Payloads may be redacted to avoid emitting secret-like fields.
- `logs/` — adapter command logs.
- `inspection-snapshots/` — bounded read-only inspection snapshots.
- `stop-outcomes/` — records of stop command results.
- `handoff-payloads/` — dispatch payloads written by Isomer before invoking Houmao mail or gateway surfaces.
- `handoff-observations/` — Signal Observation payloads collected from mail, gateway, file, or inspection sources.
- `handoff-normalizations/` — Operator Agent normalization payloads for accepted, rejected, blocked, superseded, repair-routed, or follow-up outcomes.
- `houmao-project-overlay/` — generated Houmao project overlay directory.

These files are durable runtime records unless a later accepted contract explicitly classifies a file as disposable. Do not treat them as temporary cache.

## Payload Refs

Adapter command payloads are stored as files and referenced by `AdapterPayloadRefRecord` in Workspace Runtime. Each payload ref records the payload kind, filesystem path, digest, source, and optional command run id. This lets the system correlate a Houmao CLI invocation with the exact JSON that was sent, without storing live process state in the payload.

Payloads are redacted before storage if they contain secret-like fields such as `api_key`, `secret`, `token`, or `password`.

## Durable Versus Cache Classification

The following are durable records:

- Project Manifest and Research Topic Config files.
- Workspace Runtime `state.sqlite` and its records.
- Path Plan records.
- Agent Team Instance, Agent Instance, and Agent Workspace records.
- Topic Environment Readiness records.
- Adapter manifests (`adapter-link.json`, `launch-material-manifest.json`, `adapter-runtime-manifest.json`).
- Adapter command payloads, command run records, materialization records, launch attempt records, inspection snapshots, stop outcome records, handoff dispatch records, Signal Observation records, and handoff normalization records.
- Workspace-level Artifacts, Agent Artifacts, Decision Records, Provenance Records, and Evidence Items.

The following are not durable research state and may be regenerated or lost:

- GUI Runtime State in the GUI Backend.
- AG-UI Event Batch payload content unless the user explicitly enables retention.
- Process-local Effective Topic Context.
- Uncommitted scratch files inside Agent Workspaces that have not been recorded as Artifacts or Provenance Records.

## Summary

| Surface | Typical path | Durable? |
|---|---|---|
| Project Manifest | `.isomer-labs/manifest.toml` | yes |
| Research Topic Config | `.isomer-labs/research-topics/<id>.toml` | yes |
| Topic Workspace | `topic-workspaces/<id>/` | yes (directory) |
| Workspace Runtime DB | `<topic-workspace>/state.sqlite` | yes |
| Runtime directories | `<topic-workspace>/{artifacts,agents,tasks,runs,views,logs}/` | yes |
| Agent Workspace | `<topic-workspace>/agents/<agent-instance-id>/` | yes |
| Adapter root | `<topic-workspace>/runtime/adapters/houmao/<ati-id>/` | yes |
| Adapter manifests | `<adapter-root>/{adapter-link,launch-material-manifest,adapter-runtime-manifest}.json` | yes |
| Command payloads | `<adapter-root>/command-payloads/` | yes |
| GUI Runtime State | in-memory / GUI Backend | no |
