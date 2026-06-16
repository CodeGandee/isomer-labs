# Rough Architecture

## Part 1: Isomer-Managed Project Directory Layout

This section defines the directory layout for a user-owned Project that Isomer Labs manages. The Project remains the user's repository, checkout, or directory tree. Isomer adds one project-level Project Config Directory, `.isomer-labs/`, and discovers all Isomer Workspaces through `.isomer-labs/manifest.toml`. A Research Thread is the user-facing line of inquiry, and an Isomer Workspace is the project-local storage/runtime for one Research Task handled by the Operator Agent or a delegated Agent Instance from an Agent Team Instance.

The key rule is that `.isomer-labs/` is the config and discovery root, not the required storage root for all research work. Workspaces may live in arbitrary directories inside the project as long as the manifest references them.

## Top-Level Shape

```text
<project-root>/
  .isomer-labs/
    manifest.toml
    team-templates/
    teams/
    profiles/

  <workspace-dir-a>/
    state.sqlite
    artifacts/
    agents/
    views/
    runs/
    logs/

  <workspace-dir-b>/
    state.sqlite
    artifacts/
    agents/
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
  team-templates/        # optional imported or referenced Agent Team Templates
  teams/                 # Agent Team Instances instantiated from templates
  profiles/              # reusable Agent Profiles and capability references
```

`manifest.toml` is the Project Manifest and the authority for Isomer Workspace discovery. The engine must not infer managed Isomer Workspaces by scanning arbitrary directories. A directory becomes an Isomer Workspace only when the Project Manifest declares it.

`team-templates/` stores optional imported or referenced Agent Team Templates. A template is a reusable blueprint, such as an adapter-imported Houmao team definition like `teams/lfeng-team`; it is not the project-specific team used directly by a Research Task.

Project-level `teams/` stores Agent Team Instances that the Operator Agent instantiated from templates with project-specific parameters such as role counts, model posture, credentials, project paths, domain instructions, and Gate policy. An Isomer Workspace should not contain a workspace-local `teams/` directory. The resolved Agent Team Instance identity and task handler should be recorded through manifest refs, Workspace Runtime state, or provenance Artifacts.

`profiles/` stores reusable Agent Profiles and capability references for models, tools, skills, execution environments, communication channels, or credentials. It should store references and non-secret configuration. Secrets should live in the user's credential store or another configured secret backend, not in committed TOML files.

System-owned schemas are Isomer built-in artifacts, not project-local config files. `isomer-cli` should expose commands to query built-in artifact versions, inspect schema documentation, and validate Project Manifests, Agent Team Templates, Agent Team Instances, Workspace Runtime state, and View Manifests against the built-in schemas.

`.isomer-labs/` should not include default cache or temporary directories. Runtime scratch, render cache, and disposable discovery output should live under an Isomer Workspace, an explicit tool cache, or the operating system's temporary directory.

## Workspace Directories

An Isomer Workspace is a durable research execution area referenced by `.isomer-labs/manifest.toml`. It is scoped to one Research Task and records a task handler: the Operator Agent or a delegated Agent Instance from a selected Agent Team Instance. It may live anywhere under the Project root, for example:

```text
research/main/
experiments/isomer-run-001/
research/team-alpha-task-001/
dswork/workspace/
```

The recommended minimal Isomer Workspace layout is:

```text
<workspace>/
  state.sqlite            # compact control-plane state
  artifacts/              # rich durable Artifacts
  agents/                 # per-agent Agent Workspaces
  views/                  # engine-produced GUI View Manifests
  runs/                   # per-Run prompts, command records, outputs, and traces
  logs/                   # runtime logs and diagnostics
```

`state.sqlite` is part of the Workspace Runtime. It stores compact control-plane facts across many Runs: ids, statuses, transitions, handoffs, Gates, Artifact refs, prompt refs, tool-call refs, Research Claim refs, Evidence Item refs, Decision Record refs, and provenance links.

`artifacts/` stores human-readable or tool-produced Artifacts. Examples include Markdown notes, literature summaries, experiment plans, result JSON, figures, reports, and Decision Records.

`agents/` stores Agent Workspaces for concrete Agent Instances. Each Agent Workspace owns that agent's Agent Runtime, scratch files, logs, and Agent Artifacts. Agent Workspace boundaries are advisory: README files or manifests can declare owned paths and peer-readable paths, but Isomer does not try to enforce filesystem-grade access control.

