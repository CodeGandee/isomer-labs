# Manifested Workspace Engine Design

## Status

Approved on 2026-06-15.

## Evidence

This design is based on the project goal in `context/design/project-goal.md` and the accepted exploration ADRs under `.imsight-arts/project-explore/adrs/`.

Relevant project-goal evidence:

- Isomer Labs should be an interactive, semi-automatic research-conduction platform where a human user defines goals, supplies context, chooses constraints, and steers critical decisions.
- Multi-agent research teams are the core research engine.
- Users must be able to choose predefined teams or define custom teams.
- The Operator Agent coordinates team activity, asks for user decisions, translates intent into team instructions, and presents work products.
- The platform should expose goals, teams, task plans, Artifacts, decisions, prompts, tool calls, and research state.
- The research engine and GUI should be decoupled.
- Generated GUI views should visualize task-specific Artifacts, state, and decision points.
- Project state can live inside a user-owned project instead of a system-owned workspace.

Accepted ADRs:

- `0001-config-manifest-references-project-workspaces.md`
- `0002-team-abstraction-roles-workflow-bindings.md`
- `0003-human-gates-for-irreversible-or-claim-shaping-decisions.md`
- `0004-engine-emits-view-manifests-for-task-specific-gui.md`
- `0005-sqlite-control-plane-plus-file-artifacts.md`
- `0006-manifested-workspace-engine.md`

## Overview

Isomer Labs uses a manifested workspace engine as its primary architecture. The Project Manifest at `.isomer-labs/manifest.toml` is the discovery authority for project configuration and project-local Isomer Workspaces. A Research Thread is the user-facing line of inquiry; by default, each Research Thread is backed by one Isomer Workspace. Isomer Workspaces may live in arbitrary directories inside the user-owned Project, but each workspace must be declared in the Project Manifest before the engine treats it as managed state.

Each Isomer Workspace owns its Workspace Runtime and research outputs. Compact control-plane state lives in SQLite. Rich Artifacts remain ordinary files, such as Markdown notes, JSON outputs, logs, code, figures, reports, and View Manifests. During team execution, each concrete Agent Instance receives an Agent Workspace for agent-owned runtime state and Agent Artifacts. These workspaces create advisory ownership boundaries, not filesystem-grade access control. The Operator Agent is the coordination boundary between the user, Specialist Agents, durable state, and GUI-facing views.

Isomer can use Houmao as an example Research Engine Adapter, especially for concepts such as specialists, project profiles, native roles, recipes, launch dossiers, and managed agents. These concepts should inform adapter design without becoming core Isomer terms. The core architecture should describe provider-neutral Agent Definitions, Agent Instances, Bindings, Runs, and Agent Workspaces.

The GUI is not the engine. The engine remains useful through command-line and agent workflows. When a GUI is present, it reads engine-produced View Manifests and renders task-specific views for Artifacts, Gates, Runs, Research Claims, result tables, and next actions.

## Actors & Entry Points

### Human User

The human user defines the research goal, provides context, sets constraints, approves or edits teams and workflows, resolves gated decisions, and steers active Research Threads. The user can pause, create Research Branches, resume, archive, override team composition, or alter workflow structure.

### Operator Agent

The Operator Agent is the user-controlled coordinator. It turns user intent into executable team instructions, proposes Team Definitions and workflows, dispatches work to Specialist Agents, records decisions, and asks the user for input when a decision is irreversible or claim-shaping.

The Operator Agent does not silently finalize research direction, waive baselines, choose high-impact Research Branches, strengthen Research Claims, archive work, or end a Project without a recorded Gate.

### Specialist Agents

Specialist Agents perform role-owned work. Early Roles can include scout, planner, literature reviewer, experimenter, analyst, writer, reviewer, and decision-support specialist. A Team Definition binds these Roles to Workflow Stages, runners, tools, skills, and handoff rules. Each active Agent Instance should write to its own Agent Workspace by convention; peer agents may inspect declared readable files, but the engine does not enforce OS-level file permissions.

### CLI or Agent Entry Point

The engine can be used without a GUI. CLI or agent workflows can create Isomer Workspaces, validate Project Manifests, inspect state, run the operator loop, and read or write Artifacts.

### GUI Renderer

