# Isomer Platform Language

Canonical domain language for the manifested workspace engine design. These terms should guide architecture docs, schema names, CLI labels, GUI labels, and code identifiers.

## Language

### Project and Workspace

**Project**:
A user-owned repository, checkout, or directory tree that Isomer Labs manages. A Project becomes Isomer-managed when it has a `.isomer-labs/` Project Config Directory and a Project Manifest that declares Topic Workspaces.
_Avoid_: Quest root, system-owned workspace, platform directory

**Project Config Directory**:
The `.isomer-labs/` directory at the project root. It stores project-level configuration and references, especially the Project Manifest, Research Topic Config files, Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Profiles, Artifact Format Profiles, Artifact Extensions, and GUI Component Registry refs. It should not contain default cache, temporary, or schema directories. System-owned schemas are Isomer built-in artifacts queried and validated through `isomer-cli`. `.isomer-labs/local.toml` is allowed only as untracked user-local active context.
_Avoid_: Control directory, control-plane directory, workspace root, hidden workspace

**Project Manifest**:
The `.isomer-labs/manifest.toml` file. It is the discovery authority for Research Topics, Research Topic Config paths, Topic Workspaces, project defaults, Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Profile references, Artifact Format Profile registrations, Artifact Extension registrations, and project-scope GUI component registry references.
_Avoid_: Workspace index, quest registry, config blob

**Research Topic Config**:
A Project Manifest-registered TOML file for one Research Topic. It stores topic-specific defaults and refs, such as a short topic statement, topic statement Artifact refs, Measurable Objective text or refs, default Research Inquiry refs, default Topic Agent Team Profile refs, Execution Adapter refs, Capability Binding refs, Gate policy refs, Artifact Format Profile defaults, and Artifact Extension refs. It is not Workspace Runtime state and must not contain Run status, command outputs, live process ids, resolved command results, rich Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, credentials, tokens, API keys, passwords, or secret material.
_Avoid_: Runtime config, topic database, workspace state, command log, credential file

**Topic Workspace**:
A project-local directory declared by the Project Manifest and managed by Isomer Labs for one Research Topic. It owns the topic's Workspace Runtime, Research Inquiry graph, Research Tasks, Runs, rich research Artifacts, generated View Manifests, Agent Workspaces, and logs. It references selected Topic Agent Team Profiles and Agent Team Instances used for the topic, but it does not contain a workspace-local `teams/` directory.
_Avoid_: Isomer Workspace, quest, quest workspace, run directory, task workspace, system workspace

**Workspace Runtime**:
The persistent runtime substrate inside a Topic Workspace. It includes `state.sqlite`, schema version, runtime directories, refs, validation state, and support files that let Research Inquiries, Research Tasks, Runs, Artifacts, handoffs, Gates, and View Manifests be recorded, resumed, inspected, and validated.
_Avoid_: Run, execution episode, quest state, hidden runtime, project config

**Effective Topic Context**:
The resolved process-local context that `isomer-cli`, Workspace Path Resolution, Run initialization, and future Execution Adapter command requests consume for a topic-scoped command. It includes validated Project, Research Topic, Research Topic Config, Topic Workspace, optional lifecycle refs, Topic Agent Team Profile defaults, Execution Adapter refs, Capability Binding refs, Gate policy refs, Artifact Format Profile refs, Artifact Extension refs, and source metadata. It is not a lifecycle object, not Workspace Runtime state, and not stored wholesale on every Run.
_Avoid_: Active workspace, runtime database, lifecycle state, durable context blob

### Workspace Taxonomy

Use **workspace** only for the two filesystem work areas that Isomer manages directly:

- **Topic Workspace**: the topic-level work area declared by the Project Manifest.
- **Agent Workspace**: the per-agent work area inside a Topic Workspace.

Other space-like terms have narrower meanings:

- **Project** is the outer user-owned repository, checkout, or directory tree. It is not a Topic Workspace.
- **Project Config Directory** is `.isomer-labs/`. It is configuration and discovery state, not a workspace.
- **Workspace Runtime** is persistent runtime state inside a Topic Workspace, not a separate workspace.
- **Agent Runtime** is runtime state inside an Agent Workspace, not a separate workspace.
- **Workspace Boundary** is an advisory ownership and peer-read declaration for an Agent Workspace, not a filesystem-enforced space.
- **Research Topic** is the root research problem or investigation intent that initiates work and topic-level team specialization. It is not a workspace.
- **Research Inquiry** is a question or line of inquiry under a Research Topic. It is recorded inside the topic's Topic Workspace, but it is not itself a workspace.
- **Research Task** is the bounded unit of work handled by the Operator Agent or by one delegated Agent Instance from an Agent Team Instance inside one Topic Workspace. It is not a workspace.
- **Run** is a bounded execution episode recorded through Workspace Runtime, not a workspace.

The containment relationship is:

```text
Project
  .isomer-labs/ Project Config Directory
    manifest.toml Project Manifest
    Domain Agent Team Template references
    Topic Agent Team Profile definitions
    Agent Team Instance refs
    Operator Agent configuration
    GUI Component Registry references
  Research Topic(s)
    Topic Workspace, declared by the Project Manifest
      Workspace Runtime
      Research Inquiry graph
        Research Task(s)
      Agent Workspace(s), created for Agent Instances during team execution
        Agent Runtime
        Workspace Boundary
```

### Research Lifecycle

**Research Topic**:
The root research problem or investigation intent that initiates an investigation, such as "Why is CUDA kernel A faster than kernel B?" A Research Topic frames user intent, Project context, constraints, optional Measurable Objectives, and the Topic Agent Team Profile specialization used to investigate it.
_Avoid_: Research Goal, Research Inquiry, Research Task, project, workspace

**Measurable Objective**:
An optional metric, target, tolerance, or optimization direction contained by a Research Topic. A Research Topic can have zero, one, or many Measurable Objectives, and a measurable objective does not make the topic non-exploratory.
_Avoid_: Goal kind, exclusive measurable goal, benchmark only

**Research Inquiry**:
A question or line of inquiry under a Research Topic, produced by the user, Operator Agent, or Agent Team Instance to work out the topic. A Research Inquiry can have lifecycle state, Decision Records, Artifacts, Inquiry Relationships, Research Tasks, and one or more Runs through those tasks. It is not a parallel execution scope.
_Avoid_: Research Topic, Research Task, Research Branch, parallel execution scope, quest, project, workspace, run

