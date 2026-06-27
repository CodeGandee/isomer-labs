# Runtime and Files

This page describes durable runtime files, generated adapter files, manifests, payload refs, and the boundary between durable records and cache. The canonical Topic Workspace and Agent Workspace directory structure lives in [Topic Workspace Definition](topic-workspace-definition.md).

## Project Files

A Project is a user-owned directory tree. After `isomer-cli project init`, the Project Config Directory `.isomer-labs/` contains Project bootstrap state; after explicit topic creation it also contains Research Topic registrations and config files. Common entries include:

- `manifest.toml` — the Project Manifest, the discovery authority for Research Topics, Topic Workspaces, Topic Workspace Pixi workspace bindings through `topic_standalone_pixi_bindings`, optional Project-root Pixi environment bindings through `topic_pixi_environment_bindings`, Domain Agent Team Template refs, the single Topic Agent Team Profile Bundle ref for each Research Topic, and project defaults.
- `research-topics/<topic-id>.toml` — Research Topic Config files with topic defaults and refs. Research Topic Config files do not own Pixi environment bindings or Workspace Runtime state.
- `domain-agent-team-templates/` — optional project-local Domain Agent Team Template material referenced by the Project Manifest. Built-in templates do not need a local directory.
- `team-instances/<instance-id>.toml` — optional Agent Team Instance refs or configuration.
- `local.toml` — optional untracked user-local active context.

The Project Config Directory should not contain default cache, temporary files, generated topic bodies, or schema directories. System-owned schemas are Isomer built-in artifacts queried through `isomer-cli schemas list`.

Successful Project initialization also creates the Isomer-managed Houmao overlay at `.isomer-labs/.houmao/` and the selected generated content root, which defaults to `isomer-content/` and can be set during initialization with `--content-dir <content-dir>`. The content root contains `README.md` and `.gitignore` policy files; its generated `.gitignore` ignores generated content by default while keeping those two policy files trackable. The Houmao overlay belongs to Project bootstrap and is separate from per-Agent Team Instance adapter material under a Topic Workspace runtime path.

## Topic Workspace Structure Reference

A Topic Workspace is a project-local directory declared by the Project Manifest, usually under `isomer-content/topic-ws/<topic-workspace-id>/` for fresh Projects or `<content-dir>/topic-ws/<topic-workspace-id>/` when init selected a custom content root. It is a Pixi workspace by default, and its structure is standardized in [Topic Workspace Definition](topic-workspace-definition.md).

Runtime-facing pages should refer to Topic Workspace surfaces by semantic name, such as Workspace Runtime database, Topic Agent Team Profile Bundle, Topic Main Repository, Agent Workspace root, owner-preserved Run record directory, or adapter material root. Commands should record path plans for durable surfaces before downstream work depends on them.

## Workspace Runtime Records

Workspace Runtime stores records in `state.sqlite`. Major record kinds include:

- `WorkspaceRuntimeMetadata` — schema version, Project root, Project Manifest path, Research Topic id, Topic Workspace id, Topic Workspace path, timestamps, and provenance refs.
- `PathPlanRecord` — id, Topic Workspace id, surface, path, source, source detail, and created timestamp.
- `TopicEnvironmentReadinessRecord` — readiness status, Topic Workspace Pixi manifest refs, selected Pixi environment refs, optional Project-root Pixi environment refs for platform or shared tooling use, diagnostics, checked timestamp, actor ref, and optional repair Service Request hint.
- `AgentTeamInstanceRecord` — id, Research Topic id, Topic Workspace id, Topic Agent Team Profile ref, Domain Agent Team Template id, status, agent instance ids, agent workspace ids, run ids, workflow stage cursor ids, blocker refs, handoff ids, and provenance refs.
- `AgentInstanceRecord` — id, Agent Team Instance id, Agent Role id, Research Topic id, Topic Workspace id, Agent Profile ref, status, and provenance refs.
- `AgentWorkspaceRecord` — id, globally unique Agent Instance id, topic-local Agent Name when known, Topic Workspace id, flat Agent Workspace Path Plan id, `isomer-managed/` path plan id, expected repository ref, branch namespace, current branch when known, boundary refs, generated-link summary, status, and provenance refs.
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

Path Plan records map a named surface to a concrete filesystem path. Surfaces include `isomer_content_root`, `topic_workspace_base`, `workspace_runtime_db`, `repos`, `topic_main_repo`, `topic_main_isomer_managed`, `topic_main_tracked`, `topic_main_tracked_shared`, `topic_main_tracked_artifacts`, `topic_main_tracked_tasks`, `topic_main_tracked_runs`, `topic_main_tracked_views`, `topic_main_tracked_tools`, `topic_main_tracked_boundaries`, `topic_main_tracked_manifests`, `agents`, `records`, `records_artifacts`, `records_tasks`, `records_runs`, `records_views`, `records_logs`, `runtime`, per-agent surfaces such as `agent_workspace:<agent-name>` and `agent_isomer_managed:<agent-name>`, agent support surfaces such as `agent_owned`, `agent_runtime`, `agent_artifacts`, `agent_scratch`, `agent_logs`, `agent_public_share`, `agent_inbox`, `agent_topic_readonly`, `agent_topic_writable`, and `agent_links`, and adapter-specific surfaces such as `adapter_manifest:houmao:<agent-team-instance-id>:<kind>`. Legacy `artifacts`, `tasks`, `runs`, `views`, and `logs` surface names should be treated as compatibility aliases for owner-preserved `records/*` surfaces rather than worker-visible root directories.

