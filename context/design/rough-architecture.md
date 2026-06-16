# Rough Architecture

## Part 1: Isomer-Managed Project Directory Layout

This section defines the directory layout for a user-owned Project that Isomer Labs manages. The Project remains the user's repository, checkout, or directory tree. Isomer adds one project-level Project Config Directory, `.isomer-labs/`, and discovers all Isomer Workspaces through `.isomer-labs/manifest.toml`. A Research Thread is the user-facing line of inquiry, and an Isomer Workspace is the project-local storage/runtime for one Research Task handled by the Operator Agent or a delegated Agent Instance from an Agent Team Instance created from a Topic Agent Team Profile.

The key rule is that `.isomer-labs/` is the config and discovery root, not the required storage root for all research work. Workspaces may live in arbitrary directories inside the project as long as the manifest references them.

## Top-Level Shape

```text
<project-root>/
  .isomer-labs/
    manifest.toml
    domain-team-templates/
    topic-team-profiles/
    agent-profiles/
    gui-components/

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
  domain-team-templates/ # optional imported or referenced Domain Agent Team Templates
  topic-team-profiles/   # Topic Agent Team Profiles specialized for research topics
  agent-profiles/        # reusable Agent Profiles and capability references
  gui-components/        # optional project-scope agent-generated component manifests and sources
```

`manifest.toml` is the Project Manifest and the authority for Isomer Workspace discovery. The engine must not infer managed Isomer Workspaces by scanning arbitrary directories. A directory becomes an Isomer Workspace only when the Project Manifest declares it.

`domain-team-templates/` stores optional imported or referenced Domain Agent Team Templates. A Domain Agent Team Template is a reusable method template for a research field; it is not specialized to the user's concrete research topic and is not used directly as a running team.

`topic-team-profiles/` stores Topic Agent Team Profiles that the Operator Agent specializes from Domain Agent Team Templates. A Topic Agent Team Profile records the user's research topic, topic-specific role and stage choices, constraints, expected Artifacts, Gate policy, and capability bindings. It is reviewable and editable before launch; it is not an Agent Team Instance.

Agent Team Instances are runtime teams created from Topic Agent Team Profiles. An Isomer Workspace should not contain a workspace-local `teams/` directory. The selected Topic Agent Team Profile, resolved Agent Team Instance identity, and task handler should be recorded through manifest refs, Workspace Runtime state, or provenance Artifacts.

`agent-profiles/` stores reusable Agent Profiles and capability references for models, tools, skills, execution environments, communication channels, or credentials. It should store references and non-secret configuration. Secrets should live in the user's credential store or another configured secret backend, not in committed TOML files.

`gui-components/` stores project-scope agent-generated GUI Component Registry entries, component manifests, and optionally source for agent-generated GUI Components. It is not the whole registry: Built-in GUI Components are system-owned and registered by the GUI Backend at startup. Declarative GUI Component Specs are preferred. Executable GUI Components must be registered, validated, sandboxed or isolated according to policy, and approved before the GUI Backend loads them. Direct AG-UI Event Batches may reference only registered component ids when they target Executable GUI Components.

System-owned schemas are Isomer built-in artifacts, not project-local config files. `isomer-cli` should expose commands to query built-in artifact versions, inspect schema documentation, and validate Project Manifests, Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Workspace Runtime state, and View Manifests against the built-in schemas.

`.isomer-labs/` should not include default cache or temporary directories. Runtime scratch, render cache, executable component build output, and disposable discovery output should live under an Isomer Workspace, an explicit tool cache, or the operating system's temporary directory.

## Workspace Directories

An Isomer Workspace is a durable research execution area referenced by `.isomer-labs/manifest.toml`. It is scoped to one Research Task and records a task handler: the Operator Agent or a delegated Agent Instance from a selected Agent Team Instance created from a Topic Agent Team Profile. It may live anywhere under the Project root, for example:

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

`views/` stores View Manifests emitted by the engine. These files describe task-specific GUI views, data sources, user actions, and pending Gates. The GUI Backend and Renderer render these manifests but do not own Workspace Runtime state.

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

## Team Profiles, Agent Profiles, and Execution Adapters

Isomer should define Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Roles, Agent Profiles, Capability Bindings, Coordination Policies, Agent Instances, the Operator Agent, and Workflow Stages in provider-neutral terms. An Agent Profile describes how to construct or configure a runtime actor. It can name instructions, skills, tool access, model posture, credentials, communication defaults, environment defaults, memory defaults, and launch posture. An Agent Instance is the concrete actor created from that profile and assigned to an Agent Role for a Run or team execution context.

