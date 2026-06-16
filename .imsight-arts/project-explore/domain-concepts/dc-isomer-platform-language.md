# Isomer Platform Language

Canonical domain language for the manifested workspace engine design. These terms should guide architecture docs, schema names, CLI labels, GUI labels, and code identifiers.

## Language

**Project**:
A user-owned repository or workspace that Isomer Labs manages. A project becomes Isomer-managed when it has a `.isomer-labs/` Project Config Directory and a Project Manifest that declares Isomer Workspaces.
_Avoid_: Quest root, system-owned workspace, platform directory

**Project Config Directory**:
The `.isomer-labs/` directory at the project root. It stores project-level configuration and references, especially the Project Manifest, reusable Team Definitions, profiles, schemas, cache, and temporary files.
_Avoid_: Control directory, control-plane directory, workspace root, hidden workspace

**Project Manifest**:
The `.isomer-labs/manifest.toml` file. It is the discovery authority for Isomer Workspaces, active workspace selection, project defaults, reusable Team Definitions, and profile references.
_Avoid_: Workspace index, quest registry, config blob

**Isomer Workspace**:
A project-local directory declared by the Project Manifest and managed by Isomer Labs. It owns a Workspace Runtime, rich research artifacts, team snapshots, generated View Manifests, run records, and logs.
_Avoid_: Quest, quest workspace, run directory, system workspace

**Research Thread**:
A user-facing line of inquiry within a Project. A Research Thread has a Research Goal, lifecycle state, Decision Records, Artifacts, Research Branches, and one or more Runs; by default it is backed by one Isomer Workspace.
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
A forked line of work inside a Research Thread. A Research Branch can carry its own hypothesis, Artifacts, Runs, Evidence Items, Research Claims, Findings, and Decision Records.
_Avoid_: Route, experiment route, path, Git branch unless referring to an actual Git branch

**Workspace Runtime**:
The durable execution state and support files inside an Isomer Workspace. It includes `state.sqlite` for compact control-plane state plus file directories such as `artifacts/`, `teams/`, `views/`, `runs/`, and `logs/`.
_Avoid_: Quest state, hidden runtime, project config

**Agent Workspace**:
A per-agent work area inside an Isomer Workspace assigned to one Agent Instance for owned scratch files, local runtime state, logs, and Agent Artifacts. It is an advisory ownership boundary: Isomer records and documents expected access, but does not provide filesystem-grade access control.
_Avoid_: Private sandbox, secure workspace, role directory as a generic term

**Agent Runtime**:
The durable execution state and support files scoped to one Agent Workspace, such as prompt records, tool-call traces, temporary run notes, local logs, and recovery files for that agent. Agent Runtime is subordinate to Workspace Runtime and should not be described as isolated from the operating system.
_Avoid_: OS sandbox, hidden agent state, separate workspace runtime

**Team Definition**:
A durable description of an agent team. It names Roles, Workflow Stages, and Bindings so the team can be inspected, edited, reproduced, and run.
_Avoid_: Agent prompt bundle, full execution graph, role list

**Role**:
A named responsibility inside a Team Definition, such as operator, scout, experimenter, analyst, writer, or reviewer. A Role describes what kind of work an agent owns.
_Avoid_: Persona, participant type, worker label

**Binding**:
The connection between a Role and its concrete execution resources, such as runner, model profile, tool profile, skill bundle, credential profile, or execution adapter.
_Avoid_: Hardcoded runner, agent config, tool config

**Agent Definition**:
A provider-neutral pre-launch description for constructing an Agent Instance. An Agent Definition can refer to prompts, skills, tool lane, setup, model posture, credential reference, mailbox defaults, environment defaults, and launch posture through Bindings or profiles.
_Avoid_: Houmao specialist as the generic term, hardcoded agent config, live agent

**Agent Instance**:
A concrete runtime actor created from an Agent Definition and assigned to a Role for a Run or team execution context. Agent Instances own Agent Workspaces; Roles describe responsibilities and workflow ownership.
_Avoid_: Role as the runtime actor, worker, Houmao managed agent as the generic term

**Research Engine Adapter**:
A provider-specific bridge that maps Isomer concepts such as Team Definition, Role, Agent Definition, Agent Instance, Binding, Run, Agent Workspace, and Artifact onto a concrete execution engine. Houmao can be one adapter implementation, but Isomer domain language must stay engine-neutral.
_Avoid_: Houmao as the core engine, native-agent layer as the Isomer model, provider lock-in

**Workflow Stage**:
A named step in a Team Definition's workflow. A Workflow Stage has an owning Role, expected inputs and outputs, handoff behavior, and optional Gate policy.
_Avoid_: Pipeline step, quest stage, task only

**Run**:
A bounded execution episode inside a Research Thread. A Run records prompts, tool calls, handoffs, outputs, logs, and status for one operator or specialist execution pass.
_Avoid_: Research thread, workspace, quest

