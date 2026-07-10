# Manifested Workspace Engine Design

## Status

Approved on 2026-06-15.

## Evidence

This design is based on the project goal in `context/design/project-goal.md` and the accepted exploration ADRs under `.imsight-arts/project-explore/adrs/`.

Relevant project-goal evidence:

- Isomer Labs should be an interactive, semi-automatic research-conduction platform where a human user defines goals, supplies context, chooses constraints, and steers critical decisions.
- Multi-agent research teams are the core research engine.
- Users must be able to choose predefined teams or define custom teams.
- The Operator Agent coordinates user-facing work, asks for user decisions, translates intent into team instructions, and presents work products.
- The platform should expose goals, teams, task plans, Artifacts, decisions, prompts, tool calls, and research state.
- The research engine and GUI should be decoupled.
- Generated GUI views should visualize task-specific Artifacts, state, and decision points.
- Project state can live inside a user-owned Project instead of a system-owned directory.

Accepted ADRs:

- `0001-config-manifest-references-project-workspaces.md`
- `0002-team-abstraction-roles-workflow-bindings.md`
- `0003-human-gates-for-irreversible-or-claim-shaping-decisions.md`
- `0004-engine-emits-view-manifests-for-task-specific-gui.md`
- `0005-sqlite-control-plane-plus-file-artifacts.md`
- `0006-manifested-workspace-engine.md`
- `0007-allow-direct-agent-ag-ui-publishing.md`
- `0008-persist-ag-ui-event-envelopes-by-default.md`
- `0009-register-gui-components-before-loading.md`
- `0010-project-scoped-gui-component-approve-all.md`
- `0011-domain-topic-team-lifecycle.md`
- `0018-workspace-path-resolver.md`

## Overview

Isomer Labs uses a manifested workspace engine as its primary architecture. The Project Manifest at `.isomer-labs/manifest.toml` is the discovery authority for project configuration, Research Topic Config files, and project-local Topic Workspaces. A Research Topic is the root research problem or investigation intent that initiates investigation and Topic Agent Team Profile specialization; Research Inquiries are user- or agent-generated questions under that topic. Each Topic Workspace is scoped to one Research Topic and records the topic's Research Inquiries, Research Tasks, Runs, Artifacts, selected Topic Agent Team Profiles, and selected Agent Team Instances when delegated. Topic Workspaces may live in arbitrary directories inside the user-owned Project, but each workspace must be declared in the Project Manifest before the engine treats it as managed state.

Each Topic Workspace owns its Workspace Runtime and research outputs for its Research Topic. Compact control-plane state lives in SQLite. Rich Artifacts remain ordinary files, such as Markdown notes, JSON outputs, logs, code, figures, reports, and View Manifests. During team execution, each concrete Agent Instance receives an Agent Workspace inside the Topic Workspace for agent-owned runtime state and Agent Artifacts. These workspaces create advisory ownership boundaries, not filesystem-grade access control. The Operator Agent is the human-facing coordination boundary between user intent, Agent Team Instance activity, durable state, and GUI-facing views.

Isomer's core multi-agent model is backend-neutral. Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Roles, Agent Profiles, Capability Bindings, Coordination Policies, Agent Instances, Runs, and Agent Workspaces should make sense for many execution backends. Backend-specific systems, including Houmao, should appear only through Execution Adapter mappings.

The GUI is not the engine. The engine remains useful through command-line and agent workflows. When a GUI is present, the built-in GUI Backend starts through `isomer-cli`, reports a browser URL, and serves a predefined GUI Renderer. The backend reads engine-produced View Manifests and renders task-specific views for Artifacts, Gates, Runs, Research Claims, result tables, and next actions. It can also receive direct AG-UI Event Batches from authenticated Agent Team Instance members. Those batches carry AG-UI Render Payloads such as data, DSL, JSON, Artifact refs, visualization intent, component hints, and optional layout refs. The backend resolves those payloads to registered GUI Components and live GUI Component Instances. Those events are live GUI traffic, not canonical research state.

## Actors & Entry Points

### Human User

The human user defines the Research Topic, provides context, sets constraints, approves or edits teams and workflows, resolves gated decisions, and steers active Research Inquiries through the Operator Agent. The user can pause, create follow-up Research Inquiries, record Research Inquiry Relationships, resume, archive, override team composition, or alter workflow structure.

### Operator Agent

The Operator Agent is the project-facing Agent Role and Agent Instance responsible for user-facing coordination. It turns user intent into executable team instructions, specializes Domain Agent Team Templates into Topic Agent Team Profiles, launches Topic Agent Team Profiles into Agent Team Instances, dispatches work to delegated Agent Instances, records decisions, and asks the user for input when a decision is irreversible or claim-shaping.