**Research Inquiry Relationship**:
A typed connection between Research Inquiries under a Research Topic, such as decomposes, follows from, contradicts, supports, blocks, supersedes, or alternative to. Inquiry relationships form an exploration graph and do not imply that inquiry must be represented as a tree.
_Avoid_: Research Branch, route, experiment route, path, Git branch unless referring to an actual Git branch

**Research Task**:
A bounded development, setup, experiment, analysis, writing, or operational action inside a Topic Workspace that helps answer a Research Inquiry. A Research Task belongs to one Research Inquiry and one Research Topic, has expected inputs and outputs, names an accountable task handler, and can be attempted through one or more Runs. The task handler can be the Operator Agent or a delegated Agent Instance from an Agent Team Instance. For task-level parallel execution, a Research Task can also record multiple participating Agent Instances from the selected Agent Team Instance.
_Avoid_: Task Scope, Topic Workspace, Run, Workflow Stage, task workspace, general to-do item

**Run**:
A bounded execution attempt for one Research Task. A Run has its own lifecycle, status, actor participation, prompts, tool calls, handoffs, outputs, and logs; its records are stored through the Workspace Runtime.
_Avoid_: Research task, research inquiry, workspace, quest

**Control Mode**:
A Run-level setting that defines whether the Operator Agent controls the Run automatically or manually. In `automatic` mode, the Operator Agent or scheduler may dispatch according to the approved workflow and Gate policy. In `manual` mode, the Operator Agent drives selected task Agent Instances or Service Agent Instances through direct manual handoffs according to the user's prompt scope.
_Avoid_: Project mode, Research Inquiry mode, global manual switch, handoff-only mode

**Manual Mode**:
A Control Mode for a Run where the Operator Agent sends direct messages to delegated task Agent Instances or Service Agent Instances through durable handoffs, watches configured completion signals, and records completion in Workspace Runtime. Manual Mode does not bypass Gates, and it does not make file creation, channel replies, or direct inspection authoritative without Operator Agent normalization.
_Avoid_: Direct human operation of Agent Instances, untracked operator chat, bypass mode

### Team and Agent Execution

**Domain Agent Team Template**:
A reusable multi-agent template based on the research methodology of a research field. It names default Agent Roles, Workflow Stages, Coordination Policy, Capability Binding slots, and template parameters, but it does not include a user's concrete research topic, project paths, credentials, or launch choices.
_Avoid_: Topic Agent Team Profile, Agent Team Instance, live team, project-specific team, provider-specific team as the core term

**Topic Agent Team Profile**:
A topic-level specialization of one Domain Agent Team Template for a user's research topic. It adapts the domain method to the topic context, selects or tunes roles and Workflow Stages, records constraints and expected Artifacts, and can be reviewed or edited before launch; it is not a running team.
_Avoid_: Domain Agent Team Template, Agent Team Instance, Run, live team, ad hoc role list

**Agent Team Instance**:
A concrete runtime team created from a Topic Agent Team Profile by the Operator Agent or Execution Adapter. It has launched Agent Instances, runtime refs, Agent Workspaces, and Run participation. Topic Workspaces can reference multiple Agent Team Instances when the user runs topic-level parallel execution.
_Avoid_: Domain Agent Team Template, Topic Agent Team Profile, workspace-local team, ad hoc role list

**Parallel Execution Scope**:
The approved level where the user or Operator Agent starts concurrent execution. Topic-level parallel execution runs different Agent Team Instances under one Research Topic, usually to compare team profiles, strategies, or independent inquiry paths. Task-level parallel execution distributes one Research Task across multiple Agent Instances inside the selected Agent Team Instance. Research Inquiry is not a parallel execution scope.
_Avoid_: Research Inquiry parallelism, branch-level parallelism, implicit parallelism without a recorded scope

**Agent Team**:
An umbrella phrase for a multi-agent structure. Use **Domain Agent Team Template** for the research-field method, **Topic Agent Team Profile** for the user's topic-level specialization, and **Agent Team Instance** for the runtime team. Avoid using **Agent Team** alone in schema names, manifest fields, or GUI labels when template, profile, or instance is the intended meaning.
_Avoid_: Provider-specific specialist group, prompt bundle, full execution graph, role list only, concrete team when template, profile, or instance is meant

**Service Team**:
A built-in Isomer operational support team that provides common helper work for Projects, Topic Workspaces, Runs, Agent Workspaces, and Agent Instances. The Service Team can configure development environments for a target Agent Workspace and tech stack, repair dependency, runtime, tool, or system compatibility issues, collect diagnostics, and write support Artifacts. Service Team members act at the command of the Operator Agent through specific Service Requests. The Service Team is not a Domain Agent Team Template, Topic Agent Team Profile, or Agent Team Instance, and it does not own Research Topics, Research Claims, Gates, or research decisions.
_Avoid_: Research Agent Team, Topic Agent Team Profile, Agent Team Instance, hidden Execution Adapter behavior, untracked sysadmin work

**Service Request**:
A bounded operational support command from the Operator Agent to the Service Team. A Service Request names the supported Project, Topic Workspace, Run, Agent Workspace, Agent Instance, or tech-stack scope; specific task; expected support output; authorization scope; Service Dispatch Form; and completion observation rules. A Service Request can support a Research Task or Run, but it is not itself a Research Task or Workflow Stage.
_Avoid_: Research Task, Workflow Stage, untracked support chat, generic ticket without Isomer provenance

**Service Dispatch Form**:
The runtime form the Operator Agent uses to route a Service Request to the Service Team. In `tool_native_subagent` form, the Operator Agent uses native multi-agent or subagent tooling available in its own execution surface. In `launched_service_agent` form, the Operator Agent or Execution Adapter launches or resolves Service Agent Instances and dispatches Service Requests to them, similar to launching an agent team. The dispatch form is an implementation choice; it does not change Operator Agent command authority or provenance obligations.
_Avoid_: Control Mode, Agent Team Instance, Workflow Stage, hidden backend worker

**Agent Role**:
A named responsibility inside a Domain Agent Team Template, Topic Agent Team Profile, or Agent Team Instance, such as operator, scout, coder, experimenter, analyst, writer, or reviewer. An Agent Role describes work ownership, expected inputs and outputs, authority, and handoff obligations; it is not a concrete runtime actor.
_Avoid_: Persona, participant type, worker label

