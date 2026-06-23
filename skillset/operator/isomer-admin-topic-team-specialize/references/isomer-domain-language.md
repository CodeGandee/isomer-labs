# Isomer Domain Language

Use this local reference when running the Topic Team Specialization skill. It contains the domain terms needed by the skill so the skill does not depend on project-global notes outside its own directory.

## Core Project Terms

- **Project**: A user-owned repository, checkout, or directory tree managed by Isomer Labs. A Project is not a Topic Workspace.
- **Project Manifest**: The `.isomer-labs/manifest.toml` discovery file for Research Topics, Topic Workspaces, Domain Agent Team Templates, Topic Agent Team Profile Bundle refs, Agent Team Instance refs, provider bindings, Capability Binding refs, Skill Binding projections, and related registrations.
- **Research Topic Config**: A Project Manifest-registered TOML file for one Research Topic. It stores topic defaults and refs, not Workspace Runtime state, command output, rich Artifact content, credentials, or secrets.
- **Research Topic**: The root research problem or investigation intent that initiates Topic Team Specialization.
- **Topic Workspace**: A project-local directory declared by the Project Manifest and managed for one Research Topic. It owns Workspace Runtime, rich research Artifacts, Topic Agent Team Profile Bundle material, Research Inquiries, Research Tasks, Runs, Agent Workspaces, and logs.
- **Workspace Runtime**: Persistent runtime state inside a Topic Workspace. It records Runs, Artifacts, Provenance Records, Gates, View Manifests, handoffs, and validation state.
- **Effective Topic Context**: The resolved process-local context for a topic-scoped command. It includes validated project, topic, workspace, template/profile refs, policy refs, bindings, provider refs, source metadata, and optional lifecycle refs. It is not durable runtime state.

## Team and Agent Terms

- **Domain Agent Team Template**: A reusable multi-agent template for a research field. It names default Agent Roles, Workflow Stages, Coordination Policy, Capability Binding slots, and template parameters. It does not include a user's concrete topic, credentials, launch choices, or live runtime state.
- **Topic Team Specialization**: The design-time process that adapts one Domain Agent Team Template for one Research Topic. It produces or revises that topic's Topic Agent Team Profile and Topic Agent Team Profile Bundle, and it ends before Agent Team Instance creation, adapter launch materialization, or live agent launch.
- **Topic Team Instantiation Packet**: A reviewable planning and provenance artifact that records proposed or approved Topic Team Specialization output: source template refs, topic refs, bundle refs, role bindings, policy refs, expected Artifacts, resolved placeholders, copied material choices, proposed topic edits, explicit deferrals, approval provenance, and validation refs.
- **Topic Agent Team Profile**: The topic-level design-time specialization of one Domain Agent Team Template. It adapts roles, Workflow Stages, constraints, expected Artifacts, bindings, Skill Binding projections, policies, and launch-facing blockers for one Research Topic.
- **Topic Agent Team Profile Bundle**: The fixed Topic Workspace directory `<topic-workspace>/team-profile/` that stores the authoritative profile material for one Research Topic, including `profile.toml`, the approved packet, copied topic-edited template material, validation outputs, approval provenance, and launch-facing diagnostics.
- **Agent Team Instance**: A concrete runtime team created from the Topic Agent Team Profile. It has launched Agent Instances, runtime refs, Agent Workspaces, and Run participation.
- **Agent Role**: A named responsibility inside a Domain Agent Team Template, Topic Agent Team Profile, or Agent Team Instance.
- **Agent Instance**: A concrete runtime actor created from an Agent Profile and assigned to an Agent Role for a Run or team execution context.
- **Operator Agent**: The durable user-facing Agent Role and Agent Instance that performs Topic Team Specialization, launches Topic Agent Team Profiles into Agent Team Instances, controls or delegates Research Tasks, and records routing decisions.
- **Project Operator Session**: A project-aware operating posture of an agent that has Isomer system skills available and has been pointed at a Project root. It may act as the operator surface before a durable Operator Agent exists.

## Support and Adapter Terms

- **Service Team**: Built-in operational support actors for Projects, Topic Workspaces, Runs, Agent Workspaces, Agent Instances, and Topic Team Specialization support. Service Team members do not own Research Topics, Research Claims, Gates, or research decisions.
- **Service Request**: A bounded operational support command from a Project Operator Session or Operator Agent to the Service Team. It names scope, expected output, authorization, dispatch form, and completion observation rules.
- **Topic Service Agent**: A topic-scoped Service Agent Instance that handles Service Requests for one Research Topic or Topic Workspace. It remains outside Agent Team Instance membership.
- **Execution Adapter**: A backend-specific bridge from Isomer domain records to a concrete execution engine. Houmao concepts remain adapter details unless promoted into Isomer core language.
- **Execution Adapter Command Request**: A provider-neutral dispatch envelope for executable or provider-backed operations, including Service Request dispatch, Service Agent Instance launch, and Agent Team Instance launch operations.

## Artifact and Decision Terms

- **Artifact**: A durable file or file-backed output produced or used during research work.
- **Evidence Item**: A durable source of support, contradiction, or context for a Research Claim.
- **Finding**: A reusable insight distilled from Research Claims and Evidence Items.
- **Decision Record**: A durable record of a meaningful choice, including selected option, rationale, Evidence Items, actor, and timestamp.
- **Provenance Record**: A durable record of how an Artifact, Decision Record, Research Claim, Evidence Item, or state transition was produced.
- **Gate**: A recorded decision point that must return to the human user before a governed action proceeds.

## Naming Guardrails

- Use **Topic Workspace** only for the topic-level work area and **Agent Workspace** only for per-agent work areas inside a Topic Workspace.
- Use **Research Topic** for the root investigation intent, **Research Inquiry** for a line of inquiry, **Research Task** for bounded work, and **Run** for a bounded execution attempt.
- Use **Topic Team Specialization** for design-time template-to-topic adaptation. Do not call it Agent Team Instance creation, launch, or runtime team creation.
- Use **Topic Agent Team Profile Bundle** for `<topic-workspace>/team-profile/`. Do not create a topic-local team directory outside that bundle.
- Use **Project Operator Session** or **Operator Agent** for the user-facing operator surface. Do not model direct human operation of team Agent Instances.
- Treat Houmao specialist, launch dossier, managed-agent, and mailbox concepts as Execution Adapter implementation details unless an accepted Isomer schema explicitly promotes them.