The Operator Agent does not silently finalize research direction, waive baselines, choose high-impact Research Inquiries or Inquiry Relationships, strengthen Research Claims, archive work, or end a Project without a recorded Gate.

### Team Agent Roles

Team Agent Roles perform bounded role-owned work. Early roles can include scout, planner, literature reviewer, experimenter, analyst, writer, reviewer, and decision-support. A Topic Agent Team Profile binds these roles to Workflow Stages, capabilities, profiles, tools, skills, topic constraints, and handoff rules before launch. An Agent Team Instance is the runtime team created from that profile. Each active Agent Instance should write to its own Agent Workspace by convention; peer agents may inspect declared readable files, but the engine does not enforce OS-level file permissions.

Parallel execution has two approved scopes. At the Research Topic level, the user can run multiple Research Topics in parallel, each handled by its own dedicated Agent Team Instance. At the Research Task level, a selected Agent Team Instance can distribute one task across multiple Agent Instances. Research Inquiry is not a parallel execution scope; it organizes questions, not concurrent worker ownership.

### CLI or Agent Entry Point

The engine can be used without a GUI. CLI or agent workflows can create Topic Workspaces, validate Project Manifests, inspect state, run the operator loop, and read or write Artifacts. Topic-scoped CLI commands first resolve Effective Topic Context so the command, Workspace Path Resolver, Run initialization, and future Execution Adapter command request agree on the selected Research Topic, Topic Workspace, defaults, and source metadata.

### GUI Backend and Renderer

The GUI Backend is a built-in HTTP server started through `isomer-cli`. It reports the URL that the user opens in a browser, serves the predefined GUI Renderer, reads View Manifests from Topic Workspaces, receives authenticated AG-UI Event Batches, validates GUI Component Registry entries, resolves AG-UI Render Payloads to GUI Component Instances, exposes GUI Backend APIs, and records GUI-facing metadata. The GUI Renderer renders task-specific interfaces from View Manifests, GUI Layout Specs, registered GUI Components, GUI Component Instances, and live updates produced from AG-UI Render Payloads. User actions, approvals, redirects, and comments return through defined action channels to the Operator Agent. The GUI does not own research state, team execution, or Artifact provenance.

## Components & Responsibilities

### Project Config Directory

Project-level configuration lives under the `.isomer-labs/` Project Config Directory. The required root artifact is the Project Manifest, `manifest.toml`.

The Project Manifest is responsible for:

- registering Research Topics and their Research Topic Config TOML paths
- listing known Topic Workspaces
- naming the default Research Topic when applicable
- declaring relative Topic Workspace paths
- declaring each Topic Workspace's Research Topic, selected Topic Agent Team Profiles, and selected Agent Team Instances when delegated
- storing project-level defaults
- pointing to reusable Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Profiles, Artifact Format Profile registrations, Artifact Extension registrations, and GUI Component Registry entries
- defining compatibility versions for Project Manifest and Workspace Runtime schemas

Research Topic Config files store topic-specific defaults and refs, not Runtime state. They may contain short topic statements, topic statement Artifact refs, Measurable Objective text or refs, default Research Inquiry refs, default Topic Agent Team Profile refs, default Execution Adapter refs, Capability Binding refs, Gate policy refs, Artifact Format Profile defaults, and Artifact Extension refs. They must not contain Run status, command outputs, live process ids, resolved command results, Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, credentials, tokens, API keys, passwords, or secret material.

The Project Manifest must be validated before Runs start. Missing workspace paths, duplicate topic workspace ids, paths outside the Project root, stale schema versions, missing Research Topic Config refs, and invalid default Research Topic refs are configuration errors. `.isomer-labs/local.toml` may hold untracked user-local active context for interactive use, but it is not shared project truth and must contain only candidate identity refs.

System-owned schemas and other Isomer built-in artifacts are not stored under `.isomer-labs/` by default. `isomer-cli` should query those built-ins, show supported versions, and validate project files against them.

### Workspace Runtime

Each Topic Workspace stores one Workspace Runtime plus path-bound owner records and worker surfaces. The Workspace Runtime is the persistent substrate that holds compact control-plane state, schema version, semantic path bindings, refs, and validation state across many Runs. A workspace should have a stable root path, while concrete internal paths resolve through the Topic Workspace Manifest or the `isomer-default.v1` Default Layout Profile. The default profile is:

```text
<topic-workspace>/
  topic-workspace.toml
  state.sqlite
  repos/
    topic-main/
      tmp/
  agents/
    <agent-name>/
      tmp/
  records/
    artifacts/
    tasks/
    views/
    runs/
    logs/
  runtime/
  tmp/
```

The exact layout can evolve, but the split must stay clear: SQLite stores compact control-plane facts and references; files store rich content in resolved records, repository, or agent-owned surfaces. The resolved `topic.records.runs` surface stores per-Run records for bounded execution episodes; it is part of the Workspace Runtime, not a separate workspace-level lifecycle object. `tmp/` surfaces are always ignored, local, disposable, and not shared until selected content is explicitly promoted.

### Workspace Path Resolver

All Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, and Agent Workspace paths should resolve through one Workspace Path Resolver. Research skills should request semantic surface labels or semantic targets such as Topic Workspace, task support directory, run log, analysis output Artifact, paper draft Artifact, figure Artifact, Agent Runtime state, or Agent Workspace scratch; they should not assemble paths directly or emit ordinary path TBD placeholders for surfaces covered by this resolver.

When an Effective Topic Context is available, Workspace Path Resolution consumes the validated Project, Research Topic, Topic Workspace, Research Task, Run, Agent Team Instance, and Agent Instance refs from that context. The resolver still applies its normal path precedence and does not perform independent Research Topic selection.

Resolution precedence is deterministic:

1. Recorded workspace plan for the Research Task, Run, handoff, Agent Team Instance, or Agent Instance.
2. Topic Workspace Manifest bindings.
3. Supported `ISOMER_*` environment variables exported by the Execution Adapter for the current process.
4. Project Manifest defaults.
5. Built-in `isomer-default.v1` defaults.

The built-in Topic Workspace base directory is `<project>/topic-workspaces/`. A Topic Workspace without a recorded or configured path defaults to `<project>/topic-workspaces/<topic-id>/`. Within that Topic Workspace, the path contract is semantic labels recorded in the Topic Workspace Manifest or supplied by `isomer-default.v1`; default bindings include `topic.runtime.db`, `topic.main_repo`, `topic.agents_root`, `topic.records.*`, `topic.runtime.*`, `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`. Owner-preserved task and run support directories default under `records/tasks/<task-id>/` and `records/runs/<run-id>/`; Agent Workspaces default through `agent.workspace` to `agents/<agent-name>/`.

Execution Adapters may export this bounded bootstrap context:

```text
ISOMER_PROJECT_ROOT
ISOMER_PROJECT_CONFIG_DIR
ISOMER_TOPIC_WORKSPACE_BASE_DIR
ISOMER_CURRENT_TOPIC_WORKSPACE_DIR
ISOMER_TOPIC_WORKSPACE_MANIFEST
ISOMER_EFFECTIVE_AGENT_NAME
ISOMER_CURRENT_AGENT_WORKSPACE_DIR
```

`BASE` names the directory containing many Topic Workspaces. `CURRENT` names the process-bound Topic Workspace. Adapter-provided variables are bootstrap hints, not durable path truth; the resolver should translate requested labels such as `topic.runtime.db`, `topic.records.artifacts`, `topic.records.runs`, `topic.main_repo`, `topic.tmp`, `agent.workspace`, and `agent.tmp` through the active path plan. Compatibility variables from older adapters may still be accepted when they can be mapped to semantic labels.

Every resolved path must be canonicalized before use. Paths should remain inside the Project by default; a path outside the Project root is invalid unless the recorded workspace plan or Project Manifest explicitly permits that external root. The resolver must record the effective path set and each value's source, such as `plan`, `env`, `manifest`, or `default`, in Workspace Runtime or a Provenance Record before downstream research work depends on it.

Effective Topic Context is process input, not durable research state. When a Run, Run plan, or future Execution Adapter command request consumes it, the durable record should store validated refs, source metadata, and consumed config/default versions rather than the full context snapshot.

### Agent Profile and Execution Adapter

An Agent Profile is the provider-neutral reusable description used to construct or configure an Agent Instance. It can include prompt material, skills, tool access, model posture, credential references, mailbox defaults, environment defaults, memory defaults, and launch posture through Capability Bindings or profile references.

An Execution Adapter maps Agent Profiles, Domain Agent Team Templates, Topic Agent Team Profiles, and Agent Team Instances onto a concrete execution backend. A Houmao adapter may translate Isomer concepts into Houmao specialists, project profiles, native roles, recipes, launch dossiers, and managed-agent launch commands. Other adapters should be able to provide the same Isomer contracts without implementing Houmao's internal document model.