`views/` stores View Manifests emitted by the engine. These files describe task-specific GUI views, data sources, user actions, and pending Gates. The GUI renders these manifests but does not own Workspace Runtime state.

`runs/` is part of the Workspace Runtime. It stores per-Run records for bounded execution episodes, such as prompts, runner commands, stdout or event logs, tool-call input and output refs, and Run summaries.

`logs/` stores runtime diagnostics for the Workspace Runtime and its Runs. It should be safe to rotate or prune logs without destroying the canonical research Artifacts, as long as Run summaries and provenance refs remain intact.

## Agent Workspace Layout

Each Agent Instance inside an active Agent Team Instance should get an Agent Workspace under the Isomer Workspace. The purpose is to keep each agent's local work, runtime state, and intermediate Artifacts from colliding with other agents' work while keeping collaboration inspectable.

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

The owning agent should write inside its own Agent Workspace. Peer agents may read files declared readable by `README.md`, `boundary.toml`, the Agent Team Instance, or its Coordination Policy. This Peer Read Access is a collaboration rule, not an operating-system permission guarantee. An agent with shell or filesystem tools could still modify peer files. The engine should record and validate behavior instead of treating the boundary as a security mechanism.

When one agent's output becomes an input to another agent's durable reasoning, the engine should record the dependency through a handoff, promoted workspace-level Artifact, Evidence Item, or Provenance Record. Casual peer reads are useful for collaboration, but they should not be the only trace for a claim, decision, or result.

## Agent Profiles and Execution Adapters

Isomer should define Agent Team Templates, Agent Team Instances, Agent Roles, Agent Profiles, Capability Bindings, Coordination Policies, Agent Instances, the Operator Agent, and Workflow Stages in provider-neutral terms. An Agent Profile describes how to construct or configure a runtime actor. It can name instructions, skills, tool access, model posture, credentials, communication defaults, environment defaults, memory defaults, and launch posture. An Agent Instance is the concrete actor created from that profile and assigned to an Agent Role for a Run or team execution context.

The first team stage is template instantiation. The Operator Agent selects an Agent Team Template, such as an adapter-imported Houmao team definition, and instantiates it into an Agent Team Instance with project-specific parameters. Examples include how many coder roles to materialize, which project paths the team should treat as canonical, which credentials or tools are available, and which Gates require user approval. Research Tasks are then handled either directly by the Operator Agent or by one delegated Agent Instance from the Agent Team Instance.

An Execution Adapter maps those neutral concepts onto a backend. Houmao is a useful example implementation: Houmao team definitions can map to Agent Team Templates, and Houmao specialists, project profiles, native roles, recipes, launch dossiers, and managed agents can map to Agent Profiles, Capability Bindings, Coordination Policies, and Agent Instances. Isomer should not require Houmao's document names or command structure in its core schema.

## Manifest Sketch

The exact schema is a later architecture part. This sketch shows the intended relationship between project config and arbitrary project-local Isomer Workspaces:

```toml
schema_version = "0.1"
project_id = "isomer-labs-example"
active_workspace = "main"

[defaults]
operator_agent = "operator"
agent_team_template = "lfeng-team"
agent_team_instance = "research-basic"

[[workspaces]]
id = "main"
path = "research/main"
kind = "research"
status = "active"
state_db = "state.sqlite"
description = "Primary Isomer Workspace."
thread_id = "main-thread"
research_task_id = "main-thread/initial-analysis"
task_handler = "operator"
agent_team_instance = "research-basic"

[[workspaces]]
id = "paper-draft"
path = "papers/first-study/isomer-workspace"
kind = "research"
status = "parked"
state_db = "state.sqlite"
description = "Isomer Workspace for the first paper draft Research Thread."
thread_id = "paper-draft"
research_task_id = "paper-draft/write-outline"
task_handler = "research-basic/writer"
agent_team_instance = "research-basic"

[[agent_team_templates]]
id = "lfeng-team"
path = ".isomer-labs/team-templates/lfeng-team.toml"
scope = "project"

[[agent_team_instances]]
id = "research-basic"
path = ".isomer-labs/teams/research-basic.toml"
template = "lfeng-team"
scope = "project"

[[agent_profiles]]
id = "operator"
path = ".isomer-labs/profiles/operator.toml"
scope = "project"

[[agent_profiles]]
id = "codex-researcher"
path = ".isomer-labs/profiles/codex-researcher.toml"
scope = "project"
```