The first team stage is topic-profile specialization. The Operator Agent selects a Domain Agent Team Template, asks for or infers the user's research topic, and specializes the template into a Topic Agent Team Profile. Examples include which roles to keep, which project paths the team should treat as canonical, which topic constraints apply, which expected Artifacts matter, which credentials or tools are available, and which Gates require user approval. Research Tasks are then handled either directly by the Operator Agent or by one delegated Agent Instance from the Agent Team Instance created from that Topic Agent Team Profile.

An Execution Adapter maps those neutral concepts onto a backend. Houmao is a useful example implementation: Houmao team definitions can map to Domain Agent Team Templates; Houmao specialists, project profiles, native roles, recipes, launch dossiers, and managed agents can map to Topic Agent Team Profiles, Agent Profiles, Capability Bindings, Coordination Policies, Agent Team Instances, and Agent Instances. Isomer should not require Houmao's document names or command structure in its core schema.

## GUI Backend and Component Handling

The GUI Backend is a built-in HTTP server started through `isomer-cli` for a Project. On startup it binds a local or configured address, reports a URL, registers Built-in GUI Components, and serves the predefined browser-side GUI Renderer. The user opens that URL in a browser to inspect and manipulate the Project GUI.

The GUI Backend resolves the Project Manifest, reads Workspace Runtime state, fetches View Manifests and Artifacts, maintains GUI Runtime State, and exposes GUI Backend APIs. These APIs can create or update GUI Component Instances, publish AG-UI Render Payloads, update GUI Layout Specs, refresh views, and inspect live GUI state. The GUI Renderer should reflect these backend state changes immediately through the GUI connection model. User-origin commands, approvals, Gate decisions, and task-routing changes still enter through the Operator Agent.

The GUI Backend can also receive direct AG-UI Event Batches from authenticated Agent Team Instance members. These batches carry AG-UI Render Payloads: data, DSL, JSON, Artifact refs, visualization intent, component hints, and optional layout refs. The backend resolves those payloads to registered GUI Components and GUI Component Instances. This path is for live updates, previews, and registered component output. It is not canonical research state. The backend should persist AG-UI Event Envelopes by default and save full AG-UI payload content only when the user explicitly instructs the system to retain it.

Agent-generated GUI Components use a registry-gated model. Built-in GUI Components are registered by the built-in GUI Backend, Declarative GUI Component Specs are the preferred project customization format, and Executable GUI Components require manifest validation, dependency checks, sandbox or isolation policy, compatibility checks, and user approval before loading. A project-scoped approve-all policy may skip repeated per-component approval until revoked, but it does not bypass registration, validation, sandbox policy, compatibility checks, or AG-UI publisher authentication.

GUI Layout Specs are JSON or JSON-compatible layout declarations. They arrange registered GUI Component Instances into panels, tabs, split views, ordered sections, and responsive regions. They can be referenced by View Manifests or AG-UI Render Payloads. A layout spec should contain component ids, instance ids, slots, sizing, and grouping; it should not contain executable frontend code.

## Manifest Sketch

The exact schema is a later architecture part. This sketch shows the intended relationship between project config and arbitrary project-local Isomer Workspaces:

```toml
schema_version = "0.1"
project_id = "isomer-labs-example"
active_workspace = "main"

[defaults]
operator_agent = "operator"
domain_agent_team_template = "ml-systems-research"
topic_agent_team_profile = "research-basic"

[gui]
component_registry = ".isomer-labs/gui-components"
ag_ui_payload_retention = "envelope_only"
default_layout_ref = "workspace-or-project-layout-json"

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
topic_agent_team_profile = "research-basic"
agent_team_instance = "research-basic/run-001"

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
topic_agent_team_profile = "research-basic"
agent_team_instance = "research-basic/run-002"

[[domain_agent_team_templates]]
id = "ml-systems-research"
path = ".isomer-labs/domain-team-templates/ml-systems-research.toml"
scope = "project"

[[topic_agent_team_profiles]]
id = "research-basic"
path = ".isomer-labs/topic-team-profiles/research-basic.toml"
template = "ml-systems-research"
research_topic_ref = "context/research-topic.md"
scope = "project"

[[agent_profiles]]
id = "operator"
path = ".isomer-labs/agent-profiles/operator.toml"
scope = "project"

[[agent_profiles]]
id = "codex-researcher"
path = ".isomer-labs/agent-profiles/codex-researcher.toml"
scope = "project"

[[gui_components]]
id = "artifact-matrix"
path = ".isomer-labs/gui-components/artifact-matrix/component.toml"
kind = "declarative"
scope = "project"
```