### Agent Workspace

An Agent Workspace is a per-agent work area inside a Topic Workspace. For each team execution, the engine should construct an Agent Workspace for each participating Agent Instance that needs local runtime state, scratch files, logs, or Agent Artifacts. The owning Agent Role remains responsibility metadata, not the workspace owner.

An Agent Workspace should have an advisory Workspace Boundary. The boundary can be expressed by a `README.md`, a small manifest, or both. It declares the owning agent, intended writable paths, and paths that peer agents may read. This boundary is a collaboration contract, not a security boundary. An agent with system tools may still modify peer files, so Isomer should validate and record behavior instead of assuming hard isolation.

Under the current default profile, the launch-facing Agent Workspace layout is:

```text
<topic-workspace>/
  agents/
    <agent-name>/
      README.md
      boundary.toml
      tmp/
      isomer-managed/
        agent-owned/
          runtime/
          artifacts/
          scratch/
          public/
          logs/
```

Agents should treat peer Agent Workspaces as read-only unless a workflow explicitly assigns a repair or migration task. If a peer read becomes part of durable reasoning, the engine should record the dependency through a handoff, promoted Artifact, Evidence Item, or Provenance Record.

### Domain Agent Team Template, Topic Agent Team Profile, and Instance

A Domain Agent Team Template is a reusable user-facing template based on the research methodology of a research field. A Topic Agent Team Profile is the topic-level specialization of that template for a user's research topic. An Agent Team Instance is the runtime team created from the Topic Agent Team Profile.

Agent Roles name the participating responsibilities. Workflow defines Workflow Stages, stage ownership, handoff expectations, and Gate points. Coordination Policy defines communication, review, escalation, retry, and handoff behavior. Capability Bindings connect Agent Roles and Agent Profiles to tools, skills, model profiles, credentials, data access, communication channels, workspace permissions, or Execution Adapters.

The Topic Agent Team Profile is concrete enough for the user to review, edit, approve, and reuse, but it is not running. The Agent Team Instance should contain only runtime identity, launched Agent Instances, workspace refs, Run participation, and adapter launch refs. Lower-level runtime details can live in Workspace Runtime state, default Agent Profiles, or Operator-generated execution plans.

### Operator Control Loop

The Operator control loop manages the user-facing research loop:

1. Read the Project Manifest and active Research Topic, Research Inquiry, or Topic Workspace.
2. Load the research topic, inquiry question, context, and constraints.
3. Specialize or load a Topic Agent Team Profile and workflow.
4. Ask the user to approve or edit the Topic Agent Team Profile and workflow.
5. Launch an Agent Team Instance when delegation is needed, then dispatch bounded work to delegated Agent Instances.
6. Record outputs, prompts, tool calls, Evidence Items, Decision Records, and state transitions.
7. Generate or update View Manifests.
8. Return to the user for irreversible or claim-shaping decisions.
9. Continue, create Research Inquiries or Inquiry Relationships, pause, archive, or finalize according to recorded decisions.

The Operator Agent should prefer bounded turns and durable state over long live sessions. Recovery should use persisted state, handoffs, Gates, and Run records instead of relying on in-memory conversation state.

### Artifact and Provenance Service

The Artifact and provenance service records what happened and why. It is responsible for:

- generic Artifact Core Records with ids, Topic Workspace ids, Artifact kinds, status, locators, timestamps, and media type when known
- prompt records
- tool-call records
- handoff records
- Decision Records
- Evidence Items and claim-evidence links
- Research Claim and result references
- Run status
- timestamps and actor ids

This service should expose validation commands so the engine can detect broken refs, missing files, invalid transitions, unresolved Gates, and unsupported Research Claims.

Topic-specific Artifact Format Profiles and Artifact Extensions attach as optional refs or metadata. Artifact Format Profiles are declarative-only: they can describe media type expectations, schema refs, template refs, validation hints, renderer hints, export hints, compatibility versions, and opaque future capability refs, but they do not define executable validators, renderers, exporters, command requests, provider contracts, or adapter-specific runtime behavior. Artifact Extensions are additive topic metadata contracts and must not shadow or redefine Artifact Core Record fields.

### View Manifest Generator

The View Manifest generator creates semantic GUI descriptions from Workspace Runtime state. A View Manifest describes what the GUI should display and what actions are available. It can reference registered GUI Components and GUI Layout Specs, but it should not contain executable frontend code.

A View Manifest should cover:

- view id and title
- view type, such as Artifact list, Research Claim graph, experiment matrix, decision queue, Run timeline, result table, figure review, or next-action panel
- data sources and Artifact refs
- data bindings
- registered component refs or component selection hints
- optional GUI Layout Spec refs
- available user actions
- pending Gates and required decisions
- refresh or invalidation hints

### GUI Backend, Renderer, and Component Registry

The GUI Backend owns HTTP serving, project and workspace resolution, action channels, GUI Backend APIs, AG-UI publisher authentication, AG-UI Render Payload routing, AG-UI Event Envelope persistence, GUI Runtime State, and GUI Component Registry validation. It registers Built-in GUI Components at startup, reads project-scope agent-generated component entries, reads View Manifests, fetches referenced data, receives direct AG-UI Event Batches, and serves the GUI Renderer.

The GUI Renderer is the predefined browser-side GUI served from the backend URL. It owns layout rendering, interaction widgets, visual hierarchy, and component mounting. It renders View Manifests, GUI Layout Specs, registered GUI Components, GUI Component Instances, and live updates produced from AG-UI Render Payloads. It displays pending Gates with evidence and consequences, and it sends user actions back through the Operator Agent path.

The GUI Component Registry contains both Built-in GUI Components and project-scope agent-generated GUI Components. Every component must be registered before use. Declarative GUI Component Specs are preferred for agent-generated views. Executable GUI Components require a manifest, validation, dependency checks, sandbox or isolation policy, compatibility checks, and user approval before loading. A project-scoped approve-all policy can remove repeated per-component approval until revoked, but it does not bypass validation or publisher authentication.

Agents use GUI Components by providing AG-UI Render Payloads through the AG-UI protocol. A render payload can include data, DSL, JSON, Artifact refs, schema metadata, visualization intent, component id hints, and optional GUI Layout Spec refs. The GUI Backend picks or validates the appropriate registered component, creates or updates GUI Component Instances, and updates GUI Runtime State. GUI Backend APIs can also manipulate GUI Runtime State directly, such as replacing a layout, refreshing a view, changing filters, or updating a component instance. The GUI Renderer should reflect backend state changes immediately.

GUI Layout Specs are JSON or JSON-compatible declarations for arranging registered GUI Component Instances into panels, tabs, split views, ordered sections, and responsive regions. They reference component ids or component instance ids and should not contain executable frontend code.

The GUI must tolerate View Manifest version mismatches, missing Artifacts, unavailable actions, and stale state. It should surface these as visible workspace issues rather than hiding them.

## Data Model

The first SQLite schema should stay compact and implementation-focused. It should include these entity families:

- `topic_workspace`: topic workspace id, schema version, root path, research topic id, selected topic agent team profile refs, selected agent team instance refs, status, created time, updated time
- `workspace_runtime`: topic workspace id, runtime schema version, state db path, support directory refs, validation status, updated time
- `research_topic`: topic id, topic statement ref, optional measurable objective refs, selected topic agent team profile refs, lifecycle state, created time, updated time
- `research_inquiry`: inquiry id, research topic id, question ref, lifecycle state, status, created time, updated time
- `research_inquiry_relationship`: relationship id, research topic id, from inquiry id, to inquiry id, relation type, rationale ref, status, created time, updated time
- `research_task`: research task id, research topic id, research inquiry id, topic workspace id, task handler id, participating agent instance refs, selected topic agent team profile id, selected agent team instance id, status, summary ref
- `domain_agent_team_template`: template id, research field, method family, source path, status, compatibility version
- `topic_agent_team_profile`: profile id, template id, research topic ref, source path, specialization refs, status, approved flag
- `agent_team_instance`: instance id, profile id, source path, runtime refs, status, active flag
- `agent_role`: agent role id, domain agent team template id or topic agent team profile id or agent team instance id, role kind, display name, responsibility ref
- `agent_profile`: agent profile id, source path, profile kind, instruction refs, capability refs, status
- `coordination_policy`: policy id, domain agent team template id or topic agent team profile id or agent team instance id, communication mode, handoff rules ref, review rules ref, escalation rules ref
- `capability_binding`: binding id, domain agent team template id or topic agent team profile id or agent team instance id, agent role id or agent profile id, capability kind, capability ref, scope
- `workflow_stage`: stage id, domain agent team template id or topic agent team profile id or agent team instance id, ordinal, owner agent role id, gate policy
- `run`: run id, topic workspace id, research task id, research topic id, research inquiry id, task handler id, topic agent team profile id, agent team instance id, status, current stage, started time, finished time
- `handoff`: handoff id, run id, from agent role id, to agent role id, stage id, status, attempt count, due time
- `agent_instance`: agent instance id, agent profile id, agent team instance id, run id, agent role id, execution adapter id, provider instance ref, status
- `agent_workspace`: agent workspace id, topic workspace id, agent team instance id, run id, agent role id, agent instance id, root path, status, boundary ref
- `agent_runtime`: agent runtime id, agent workspace id, run id, status, prompt refs, tool trace refs, log path
- `workspace_boundary`: boundary id, agent workspace id, declaration path, readable path rules, owner write path rules, advisory flag
- `artifact`: artifact id, topic workspace id, owner agent workspace id when applicable, kind, path, content type, producing run or stage, promotion state
- `decision_record`: decision id, run id, stage id, kind, selected option, rationale artifact ref, user gate flag
- `gate`: gate id, run id, decision id, status, required actor, consequence summary
- `prompt_record`: prompt id, run id, agent role id, agent instance id, path, model or runner ref
- `tool_call_record`: tool call id, run id, agent role id, agent instance id, tool name, input ref, output ref, status
- `research_claim`: claim id, run id, status, text ref
- `evidence_item`: evidence id, topic workspace id, source kind, source ref, summary ref
- `claim_evidence_link`: link id, claim id, evidence id, relation, resolved flag
- `finding`: finding id, research inquiry id, status, summary ref, primary evidence id
- `view_manifest`: view id, topic workspace id, path, schema version, component refs, layout spec refs, status
- `gui_component`: component id, project id, source path, manifest path, component kind, registration source, dependency refs, build output ref, sandbox policy, producer agent instance id, approval state, compatibility version, status
- `gui_component_instance`: instance id, component id, project id, topic workspace id, run id, view id, render payload id, layout slot id, visible state ref, lifecycle status
- `gui_component_approval_policy`: project id, approve-all flag, enabled by actor id, enabled time, revoked time, status
- `gui_runtime_state`: runtime state id, project id, topic workspace id, session id, active view id, layout spec id, component instance refs, filter state ref, selection state ref, connection status, updated time
- `gui_layout_spec`: layout spec id, project id, topic workspace id, path or inline ref, schema version, component instance refs, status
- `ag_ui_render_payload`: payload id, project id, topic workspace id, run id, publisher agent instance id, component hint, data refs, schema refs, layout spec refs, payload ref when explicitly retained, status
- `ag_ui_event_envelope`: envelope id, project id, topic workspace id, run id, agent team instance id, agent instance id, component id, artifact refs, timestamp, status, retention policy, payload ref when explicitly retained

Rich content should stay outside SQLite unless it is a short label, status, id, path, timestamp, or scalar value needed for validation and scheduling.

## Data Flow

```text
User goal and context
        |
        v
.isomer-labs/manifest.toml resolves Research Topic, Research Inquiry, Topic Workspace, Topic Agent Team Profile, and GUI registry
        |
        v
Operator Agent loads Workspace Runtime state and specializes or selects a Topic Agent Team Profile
        |
        v
User approves, edits, or replaces Topic Agent Team Profile/workflow
        |
        v
Execution Adapter launches or resolves Agent Team Instance and Agent Instances
        |
        v
Operator Agent dispatches bounded work to delegated Agent Instances
        |
        v
Engine constructs or resolves Agent Workspaces and advisory boundaries
        |
        v
Agent Instances produce Artifacts, prompts, tool calls, and results
        |
        +------------------------------+
        |                              |
        v                              v
Workspace Runtime stores compact       GUI Backend receives authenticated
state in SQLite and rich per-Run       AG-UI Event Batches with
files on disk                          AG-UI Render Payloads
                                       |
                                       v
                              GUI Backend resolves registered
                              GUI Components, updates Component
                              Instances, Layout Specs, and
                              GUI Runtime State, and persists
                              AG-UI Event Envelopes
        |
        v
Engine emits or updates View Manifests
        |
        v
GUI Backend and Renderer show View Manifests, layout, AG-UI Render Payload updates, and pending Gates
        |
        v
User actions return through the Operator Agent
        |
        v
User steers, creates Research Inquiries or Inquiry Relationships, pauses, archives, or continues
```

## Error Handling & Edge Cases

Project Manifest validation must catch invalid workspace references before the engine opens a Topic Workspace. Workspace paths should be relative to the project root unless the project explicitly allows another rule. Paths outside the project root should be rejected by default.

State migrations must be explicit. If a workspace schema is too old or too new, the engine should stop with a clear message rather than partially opening it.