Commands use Path Plan records to locate durable files without recomputing layout from configuration. `isomer-cli project paths preview` prints the path plan without creating files.

## Agent Workspaces

Agent Workspace structure, agent-owned Git worktrees, per-agent branch namespaces, launch cwd behavior, `isomer-managed/` tracked material, agent-owned untracked material, topic-owned projections, generated links, topic-owned Pixi task channels, environment inheritance, and Workspace Boundary meanings are standardized in [Topic Workspace Definition](topic-workspace-definition.md). Runtime records should create Agent Workspace path plans under `<topic-workspace>/agents/<agent-name>` and `isomer-managed/` support path plans under `<topic-workspace>/agents/<agent-name>/isomer-managed/` while preserving Agent Instance ids and adapter refs as runtime records.

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
- Project-level Houmao overlay at `.isomer-labs/.houmao/`.
- Topic Workspace Pixi manifests and lockfiles.
- Topic Agent Team Profile Bundles under `<topic-workspace>/team-profile/`.
- Workspace Runtime `state.sqlite` and its records.
- Path Plan records.
- Agent Team Instance, Agent Instance, and Agent Workspace records.
- Topic Environment Readiness records.
- Adapter manifests (`adapter-link.json`, `launch-material-manifest.json`, `adapter-runtime-manifest.json`).
- Adapter command payloads, command run records, materialization records, launch attempt records, inspection snapshots, stop outcome records, handoff dispatch records, Signal Observation records, and handoff normalization records.
- Owner-preserved records under `records/*`, Workspace-level Artifacts, Agent Artifacts, Decision Records, Provenance Records, and Evidence Items.

The following are not durable research state and may be regenerated or lost:

- GUI Runtime State in the GUI Backend.
- AG-UI Event Batch payload content unless the user explicitly enables retention.
- Process-local Effective Topic Context.
- Topic Workspace `.pixi/` environment directories.
- Uncommitted scratch files inside Agent Workspaces that have not been recorded as Artifacts or Provenance Records.
- Untracked `isomer-managed/agent-owned/`, `isomer-managed/topic-owned/`, and `isomer-managed/links/` material unless an Artifact locator, path plan, or Provenance Record explicitly promotes it to durable state.

## Summary

| Surface | Typical path | Durable? |
|---|---|---|
| Project Manifest | `.isomer-labs/manifest.toml` | yes |
| Project-level Houmao overlay | `.isomer-labs/.houmao/` | yes |
| Research Topic Config | `.isomer-labs/research-topics/<id>.toml` | yes |
| Generated content root | `isomer-content/` or selected `<content-dir>/` | yes for policy files; generated contents ignored by default |
| Topic Workspace | `isomer-content/topic-ws/<id>/` or `<content-dir>/topic-ws/<id>/` | yes (directory) |
| Topic Workspace Pixi manifest | `<topic-workspace>/pixi.toml` or `<topic-workspace>/pyproject.toml` | yes |
| Topic Workspace Pixi lockfile | `<topic-workspace>/pixi.lock` | yes |
| Topic Workspace Pixi environment | `<topic-workspace>/.pixi/` | no |
| Topic Agent Team Profile Bundle | `<topic-workspace>/team-profile/` | yes |
| Topic Main Repository | `<topic-workspace>/repos/topic-main/` | policy-dependent topic support surface |
| Topic Main Isomer-managed namespace | `<topic-workspace>/repos/topic-main/isomer-managed/` | yes for path plan; tracked subpaths are Git policy surfaces |
| Isomer-managed tracked material | `<topic-workspace>/repos/topic-main/isomer-managed/tracked/` | yes when committed or recorded |
| Workspace Runtime DB | `<topic-workspace>/state.sqlite` | yes |
| Owner-preserved records | `<topic-workspace>/records/{artifacts,tasks,runs,views,logs}/` | yes |
| Runtime support root | `<topic-workspace>/runtime/` | yes |
| Agent Workspace | `<topic-workspace>/agents/<agent-name>/` | yes after runtime path-plan creation |
| Agent Workspace worktree | `<topic-workspace>/agents/<agent-name>/` as a worktree of `repos/topic-main` on `per-agent/<agent-name>/...` | policy-dependent Git state plus durable runtime path plan |
| Agent Isomer-managed namespace | `<topic-workspace>/agents/<agent-name>/isomer-managed/` | yes for path plan; untracked subpaths require promotion for durable research dependency |
| Agent-owned public share | `<topic-workspace>/agents/<agent-name>/isomer-managed/agent-owned/public/` | no unless promoted or recorded |
| Topic-owned projection | `<topic-workspace>/agents/<agent-name>/isomer-managed/topic-owned/{readonly,writable}/` | no unless promoted or recorded |
| Generated links | `<topic-workspace>/agents/<agent-name>/isomer-managed/links/` | no, advisory |
| Adapter root | `<topic-workspace>/runtime/adapters/houmao/<ati-id>/` | yes |
| Adapter manifests | `<adapter-root>/{adapter-link,launch-material-manifest,adapter-runtime-manifest}.json` | yes |
| Command payloads | `<adapter-root>/command-payloads/` | yes |
| GUI Runtime State | in-memory / GUI Backend | no |
