# Isomer Platform Language

Canonical domain language for the manifested workspace engine design. These terms should guide architecture docs, schema names, CLI labels, GUI labels, and code identifiers.

## Language

### Project and Workspace

**Project**:
A user-owned repository, checkout, or directory tree that Isomer Labs manages. A Project becomes Isomer-managed when it has a `.isomer-labs/` Project Config Directory and a Project Manifest that declares Isomer Workspaces.
_Avoid_: Quest root, system-owned workspace, platform directory

**Project Config Directory**:
The `.isomer-labs/` directory at the project root. It stores project-level configuration and references, especially the Project Manifest, Agent Team Templates, Agent Team Instances, and Agent Profiles. It should not contain default cache, temporary, or schema directories. System-owned schemas are Isomer built-in artifacts queried and validated through `isomer-cli`.
_Avoid_: Control directory, control-plane directory, workspace root, hidden workspace

**Project Manifest**:
The `.isomer-labs/manifest.toml` file. It is the discovery authority for Isomer Workspaces, active workspace selection, project defaults, Agent Team Templates, Agent Team Instances, and Agent Profile references.
_Avoid_: Workspace index, quest registry, config blob

**Isomer Workspace**:
A project-local directory declared by the Project Manifest and managed by Isomer Labs for one Research Task. It owns a Workspace Runtime, rich research Artifacts, generated View Manifests, Run records, and logs. It records the task handler: the Operator Agent or a delegated Agent Instance from a selected Agent Team Instance. It references Agent Team Instances but does not contain a workspace-local `teams/` directory.
_Avoid_: Quest, quest workspace, run directory, system workspace

**Workspace Runtime**:
The persistent runtime substrate inside an Isomer Workspace. It includes `state.sqlite`, schema version, runtime directories, refs, validation state, and support files that let many Runs be recorded, resumed, inspected, and validated.
_Avoid_: Run, execution episode, quest state, hidden runtime, project config

### Workspace Taxonomy

Use **workspace** only for the two filesystem work areas that Isomer manages directly:

- **Isomer Workspace**: the research-level work area declared by the Project Manifest.
- **Agent Workspace**: the per-agent work area inside an Isomer Workspace.

Other space-like terms have narrower meanings:

- **Project** is the outer user-owned repository, checkout, or directory tree. It is not an Isomer Workspace.
- **Project Config Directory** is `.isomer-labs/`. It is configuration and discovery state, not a workspace.
- **Workspace Runtime** is persistent runtime state inside an Isomer Workspace, not a separate workspace.
- **Agent Runtime** is runtime state inside an Agent Workspace, not a separate workspace.
- **Workspace Boundary** is an advisory ownership and peer-read declaration for an Agent Workspace, not a filesystem-enforced space.
- **Research Thread** is the user-facing research lifecycle object. It can span many Isomer Workspaces, but it is not itself a workspace.
- **Research Task** is the bounded unit of work handled by the Operator Agent or by one delegated Agent Instance from an Agent Team Instance in one Isomer Workspace. It is not a workspace.
- **Run** is a bounded execution episode recorded through Workspace Runtime, not a workspace.

The containment relationship is:

```text
Project
  .isomer-labs/ Project Config Directory
    manifest.toml Project Manifest
    Agent Team Template references
    Agent Team Instance definitions
    Operator Agent configuration
  Isomer Workspace(s), declared by the Project Manifest
    one Research Task
    one task handler: Operator Agent or delegated team Agent Instance
    optional selected Agent Team Instance reference
    Workspace Runtime
    Agent Workspace(s), created for Agent Instances during team execution
      Agent Runtime
      Workspace Boundary
```

### Research Lifecycle

**Research Thread**:
A user-facing line of inquiry within a Project. A Research Thread has a Research Goal, lifecycle state, Decision Records, Artifacts, Research Branches, Research Tasks, and one or more Runs. Its work can be distributed across multiple Isomer Workspaces.
_Avoid_: Quest, project, workspace, run