Invalid Domain Agent Team Templates, Topic Agent Team Profiles, or Agent Team Instances should fail before execution. Examples include missing Operator Agent binding, unbound stage owner, unknown Capability Binding, duplicate Agent Role ids, missing research-topic specialization, and Gate policies that reference missing Workflow Stages.

Adapter mapping errors should fail before launch. A Topic Agent Team Profile may be valid while a selected Execution Adapter cannot construct the required Agent Team Instance or Agent Instances because an Agent Profile, Capability Binding, credential reference, launch posture, or tool access is missing. The error should name the neutral Isomer concept first and provider-specific details second.

Unresolved Gates should block only the actions they govern. For example, a pending baseline waiver Gate should block downstream experiment synthesis but should not prevent the user from inspecting Artifacts or editing team configuration.

Failed handoffs should become durable state. The operator can retry, reroute, ask the user, or mark the stage blocked. It should not spin in a hidden retry loop.

Agent Workspace boundaries are advisory. If validation detects that an agent wrote into a peer workspace without an explicit repair or migration task, the engine should record a workspace issue or Provenance Record. It should not claim that filesystem controls made the write impossible.

Contradictory Evidence Items should block Research Claim strengthening until resolved. A Research Claim can remain open, be weakened, be withdrawn, or be marked supported only after the contradiction has a recorded resolution.

Missing Artifact files should be visible validation failures. The database should keep the ref, but views and reports should mark the Artifact missing until repaired or superseded.

Invalid GUI Component Registry entries should fail before component load. Missing manifests, invalid dependency declarations, unsupported compatibility versions, failed sandbox policy checks, or missing approval should surface as GUI issues and Operator Agent notifications.

Direct AG-UI Event Batches from unknown publishers, malformed AG-UI Render Payloads, or unregistered component ids should be rejected. The GUI Backend should persist the rejection envelope when useful for audit, but it should not render untrusted executable component output.

Invalid GUI Layout Specs should fail before the GUI Renderer applies them. Unknown component instance refs, unregistered component ids, unsupported layout schema versions, conflicting slot ids, or non-JSON executable layout content should surface as GUI issues and Operator Agent notifications.

GUI Backend API calls should be authenticated and scoped to a Project, Topic Workspace, Run, Agent Team Instance, Agent Instance, or Operator Agent as appropriate. An API call that updates GUI Runtime State must not bypass Gate resolution or mutate canonical research state directly.

Full AG-UI payload retention should be disabled by default. If a user explicitly enables it, the retention posture should be visible through the Operator Agent and GUI because payloads can contain sensitive research context or bulky generated UI data.

## Testing Strategy

Early tests should focus on contracts that will be expensive to change later:

- manifest parsing and path normalization
- Research Topic Config registration and validation
- Effective Topic Context resolution and source reporting
- topic-context identity environment variable validation
- Topic Workspace discovery from `.isomer-labs/manifest.toml`
- Workspace Runtime creation, schema versioning, and support directory validation
- Research Topic to Topic Workspace binding plus Research Inquiry and Research Task lifecycle state
- topic-level parallel execution across multiple Research Topics with different dedicated Agent Team Instances, and task-level parallel execution across Agent Instances
- rejection of workspace paths outside the project root
- Domain Agent Team Template and Topic Agent Team Profile validation for Agent Roles, Workflow Stages, Coordination Policy, Capability Bindings, and required topic specialization
- Domain Agent Team Template specialization into Topic Agent Team Profile records
- Topic Agent Team Profile launch into Agent Team Instance records
- Execution Adapter mapping from Agent Profiles to Agent Instances
- Agent Workspace layout creation and boundary declaration parsing
- advisory peer-read behavior, peer-write issue detection, and Agent Artifact promotion
- SQLite migration creation and version checks
- Artifact ref validation
- generic Artifact Core Record fallback when Artifact Format Profiles or Artifact Extensions are missing, unsupported, disabled, or unknown
- Gate lifecycle transitions
- handoff status transitions and retry limits
- Research Claim and Evidence Item consistency rules
- View Manifest schema validation
- GUI Layout Spec validation and component-instance layout resolution
- GUI Component Registry validation, executable component approval, and approve-all revocation behavior
- AG-UI Render Payload routing, component resolution, GUI Runtime State updates, GUI Backend API authorization, AG-UI Event Envelope persistence, payload-retention opt-in behavior, and publisher authentication
- end-to-end creation of a minimal Topic Workspace, Research Topic, Research Inquiry, Topic Agent Team Profile, Agent Team Instance, Run, Artifact, Gate, and View Manifest

