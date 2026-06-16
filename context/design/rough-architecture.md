# Rough Architecture

## Part 1: Isomer-Managed Project Directory Layout

This section defines the directory layout for a user-owned Project that Isomer Labs manages. The Project remains the user's repository or workspace. Isomer adds one project-level Project Config Directory, `.isomer-labs/`, and discovers all Isomer Workspaces through `.isomer-labs/manifest.toml`. A Research Thread is the user-facing line of inquiry, and an Isomer Workspace is the project-local storage/runtime backing for that thread by default.

The key rule is that `.isomer-labs/` is the config and discovery root, not the required storage root for all research work. Workspaces may live in arbitrary directories inside the project as long as the manifest references them.

## Top-Level Shape

```text
<project-root>/
  .isomer-labs/
    manifest.toml
    teams/
    profiles/
    schemas/
    cache/
    tmp/

  <workspace-dir-a>/
    state.sqlite
    artifacts/
    agents/
    teams/
    views/
    runs/
    logs/

  <workspace-dir-b>/
    state.sqlite
    artifacts/
    agents/
    teams/
    views/
    runs/
    logs/

  <normal-user-files-and-project-code>/
```

Only `.isomer-labs/manifest.toml` is required at the project level. Other `.isomer-labs/` subdirectories are optional support directories.

## `.isomer-labs/` Project Config Directory

`.isomer-labs/` stores project-level Isomer configuration and references. It should stay small and should not become a hidden workspace where all research output is forced to live.

Recommended contents:

```text
.isomer-labs/
  manifest.toml          # required project discovery manifest
    teams/                 # reusable project-level Agent Teams
    profiles/              # reusable Agent Profiles and capability references
  schemas/               # pinned schema copies or generated schema docs
  cache/                 # disposable discovery or render cache
  tmp/                   # temporary files safe to delete
```

`manifest.toml` is the Project Manifest and the authority for Isomer Workspace discovery. The engine must not infer managed Isomer Workspaces by scanning arbitrary directories. A directory becomes an Isomer Workspace only when the Project Manifest declares it.

Project-level `teams/` stores reusable Agent Teams that multiple Isomer Workspaces can reference. Workspace-local Agent Teams still belong inside the Isomer Workspace when they are specific to one Research Thread.

`profiles/` stores reusable Agent Profiles and capability references for models, tools, skills, execution environments, communication channels, or credentials. It should store references and non-secret configuration. Secrets should live in the user's credential store or another configured secret backend, not in committed TOML files.

`schemas/` can store pinned schema files or generated schema documentation for Project Manifest, Agent Team, Workspace Runtime, and View Manifest validation. The engine should have built-in schemas, so this directory is a project override or documentation surface rather than the only source of truth.

`cache/` and `tmp/` are disposable. They should be ignored by default.

## Workspace Directories

An Isomer Workspace is a durable research execution area referenced by `.isomer-labs/manifest.toml`. It backs a Research Thread by default and may live anywhere under the Project root, for example:

```text
research/main/
experiments/isomer-run-001/
teams/lfeng-workspace/
dswork/workspace/
```

The recommended minimal Isomer Workspace layout is:

```text
<workspace>/
  state.sqlite            # compact control-plane state
  artifacts/              # rich durable Artifacts
  agents/                 # per-agent Agent Workspaces
  teams/                  # workspace-local Agent Teams and snapshots
  views/                  # engine-produced GUI View Manifests
  runs/                   # per-Run prompts, command records, outputs, and traces
  logs/                   # runtime logs and diagnostics
```

`state.sqlite` is part of the Workspace Runtime. It stores compact control-plane facts across many Runs: ids, statuses, transitions, handoffs, Gates, Artifact refs, prompt refs, tool-call refs, Research Claim refs, Evidence Item refs, Decision Record refs, and provenance links.

`artifacts/` stores human-readable or tool-produced Artifacts. Examples include Markdown notes, literature summaries, experiment plans, result JSON, figures, reports, and Decision Records.

`agents/` stores Agent Workspaces for concrete Agent Instances. Each Agent Workspace owns that agent's Agent Runtime, scratch files, logs, and Agent Artifacts. Agent Workspace boundaries are advisory: README files or manifests can declare owned paths and peer-readable paths, but Isomer does not try to enforce filesystem-grade access control.

`teams/` stores the Agent Team actually used by an Isomer Workspace. If a workspace starts from a project-level team, the workspace should snapshot or lock the resolved Agent Team so later project-level edits do not silently rewrite historical Runs.

`views/` stores View Manifests emitted by the engine. These files describe task-specific GUI views, data sources, user actions, and pending Gates. The GUI renders these manifests but does not own Workspace Runtime state.

`runs/` is part of the Workspace Runtime. It stores per-Run records for bounded execution episodes, such as prompts, runner commands, stdout or event logs, tool-call input and output refs, and Run summaries.

`logs/` stores runtime diagnostics for the Workspace Runtime and its Runs. It should be safe to rotate or prune logs without destroying the canonical research Artifacts, as long as Run summaries and provenance refs remain intact.

## Agent Workspace Layout

Each Agent Instance inside an active team should get an Agent Workspace under the Isomer Workspace. The purpose is to keep each agent's local work, runtime state, and intermediate Artifacts from colliding with other agents' work while keeping collaboration inspectable.

Recommended shape:

```text
<workspace>/
  agents/
    <agent-instance-id>/
      README.md            # advisory ownership and peer-read notes
      boundary.toml        # optional machine-readable boundary declaration
      runtime/             # Agent Runtime state and recovery files
      artifacts/           # Agent Artifacts produced or curated by this agent
      scratch/             # local draft or temporary work
      logs/                # agent-local logs and diagnostics
```