**Research Goal**:
The user-facing intent for a Research Thread. A Research Goal can be measurable or exploratory; it does not need to include a numeric target.
_Avoid_: Objective as the umbrella term, task prompt, assignment

**Measurable Objective**:
A Research Goal kind with a metric, target, or optimization direction, such as improving performance by a fixed percentage or improving it as much as possible.
_Avoid_: Research goal as if all goals are measurable, benchmark only

**Exploratory Goal**:
A Research Goal kind focused on understanding, explanation, discovery, or factor identification, such as figuring out how a system works or identifying critical factors that affect performance.
_Avoid_: Vague goal, non-measurable objective

**Research Branch**:
A forked line of work inside a Research Thread. A Research Branch can carry its own hypothesis, Research Tasks, Artifacts, Runs, Evidence Items, Research Claims, Findings, and Decision Records.
_Avoid_: Route, experiment route, path, Git branch unless referring to an actual Git branch

**Research Task**:
A bounded unit of research work inside one Isomer Workspace. A Research Task belongs to a Research Thread or Research Branch, has expected inputs and outputs, names a task handler, and can be attempted through one or more Runs. The task handler can be the Operator Agent or a delegated Agent Instance from an Agent Team Instance.
_Avoid_: Task Scope, Isomer Workspace, Run, Workflow Stage, general to-do item

**Run**:
A bounded execution attempt for one Research Task. A Run has its own lifecycle, status, actor participation, prompts, tool calls, handoffs, outputs, and logs; its records are stored through the Workspace Runtime.
_Avoid_: Research task, research thread, workspace, quest

### Team and Agent Execution

**Agent Team Template**:
A reusable multi-agent blueprint that can be instantiated into a Project. It names default Agent Roles, Workflow Stages, Coordination Policy, Capability Bindings, and template parameters, but it should not carry project-specific choices. A Houmao team definition such as `teams/lfeng-team` can be imported through an Execution Adapter as an Agent Team Template.
_Avoid_: Agent Team Instance, live team, Run, provider-specific team as the core term

**Agent Team Instance**:
A concrete multi-agent structure instantiated from an Agent Team Template by the Operator Agent. It resolves project-specific parameters such as role count, model posture, credentials, project paths, domain instructions, and Gate policy. Isomer Workspaces reference Agent Team Instances when a Research Task is delegated to the team.
_Avoid_: Agent Team Template, workspace-local team, ad hoc role list

**Agent Team**:
An umbrella phrase for a multi-agent structure. Use **Agent Team Template** for the reusable blueprint and **Agent Team Instance** for the instantiated team. Avoid using **Agent Team** alone in schema names, manifest fields, or GUI labels when template or instance is the intended meaning.
_Avoid_: Provider-specific specialist group, prompt bundle, full execution graph, role list only, concrete team when template or instance is meant

**Agent Role**:
A named responsibility inside an Agent Team Template or Agent Team Instance, such as operator, scout, coder, experimenter, analyst, writer, or reviewer. An Agent Role describes work ownership, expected inputs and outputs, authority, and handoff obligations; it is not a concrete runtime actor.
_Avoid_: Persona, participant type, worker label

**Agent Profile**:
A provider-neutral reusable description of how to construct or configure an Agent Instance. An Agent Profile can reference instructions, skills, model posture, tool access, execution environment, credentials, mailbox defaults, memory defaults, and launch posture without assuming one backend's document model.
_Avoid_: Agent Definition, provider-specific specialist as the generic term, hardcoded agent config, live agent

**Capability Binding**:
The connection between an Agent Role or Agent Profile and the capabilities available to it, such as tools, skills, model profiles, data access, credentials, execution adapters, communication channels, or workspace permissions.
_Avoid_: Binding as an unqualified term, hardcoded runner, tool config, provider-specific profile

**Agent Instance**:
A concrete runtime actor created from an Agent Profile and assigned to an Agent Role for a Run or team execution context. Agent Instances own Agent Workspaces; Agent Roles describe responsibilities and workflow ownership.
_Avoid_: Agent Role as the runtime actor, worker, provider-specific managed agent as the generic term

