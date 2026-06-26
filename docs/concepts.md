# Concepts

This page summarizes the canonical Isomer Labs domain language. The full source lives in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`; this page selects the concepts most useful when reading the rest of the documentation.

## Project and Workspace

**Project**: a user-owned repository, checkout, or directory tree that Isomer Labs manages. A Project becomes Isomer-managed when it has a `.isomer-labs/` Project Config Directory and a Project Manifest that declares Research Topics and Topic Workspaces.

**Project Config Directory**: the `.isomer-labs/` directory at the project root. It stores project-level configuration and references, especially the Project Manifest, Research Topic Config files, Domain Agent Team Template refs or material, the single Topic Agent Team Profile Bundle ref for each Research Topic, Agent Team Instance refs, Agent Profile refs, Artifact Format Profile refs, Artifact Extension refs, and GUI Component Registry refs. It does not own Workspace Runtime state, Topic Agent Team Profile Bundle bodies, default cache, or temporary files.

**Project Manifest**: the `.isomer-labs/manifest.toml` file. It is the discovery authority for Research Topics, Research Topic Config paths, Topic Workspaces, explicit Topic Workspace Pixi workspace bindings through repeated `topic_standalone_pixi_bindings` entries with `manifest_path_or_dir`, optional Project-root Pixi environment bindings through repeated `topic_pixi_environment_bindings` entries, and project defaults. When no explicit Topic Workspace Pixi binding exists, the registered Topic Workspace directory is the implicit default Pixi binding target.

**Research Topic Config**: a Project Manifest-registered TOML file for one Research Topic. It stores topic-specific defaults and refs, such as a short topic statement, Measurable Objectives, default Research Inquiry refs, the Topic Agent Team Profile Bundle ref, Execution Adapter refs, Capability Binding refs, Skill Binding Projection refs, and policy refs. It does not own Pixi environment bindings or Workspace Runtime state.

**Research Topic**: the root research problem or investigation intent that initiates work and Topic Team Specialization.

**Topic Workspace**: a project-local directory declared by the Project Manifest and managed by Isomer Labs for one Research Topic. It owns the topic's Workspace Runtime, Pixi manifest and environment, Topic Agent Team Profile Bundle, Research Inquiry graph, Research Tasks, Runs, rich research Artifacts, generated View Manifests, Agent Workspaces, and logs.

**Workspace Runtime**: the persistent runtime substrate inside a Topic Workspace. It includes `state.sqlite`, schema version, runtime directories, refs, validation state, and support files that let Research Inquiries, Research Tasks, Runs, Artifacts, handoffs, Gates, and View Manifests be recorded, resumed, inspected, and validated.

**Effective Topic Context**: the resolved process-local context that `isomer-cli`, Workspace Path Resolution, Run initialization, Execution Adapter Command Requests, and provider-backed extension operations consume for a topic-scoped command. It is not a lifecycle object, not Workspace Runtime state, and not stored wholesale on every Run.

## Research Lifecycle

**Research Inquiry**: a question or line of inquiry under a Research Topic. A Research Inquiry can have lifecycle state, Decision Records, Artifacts, Inquiry Relationships, Research Tasks, and one or more Runs.

**Research Task**: a bounded development, setup, experiment, analysis, writing, or operational action inside a Topic Workspace that helps answer a Research Inquiry. A Research Task belongs to one Research Inquiry and one Research Topic, names a Task Handler, and can be attempted through one or more Runs.

**Run**: a bounded execution attempt for one Research Task. A Run has its own lifecycle, status, actor participation, prompts, tool calls, handoffs, outputs, and logs recorded through Workspace Runtime.

**Control Mode**: a Run-level setting that defines whether the Operator Agent controls the Run automatically or manually. In `automatic` mode, the Operator Agent or scheduler may dispatch according to the approved workflow and Gate policy. In `manual` mode, the Operator Agent drives selected task Agent Instances or Service Agent Instances through direct manual handoffs.

## Team and Agent Execution

**Domain Agent Team Template**: a reusable multi-agent template based on the research methodology of a research field. It names default Agent Roles, Workflow Stages, Coordination Policy, Capability Binding slots, and template parameters, but it does not include a user's concrete research topic, project paths, credentials, or launch choices.

**Topic Agent Team Profile**: a topic-level specialization of one Domain Agent Team Template for a user's research topic. It adapts the domain method to the topic context, selects or tunes roles and Workflow Stages, records constraints and expected Artifacts, and can carry role-scoped or Workflow Stage-scoped Capability Binding refs, Skill Binding Projections, allowed Research Operation Extension Points, and policy refs. Each Research Topic has one authoritative Topic Agent Team Profile at a time; topic-level parallelism means multiple Research Topics researched by different dedicated teams, not one topic researched by multiple teams. For deep specialization, it is stored as a Topic Agent Team Profile Bundle inside the owning Topic Workspace. It can be reviewed or edited before launch; it is not a running team.

**Topic Team Specialization**: the design-time process that adapts one Domain Agent Team Template for one Research Topic and produces or revises that topic's Topic Agent Team Profile and Topic Agent Team Profile Bundle. It resolves topic context, template placeholders, role bindings, Workflow Stages, policy refs, expected Artifacts, copied template material choices, and launch-facing blockers. It ends before Agent Team Instance creation or live launch.

**Topic Agent Team Profile Bundle**: a fixed Topic Workspace directory, `<topic-workspace>/team-profile/`, that stores the Research Topic's one authoritative Topic Agent Team Profile and its editable topic-specialized material. It contains `profile.toml`, the approved Topic Team Instantiation Packet, copied and topic-modified template material such as `execplan/`, validation outputs, and provenance refs. The Project Manifest keeps a ref to the bundle for discovery.

**Agent Team Instance**: a concrete runtime team created from a Topic Agent Team Profile by the Operator Agent or Execution Adapter. It has launched Agent Instances, runtime refs, Agent Workspaces, and Run participation.

**Agent Role**: a named responsibility inside a Domain Agent Team Template, Topic Agent Team Profile, or Agent Team Instance, such as operator, scout, coder, experimenter, analyst, writer, or reviewer. An Agent Role describes work ownership; it is not a concrete runtime actor.

**Agent Profile**: a provider-neutral reusable description of how to construct or configure an Agent Instance. An Agent Profile can reference instructions, skills, model posture, tool access, execution environment, credentials, mailbox defaults, memory defaults, and launch posture.

**Agent Instance**: a concrete runtime actor created from an Agent Profile and assigned to an Agent Role for a Run or team execution context. Agent Instance ids are globally unique by design. Agent Instances own Agent Workspaces.

**Operator Agent**: the project-facing Agent Role and corresponding Agent Instance that acts as the main interaction point with the user, performs Topic Team Specialization, launches Topic Agent Team Profiles into Agent Team Instances, controls or delegates Research Tasks, resolves fallback handling, and records task routing decisions. Human users operate through the Operator Agent.

**Execution Adapter**: a backend-specific bridge that maps Isomer's generic Domain Agent Team Template, Topic Agent Team Profile, Agent Team Instance, Agent Profile, Agent Instance, Capability Binding, Run, Agent Workspace, and Artifact concepts onto a concrete execution engine. Execution Adapters must not change Isomer's core domain language.

**Service Team**: a built-in Isomer operational support team that provides common helper work for Projects, Topic Workspaces, Runs, Agent Workspaces, and Agent Instances. The Service Team acts at the command of the Operator Agent through specific Service Requests.

**Service Request**: a bounded operational support command from the Operator Agent to the Service Team. It names the supported scope, specific task, expected output, authorization scope, Service Dispatch Form, and completion observation rules.

## Agent Workspace and Collaboration

**Agent Workspace**: a per-agent work area inside a Topic Workspace assigned to one globally unique Agent Instance for owned scratch files, local runtime state, logs, and Agent Artifacts. Runtime uses `<topic-workspace>/agents/<agent-instance-id>/` by default, or an approved `agent_workspace_ref` under the selected Topic Workspace when profile or packet material names one. It uses the parent Topic Workspace Pixi environment by default and remains an advisory ownership boundary: Isomer records expected access, but does not provide filesystem-grade access control.

**Agent Runtime**: the durable execution state and support files scoped to one Agent Workspace, such as prompt records, tool-call traces, temporary run notes, local logs, and recovery files for that agent.

**Workspace Boundary**: an advisory boundary that declares which parts of an Agent Workspace an agent owns and which parts peers may inspect. Boundaries can be documented in README files or declared in manifests, but Isomer does not rely on them for hard filesystem protection.

**Peer Read Access**: the advisory ability for one team agent to inspect another agent's declared readable files or Agent Artifacts without taking ownership of them. Durable dependencies should still be recorded through handoffs, promoted Artifacts, Evidence Items, or Provenance Records.

## Artifacts, Evidence, and Decisions

**Artifact**: a durable file or file-backed output produced or used during research work, such as a literature note, hypothesis, baseline report, experiment plan, result table, figure, report, Decision Record, prompt record, or tool output.

**Artifact Core Record**: the generic minimal index for one Artifact. It contains stable Artifact id, Topic Workspace id, Artifact kind, status, locator kind, locator, timestamps, and media type when known.

**Artifact Format Profile**: an optional declarative profile for content-level Artifact expectations, such as Artifact kind applicability, media type expectations, schema refs, template refs, validation hints, renderer hints, and export hints.

**Research Claim**: a statement made inside a Research Topic or Research Inquiry that may need support, contradiction handling, or withdrawal. A Research Claim can be open, supported, refuted, or withdrawn.

**Evidence Item**: a durable source of support, contradiction, or context for a Research Claim. An Evidence Item can reference an Artifact, result, measurement, analysis, source document, or external reference.

**Finding**: a reusable insight distilled from Research Claims and Evidence Items.

**Decision Record**: a durable record of a meaningful choice made by the user, the Operator Agent, or the team, including selected option, rationale, Evidence Items, consequences, actor, and timestamp.

**Provenance Record**: a durable record of how an Artifact, Decision Record, Research Claim, Evidence Item, or state transition was produced.

**Gate**: a recorded decision point that must return to the human user before the governed action proceeds. Gates apply to irreversible or claim-shaping decisions, not every Workflow Stage boundary.

## GUI and Views

**View Manifest**: an engine-produced data document that describes a durable task-specific GUI view, including view type, data sources, data bindings, user actions, pending Gates, optional registered component refs, and optional GUI Layout Spec refs.

**GUI Backend**: the built-in HTTP server started by `isomer-cli` for a Project. It binds a local or configured address, reports a URL for the user to open in a browser, serves the predefined GUI Renderer, exposes GUI Backend APIs, reads View Manifests and referenced Artifacts, receives authenticated AG-UI Event Batches, validates GUI Component Registry entries, and resolves AG-UI Render Payloads to registered GUI Components. It does not own canonical research state.

**GUI Renderer**: the predefined browser-side GUI served by the GUI Backend URL. It renders task-specific interactive views from View Manifests, GUI Layout Specs, registered GUI Components, GUI Component Instances, and live updates produced from AG-UI Render Payloads.

**AG-UI Render Payload**: a data, DSL, or JSON payload sent through the AG-UI protocol to request or update a GUI visualization.

**AG-UI Event Batch**: a live protocol batch published to the GUI Backend by the Operator Agent or an authenticated Agent Team Instance member. It can carry AG-UI Render Payloads, GUI Runtime State updates, component-instance updates, layout updates, or tool-call rendering events. Direct AG-UI publishing is for low-latency updates and previews; it is not canonical research state.