The owning agent should write inside its own Agent Workspace. Peer agents may read files declared readable by `README.md`, `boundary.toml`, or the Agent Team. This Peer Read Access is a collaboration rule, not an operating-system permission guarantee. An agent with shell or filesystem tools could still modify peer files, so the engine should record and validate behavior instead of treating the boundary as a security mechanism.

When one agent's output becomes an input to another agent's durable reasoning, the engine should record the dependency through a handoff, promoted workspace-level Artifact, Evidence Item, or Provenance Record. Casual peer reads are useful for collaboration, but they should not be the only trace for a claim, decision, or result.

## Agent Profiles and Execution Adapters

Isomer should define Agent Teams, Agent Profiles, and Agent Instances in provider-neutral terms. An Agent Profile describes how to construct or configure a runtime actor: instructions, skills, tool access, model posture, credentials, communication defaults, environment defaults, memory defaults, and launch posture. An Agent Instance is the concrete actor created from that profile for a Run or team execution context.

An Execution Adapter maps those neutral concepts onto a backend. Houmao is a useful example implementation: Houmao specialists, project profiles, native roles, recipes, launch dossiers, and managed agents can map to Agent Profiles, Capability Bindings, and Agent Instances. Isomer should not require Houmao's document names or command structure in its core schema.

## Manifest Sketch

The exact schema is a later architecture part. This sketch shows the intended relationship between project config and arbitrary project-local Isomer Workspaces:

```toml
schema_version = "0.1"
project_id = "isomer-labs-example"
active_workspace = "main"

[defaults]
team = "research-basic"
runner_profile = "local-codex"

[[workspaces]]
id = "main"
path = "research/main"
kind = "research"
status = "active"
state_db = "state.sqlite"
description = "Primary Isomer Workspace."
thread_id = "main-thread"

[[workspaces]]
id = "paper-draft"
path = "papers/first-study/isomer-workspace"
kind = "research"
status = "parked"
state_db = "state.sqlite"
description = "Isomer Workspace for the first paper draft Research Thread."
thread_id = "paper-draft"

[[team_defs]]
id = "research-basic"
path = ".isomer-labs/teams/research-basic.toml"
scope = "project"

[[profiles]]
id = "local-codex"
path = ".isomer-labs/profiles/local-codex.toml"
kind = "runner"
```

## Path Rules

All manifest paths are resolved relative to the project root by default.

Isomer Workspace paths must stay inside the Project root unless a future explicit trust policy allows external paths. The first implementation should reject paths that escape through absolute paths, `..`, symlinks, or platform-specific path quirks.

Workspace ids must be stable and unique within one Project Manifest. The id is the logical name used by CLI commands, GUI routes, state records, and cross-Artifact references. The path may move through an explicit migration, but the id should not change casually.

The active workspace is a convenience pointer, not the only valid Isomer Workspace. Commands should accept an explicit workspace id and should fall back to `active_workspace` only when the user did not specify one.

The engine should open only Project Manifest-declared Isomer Workspaces. It may inspect directories for repair or import workflows, but it must not treat an undeclared directory as managed state.

Agent Workspace paths must stay inside their parent Isomer Workspace. Agent Instance ids should be stable within the relevant Agent Team or Run record. Peer writes should be treated as validation issues unless the workflow explicitly assigns a repair, migration, or cleanup task.

## Tracking and Ignore Posture

The default tracking posture should be transparent but conservative:

- Track `.isomer-labs/manifest.toml`.
- Track project-level team and profile files when they contain no secrets.
- Ignore `.isomer-labs/cache/` and `.isomer-labs/tmp/`.
- Treat Isomer Workspace tracking as a workspace policy, because some Projects should commit research Artifacts and others should keep them local.
- Never store secrets in tracked Isomer config files.

An Isomer Workspace should be able to declare whether `state.sqlite`, `artifacts/`, `views/`, `runs/`, and `logs/` are intended to be committed, ignored, or selectively exported. The architecture should not assume one universal policy for all research Projects.

## Invariants

- `.isomer-labs/manifest.toml` is the project discovery authority.
- `.isomer-labs/` is the config root, not the required workspace root.
- Research Threads are the user-facing research lifecycle concept.
- Isomer Workspaces can live in arbitrary project-local directories.
- A workspace is managed only when the Project Manifest references it.
- Each Isomer Workspace owns its control-plane SQLite database and rich file Artifacts.
- Workspace Runtime is the persistent substrate for state, refs, validation, and per-Run records; a Run is one bounded execution episode recorded through that substrate.
- Workspace-local Agent Team snapshots preserve Run reproducibility.
- GUI View Manifests live in the Isomer Workspace and are generated from engine state.
- Each active Agent Instance should have an Agent Workspace for its Agent Runtime and Agent Artifacts.
- Agent Roles describe responsibilities; Agent Instances own Agent Workspaces.
- Coordination Policy defines how Agent Instances communicate, hand off work, review outputs, escalate decisions, and use Gates.
- Houmao can be an Execution Adapter, but Isomer core docs and schemas should use provider-neutral multi-agent terms.
- Agent Workspace boundaries are advisory ownership and peer-read contracts, not filesystem-grade access control.
- Disposable cache and temporary files stay separate from durable research Artifacts.

## Open Questions for Later Parts

- Exact manifest schema and validation errors.
- Exact Workspace Runtime schema and migration policy.
- Exact Agent Workspace boundary declaration format.
- Exact Agent Profile schema and Execution Adapter interface.
- Agent Team file format.
- View Manifest schema and supported view types.
- Workspace tracking policy format.
- Import flow for an existing directory that should become an Isomer Workspace.