The Agent Team Template file should define the reusable team blueprint. The Agent Team Instance file should record the Operator Agent's instantiated project-specific choices and usually bind Agent Roles to Agent Profiles through Capability Bindings. The Project Manifest should discover project-level entries and select defaults, not encode the full team workflow inline.

## Path Rules

All manifest paths are resolved relative to the project root by default.

Isomer Workspace paths must stay inside the Project root unless a future explicit trust policy allows external paths. The first implementation should reject paths that escape through absolute paths, `..`, symlinks, or platform-specific path quirks.

Workspace ids must be stable and unique within one Project Manifest. The id is the logical name used by CLI commands, GUI routes, state records, and cross-Artifact references. The path may move through an explicit migration, but the id should not change casually.

The active workspace is a convenience pointer, not the only valid Isomer Workspace. Commands should accept an explicit workspace id and should fall back to `active_workspace` only when the user did not specify one.

The engine should open only Project Manifest-declared Isomer Workspaces. It may inspect directories for repair or import workflows, but it must not treat an undeclared directory as managed state.

Agent Workspace paths must stay inside their parent Isomer Workspace. Agent Instance ids should be stable within the relevant Agent Team Instance or Run record. Peer writes should be treated as validation issues unless the workflow explicitly assigns a repair, migration, or cleanup task.

## Tracking and Ignore Posture

The default tracking posture should be transparent but conservative:

- Track `.isomer-labs/manifest.toml`.
- Track project-level Agent Team Instance and Agent Profile files when they contain no secrets.
- Treat Isomer Workspace tracking as a workspace policy, because some Projects should commit research Artifacts and others should keep them local.
- Never store secrets in tracked Isomer config files.

An Isomer Workspace should be able to declare whether `state.sqlite`, `artifacts/`, `views/`, `runs/`, and `logs/` are intended to be committed, ignored, or selectively exported. The architecture should not assume one universal policy for all research Projects.

## Invariants

- `.isomer-labs/manifest.toml` is the project discovery authority.
- `.isomer-labs/` is the config root, not the required workspace root.
- Research Threads are the user-facing research lifecycle concept.
- Isomer Workspaces can live in arbitrary project-local directories.
- An Isomer Workspace is managed only when the Project Manifest references it.
- Each Isomer Workspace is scoped to one Research Task and records a task handler.
- A task handler is the Operator Agent or a delegated Agent Instance from a selected Agent Team Instance.
- Each Isomer Workspace owns its control-plane SQLite database and rich file Artifacts.
- Workspace Runtime is the persistent substrate for state, refs, validation, and per-Run records; a Run is one bounded Research Task execution attempt recorded through that substrate.
- Isomer Workspaces do not contain `teams/`; selected Agent Team Instance identity and task-handler identity are recorded through manifest refs, Workspace Runtime state, or provenance Artifacts.
- GUI View Manifests live in the Isomer Workspace and are generated from engine state.
- Each active Agent Instance should have an Agent Workspace for its Agent Runtime and Agent Artifacts.
- Agent Roles describe responsibilities; Agent Instances own Agent Workspaces.
- Agent Team Templates are reusable blueprints; Agent Team Instances are instantiated by the Operator Agent with project-specific parameters.
- The Operator Agent is the main interaction point with the user, the controller, and the final fallback handler.
- Human users operate through the Operator Agent for commands, approvals, Gate decisions, and task-routing changes.
- The Operator Agent is outside Agent Team Instance membership; all other task Agent Instances belong to an Agent Team Instance.
- Coordination Policy defines how Agent Instances communicate, hand off work, review outputs, escalate decisions, and use Gates.
- Houmao can be an Execution Adapter, but Isomer core docs and schemas should use provider-neutral multi-agent terms.
- Agent Workspace boundaries are advisory ownership and peer-read contracts, not filesystem-grade access control.
- `.isomer-labs/` has no default cache, temporary, or schema directories.
- System-owned schemas and other Isomer built-in artifacts are queried and validated through `isomer-cli`.

## Open Questions for Later Parts

- Exact manifest schema and validation errors.
- Exact Workspace Runtime schema and migration policy.
- Exact Agent Workspace boundary declaration format.
- Exact Agent Profile schema and Execution Adapter interface.
- Agent Team Template and Agent Team Instance file formats.
- View Manifest schema and supported view types.
- Workspace tracking policy format.
- Import flow for an existing directory that should become an Isomer Workspace.
