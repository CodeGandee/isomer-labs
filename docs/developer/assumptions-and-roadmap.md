# Assumptions and Roadmap

This developer page documents the assumptions Isomer Labs currently makes, the non-goals that shape its scope, the advisory nature of workspace boundaries, and the status of current milestones versus future work. Reading this page helps you avoid inferring guarantees that the system does not yet provide.

## Implementation Assumptions

### Filesystem and workspace boundaries are advisory

Agent Workspace, Workspace Boundary, Peer Read Access, the `isomer-managed/` owner/reader split, and generated-link semantics declare intended write ownership and read access rules, but they do not provide filesystem-grade isolation. An agent with system tools may still inspect or modify files outside its declared boundary. Durable cross-agent dependencies should be recorded through handoffs, promoted Artifacts, Evidence Items, or Provenance Records rather than relying on boundary enforcement.

### Topic-to-environment bindings do not come from names

Isomer never infers a Research Topic's Pixi environment from its id, name, or naming convention. Project-root Pixi environment bindings must appear as repeated `topic_pixi_environment_bindings` entries in the Project Manifest. Topic Workspace Pixi bindings may appear as repeated `topic_standalone_pixi_bindings` entries with `manifest_path_or_dir`, and when no explicit standalone binding exists, commands use the registered Topic Workspace directory as the default target and ask Pixi to resolve it.

### Repair is explicit

When `isomer-cli doctor`, `project runtime prepare`, or `project runtime validate` reports a missing dependency, failed readiness check, or environment mismatch, the repair should be explicit. Represent setup or compatibility work as a Service Request rather than hiding it inside a read-only diagnostic command or a runtime preparation step.

### Houmao is an adapter-specific backend

Houmao is the current Execution Adapter backend. Isomer invokes Houmao through the public `houmao-mgr --print-json` CLI and records adapter state in Workspace Runtime. Houmao concepts such as specialist, project profile, native role, recipe, launch dossier, and managed-agent id are adapter-specific unless accepted domain language explicitly promotes a term.

### CLI-first operation

The current implementation exposes behavior primarily through `isomer-cli`. The GUI Backend exists in the domain model and may be started through `isomer-cli`, but the documented workflows in this milestone are CLI-first.

### Durable records live in the Project tree

Workspace Runtime, adapter manifests, command payloads, and research Artifacts are stored as files inside the Project tree. There is no external database or remote service required for normal operation.

### Workspace path contracts are semantic labels

Topic-internal paths are resolved through semantic workspace surface labels and the Topic Workspace Manifest, not by assuming fixed directory names. The built-in `isomer-default.v1` layout remains the default profile for fresh topics and explicit materialization. Read-only commands such as `project paths get`, `project paths list`, `project paths preview`, `project paths default`, and `project paths explain` must not create manifests, directories, repositories, or runtime records. Manifest bindings use `label`, `path`, and explicit `storage_profile`; user-defined labels live under `custom.*`, while additional topic repositories may use grouped `topic.repos.*` labels and helper-created non-main repositories default under `repos/extern/...`.

### Local tmp surfaces are semantic labels

Local `tmp/` surfaces are implemented as semantic labels: `topic.tmp`, `topic.repos.main.tmp`, and `agent.tmp`. Under `isomer-default.v1`, they bind to `<topic-workspace>/tmp/`, `<resolved topic.repos.main>/tmp/`, and `<resolved agent.workspace>/tmp/`. They remain local, ignored, disposable, not shared, and not durable evidence unless promoted or recorded by another accepted contract.

## Non-goals

The documentation rewrite does not change runtime CLI behavior, Workspace Runtime schema behavior, or Houmao adapter behavior.

The platform intentionally does not:

- provide filesystem-grade sandboxing for Agent Workspaces;
- infer topic-to-environment relationships from names;
- hide environment repair inside read-only diagnostics or `project runtime prepare`;
- promote Houmao specialists, project profiles, launch dossiers, mailboxes, gateways, or managed-agent ids into core Isomer language;
- require an external documentation hosting service or publication pipeline;
- generate the entire CLI reference from Click help, because raw help does not explain side effects, prerequisites, and safe usage.

## Current Milestone Status

### Implemented

- Project discovery through `.isomer-labs/manifest.toml`.
- Project Manifest validation and Research Topic Config validation.
- Effective Topic Context resolution.
- Side-effect-free Workspace Path Resolution previews.
- Domain Agent Team Template registration, inspection, and validation.
- Topic Team Specialization, Topic Agent Team Profile validation, and optional write.
- Workspace Runtime initialization, reopening, and schema checking.
- Topic Environment Readiness recording.
- Read-only Workspace Runtime inspection and validation.
- Agent Team Instance record creation with Agent Instance records, Agent Workspace records, and directory materialization.
- Topic Workspace Manifest-backed semantic path resolution through `project paths get`, `project paths list`, `project paths preview`, `project paths default`, `project paths explain`, explicit `project paths materialize-default`, configured-target `project paths materialize`, binding lifecycle commands, generated `ISOMER_PATH__...` variables, and `project repos create`.
- Isomer-managed Agent Workspace support paths under `isomer-managed/`, including tracked material, agent-owned support, topic-owned projections, and generated-link diagnostics.
- Houmao adapter quick launch, prepare-only materialization, inspect-live, stop, reconcile, and adopt.
- Houmao adapter JSON manifests (`adapter-link.json`, `launch-material-manifest.json`, `adapter-runtime-manifest.json`), command payload recording, manifest digest tracking, and material drift detection.
- Manual handoff dispatch, Signal Observation ingestion, and Operator Agent handoff normalization for the Houmao Execution Adapter.

### Partially Implemented

- Research Inquiry graph records exist in the Workspace Runtime schema and domain language, but full inquiry-driven execution with Operator Agent dispatch is not yet complete.
- GUI Backend, View Manifests, and AG-UI event handling exist in the domain model and may be partially wired, but task-specific GUI rendering is future work.
- Service Request and Service Team concepts exist, but automated launched-service-agent dispatch is future work.
- Gate, Decision Record, Evidence Item, and Provenance Record schemas exist, but workflow-level Gate enforcement is future work.

### Planned / Future Work

- Automatic Completion Watcher Contract execution and multi-step manual Control Mode.
- Full Run lifecycle with automatic fanout and long-running recovery.
- GUI Backend runtime rendering and View Manifest consumption.
- Service Agent Instance launch and Service Request monitoring.
- Research Claim, Evidence Item, Finding, and Decision Record workflow integration.
- Additional Execution Adapters beyond Houmao.
- Multi-topic and multi-workspace migration, archive, and fork operations.

## Advisory Workspace Boundaries

When a page describes an Agent Workspace as "owned" by an Agent Instance, it means ownership is recorded and declared, not enforced by the operating system. Contributors should not add language that implies filesystem access control, OS sandboxing, or permission enforcement unless a future accepted contract explicitly introduces it.

## Security Posture

- Adapter command payloads are redacted before storage when they contain secret-like field names.
- The Project Manifest and Research Topic Config must not contain credentials, tokens, API keys, passwords, or other secret material.
- GUI Backend APIs are authenticated and must not bypass Gate resolution or turn team Agent Instances into direct human-operated control surfaces.
- Workspace boundaries are advisory; do not rely on them for security isolation.

## How to Read the Rest of the Docs

Pages such as [Architecture](architecture.md), [Project Lifecycle](../manual/project-lifecycle.md), and [Houmao Adapter](../manual/houmao-adapter.md) describe implemented behavior first and label planned or partial behavior explicitly. If a sentence sounds like a guarantee, check whether the capability is listed under Implemented above.