These tests can start with `unittest` under `tests/unit/`, with filesystem and SQLite checks promoted to `tests/integration/` when needed.

## Key Constraints

- Project state discovery starts from `.isomer-labs/manifest.toml`.
- The Project Manifest registers Research Topic Config files and Topic Workspaces.
- Research Topic Config files store topic defaults and refs, not Workspace Runtime state, command outputs, research records, Artifact contents, or secrets.
- Effective Topic Context is resolved process input for topic-scoped CLI behavior and path resolution, not a durable lifecycle object.
- Durable Run records store validated refs, source metadata, and consumed config/default versions rather than full Effective Topic Context snapshots.
- Research Topics are root research problems or investigation intents; Research Inquiries are questions under a topic.
- Research Inquiry is not a parallel execution scope.
- Topic Workspaces are project-local directories referenced by the Project Manifest.
- Each Topic Workspace is scoped to one Research Topic; Research Tasks inside it record task handlers.
- Topic-level parallel execution uses multiple Research Topics, each with one dedicated Agent Team Instance; task-level parallel execution distributes one Research Task across multiple Agent Instances inside one selected Agent Team Instance.
- Topic Workspaces do not contain a workspace-local `teams/` directory.
- Domain Agent Team Templates are reusable research-field method templates.
- Topic Agent Team Profiles are topic-level specializations of Domain Agent Team Templates, and they are not running teams.
- Agent Team Instances are runtime teams created from Topic Agent Team Profiles.
- Every non-operator task Agent Instance belongs to an Agent Team Instance.
- Agent Profiles and Agent Instances are core Isomer concepts; Houmao specialists, profiles, roles, recipes, launch dossiers, and managed agents are adapter details.
- Team execution should construct Agent Workspaces so agents can own local runtime state and Agent Artifacts without relying on one shared scratch area.
- Agent Workspace boundaries and Peer Read Access are advisory contracts, not filesystem-grade access control.
- Gates apply to irreversible or claim-shaping decisions, not every stage boundary.
- Human user actions enter through the Operator Agent.
- The engine emits View Manifests; the GUI Backend and Renderer render them.
- The GUI Backend serves the predefined browser-side GUI Renderer from a URL reported by `isomer-cli`.
- Built-in GUI Components and agent-generated GUI Components must be registered before use.
- Authenticated Agent Team Instance members may publish direct AG-UI Event Batches for live GUI updates.
- Agents use GUI Components by sending AG-UI Render Payloads with data, DSL, JSON, refs, component hints, or layout refs; they do not manipulate browser components directly.
- The GUI Backend resolves AG-UI Render Payloads to registered GUI Components and GUI Component Instances.
- GUI Backend APIs can manipulate GUI Runtime State, and the GUI Renderer should reflect those changes immediately.
- GUI Layout Specs are JSON or JSON-compatible declarations for arranging registered GUI Component Instances.
- Direct AG-UI Event Batches are live traffic, not canonical research state.
- AG-UI Event Envelopes are persisted by default; full payload content requires explicit user instruction.
- Executable GUI Components must be registered, validated, sandboxed or isolated according to policy, and approved before loading.
- Project-scoped approve-all can remove repeated Executable GUI Component approval until revoked, but it does not bypass validation or publisher authentication.
- SQLite stores compact control-plane state; files store rich Artifacts.
- Artifact Core Records stay generic and minimal; Artifact Format Profiles and Artifact Extensions remain optional declarative refs or metadata.
- The Operator Agent coordinates team work and mediates between user intent, Agent Instance execution, durable state, and GUI-facing views.
- The first implementation should avoid a fully declarative graph engine until the manifested workspace loop proves useful.

## Open Questions

- Exact TOML schema for `.isomer-labs/manifest.toml`.
- Exact Research Topic Config schema evolution policy.
- Exact Topic Workspace directory layout.
- Initial Domain Agent Team Template, Topic Agent Team Profile, and Agent Team Instance file formats.
- Initial View Manifest schema and supported view types.
- GUI Component Registry schema, GUI Runtime State schema, GUI Layout Spec schema, and Executable GUI Component sandbox contract.
- AG-UI Render Payload contract, AG-UI Event Envelope schema, and payload-retention controls.
- Migration command shape and schema-version policy.
- Exact representation for selected Topic Agent Team Profile refs, selected Agent Team Instance refs, task-handler refs, participating Agent Instance refs, and Research Task ids inside Project Manifest and Workspace Runtime.
- How much DeepScientist skill and artifact structure should be adapted into initial workspace templates.