**Agent Profile**:
A provider-neutral reusable description of how to construct or configure an Agent Instance. An Agent Profile can reference instructions, skills, model posture, tool access, execution environment, credentials, mailbox defaults, memory defaults, and launch posture without assuming one backend's document model.
_Avoid_: Topic Agent Team Profile, Agent Definition, provider-specific specialist as the generic term, hardcoded agent config, live agent

**Capability Binding**:
The connection between an Agent Role or Agent Profile and the capabilities available to it, such as tools, skills, model profiles, data access, credentials, execution adapters, communication channels, or workspace permissions.
_Avoid_: Binding as an unqualified term, hardcoded runner, tool config, provider-specific profile

**Agent Instance**:
A concrete runtime actor created from an Agent Profile and assigned to an Agent Role for a Run or team execution context. Agent Instances own Agent Workspaces; Agent Roles describe responsibilities and workflow ownership.
_Avoid_: Agent Role as the runtime actor, worker, provider-specific managed agent as the generic term

**Service Agent Instance**:
A runtime service actor from the Service Team that handles Service Requests at the command of the Operator Agent. A Service Agent Instance can be represented by a tool-native subagent invocation or by a launched service agent, depending on the Service Dispatch Form. It may inspect or modify the authorized support surfaces named by a Service Request, such as a target Agent Workspace's environment setup, but it must record support Artifacts and Provenance Records. It is not a task handler for a Research Task and must not make research decisions.
_Avoid_: Agent Team Instance member, research task Agent Instance, Operator Agent, Execution Adapter internals

**Operator Agent**:
The project-facing Agent Role and corresponding Agent Instance that acts as the main interaction point with the user, specializes Domain Agent Team Templates into Topic Agent Team Profiles, launches Topic Agent Team Profiles into Agent Team Instances, controls or delegates Research Tasks, resolves fallback handling, and records task routing decisions. Human users operate through the Operator Agent: user-origin commands, approvals, Gate decisions, and task-routing changes enter Isomer through the Operator Agent. The Operator Agent can handle a Research Task directly or delegate it to a team Agent Instance.
_Avoid_: Controller as a separate entity outside Agent Role and Agent Instance, backend-specific operator implementation

**Coordination Policy**:
The rules that govern how Agent Instances collaborate inside a Topic Agent Team Profile or Agent Team Instance. A Coordination Policy can define operator behavior, peer communication, handoff routing, review loops, conflict handling, retry behavior, escalation, fallback behavior, and Gates.
_Avoid_: Orchestration code, implicit team convention, backend-specific routing rules

**Completion Watcher Contract**:
A resolved per-handoff declaration of how the Operator Agent will observe candidate completion for a delegated task. It can be derived from Coordination Policy defaults and handoff overrides, and can include Agent Instance inspection, file observation, channel replies, adapter events, validation rules, correlation keys, and staleness rules.
_Avoid_: Completion source of truth, adapter-only callback, unrecorded watcher convention

**Execution Adapter**:
A backend-specific bridge that maps Isomer's generic Domain Agent Team Template, Topic Agent Team Profile, Agent Team Instance, Agent Profile, Agent Instance, Capability Binding, Run, Agent Workspace, and Artifact concepts onto a concrete execution engine. Execution Adapters must not change Isomer's core domain language.
_Avoid_: Research Engine Adapter, backend as the core engine, native-agent layer as the Isomer model, provider lock-in

**Workflow Stage**:
A named step in a Domain Agent Team Template, Topic Agent Team Profile, or Agent Team Instance workflow. A Workflow Stage has an owning Agent Role, expected inputs and outputs, handoff behavior, and optional Gate policy.
_Avoid_: Pipeline step, quest stage, task only

**Task Handler**:
The Agent Instance responsible for directly handling a Research Task or controlling its delegated execution. A Task Handler is usually the Operator Agent for project interaction and fallback work, or one Agent Instance from the selected Agent Team Instance for specialized work.
_Avoid_: Owning workspace, task type, unmanaged worker

### Agent Workspace and Collaboration

**Agent Workspace**:
A per-agent work area inside a Topic Workspace assigned to one Agent Instance for owned scratch files, local runtime state, logs, and Agent Artifacts. It is an advisory ownership boundary: Isomer records and documents expected access, but does not provide filesystem-grade access control.
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

**Artifact Core Record**:
The generic minimal index for one Artifact. It contains only stable Artifact id, Topic Workspace id, Artifact kind, status, locator kind, locator, timestamps, and media type when known. Lifecycle refs, producer refs, Run refs, Provenance Record refs, Evidence Item refs, supersession refs, format profile refs, extension refs, validation outcomes, and renderer hints attach through links, metadata records, Provenance Records, or other accepted recording APIs.
_Avoid_: Format-specific Artifact schema, full artifact content, mandatory extension record

**Artifact Format Profile**:
An optional declarative profile for content-level Artifact expectations. It can describe Artifact kind applicability, media type expectations, schema refs, template refs, validation hints, renderer hints, export hints, opaque future capability refs, compatibility version, and status. It must not define executable validators, renderers, exporters, command requests, provider contracts, adapter-specific runtime behavior, or mandatory Artifact core fields.
_Avoid_: Command runner, validator implementation, renderer implementation, provider plugin, required Artifact field

**Artifact Extension**:
An optional additive metadata contract for topic-specific Artifact metadata, such as CUDA kernel metadata or GPU hardware context. It can add extension records, metadata records, sidecar Artifacts, validation hints, or renderer hints linked to an Artifact Core Record, but it must not shadow, rename, or redefine core Artifact fields or accepted durable record refs.
_Avoid_: Core Artifact schema, mandatory Artifact field, replacement record type

**Research Claim**:
A statement made inside a Research Topic or Research Inquiry that may need support, contradiction handling, or withdrawal. A Research Claim can be open, supported, refuted, or withdrawn.
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

**Signal Observation**:
A recorded observation from a Completion Watcher Contract, such as a file appearing, a channel reply arriving, an Agent Instance inspection result, or an adapter event. A Signal Observation can support completion normalization, but it is not authoritative completion until the Operator Agent records the handoff result in Workspace Runtime.
_Avoid_: Handoff completion, source of truth, raw log as state