**Operator Agent**:
The project-facing Agent Role and corresponding Agent Instance that acts as the main interaction point with the user, instantiates Agent Team Templates into Agent Team Instances, controls or delegates Research Tasks, resolves fallback handling, and records task routing decisions. The Operator Agent can handle a Research Task directly or delegate it to a team Agent Instance.
_Avoid_: Controller as a separate entity outside Agent Role and Agent Instance, backend-specific operator implementation

**Coordination Policy**:
The rules that govern how Agent Instances collaborate inside an Agent Team Instance. A Coordination Policy can define operator behavior, peer communication, handoff routing, review loops, conflict handling, retry behavior, escalation, fallback behavior, and Gates.
_Avoid_: Orchestration code, implicit team convention, backend-specific routing rules

**Execution Adapter**:
A backend-specific bridge that maps Isomer's generic Agent Team Template, Agent Team Instance, Agent Profile, Agent Instance, Capability Binding, Run, Agent Workspace, and Artifact concepts onto a concrete execution engine. Execution Adapters must not change Isomer's core domain language.
_Avoid_: Research Engine Adapter, backend as the core engine, native-agent layer as the Isomer model, provider lock-in

**Workflow Stage**:
A named step in an Agent Team Template or Agent Team Instance workflow. A Workflow Stage has an owning Agent Role, expected inputs and outputs, handoff behavior, and optional Gate policy.
_Avoid_: Pipeline step, quest stage, task only

**Task Handler**:
The Agent Instance responsible for directly handling a Research Task or controlling its delegated execution. A Task Handler is usually the Operator Agent for project interaction and fallback work, or one Agent Instance from the selected Agent Team Instance for specialized work.
_Avoid_: Owning workspace, task type, unmanaged worker

### Agent Workspace and Collaboration

**Agent Workspace**:
A per-agent work area inside an Isomer Workspace assigned to one Agent Instance for owned scratch files, local runtime state, logs, and Agent Artifacts. It is an advisory ownership boundary: Isomer records and documents expected access, but does not provide filesystem-grade access control.
_Avoid_: Private sandbox, secure workspace, role directory as a generic term

**Agent Runtime**:
The durable execution state and support files scoped to one Agent Workspace, such as prompt records, tool-call traces, temporary run notes, local logs, and recovery files for that agent. Agent Runtime is subordinate to Workspace Runtime and should not be described as isolated from the operating system.
_Avoid_: OS sandbox, hidden agent state, separate workspace runtime

**Agent Artifact**:
An Artifact produced, curated, or owned by a specific agent inside its Agent Workspace. Agent Artifacts can be promoted or referenced as workspace-level Artifacts when they become shared evidence, handoff material, or GUI-visible outputs.
_Avoid_: Private output, scratch blob, team artifact when ownership matters

**Workspace Boundary**:
An advisory boundary that declares which parts of an Agent Workspace an agent owns and which parts peers may inspect. Boundaries can be documented in README files or declared in manifests, but Isomer does not rely on them for hard filesystem protection.
_Avoid_: Security boundary, access-control boundary, permission wall

**Peer Read Access**:
The advisory ability for one team agent to inspect another agent's declared readable files or Agent Artifacts without taking ownership of them. Peer Read Access supports collaboration and review, but durable dependencies should still be recorded through handoffs, promoted Artifacts, Evidence Items, or Provenance Records.
_Avoid_: Write sharing, filesystem permission, unrestricted shared workspace

### Artifacts, Evidence, and Decisions

**Artifact**:
A durable file or file-backed output produced or used during research work, such as a literature note, hypothesis, baseline report, experiment plan, result table, figure, report, Decision Record, prompt record, or tool output.
_Avoid_: Blob, attachment, output only

**Research Claim**:
A statement made by a Research Thread that may need support, contradiction handling, or withdrawal. A Research Claim can be open, supported, refuted, or withdrawn.
_Avoid_: Assertion, conclusion as an unsupported statement, finding

**Evidence Item**:
A durable source of support, contradiction, or context for a Research Claim. An Evidence Item can reference an Artifact, result, measurement, analysis, source document, or external reference.
_Avoid_: Attachment, citation only, proof