The GUI Renderer reads View Manifests from an Isomer Workspace and renders task-specific interfaces. It sends user actions, approvals, redirects, and comments back to the engine through defined action channels. It does not own research state, team execution, or Artifact provenance.

## Components & Responsibilities

### Project Config Directory

Project-level configuration lives under the `.isomer-labs/` Project Config Directory. The required root artifact is the Project Manifest, `manifest.toml`.

The Project Manifest is responsible for:

- listing known Isomer Workspaces
- naming the active Research Thread or active Isomer Workspace when applicable
- declaring relative Isomer Workspace paths
- storing project-level defaults
- pointing to reusable Team Definitions when they are shared across Isomer Workspaces
- defining compatibility versions for Project Manifest and Workspace Runtime schemas

The Project Manifest must be validated before Runs start. Missing workspace paths, duplicate workspace ids, paths outside the Project root, stale schema versions, and invalid active-workspace references are configuration errors.

### Workspace Runtime

Each Isomer Workspace stores Workspace Runtime state and Artifacts. A workspace should have a stable root path and a small internal layout, for example:

```text
<workspace>/
  state.sqlite
  artifacts/
  agents/
  teams/
  views/
  runs/
  logs/
```

The exact layout can evolve, but the split must stay clear: SQLite stores compact control-plane facts and references; files store rich content. `runs/` stores bounded execution episodes inside the Research Thread backed by the workspace.

### Agent Definition and Engine Adapter

An Agent Definition is the provider-neutral pre-launch description used to construct an Agent Instance. It can include prompt material, skills, tool lane, setup, model posture, credential references, mailbox defaults, environment defaults, and launch posture through Bindings or profile references.

A Research Engine Adapter maps Agent Definitions and Team Definitions onto a concrete execution backend. A Houmao adapter may translate Isomer concepts into Houmao specialists, project profiles, native roles, recipes, launch dossiers, and managed-agent launch commands. Other adapters should be able to provide the same Isomer contracts without implementing Houmao's internal document model.

### Agent Workspace

An Agent Workspace is a per-agent work area inside an Isomer Workspace. For each team execution, the engine should construct an Agent Workspace for each participating Agent Instance that needs local runtime state, scratch files, logs, or Agent Artifacts. The owning Role remains responsibility metadata, not the workspace owner.

An Agent Workspace should have an advisory Workspace Boundary. The boundary can be expressed by a `README.md`, a small manifest, or both. It declares the owning agent, intended writable paths, and paths that peer agents may read. This boundary is a collaboration contract, not a security boundary. An agent with system tools may still modify peer files, so Isomer should validate and record behavior instead of assuming hard isolation.

One possible layout is:

```text
<workspace>/
  agents/
    <agent-instance-id>/
      README.md
      boundary.toml
      runtime/
      artifacts/
      scratch/
      logs/
```

Agents should treat peer Agent Workspaces as read-only unless a workflow explicitly assigns a repair or migration task. If a peer read becomes part of durable reasoning, the engine should record the dependency through a handoff, promoted Artifact, Evidence Item, or Provenance Record.

### Team Definition

A Team Definition includes Roles, workflow, and Bindings.

Roles name the participating agents and their responsibilities. Workflow defines Workflow Stages, stage ownership, handoff expectations, and Gate points. Bindings connect Roles to concrete runners, tools, skills, model profiles, or execution adapters.

The Team Definition is concrete enough to run and inspect, but it should not require users to write a full execution graph. Lower-level runtime details can live in Workspace Runtime state, default profiles, or Operator-generated execution plans.

### Operator Control Loop

The operator control loop manages the user-facing research loop:

1. Read the Project Manifest and active Research Thread or Isomer Workspace.
2. Load the research goal, context, and constraints.
3. Propose or load a Team Definition and workflow.
4. Ask the user to approve or edit the team and workflow.
5. Dispatch bounded work to Specialist Agents.
6. Record outputs, prompts, tool calls, Evidence Items, Decision Records, and state transitions.
7. Generate or update View Manifests.
8. Return to the user for irreversible or claim-shaping decisions.
9. Continue, create Research Branches, pause, archive, or finalize according to recorded decisions.

The Operator Agent should prefer bounded turns and durable state over long live sessions. Recovery should use persisted state, handoffs, Gates, and Run records instead of relying on in-memory conversation state.

### Artifact and Provenance Service