**Gate**:
A recorded decision point that must return to the human user before the governed action proceeds. Gates apply to irreversible or claim-shaping decisions, not every Workflow Stage boundary.
_Avoid_: Approval step, interaction request, manual checkpoint

### GUI and Views

**View Manifest**:
An engine-produced data document that describes a durable task-specific GUI view, including view type, data sources, data bindings, user actions, pending Gates, optional registered component refs, and optional GUI Layout Spec refs. The GUI Renderer renders View Manifests, while Workspace Runtime, Artifacts, and Provenance Records own durable research state.
_Avoid_: View spec, generated frontend code, dashboard config

**GUI Backend**:
The built-in HTTP server started by `isomer-cli` for a Project. It binds a local or configured address, reports a URL for the user to open in a browser, serves the predefined GUI Renderer, exposes GUI Backend APIs, reads View Manifests and referenced Artifacts, receives authenticated AG-UI Event Batches, validates GUI Component Registry entries, resolves AG-UI Render Payloads to registered GUI Components, and owns GUI Runtime State. It does not own canonical research state.
_Avoid_: Research engine, GUI as state owner, direct human control surface for team agents, untracked event sink

**GUI Renderer**:
The predefined browser-side GUI served by the GUI Backend URL. It renders task-specific interactive views from View Manifests, GUI Layout Specs, registered GUI Components, GUI Component Instances, and live updates produced from AG-UI Render Payloads. It reflects GUI Runtime State changes from the GUI Backend immediately, while the engine owns semantic research state and view intent.
_Avoid_: Generated GUI, engine UI, fixed dashboard

**GUI Component**:
A registered display or interaction unit that the GUI Renderer can use to visualize data, DSL, JSON, or Artifact refs supplied through View Manifests or AG-UI Render Payloads. Use **Built-in GUI Component** for Isomer-shipped components, **Project GUI Component** for project-supplied components, and **Agent-generated GUI Component** when the component was produced by an Agent Instance.
_Avoid_: Arbitrary frontend code, unregistered plugin, view manifest as a component, raw AG-UI payload as a component

**Built-in GUI Component**:
A GUI Component shipped with Isomer and registered by the built-in GUI Backend at startup. Built-in GUI Components are versioned with Isomer, have `builtin` origin, do not have a project producer, and do not require per-component user approval.
_Avoid_: Project plugin, agent-generated component, custom component

**Project GUI Component**:
A GUI Component supplied by the Project rather than shipped with Isomer. Project GUI Components can be human-authored or agent-generated. They must be registered before use and should carry project path, source, compatibility, approval, and provenance metadata.
_Avoid_: Built-in component, arbitrary frontend file, unregistered custom component

**Agent-generated GUI Component**:
A Project GUI Component produced by an Agent Instance. It must carry producer Agent Instance identity and Provenance Record refs when available. If it is executable, it needs validation, sandbox or isolation policy, and approval or approve-all before loading.
_Avoid_: Built-in component, human-authored component, generated GUI

**GUI Component Instance**:
A live mounted use of one registered GUI Component inside GUI Runtime State. A GUI Component Instance has an instance id, component id, data or Artifact refs, optional AG-UI Render Payload refs, layout placement, visible state, and lifecycle status.
_Avoid_: Component definition, artifact, view manifest, browser DOM node as a domain object

**Declarative GUI Component Spec**:
A data-only Project GUI Component definition that selects rendering behavior from supported GUI primitives. This is the preferred format for Project GUI Components, especially Agent-generated GUI Components, because it can be validated without executing project-provided UI code.
_Avoid_: Generated frontend code, executable plugin when data-only rendering is enough

**Executable GUI Component**:
A Project GUI Component implemented as executable UI code with a component manifest. It must be registered, validated, sandboxed or isolated according to policy, and approved before the GUI Backend loads it. If it is agent-generated, approve-all can remove repeated per-component approval until revoked.
_Avoid_: Direct file load, unchecked component code, implicit approval

**GUI Component Registry**:
The registry of GUI Components available to the GUI Backend and GUI Renderer. It includes Built-in GUI Components and Project GUI Components. It records component id, component origin (`builtin` or `project`), producer kind (`isomer`, `human`, or `agent`), component kind (`builtin`, `declarative`, or `executable`), source paths, manifest paths, dependency declarations, build outputs, sandbox policy, producer Agent Instance when applicable, approval state, compatibility version, and status. Every GUI Component must be registered before use.
_Avoid_: Component folder as authority, package manager as authority, ad hoc imports

**AG-UI Render Payload**:
A data, DSL, or JSON payload sent through the AG-UI protocol to request or update a GUI visualization. It can include data refs, inline small data, schema metadata, visualization intent, component id hints, and optional GUI Layout Spec refs. The GUI Backend resolves an AG-UI Render Payload to one or more registered GUI Components and GUI Component Instances.
_Avoid_: Frontend source code, component definition, canonical artifact content, direct browser manipulation

**AG-UI Event Batch**:
A live protocol batch published to the GUI Backend by the Operator Agent or an authenticated Agent Team Instance member. It can carry AG-UI Render Payloads, GUI Runtime State updates, component-instance updates, layout updates, or tool-call rendering events. Direct AG-UI publishing is for low-latency updates, previews, and registered component output; it is not canonical research state.
_Avoid_: View Manifest, Artifact, Provenance Record, durable state transition

**AG-UI Event Envelope**:
The durable metadata record for an AG-UI Event Batch. The envelope stores publisher identity, Project, Topic Workspace, Run, Agent Team Instance, Agent Instance, component id, Artifact refs, timestamps, status, and retention policy. The envelope is persisted by default, while full event payload content is saved only by explicit user instruction.
_Avoid_: Full event replay by default, prompt log, canonical artifact content

**GUI Component Approve-All Policy**:
A project-scoped approval posture that the human user enables through the Operator Agent. While active, registered Agent-generated GUI Components that are executable and pass validation may load without per-component approval until the policy is revoked. It does not apply to Built-in GUI Components because they do not require per-component approval, and it does not bypass registration, validation, sandbox policy, compatibility checks, or AG-UI publisher authentication.
_Avoid_: Session-only approval, workspace-only approval, bypassing validation