**Finding**:
A reusable insight distilled from Research Claims and Evidence Items. A Finding should be grounded by Evidence Items and useful for future steering, writing, review, or reuse.
_Avoid_: Any note, raw result, unsupported claim

**Decision Record**:
A durable record of a meaningful choice made by the user, the Operator Agent, or the team, including selected option, rationale, Evidence Items, consequences, actor, and timestamp.
_Avoid_: Gate, approval, log entry

**Provenance Record**:
A durable record of how an Artifact, Decision Record, Research Claim, Evidence Item, or state transition was produced. It links actors, prompts, tool calls, inputs, outputs, Evidence Items, timestamps, and state changes.
_Avoid_: Log line, audit note, metadata only

**Gate**:
A recorded decision point that must return to the human user before the governed action proceeds. Gates apply to irreversible or claim-shaping decisions, not every Workflow Stage boundary.
_Avoid_: Approval step, interaction request, manual checkpoint

### GUI and Views

**View Manifest**:
An engine-produced data document that describes a task-specific GUI view, including view type, data sources, data bindings, user actions, and pending Gates. The GUI renders View Manifests but does not own research state.
_Avoid_: View spec, generated frontend code, dashboard config

**GUI Renderer**:
The GUI layer that reads View Manifests and renders task-specific interactive views. It owns layout and interaction widgets, while the engine owns semantic state and view intent.
_Avoid_: Generated GUI, engine UI, fixed dashboard

## Identifier Guidance

### Project and Workspace

- Use `project_root` for the root path of the user-owned Project.
- Use `project_config_dir` for `.isomer-labs/`.
- Use `project_manifest` for `.isomer-labs/manifest.toml`.
- Use `isomer_workspace` for a manifest-declared workspace.
- Use `research_task` for the bounded work handled in one Isomer Workspace.
- Use `task_handler` for the Operator Agent or delegated team Agent Instance responsible for a Research Task.
- Use `workspace_runtime` for the persistent workspace substrate that stores and validates state across many Runs.
- Use `agent_workspace` only for a per-agent work area inside an Isomer Workspace.
- Avoid bare `workspace` when the scope could mean Project, Isomer Workspace, or Agent Workspace.

### Research Lifecycle

- Use `research_thread` for a user-facing line of inquiry.
- Use `research_goal` for the user-facing intent attached to a Research Thread.
- Use `goal_kind` for the distinction between `measurable_objective` and `exploratory_goal`.
- Use `measurable_objective` only for Research Goals with metrics, targets, or optimization direction.
- Use `exploratory_goal` for Research Goals centered on understanding, explanation, discovery, or factor identification.
- Use `research_branch` for a forked line of work inside a Research Thread.
- Use `active_research_branch_id` for the active Research Branch pointer.
- Use `research_task_id` for the Research Task realized by an Isomer Workspace.
- Use `run` for one bounded execution episode recorded in Workspace Runtime.

### Team and Agent Execution

- Use `agent_team_template`, `agent_team_instance`, `operator_agent`, `agent_role`, `agent_profile`, `agent_instance`, `capability_binding`, `coordination_policy`, `execution_adapter`, and `workflow_stage` for team and execution concepts.
- Use terms such as `operator`, `reviewer`, `writer`, `coder`, `experimenter`, or `scout` as Agent Role kinds. Model `operator_agent` as an Agent Role and Agent Instance identity, not as a separate entity table outside the generic agent model.

### Agent Workspace and Collaboration

- Use `agent_workspace` for a per-agent work area inside an Isomer Workspace.
- Use `agent_runtime` for execution state and support files scoped to one Agent Workspace.
- Use `agent_artifact` when an Artifact's producing or owning agent matters.
- Use `workspace_boundary` for advisory ownership and readable-surface declarations.
- Use `peer_read_access` for non-enforced cross-agent reading.

### Artifacts, Evidence, and Decisions