The Artifact and provenance service records what happened and why. It is responsible for:

- Artifact ids and paths
- prompt records
- tool-call records
- handoff records
- Decision Records
- Evidence Items and claim-evidence links
- Research Claim and result references
- Run status
- timestamps and actor ids

This service should expose validation commands so the engine can detect broken refs, missing files, invalid transitions, unresolved Gates, and unsupported Research Claims.

### View Manifest Generator

The View Manifest generator creates semantic GUI specifications from Workspace Runtime state. A View Manifest describes what the GUI should display and what actions are available, not how the GUI should implement pixels or components.

A View Manifest should cover:

- view id and title
- view type, such as Artifact list, Research Claim graph, experiment matrix, decision queue, Run timeline, result table, figure review, or next-action panel
- data sources and Artifact refs
- data bindings
- available user actions
- pending Gates and required decisions
- refresh or invalidation hints

### GUI Renderer

The GUI Renderer owns layout, interaction widgets, visual hierarchy, and rendering. It reads View Manifests, fetches referenced data, displays pending Gates with evidence and consequences, and sends user actions back to the engine.

The GUI must tolerate View Manifest version mismatches, missing Artifacts, unavailable actions, and stale state. It should surface these as visible workspace issues rather than hiding them.

## Data Model

The first SQLite schema should stay compact and implementation-focused. It should include these entity families:

- `workspace`: workspace id, schema version, root path, status, created time, updated time
- `research_thread`: thread id, workspace id, research goal ref, goal kind, lifecycle state, active research branch id, created time, updated time
- `research_branch`: branch id, research thread id, parent branch id, status, hypothesis ref, created time, updated time
- `team`: team id, source path, status, active flag
- `role`: role id, team id, role kind, display name, binding ref
- `agent_definition`: agent definition id, source path, adapter kind, profile refs, credential refs, prompt refs, status
- `workflow_stage`: stage id, team id, ordinal, owner role, gate policy
- `run`: run id, research thread id, research branch id, team id, status, current stage, started time, finished time
- `handoff`: handoff id, run id, from role, to role, stage id, status, attempt count, due time
- `agent_instance`: agent instance id, agent definition id, team id, run id, role id, adapter kind, provider instance ref, status
- `agent_workspace`: agent workspace id, workspace id, team id, run id, role id, agent instance id, root path, status, boundary ref
- `agent_runtime`: agent runtime id, agent workspace id, run id, status, prompt refs, tool trace refs, log path
- `workspace_boundary`: boundary id, agent workspace id, declaration path, readable path rules, owner write path rules, advisory flag
- `artifact`: artifact id, workspace id, owner agent workspace id when applicable, kind, path, content type, producing run or stage, promotion state
- `decision_record`: decision id, run id, stage id, kind, selected option, rationale artifact ref, user gate flag
- `gate`: gate id, run id, decision id, status, required actor, consequence summary
- `prompt_record`: prompt id, run id, role id, agent instance id, path, model or runner ref
- `tool_call_record`: tool call id, run id, role id, agent instance id, tool name, input ref, output ref, status
- `research_claim`: claim id, run id, status, text ref
- `evidence_item`: evidence id, workspace id, source kind, source ref, summary ref
- `claim_evidence_link`: link id, claim id, evidence id, relation, resolved flag
- `finding`: finding id, research thread id, status, summary ref, primary evidence id
- `view_manifest`: view id, workspace id, path, schema version, status

Rich content should stay outside SQLite unless it is a short label, status, id, path, timestamp, or scalar value needed for validation and scheduling.

## Data Flow

```text
User goal and context
        |
        v
.isomer-labs/manifest.toml resolves Research Thread and Isomer Workspace
        |
        v
Operator loads Workspace Runtime state and proposes team/workflow
        |
        v
User approves, edits, or replaces team/workflow
        |
        v
Research Engine Adapter creates or resolves Agent Instances
        |
        v
Operator dispatches bounded work to Specialist Agents
        |
        v
Engine constructs or resolves Agent Workspaces and advisory boundaries
        |
        v
Specialist Agents produce Artifacts, prompts, tool calls, and results
        |
        v
Workspace Runtime records compact state in SQLite and rich files on disk
        |
        v
Engine emits or updates View Manifests
        |
        v
GUI renders task-specific views and pending Gates
        |
        v
User steers, creates Research Branches, pauses, archives, or continues
```