**GUI Runtime State**:
The GUI Backend-owned live state for a browser GUI session or project GUI session. It includes active Topic Workspace and view selection, GUI Component Instances, AG-UI Render Payload refs, layout state, filters, selections, expanded panels, pending visual updates, and connection status. It can be changed through GUI Backend APIs and reflected immediately by the GUI Renderer. It is not canonical research state unless converted into an Artifact, View Manifest, Decision Record, or Provenance Record.
_Avoid_: Workspace Runtime, research state, durable artifact, browser-only state

**GUI Backend API**:
An authenticated API exposed by the GUI Backend for creating, updating, and inspecting GUI Runtime State. The Operator Agent, engine, and authorized Agent Team Instance members can use it to publish AG-UI Render Payloads, create or update GUI Component Instances, adjust layout, and refresh views. GUI Backend APIs must not bypass Gate resolution or turn team Agent Instances into direct human-operated control surfaces.
_Avoid_: Research engine API, unrestricted browser API, direct filesystem control

**GUI Layout Spec**:
A JSON document or JSON-compatible object that declares how registered GUI Component Instances are arranged in the GUI Renderer. It can define component slots, panels, tabs, split views, ordering, sizing, grouping, and responsive behavior. It references registered component ids or component instance ids; it does not contain executable frontend code.
_Avoid_: CSS theme, generated frontend layout code, canonical research state

## Identifier Guidance

### Project and Workspace

- Use `project_root` for the root path of the user-owned Project.
- Use `project_config_dir` for `.isomer-labs/`.
- Use `project_manifest` for `.isomer-labs/manifest.toml`.
- Use `research_topic_config` for Project Manifest-registered topic-specific defaults and refs.
- Use `topic_workspace` for a manifest-declared topic-level workspace.
- Use `topic_workspace_id` for references to the Topic Workspace that owns topic runtime state and files.
- Use `effective_topic_context` for the resolved process-local context consumed by `isomer-cli`, Workspace Path Resolution, Run initialization, and future Execution Adapter command requests.
- Use `research_task` for bounded work recorded inside one Topic Workspace.
- Use `task_handler` for the Operator Agent or delegated Agent Team Instance member responsible for a Research Task.
- Use `workspace_runtime` for the persistent workspace substrate that stores and validates state across many Runs.
- Use `agent_workspace` only for a per-agent work area inside a Topic Workspace.
- Avoid bare `workspace` when the scope could mean Project, Topic Workspace, or Agent Workspace.

### Research Lifecycle

- Use `research_topic` for the root research problem or investigation intent that initiates work and topic-level team specialization.
- Use `research_inquiry` for a user-facing line of inquiry.
- Use `measurable_objective` for optional metric, target, tolerance, or optimization-direction fields contained by a Research Topic.
- Use `inquiry_relationship` or `research_inquiry_relationship` for typed graph links between Research Inquiries.
- Use `research_task_id` for a bounded work item recorded inside a Topic Workspace.
- Use `parallel_execution_scope` for the approved level of concurrent execution; valid values are Research Topic and Research Task, not Research Inquiry.
- Use `run` for one bounded execution episode recorded in Workspace Runtime.
- Use `control_mode` for the Run-level distinction between `automatic` and `manual`.
- Use `prompt_scope_kind` for the Manual Mode distinction between `single_stage` and `multi_step`.

### Team and Agent Execution

- Use `domain_agent_team_template`, `topic_agent_team_profile`, `agent_team_instance`, `operator_agent`, `agent_role`, `agent_profile`, `agent_instance`, `capability_binding`, `coordination_policy`, `execution_adapter`, and `workflow_stage` for team and execution concepts.
- Use `service_team` for the built-in operational support team, `service_request` for one bounded support assignment, and `service_agent_instance` for the runtime support actor.
- Use `service_dispatch_form` for the Operator Agent's Service Request routing choice. Use `tool_native_subagent` when the Operator Agent uses native subagent or multi-agent tooling, and `launched_service_agent` when the Operator Agent or Execution Adapter launches or resolves service agents and dispatches requests to them.
- Use terms such as `operator`, `reviewer`, `writer`, `coder`, `experimenter`, or `scout` as Agent Role kinds. Model `operator_agent` as an Agent Role and Agent Instance identity, not as a separate entity table outside the generic agent model.
- Use `completion_watcher_contract` or `watcher_contract` for the resolved per-handoff completion observation contract.

### Agent Workspace and Collaboration

- Use `agent_workspace` for a per-agent work area inside a Topic Workspace.
- Use `agent_runtime` for execution state and support files scoped to one Agent Workspace.
- Use `agent_artifact` when an Artifact's producing or owning agent matters.
- Use `workspace_boundary` for advisory ownership and readable-surface declarations.
- Use `peer_read_access` for non-enforced cross-agent reading.

### Artifacts, Evidence, and Decisions

- Use `artifact`, `artifact_core_record`, `artifact_format_profile`, `artifact_extension`, `gate`, and `provenance_record` for durable output, optional topic-specific Artifact expectations, decision-point, and production-history concepts.
- Use `research_claim`, `evidence_item`, `finding`, and `decision_record` for claim/evidence/decision semantics.
- Use `signal_observation` for observed completion signals before Operator Agent normalization.

### GUI and Views

- Use `view_manifest`, `gui_backend`, and `gui_renderer` for the durable view contract, HTTP backend, and client renderer.
- Use `gui_component` as the umbrella component term.
- Use `built_in_gui_component` for Isomer-shipped components registered by the GUI Backend at startup.
- Use `project_gui_component` for Project-supplied components.
- Use `agent_generated_gui_component` only when the component was produced by an Agent Instance.
- Use `component_origin` for `builtin` versus `project`.
- Use `producer_kind` for `isomer`, `human`, or `agent`.
- Use `component_kind` for `builtin`, `declarative`, or `executable`.
- Use `gui_component_instance`, `declarative_gui_component_spec`, `executable_gui_component`, and `gui_component_registry` for component handling.
- Use `ag_ui_render_payload` for data, DSL, or JSON sent through AG-UI to request or update visualizations.
- Use `ag_ui_event_batch` for live AG-UI traffic and `ag_ui_event_envelope` for the persisted metadata record.
- Use `gui_runtime_state` for backend-owned live GUI state.
- Use `gui_backend_api` for authenticated APIs that create, update, or inspect GUI Runtime State.
- Use `gui_layout_spec` for JSON layout declarations.
- Use `gui_component_approve_all_policy` for the project-scoped executable component approval posture.

