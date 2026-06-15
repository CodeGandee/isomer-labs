# Manifested Workspace Engine Design

## Status

Approved on 2026-06-15.

## Evidence

This design is based on the project goal in `context/design/project-goal.md` and the accepted exploration ADRs under `.imsight-arts/project-explore/adrs/`.

Relevant project-goal evidence:

- Isomer Labs should be an interactive, semi-automatic research-conduction platform where a human user defines goals, supplies context, chooses constraints, and steers critical decisions.
- Multi-agent research teams are the core research engine.
- Users must be able to choose predefined teams or define custom teams.
- The operator agent coordinates team activity, asks for user decisions, translates intent into team instructions, and presents work products.
- The platform should expose goals, teams, task plans, artifacts, decisions, prompts, tool calls, and research state.
- The research engine and GUI should be decoupled.
- Generated GUI views should visualize task-specific artifacts, state, and decision points.
- Project state can live inside a user-owned project instead of a system-owned workspace.

Accepted ADRs:

- `0001-config-manifest-references-project-workspaces.md`
- `0002-team-abstraction-roles-workflow-bindings.md`
- `0003-human-gates-for-irreversible-or-claim-shaping-decisions.md`
- `0004-engine-emits-view-manifests-for-task-specific-gui.md`
- `0005-sqlite-control-plane-plus-file-artifacts.md`
- `0006-manifested-workspace-engine.md`

## Overview

Isomer Labs uses a manifested workspace engine as its primary architecture. A project-level `.isomer-labs/manifest.toml` file is the discovery authority for project configuration and project-local research workspaces. Workspaces may live in arbitrary directories inside the user-owned project, but each workspace must be declared in the manifest before the engine treats it as managed state.

Each workspace owns its execution state and research outputs. Compact control-plane state lives in SQLite. Rich artifacts remain ordinary files, such as Markdown notes, JSON outputs, logs, code, figures, reports, and view manifests. The operator agent is the coordination boundary between the user, specialist agents, durable state, and GUI-facing views.

The GUI is not the engine. The engine remains useful through command-line and agent workflows. When a GUI is present, it reads engine-produced view manifests and renders task-specific views for artifacts, decision gates, runs, claims, result tables, and next actions.

## Actors & Entry Points

### Human User

The human user defines the research goal, provides context, sets constraints, approves or edits teams and workflows, resolves gated decisions, and steers active work. The user can pause, branch, resume, archive, override team composition, or alter workflow structure.

### Operator Agent

The operator agent is the user-controlled coordinator. It turns user intent into executable team instructions, proposes team and workflow definitions, dispatches work to specialists, records decisions, and asks the user for input when a decision is irreversible or claim-shaping.

The operator agent does not silently finalize research direction, waive baselines, choose high-impact routes, strengthen claims, archive work, or end a project without a recorded human gate.

### Specialist Agents

Specialist agents perform role-owned work. Early roles can include scout, planner, literature reviewer, experimenter, analyst, writer, reviewer, and decision-support specialist. A team definition binds these roles to workflow stages, runners, tools, skills, and handoff rules.

### CLI or Agent Entry Point

The engine can be used without a GUI. CLI or agent workflows can create workspaces, validate manifests, inspect state, run the operator loop, and read or write artifacts.

### GUI Renderer

The GUI renderer reads view manifests from a workspace and renders task-specific interfaces. It sends user actions, approvals, redirects, and comments back to the engine through defined action channels. It does not own research state, team execution, or artifact provenance.

## Components & Responsibilities

### Project Config

Project config lives under `.isomer-labs/`. The required root artifact is `manifest.toml`.

The manifest is responsible for:

- listing known workspaces
- naming the active workspace when applicable
- declaring relative workspace paths
- storing project-level defaults
- pointing to reusable team definitions when they are shared across workspaces
- defining compatibility versions for manifest and workspace schemas

The manifest must be validated before runs start. Missing workspace paths, duplicate workspace ids, paths outside the project root, stale schema versions, and invalid active-workspace references are configuration errors.

### Workspace Runtime

Each workspace stores runtime state and artifacts. A workspace should have a stable root path and a small internal layout, for example:

```text
<workspace>/
  state.sqlite
  artifacts/
  teams/
  views/
  runs/
  logs/
```

The exact layout can evolve, but the split must stay clear: SQLite stores compact control-plane facts and references; files store rich content.

### Team Definition

A team definition includes roles, workflow, and bindings.

Roles name the participating agents and their responsibilities. Workflow defines stages, stage ownership, handoff expectations, and gate points. Bindings connect roles to concrete runners, tools, skills, model profiles, or execution adapters.

The team definition is concrete enough to run and inspect, but it should not require users to write a full execution graph. Lower-level runtime details can live in workspace state, default profiles, or operator-generated execution plans.

### Operator Control Loop

The operator control loop manages the user-facing research loop:

1. Read the project manifest and active workspace.
2. Load the research goal, context, and constraints.
3. Propose or load a team definition and workflow.
4. Ask the user to approve or edit the team and workflow.
5. Dispatch bounded work to specialist agents.
6. Record outputs, prompts, tool calls, evidence, decisions, and state transitions.
7. Generate or update view manifests.
8. Return to the user for irreversible or claim-shaping decisions.
9. Continue, branch, pause, archive, or finalize according to recorded decisions.

The operator should prefer bounded turns and durable state over long live sessions. Recovery should use persisted state, handoffs, gates, and run records instead of relying on in-memory conversation state.

### Artifact and Provenance Service

The artifact and provenance service records what happened and why. It is responsible for:

- artifact ids and paths
- prompt records
- tool-call records
- handoff records
- decision records
- evidence links
- claim and result references
- run status
- timestamps and actor ids

This service should expose validation commands so the engine can detect broken refs, missing files, invalid transitions, unresolved gates, and unsupported claims.

### View Manifest Generator

The view manifest generator creates semantic GUI specifications from workspace state. A view manifest describes what the GUI should display and what actions are available, not how the GUI should implement pixels or components.

A view manifest should cover:

- view id and title
- view type, such as artifact list, claim graph, experiment matrix, decision queue, run timeline, result table, figure review, or next-action panel
- data sources and artifact refs
- data bindings
- available user actions
- pending gates and required decisions
- refresh or invalidation hints

### GUI Renderer

The GUI renderer owns layout, interaction widgets, visual hierarchy, and rendering. It reads view manifests, fetches referenced data, displays pending gates with evidence and consequences, and sends user actions back to the engine.

The GUI must tolerate view-manifest version mismatches, missing artifacts, unavailable actions, and stale state. It should surface these as visible workspace issues rather than hiding them.

## Data Model

The first SQLite schema should stay compact and implementation-focused. It should include these entity families:

- `workspace`: workspace id, schema version, root path, status, created time, updated time
- `team`: team id, source path, status, active flag
- `role`: role id, team id, role kind, display name, binding ref
- `workflow_stage`: stage id, team id, ordinal, owner role, gate policy
- `run`: run id, workspace id, team id, status, current stage, started time, finished time
- `handoff`: handoff id, run id, from role, to role, stage id, status, attempt count, due time
- `artifact`: artifact id, workspace id, kind, path, content type, producing run or stage
- `decision`: decision id, run id, stage id, kind, selected option, rationale artifact ref, user gate flag
- `gate`: gate id, run id, decision id, status, required actor, consequence summary
- `prompt_record`: prompt id, run id, role id, path, model or runner ref
- `tool_call_record`: tool call id, run id, role id, tool name, input ref, output ref, status
- `claim`: claim id, run id, status, text ref
- `evidence_link`: link id, claim id, source kind, source ref, relation, resolved flag
- `view_manifest`: view id, workspace id, path, schema version, status

Rich content should stay outside SQLite unless it is a short label, status, id, path, timestamp, or scalar value needed for validation and scheduling.

## Data Flow

```text
User goal and context
        |
        v
.isomer-labs/manifest.toml resolves workspace
        |
        v
Operator loads workspace state and proposes team/workflow
        |
        v
User approves, edits, or replaces team/workflow
        |
        v
Operator dispatches bounded work to specialist agents
        |
        v
Specialists produce artifacts, prompts, tool calls, and results
        |
        v
Workspace records compact state in SQLite and rich files on disk
        |
        v
Engine emits or updates view manifests
        |
        v
GUI renders task-specific views and pending gates
        |
        v
User steers, branches, pauses, archives, or continues
```

## Error Handling & Edge Cases

Manifest validation must catch invalid workspace references before the engine opens a workspace. Workspace paths should be relative to the project root unless the project explicitly allows another rule. Paths outside the project root should be rejected by default.

State migrations must be explicit. If a workspace schema is too old or too new, the engine should stop with a clear message rather than partially opening it.

Invalid team definitions should fail before execution. Examples include missing operator role, unbound stage owner, unknown runner binding, duplicate role ids, and gate policies that reference missing stages.

Unresolved gates should block only the actions they govern. For example, a pending baseline waiver gate should block downstream experiment synthesis but should not prevent the user from inspecting artifacts or editing team configuration.

Failed handoffs should become durable state. The operator can retry, reroute, ask the user, or mark the stage blocked. It should not spin in a hidden retry loop.

Contradictory evidence should block claim strengthening until resolved. A claim can remain open, be weakened, be withdrawn, or be marked supported only after the contradiction has a recorded resolution.

Missing artifact files should be visible validation failures. The database should keep the ref, but views and reports should mark the artifact missing until repaired or superseded.

## Testing Strategy

Early tests should focus on contracts that will be expensive to change later:

- manifest parsing and path normalization
- workspace discovery from `.isomer-labs/manifest.toml`
- rejection of workspace paths outside the project root
- team definition validation for roles, workflow stages, and bindings
- SQLite migration creation and version checks
- artifact ref validation
- decision-gate lifecycle transitions
- handoff status transitions and retry limits
- claim/evidence consistency rules
- view-manifest schema validation
- end-to-end creation of a minimal workspace, team, run, artifact, gate, and view manifest

These tests can start with `unittest` under `tests/unit/`, with filesystem and SQLite checks promoted to `tests/integration/` when needed.

## Key Constraints

- Project state discovery starts from `.isomer-labs/manifest.toml`.
- Workspaces are project-local directories referenced by the manifest.
- Team definitions include roles, workflow, and bindings.
- Human gates apply to irreversible or claim-shaping decisions, not every stage boundary.
- The engine emits view manifests; the GUI renders them.
- SQLite stores compact control-plane state; files store rich artifacts.
- The operator agent coordinates team work and mediates between user intent, specialist execution, durable state, and GUI-facing views.
- The first implementation should avoid a fully declarative graph engine until the manifested workspace loop proves useful.

## Open Questions

- Exact TOML schema for `.isomer-labs/manifest.toml`.
- Exact workspace directory layout.
- Initial team-definition file format.
- Initial view-manifest schema and supported view types.
- Migration command shape and schema-version policy.
- Whether reusable team definitions should live under `.isomer-labs/teams/`, inside workspaces, or both.
- How much DeepScientist skill and artifact structure should be adapted into initial workspace templates.