- Use `artifact`, `gate`, and `provenance_record` for durable output, decision-point, and production-history concepts.
- Use `research_claim`, `evidence_item`, `finding`, and `decision_record` for claim/evidence/decision semantics.

### GUI and Views

- Use `view_manifest` and `gui_renderer` for GUI concepts.

## Relationships

### Project and Research Lifecycle

- A **Project** has one **Project Config Directory**.
- A **Project** is the outer container and is not an **Isomer Workspace**.
- A **Project Config Directory** contains one **Project Manifest**.
- A **Project Config Directory** is config and discovery state; it does not own **Workspace Runtime** or research **Artifacts**.
- A **Project Manifest** declares zero or more **Isomer Workspaces**.
- A **Project** contains zero or more **Research Threads**.
- A **Research Thread** has one **Research Goal**.
- A **Research Goal** has a goal kind: **Measurable Objective** or **Exploratory Goal**.
- A **Research Thread** contains zero or more **Research Branches**.
- A **Research Branch** belongs to one **Research Thread**.
- A **Research Thread** can span one or more **Research Tasks**.
- A **Research Task** belongs to one **Research Thread** or **Research Branch**.
- An **Isomer Workspace** realizes exactly one **Research Task**.
- A **Research Task** records one **Task Handler**: the **Operator Agent** or a delegated **Agent Instance** from a selected **Agent Team Instance**.
- A **Research Task** can be attempted through one or more **Runs**.
- An **Isomer Workspace** owns one **Workspace Runtime**.
- A **Workspace Runtime** stores, indexes, validates, and recovers **Run** records, but it is not itself a Run.

### Team and Agent Execution

- An **Isomer Workspace** may contain many **Agent Workspaces** during team execution.
- An **Agent Workspace** is contained by exactly one **Isomer Workspace**.
- An **Agent Workspace** belongs to one **Agent Instance** within a team execution context.
- An **Agent Workspace** contains one **Agent Runtime** and zero or more **Agent Artifacts**.
- **Agent Runtime** is subordinate to **Workspace Runtime**.
- An **Agent Team Template** contains default **Agent Roles**, **Workflow Stages**, **Coordination Policy**, **Capability Bindings**, and template parameters.
- An **Agent Team Instance** is instantiated from one **Agent Team Template** by the **Operator Agent**.
- An **Agent Team Instance** contains resolved **Agent Roles**, **Workflow Stages**, **Coordination Policy**, **Capability Bindings**, and project-specific parameters.
- An **Isomer Workspace** may reference one selected **Agent Team Instance** when its **Research Task** is delegated to a team.
- Reusable **Agent Team Templates** and **Agent Team Instances** live outside the Isomer Workspace.
- An **Agent Profile** describes how an **Execution Adapter** can construct or configure an **Agent Instance**.
- An **Agent Instance** is assigned to one **Agent Role** for a Run or team execution context.
- An **Agent Role** may be served by different **Agent Instances** across retries, Runs, or adapter implementations.
- The **Operator Agent** is the main user interaction point, task controller, team-instantiation actor, and final fallback handler.
- A **Coordination Policy** defines how Agent Instances communicate, hand off work, review outputs, escalate decisions, and use Gates.
- An **Execution Adapter** may map Isomer **Agent Profiles** to backend-specific launch material, but those backend concepts are adapter details.
- A **Workspace Boundary** declares intended write ownership and **Peer Read Access** for an **Agent Workspace**.
- A **Workspace Boundary** belongs to an **Agent Workspace**, but it is not itself a workspace.
- **Peer Read Access** allows inspection of declared readable files, but it does not grant write ownership or filesystem-grade protection.
- **Agent Artifacts** can be promoted or referenced as workspace-level **Artifacts**, **Evidence Items**, or handoff inputs.
- A **Workspace Runtime** records **Runs**, **Artifacts**, **Provenance Records**, **Gates**, and **View Manifests**.
- The **Operator Agent**, when delegating work, coordinates other **Agent Instances** according to the selected Agent Team Instance's **Coordination Policy**.

### Artifacts, Evidence, and Decisions