## Relationships

### Project and Research Lifecycle

- A **Project** has one **Project Config Directory**.
- A **Project** is the outer container and is not a **Topic Workspace**.
- A **Project Config Directory** contains one **Project Manifest**.
- A **Project Config Directory** is config and discovery state; it does not own **Workspace Runtime** or research **Artifacts**.
- A **Project Manifest** declares zero or more **Research Topics**, **Research Topic Config** paths, and **Topic Workspaces**.
- A **Research Topic Config** belongs to one **Research Topic** and stores defaults and refs, not Runtime state.
- A **Project** contains zero or more **Research Topics**.
- A **Research Topic** has zero or one active **Topic Workspace** at a time, and may have historical Topic Workspaces after migration, archive, or fork operations.
- A **Topic Workspace** belongs to one **Research Topic**.
- A **Research Topic** contains zero or more **Measurable Objectives**.
- A **Research Topic** can be exploratory whether or not it contains Measurable Objectives.
- A **Research Topic** contains a graph of zero or more **Research Inquiries**.
- A **Research Inquiry** belongs to one **Research Topic**.
- A **Research Inquiry Relationship** connects two **Research Inquiries** under a **Research Topic**.
- A **Research Inquiry** can span one or more **Research Tasks**.
- A **Research Inquiry** is not a **Parallel Execution Scope**.
- A **Research Task** belongs to one **Research Inquiry** and one **Topic Workspace**.
- A **Research Task** records one accountable **Task Handler**: the **Operator Agent** or a delegated **Agent Instance** from a selected **Agent Team Instance**.
- A **Research Task** may record multiple participating **Agent Instances** for task-level parallel execution inside the selected **Agent Team Instance**.
- A **Research Task** can be attempted through one or more **Runs**.
- A **Run** has one **Control Mode**.
- **Manual Mode** is a **Control Mode** for a Run, not a Project, Research Inquiry, or Research Task mode.
- A **Topic Workspace** owns one **Workspace Runtime**.
- A **Workspace Runtime** stores, indexes, validates, and recovers **Run** records, but it is not itself a Run.
- **Effective Topic Context** is resolved before topic-scoped CLI behavior and supplies selected refs to Workspace Path Resolution without becoming durable research state.

### Team and Agent Execution

- A **Topic Workspace** may contain many **Agent Workspaces** during team execution.
- An **Agent Workspace** is contained by exactly one **Topic Workspace**.
- An **Agent Workspace** belongs to one **Agent Instance** within a team execution context.
- An **Agent Workspace** contains one **Agent Runtime** and zero or more **Agent Artifacts**.
- **Agent Runtime** is subordinate to **Workspace Runtime**.
- A **Domain Agent Team Template** contains default **Agent Roles**, **Workflow Stages**, **Coordination Policy**, **Capability Binding** slots, and template parameters for one research field or method family.
- A **Topic Agent Team Profile** specializes one **Domain Agent Team Template** for a user's research topic.
- A **Topic Agent Team Profile** contains topic-adapted **Agent Roles**, **Workflow Stages**, **Coordination Policy**, **Capability Bindings**, constraints, and expected **Artifacts**, but it is not running.
- An **Agent Team Instance** is created from one **Topic Agent Team Profile** by the **Operator Agent** or **Execution Adapter**.
- An **Agent Team Instance** contains runtime **Agent Instances**, launch refs, **Agent Workspaces**, Run participation, and resolved execution state.
- Topic-level **Parallel Execution Scope** runs multiple **Agent Team Instances** under one **Research Topic**.
- Task-level **Parallel Execution Scope** distributes one **Research Task** across multiple **Agent Instances** within one selected **Agent Team Instance**.
- **Research Inquiry** must not be used as a **Parallel Execution Scope**.
- All non-operator task **Agent Instances** belong to an **Agent Team Instance**.
- A **Topic Workspace** may reference selected **Agent Team Instances** for topic-level execution, and individual **Research Tasks** record the task handler and participating Agent Instances that perform the work.
- Reusable **Domain Agent Team Templates**, editable **Topic Agent Team Profiles**, and **Agent Team Instance** refs live outside the Topic Workspace.
- The built-in **Service Team** is Isomer infrastructure, not a **Domain Agent Team Template**, **Topic Agent Team Profile**, or **Agent Team Instance**.
- A **Project** can use the built-in **Service Team** without declaring it as a project research team.
- The **Operator Agent** may open a **Service Request** for a **Project**, **Topic Workspace**, **Run**, **Agent Workspace**, **Agent Instance**, or tech-stack support scope.
- Service Team members act only through specific **Service Requests** from the **Operator Agent**.
- A **Service Request** can support a **Research Task** or **Run**, but it is not a **Research Task** or **Workflow Stage**.
- The **Operator Agent** chooses a **Service Dispatch Form** for each **Service Request**.
- In `tool_native_subagent` form, the **Operator Agent** may use its native multi-agent or subagent tool surface to assign the support task.
- In `launched_service_agent` form, the **Operator Agent** or **Execution Adapter** may launch or resolve **Service Agent Instances** and dispatch **Service Requests** to them.
- The **Service Team** handles **Service Requests** through **Service Agent Instances** regardless of dispatch form.
- **Service Agent Instances** are outside **Agent Team Instance** membership and cannot be selected as **Task Handlers** for **Research Tasks**.
- When a **Service Agent Instance** changes project, workspace, runtime, dependency, or environment state, the **Operator Agent** records the **Service Request**, support **Artifacts**, and **Provenance Records**.
- Workspace-scoped **Service Requests** use **Workspace Runtime** for handoff and completion records.
- An **Agent Profile** describes how an **Execution Adapter** can construct or configure an **Agent Instance**.
- An **Agent Instance** is assigned to one **Agent Role** for a Run or team execution context.
- An **Agent Role** may be served by different **Agent Instances** across retries, Runs, or adapter implementations.
- The **Operator Agent** is the main user interaction point, task controller, team-specialization actor, team-launch actor, and final fallback handler.
- Human users operate through the **Operator Agent** for commands, approvals, Gate decisions, and task-routing changes.
- A **Coordination Policy** defines how Agent Instances communicate, hand off work, review outputs, escalate decisions, and use Gates.
- A **Coordination Policy** can define default **Completion Watcher Contracts** for manual handoffs.
- A manual handoff stores its resolved **Completion Watcher Contract** before the Operator Agent sends the direct message.
- An **Execution Adapter** may map Isomer **Agent Profiles** to backend-specific launch material, but those backend concepts are adapter details.
- A **Workspace Boundary** declares intended write ownership and **Peer Read Access** for an **Agent Workspace**.
- A **Workspace Boundary** belongs to an **Agent Workspace**, but it is not itself a workspace.
- **Peer Read Access** allows inspection of declared readable files, but it does not grant write ownership or filesystem-grade protection.
- **Agent Artifacts** can be promoted or referenced as workspace-level **Artifacts**, **Evidence Items**, or handoff inputs.
- A **Workspace Runtime** records **Runs**, **Artifacts**, **Provenance Records**, **Gates**, **View Manifests**, and workspace-scoped **AG-UI Event Envelopes**.
- In Manual Mode, **Workspace Runtime** is authoritative for handoff completion. **Signal Observations** from files, channels, inspection, or adapter events are inputs to Operator Agent normalization.
- The **Operator Agent**, when delegating work, coordinates other **Agent Instances** according to the selected **Topic Agent Team Profile** and runtime **Agent Team Instance** **Coordination Policy**.