**Operator Agent**:
The user-controlled coordinating agent. It translates user intent into team instructions, proposes Team Definitions and workflows, dispatches work to Specialist Agents, records decisions, and returns gated decisions to the user. In a concrete Run, it can be represented by an Agent Instance.
_Avoid_: Orchestrator, supervisor, root agent

**Specialist Agent**:
An agent assigned to a non-operator Role in a Team Definition. Specialist Agents perform bounded role-owned work and return Artifacts, Evidence Items, or results to the Operator Agent. In a concrete Run, each active Specialist Agent is represented by an Agent Instance.
_Avoid_: Worker, subagent, participant

**Gate**:
A recorded decision point that must return to the human user before the governed action proceeds. Gates apply to irreversible or claim-shaping decisions, not every Workflow Stage boundary.
_Avoid_: Approval step, interaction request, manual checkpoint

**Artifact**:
A durable file or file-backed output produced or used during research work, such as a literature note, hypothesis, baseline report, experiment plan, result table, figure, report, Decision Record, prompt record, or tool output.
_Avoid_: Blob, attachment, output only

**Agent Artifact**:
An Artifact produced, curated, or owned by a specific agent inside its Agent Workspace. Agent Artifacts can be promoted or referenced as workspace-level Artifacts when they become shared evidence, handoff material, or GUI-visible outputs.
_Avoid_: Private output, scratch blob, team artifact when ownership matters

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
A durable record of a meaningful choice made by the user, Operator Agent, or team, including selected option, rationale, Evidence Items, consequences, actor, and timestamp.
_Avoid_: Gate, approval, log entry

**Provenance Record**:
A durable record of how an Artifact, Decision Record, Research Claim, Evidence Item, or state transition was produced. It links actors, prompts, tool calls, inputs, outputs, Evidence Items, timestamps, and state changes.
_Avoid_: Log line, audit note, metadata only

**Workspace Boundary**:
An advisory boundary that declares which parts of an Agent Workspace an agent owns and which parts peers may inspect. Boundaries can be documented in README files or declared in manifests, but Isomer does not rely on them for hard filesystem protection.
_Avoid_: Security boundary, access-control boundary, permission wall

**Peer Read Access**:
The advisory ability for one team agent to inspect another agent's declared readable files or Agent Artifacts without taking ownership of them. Peer Read Access supports collaboration and review, but durable dependencies should still be recorded through handoffs, promoted Artifacts, Evidence Items, or Provenance Records.
_Avoid_: Write sharing, filesystem permission, unrestricted shared workspace

**View Manifest**:
An engine-produced data document that describes a task-specific GUI view, including view type, data sources, data bindings, user actions, and pending Gates. The GUI renders View Manifests but does not own research state.
_Avoid_: View spec, generated frontend code, dashboard config

**GUI Renderer**:
The GUI layer that reads View Manifests and renders task-specific interactive views. It owns layout and interaction widgets, while the engine owns semantic state and view intent.
_Avoid_: Generated GUI, engine UI, fixed dashboard

## Identifier Guidance

- Use `project_config_dir` for `.isomer-labs/`.
- Use `project_manifest` for `.isomer-labs/manifest.toml`.
- Use `isomer_workspace` for a manifest-declared workspace.
- Use `research_thread` for a user-facing line of inquiry.
- Use `research_goal` for the user-facing intent attached to a Research Thread.
- Use `goal_kind` for the distinction between `measurable_objective` and `exploratory_goal`.
- Use `measurable_objective` only for Research Goals with metrics, targets, or optimization direction.
- Use `exploratory_goal` for Research Goals centered on understanding, explanation, discovery, or factor identification.
- Use `research_branch` for a forked line of work inside a Research Thread.
- Use `active_research_branch_id` for the active Research Branch pointer.
- Use `workspace_runtime` for workspace-local execution state and support files.
- Use `agent_workspace` for a per-agent work area inside an Isomer Workspace.
- Use `agent_runtime` for execution state and support files scoped to one Agent Workspace.
- Use `agent_artifact` when an Artifact's producing or owning agent matters.
- Use `workspace_boundary` for advisory ownership and readable-surface declarations.
- Use `peer_read_access` for non-enforced cross-agent reading.
- Use `team_definition`, `role`, `binding`, `agent_definition`, `agent_instance`, `research_engine_adapter`, and `workflow_stage` for team and execution concepts.
- Use `run` for a bounded execution episode.
- Use `operator_agent` and `specialist_agent` for agent roles.
- Use `gate`, `artifact`, `provenance_record`, `view_manifest`, and `gui_renderer` for state and GUI concepts.
- Use `research_claim`, `evidence_item`, `finding`, and `decision_record` for claim/evidence/decision semantics.