- A **Research Claim** can be supported, contradicted, or contextualized by one or more **Evidence Items**.
- A **Finding** is distilled from Research Claims and Evidence Items.
- A **Decision Record** may resolve a **Gate**, select a **Research Branch**, archive a Research Thread, or record another meaningful choice.
- A **Decision Record** should cite relevant **Evidence Items**, **Artifacts**, or **Provenance Records** when the choice depends on research evidence.
- A **Gate** can block a Workflow Stage action until the human user resolves it.

### GUI and Views

- The **GUI Renderer** renders **View Manifests** emitted from Workspace Runtime state.

## Flagged Ambiguities

### Project and Research Lifecycle

- Use **Project Config Directory** for `.isomer-labs/`. Reserve "control plane" for compact runtime state, especially SQLite-backed Workspace Runtime state.
- Do not use bare "workspace" when **Project**, **Isomer Workspace**, and **Agent Workspace** are all plausible readings.
- Do not call **Project** or **Project Config Directory** a workspace.
- Use **Isomer Workspace** instead of "quest" or "quest workspace" for Isomer-managed research execution areas. "Quest" is DeepScientist reference language, not Isomer canonical language.
- Use **Research Thread** for the user-facing research lifecycle. Do not use **Isomer Workspace** when discussing pause, branch, resume, archive, or goal-level steering unless the storage location itself matters.
- Use **Research Goal** as the umbrella term. Use **Measurable Objective** only for the metric-bearing kind of Research Goal.
- Use **Research Branch** for forked lines of work. Avoid "route" as a first-class noun except when quoting prior docs or describing informal route-selection language.
- Use **Research Task** for the bounded unit of work handled in one Isomer Workspace.
- Use **Task Handler** for the **Operator Agent** or delegated team **Agent Instance** that controls the Research Task.
- Use **Workspace Runtime** for the persistent state substrate owned by an Isomer Workspace. Use **Run** only for bounded execution attempts for a Research Task.

### Team and Agent Execution

- Use **Agent Workspace** for per-agent work areas inside an Isomer Workspace. Do not call it a secure sandbox.
- Do not put `teams/` under an **Isomer Workspace**. Agent Team Templates and Agent Team Instances are project-level or built-in references; the workspace records Agent Team Instance identity and task-handler identity through manifest refs, Workspace Runtime, or provenance Artifacts.
- Use **Agent Team Template**, **Agent Team Instance**, **Operator Agent**, **Agent Role**, **Agent Profile**, **Capability Binding**, **Coordination Policy**, **Agent Instance**, **Workflow Stage**, and **Execution Adapter** as the generic multi-agent core.
- Use **Agent Instance** for the concrete runtime actor that owns an Agent Workspace. Do not use **Agent Role** as the workspace owner except when discussing responsibility or workflow ownership.
- Use **Operator Agent** for the user-facing controller, project-scope team instantiator, task router, and fallback handler. Use **Coordination Policy** for the rules that govern collaboration among delegated team agents.
- Operator, reviewer, writer, coder, experimenter, and scout should be Agent Role kinds, not separate entity types.
- Treat Houmao's specialist, project profile, native role, recipe, launch dossier, and managed-agent concepts as possible mappings inside a Houmao **Execution Adapter**. Do not use them as Isomer core terms.

### Agent Workspace and Collaboration

- Use **Peer Read Access** for the advisory collaboration rule that lets agents inspect declared peer files. It does not prevent an agent with system tools from modifying files, so do not describe it as filesystem access control.
- Use **Workspace Boundary** for README- or manifest-declared ownership/readability rules. Use **Handoff**, **Artifact**, **Evidence Item**, or **Provenance Record** when another agent's read becomes a durable dependency.

### Artifacts, Evidence, and Decisions

- Use **Research Claim** for statements that need evidence status. Use **Finding** only after evidence has been distilled into a reusable insight.
- Use **Decision Record** for the durable result of a choice. Use **Gate** for the pending decision point before that choice is resolved.

### GUI and Views

- Use **View Manifest** instead of "view spec" or "dashboard config" for engine-produced GUI description files.