### Artifacts, Evidence, and Decisions

- A **Research Claim** can be supported, contradicted, or contextualized by one or more **Evidence Items**.
- A **Finding** is distilled from Research Claims and Evidence Items.
- A **Decision Record** may resolve a **Gate**, select or create a **Research Inquiry**, record a **Research Inquiry Relationship**, archive a Research Topic, or record another meaningful choice.
- A **Decision Record** should cite relevant **Evidence Items**, **Artifacts**, or **Provenance Records** when the choice depends on research evidence.
- A **Gate** can block a Workflow Stage action until the human user resolves it.
- An **Artifact Core Record** remains valid when an **Artifact Format Profile** or **Artifact Extension** is missing, unsupported, disabled, or unknown.
- **Artifact Format Profiles** and **Artifact Extensions** attach as optional refs or metadata; they do not become mandatory core Artifact fields.

### GUI and Views

- The **GUI Backend** starts through `isomer-cli`, reports a URL, and serves the predefined browser-side **GUI Renderer**.
- The user opens the **GUI Backend** URL in a browser to use the predefined GUI.
- The **GUI Renderer** renders **View Manifests** emitted from Workspace Runtime state.
- The **GUI Backend** reads **View Manifests**, **Artifacts**, **GUI Layout Specs**, and **GUI Component Registry** entries, then serves the **GUI Renderer**.
- The **GUI Component Registry** contains both **Built-in GUI Components** and **Project GUI Components**. All **GUI Components** must be registered before use.
- **Built-in GUI Components** have `builtin` component origin and `isomer` producer kind.
- **Project GUI Components** have `project` component origin and `human` or `agent` producer kind.
- **Agent-generated GUI Components** are **Project GUI Components** with `agent` producer kind and producer Agent Instance provenance.
- **Declarative GUI Component Spec** and **Executable GUI Component** describe implementation kind for **Project GUI Components**; they do not replace origin or producer fields.
- A **GUI Component Instance** is the live mounted use of a registered **GUI Component** inside **GUI Runtime State**.
- Agents use **GUI Components** by sending data, DSL, JSON, or refs as **AG-UI Render Payloads** through the AG-UI protocol. They do not call browser components directly.
- The **GUI Backend** resolves **AG-UI Render Payloads** to registered **GUI Components** and creates or updates **GUI Component Instances**.
- The **GUI Backend** may receive **AG-UI Event Batches** directly from authenticated **Agent Team Instance** members.
- **GUI Backend APIs** can manipulate **GUI Runtime State**; the **GUI Renderer** reflects those changes immediately.
- **GUI Layout Specs** control arrangement of registered **GUI Component Instances** and can be referenced by **View Manifests** or **AG-UI Render Payloads**.
- Direct **AG-UI Event Batches** are live GUI traffic. Durable recovery should use **Workspace Runtime**, **Artifacts**, **View Manifests**, **AG-UI Event Envelopes**, and **Provenance Records**.
- **AG-UI Event Envelopes** are persisted by default; full AG-UI payload content is saved only by explicit user instruction.
- Direct agent publishing to the **GUI Backend** does not mean direct human operation of team **Agent Instances**. Human user actions still enter through the **Operator Agent**.
- **Executable GUI Components** must be registered, validated, sandboxed or isolated according to policy, and approved before loading when approval is required.
- The **GUI Component Approve-All Policy** applies to agent-generated **Executable GUI Components**. It is project-scoped, revocable, and subordinate to registration, validation, sandbox policy, compatibility checks, and publisher authentication.

## Flagged Ambiguities

### Project and Research Lifecycle

- Use **Project Config Directory** for `.isomer-labs/`. Reserve "control plane" for compact runtime state, especially SQLite-backed Workspace Runtime state.
- Do not use bare "workspace" when **Project**, **Topic Workspace**, and **Agent Workspace** are all plausible readings.
- Do not call **Project** or **Project Config Directory** a workspace.
- Use **Research Topic Config** for topic-specific defaults and refs. Do not use it for **Workspace Runtime** state, command logs, research records, rich Artifact contents, or secrets.
- Use **Effective Topic Context** for resolved process input to topic-scoped command behavior. Do not describe it as durable lifecycle state or a full snapshot stored on every Run.
- Use **Topic Workspace** instead of "quest" or "quest workspace" for Isomer-managed research execution areas. "Quest" is DeepScientist reference language, not Isomer canonical language.
- Use **Research Topic** for the root research problem or investigation intent that initiates the research and drives Topic Agent Team Profile specialization. Do not use **Research Goal** as a separate level.
- Use **Measurable Objective** only for optional metric-bearing content inside a **Research Topic**. Do not model measurable and exploratory as exclusive goal kinds.
- Use **Research Inquiry** for questions or lines of inquiry under a **Research Topic**. Do not use **Topic Workspace** when discussing pause, resume, archive, or topic-level steering unless the storage location itself matters.
- Use **Research Inquiry Relationship** for graph links between inquiries. Do not use **Research Branch** unless quoting stale docs or referring to a separate compatibility migration.
- Use **Research Task** for a bounded unit of work recorded inside one Topic Workspace.
- Use **Task Handler** for the **Operator Agent** or delegated **Agent Team Instance** member that controls the Research Task.
- Use **Parallel Execution Scope** only at the **Research Topic** level or **Research Task** level. Do not describe a **Research Inquiry** as running in parallel.
- Use **Workspace Runtime** for the persistent state substrate owned by a Topic Workspace. Use **Run** only for bounded execution attempts for a Research Task.
- Use **Control Mode** for Run-level manual versus automatic control. Do not describe Manual Mode as a Project-wide or Research Inquiry-wide switch.