The Domain Agent Team Template file should define the reusable research-field method. The Topic Agent Team Profile file should record the Operator Agent's topic-level specialization and usually bind Agent Roles to Agent Profiles through Capability Bindings. Agent Team Instance records should be created only when the profile is launched. The Project Manifest should discover project-level entries and select defaults, not encode the full team workflow inline.

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
- Track project-level Domain Agent Team Template, Topic Agent Team Profile, and Agent Profile files when they contain no secrets.
- Track project-scope GUI component manifests, Declarative GUI Component Specs, and GUI Layout Specs when they contain no secrets or bulky generated output.
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
- A task handler is the Operator Agent or a delegated Agent Instance from a selected Agent Team Instance created from a Topic Agent Team Profile.
- Each Isomer Workspace owns its control-plane SQLite database and rich file Artifacts.
- Workspace Runtime is the persistent substrate for state, refs, validation, and per-Run records; a Run is one bounded Research Task execution attempt recorded through that substrate.
- Isomer Workspaces do not contain `teams/`; selected Topic Agent Team Profile identity, selected Agent Team Instance identity, and task-handler identity are recorded through manifest refs, Workspace Runtime state, or provenance Artifacts.
- GUI View Manifests live in the Isomer Workspace and are generated from engine state.
- Each active Agent Instance should have an Agent Workspace for its Agent Runtime and Agent Artifacts.
- Agent Roles describe responsibilities; Agent Instances own Agent Workspaces.
- Domain Agent Team Templates are reusable research-field method templates.
- Topic Agent Team Profiles are topic-level specializations of Domain Agent Team Templates, and they are not running teams.
- Agent Team Instances are runtime teams created from Topic Agent Team Profiles.
- The Operator Agent is the main interaction point with the user, the controller, and the final fallback handler.
- Human users operate through the Operator Agent for commands, approvals, Gate decisions, and task-routing changes.
- The Operator Agent is outside Agent Team Instance membership; all other task Agent Instances belong to an Agent Team Instance.
- Coordination Policy defines how Agent Instances communicate, hand off work, review outputs, escalate decisions, and use Gates.
- Houmao can be an Execution Adapter, but Isomer core docs and schemas should use provider-neutral multi-agent terms.
- Agent Workspace boundaries are advisory ownership and peer-read contracts, not filesystem-grade access control.
- `.isomer-labs/` has no default cache, temporary, or schema directories.
- System-owned schemas and other Isomer built-in artifacts are queried and validated through `isomer-cli`.
- The GUI Backend is started through `isomer-cli` and does not own canonical research state.
- The GUI Backend serves a predefined browser-side GUI Renderer from a local or configured URL.
- Built-in GUI Components and agent-generated GUI Components must be registered before use.
- View Manifests are durable semantic view descriptions; direct AG-UI Event Batches are live GUI traffic.
- AG-UI Render Payloads carry data, DSL, JSON, Artifact refs, visualization intent, component hints, and optional layout refs; they are resolved to registered GUI Components by the GUI Backend.
- AG-UI Event Envelopes are persisted by default; full AG-UI payload content is retained only by explicit user instruction.
- Authenticated Agent Team Instance members may publish direct AG-UI Event Batches, but human user actions still go through the Operator Agent.
- GUI Backend APIs can manipulate GUI Runtime State and the GUI Renderer should reflect those changes immediately.
- GUI Layout Specs are JSON or JSON-compatible declarations that arrange registered GUI Component Instances.
- Executable GUI Components must pass registry validation, sandbox or isolation policy, compatibility checks, and approval before loading.
- Project-scoped approve-all can remove repeated per-component approval until revoked, but it does not bypass component or publisher validation.

## Open Questions for Later Parts

- Exact manifest schema and validation errors.
- Exact Workspace Runtime schema and migration policy.
- Exact Agent Workspace boundary declaration format.
- Exact Agent Profile schema and Execution Adapter interface.
- Domain Agent Team Template, Topic Agent Team Profile, and Agent Team Instance file formats.
- View Manifest schema and supported view types.
- GUI Component Registry schema, GUI Runtime State schema, GUI Layout Spec schema, Executable GUI Component sandbox contract, AG-UI Render Payload contract, and AG-UI Event Envelope schema.
- Workspace tracking policy format.
- Import flow for an existing directory that should become an Isomer Workspace.