## Error Handling & Edge Cases

Project Manifest validation must catch invalid workspace references before the engine opens an Isomer Workspace. Workspace paths should be relative to the project root unless the project explicitly allows another rule. Paths outside the project root should be rejected by default.

State migrations must be explicit. If a workspace schema is too old or too new, the engine should stop with a clear message rather than partially opening it.

Invalid Team Definitions should fail before execution. Examples include missing Operator Agent Role, unbound stage owner, unknown runner Binding, duplicate Role ids, and Gate policies that reference missing Workflow Stages.

Adapter mapping errors should fail before launch. A Team Definition may be valid while a selected Research Engine Adapter cannot construct the required Agent Instances because an Agent Definition, credential reference, profile, launch posture, or tool lane is missing. The error should name the neutral Isomer concept first and provider-specific details second.

Unresolved Gates should block only the actions they govern. For example, a pending baseline waiver Gate should block downstream experiment synthesis but should not prevent the user from inspecting Artifacts or editing team configuration.

Failed handoffs should become durable state. The operator can retry, reroute, ask the user, or mark the stage blocked. It should not spin in a hidden retry loop.

Agent Workspace boundaries are advisory. If validation detects that an agent wrote into a peer workspace without an explicit repair or migration task, the engine should record a workspace issue or Provenance Record. It should not claim that filesystem controls made the write impossible.

Contradictory Evidence Items should block Research Claim strengthening until resolved. A Research Claim can remain open, be weakened, be withdrawn, or be marked supported only after the contradiction has a recorded resolution.

Missing Artifact files should be visible validation failures. The database should keep the ref, but views and reports should mark the Artifact missing until repaired or superseded.

## Testing Strategy

Early tests should focus on contracts that will be expensive to change later:

- manifest parsing and path normalization
- Isomer Workspace discovery from `.isomer-labs/manifest.toml`
- Research Thread lifecycle state and workspace binding
- rejection of workspace paths outside the project root
- Team Definition validation for Roles, Workflow Stages, and Bindings
- Research Engine Adapter mapping from Agent Definitions to Agent Instances
- Agent Workspace layout creation and boundary declaration parsing
- advisory peer-read behavior, peer-write issue detection, and Agent Artifact promotion
- SQLite migration creation and version checks
- Artifact ref validation
- Gate lifecycle transitions
- handoff status transitions and retry limits
- Research Claim and Evidence Item consistency rules
- View Manifest schema validation
- end-to-end creation of a minimal Isomer Workspace, Research Thread, team, Run, Artifact, Gate, and View Manifest

These tests can start with `unittest` under `tests/unit/`, with filesystem and SQLite checks promoted to `tests/integration/` when needed.

## Key Constraints

- Project state discovery starts from `.isomer-labs/manifest.toml`.
- Research Threads are the user-facing research lifecycle concept.
- Isomer Workspaces are project-local directories referenced by the Project Manifest.
- Team Definitions include Roles, workflow, and Bindings.
- Agent Definitions and Agent Instances are core Isomer concepts; Houmao specialists, profiles, roles, recipes, launch dossiers, and managed agents are adapter details.
- Team execution should construct Agent Workspaces so agents can own local runtime state and Agent Artifacts without relying on one shared scratch area.
- Agent Workspace boundaries and Peer Read Access are advisory contracts, not filesystem-grade access control.
- Gates apply to irreversible or claim-shaping decisions, not every stage boundary.
- The engine emits View Manifests; the GUI renders them.
- SQLite stores compact control-plane state; files store rich Artifacts.
- The Operator Agent coordinates team work and mediates between user intent, Specialist Agent execution, durable state, and GUI-facing views.
- The first implementation should avoid a fully declarative graph engine until the manifested workspace loop proves useful.

## Open Questions

- Exact TOML schema for `.isomer-labs/manifest.toml`.
- Exact Isomer Workspace directory layout.
- Initial Team Definition file format.
- Initial View Manifest schema and supported view types.
- Migration command shape and schema-version policy.
- Whether reusable Team Definitions should live under `.isomer-labs/teams/`, inside Isomer Workspaces, or both.
- How much DeepScientist skill and artifact structure should be adapted into initial workspace templates.