### Team and Agent Execution

- Use **Agent Workspace** for per-agent work areas inside a Topic Workspace. Do not call it a secure sandbox.
- Do not put `teams/` under a **Topic Workspace**. **Domain Agent Team Templates**, **Topic Agent Team Profiles**, and **Agent Team Instance** refs are project-level or built-in references; the workspace records Topic Agent Team Profile identity, Agent Team Instance identity, and task-handler identity through manifest refs, Workspace Runtime, or provenance Artifacts.
- Use **Domain Agent Team Template**, **Topic Agent Team Profile**, **Agent Team Instance**, **Operator Agent**, **Agent Role**, **Agent Profile**, **Capability Binding**, **Coordination Policy**, **Agent Instance**, **Workflow Stage**, and **Execution Adapter** as the generic multi-agent core.
- Use **Agent Instance** for the concrete runtime actor that owns an Agent Workspace. Do not use **Agent Role** as the workspace owner except when discussing responsibility or workflow ownership.
- Use **Operator Agent** for the user-facing controller, topic-profile author, team launcher, task router, and fallback handler. Do not model direct human operation of team Agent Instances or runtime state. Use **Coordination Policy** for the rules that govern collaboration among delegated team agents.
- Manual Mode still routes user intent through the **Operator Agent**. Do not describe manual direct messages as untracked human-to-agent chat.
- Use **Completion Watcher Contract** for the resolved per-handoff watcher rules. Do not treat file creation, channel replies, direct inspection, or adapter events as authoritative completion until the **Operator Agent** records the handoff result in **Workspace Runtime**.
- Treat the **Operator Agent** as outside Agent Team Instance membership. Every other task Agent Instance should be a member of an Agent Team Instance.
- Use **Service Team** only for common operational support, such as environment setup, dependency repair, runtime diagnostics, and system compatibility fixes. Do not assign research ownership, Research Claims, or Gate decisions to the Service Team.
- Treat **Service Team** work as Operator Agent commanded work. Do not describe Service Team members as self-directed agents that interpret user goals or choose research actions.
- Use **Service Dispatch Form** to describe whether a Service Request used native subagent tooling or launched service agents. Do not model launched Service Agent Instances as a research **Agent Team Instance**.
- Record user-visible environment repair or setup mutation as a **Service Request** when it creates Artifacts or changes project, workspace, runtime, dependency, or environment state. Do not hide this work only inside **Execution Adapter** internals.
- A **Service Request** authorization scope documents intended support access. Do not describe it as filesystem-grade isolation or security enforcement.
- Operator, reviewer, writer, coder, experimenter, and scout should be Agent Role kinds, not separate entity types.
- Treat Houmao's specialist, project profile, native role, recipe, launch dossier, and managed-agent concepts as possible mappings inside a Houmao **Execution Adapter**. Do not use them as Isomer core terms.

### Agent Workspace and Collaboration

- Use **Peer Read Access** for the advisory collaboration rule that lets agents inspect declared peer files. It does not prevent an agent with system tools from modifying files, so do not describe it as filesystem access control.
- Use **Workspace Boundary** for README- or manifest-declared ownership/readability rules. Use **Handoff**, **Artifact**, **Evidence Item**, or **Provenance Record** when another agent's read becomes a durable dependency.

### Artifacts, Evidence, and Decisions

- Use **Research Claim** for statements that need evidence status. Use **Finding** only after evidence has been distilled into a reusable insight.
- Use **Decision Record** for the durable result of a choice. Use **Gate** for the pending decision point before that choice is resolved.
- Use **Signal Observation** for raw or normalized completion-signal observations that have not yet become authoritative handoff completion.
- Use **Artifact Core Record** for the minimal generic Artifact index.
- Use **Artifact Format Profile** for declarative content expectations only. Do not use it for executable validation, rendering, export, provider behavior, or command requests.
- Use **Artifact Extension** for additive topic metadata only. Do not let an extension shadow, rename, or redefine core Artifact fields.

### GUI and Views

- Use **View Manifest** instead of "view spec" or "dashboard config" for engine-produced GUI description files.
- Use **GUI Renderer** for the predefined browser-side GUI served by the **GUI Backend**. Do not call agent-generated components a generated GUI.
- Use **GUI Runtime State** for live backend-owned UI state. Do not confuse it with **Workspace Runtime**.
- Use **GUI Layout Spec** for JSON layout declarations. Do not put executable frontend layout code in layout specs.
- Use **AG-UI Render Payload** for data, DSL, JSON, or refs sent through AG-UI for visualization.
- Use **AG-UI Event Batch** for live GUI event traffic, not for durable research state.
- Use **AG-UI Event Envelope** for persisted metadata about direct AG-UI traffic. Do not assume full payload replay is available unless the user explicitly enabled payload retention.
- Use **Built-in GUI Component** only for Isomer-shipped, backend-registered components.
- Use **Project GUI Component** for project-supplied components, whether human-authored or agent-generated.
- Use **Agent-generated GUI Component** only when producer Agent Instance identity matters.
- Avoid "custom GUI Component" as a canonical term because it hides whether the component is human-authored, agent-generated, project-supplied, or built-in.
- Use **GUI Component Registry** as the authority for **Built-in GUI Components** and **Project GUI Components**. Do not describe the GUI Backend as loading arbitrary project UI files directly.
- Prefer **Declarative GUI Component Spec** for **Project GUI Components** when data-only rendering is sufficient. Use **Executable GUI Component** only when a declarative spec cannot express the interaction.
- Agents should provide data, DSL, JSON, Artifact refs, component hints, and layout refs through AG-UI. They should not manipulate browser DOM or component internals directly.
- Direct **AG-UI Event Batches** from team agents are allowed for GUI updates, but user commands, approvals, Gate decisions, and task-routing changes still go through the **Operator Agent**.