## Relationships

- A **Project** has one **Project Config Directory**.
- A **Project Config Directory** contains one **Project Manifest**.
- A **Project Manifest** declares zero or more **Isomer Workspaces**.
- A **Project** contains zero or more **Research Threads**.
- A **Research Thread** has one **Research Goal**.
- A **Research Goal** has a goal kind: **Measurable Objective** or **Exploratory Goal**.
- A **Research Thread** contains zero or more **Research Branches**.
- A **Research Branch** belongs to one **Research Thread**.
- A **Research Thread** is backed by one **Isomer Workspace** by default.
- A **Research Thread** contains one or more **Runs**.
- An **Isomer Workspace** owns one **Workspace Runtime**.
- An **Isomer Workspace** may contain many **Agent Workspaces** during team execution.
- An **Agent Workspace** belongs to one **Agent Instance** within a team execution context.
- An **Agent Workspace** contains one **Agent Runtime** and zero or more **Agent Artifacts**.
- **Agent Runtime** is subordinate to **Workspace Runtime**.
- An **Agent Definition** describes how a **Research Engine Adapter** can construct an **Agent Instance**.
- An **Agent Instance** is assigned to one **Role** for a Run or team execution context.
- A **Role** may be served by different **Agent Instances** across retries, Runs, or adapter implementations.
- A **Research Engine Adapter** may map Isomer **Agent Definitions** to Houmao specialists, project profiles, native roles, recipes, or launch dossiers, but those Houmao concepts are adapter details.
- A **Workspace Boundary** declares intended write ownership and **Peer Read Access** for an **Agent Workspace**.
- **Peer Read Access** allows inspection of declared readable files, but it does not grant write ownership or filesystem-grade protection.
- **Agent Artifacts** can be promoted or referenced as workspace-level **Artifacts**, **Evidence Items**, or handoff inputs.
- A **Workspace Runtime** records **Artifacts**, **Provenance Records**, **Gates**, and **View Manifests**.
- A **Research Claim** can be supported, contradicted, or contextualized by one or more **Evidence Items**.
- A **Finding** is distilled from Research Claims and Evidence Items.
- A **Decision Record** may resolve a **Gate**, select a **Research Branch**, archive a Research Thread, or record another meaningful choice.
- A **Decision Record** should cite relevant **Evidence Items**, **Artifacts**, or **Provenance Records** when the choice depends on research evidence.
- A **Team Definition** contains **Roles**, **Workflow Stages**, and **Bindings**.
- The **Operator Agent** coordinates **Specialist Agents** through a **Team Definition**.
- A **Gate** can block a Workflow Stage action until the human user resolves it.
- The **GUI Renderer** renders **View Manifests** emitted from Workspace Runtime state.

## Flagged Ambiguities

- Use **Project Config Directory** for `.isomer-labs/`. Reserve "control plane" for compact runtime state, especially SQLite-backed Workspace Runtime state.
- Use **Isomer Workspace** instead of "quest" or "quest workspace" for Isomer-managed research execution areas. "Quest" is DeepScientist reference language, not Isomer canonical language.
- Use **Research Thread** for the user-facing research lifecycle. Do not use **Isomer Workspace** when discussing pause, branch, resume, archive, or goal-level steering unless the storage location itself matters.
- Use **Agent Workspace** for per-agent work areas inside an Isomer Workspace. Do not call it a secure sandbox.
- Use **Agent Instance** for the concrete runtime actor that owns an Agent Workspace. Do not use **Role** as the workspace owner except when discussing responsibility or workflow ownership.
- Use **Agent Definition** and **Research Engine Adapter** for provider-neutral launch concepts. Houmao's specialist, project profile, native role, recipe, launch dossier, and managed agent concepts can inform an adapter, but they are not Isomer core terms.
- Use **Peer Read Access** for the advisory collaboration rule that lets agents inspect declared peer files. It does not prevent an agent with system tools from modifying files, so do not describe it as filesystem access control.
- Use **Workspace Boundary** for README- or manifest-declared ownership/readability rules. Use **Handoff**, **Artifact**, **Evidence Item**, or **Provenance Record** when another agent's read becomes a durable dependency.
- Use **Research Goal** as the umbrella term. Use **Measurable Objective** only for the metric-bearing kind of Research Goal.
- Use **Research Branch** for forked lines of work. Avoid "route" as a first-class noun except when quoting prior docs or describing informal route-selection language.
- Use **Run** only for bounded execution episodes inside a Research Thread.
- Use **Research Claim** for statements that need evidence status. Use **Finding** only after evidence has been distilled into a reusable insight.
- Use **Decision Record** for the durable result of a choice. Use **Gate** for the pending decision point before that choice is resolved.
- Use **View Manifest** instead of "view spec" or "dashboard config" for engine-produced GUI description files.
