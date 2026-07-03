# System Design

This page describes the current Isomer Labs architecture: Project discovery, Effective Topic Context, Workspace Path Resolution, Workspace Runtime, Topic Team Specialization from Domain Agent Team Template to Topic Agent Team Profile, Agent Team Instance creation, the Operator Agent role, the Execution Adapter boundary, and the boundary between implemented behavior and future roadmap behavior.

## Project Discovery

`isomer-cli` discovers a Project by walking up from the current working directory until it finds a `.isomer-labs/` Project Config Directory. You can override the Project root with `isomer-cli project --root <path> ...` and the Project Manifest with `isomer-cli project --manifest <path> ...`, but normal operation relies on the discovered `.isomer-labs/manifest.toml`.

The Project Manifest is the authority for:

- Research Topic ids and their Research Topic Config paths.
- Topic Workspace ids and their filesystem paths.
- Explicit Research Topic to Pixi environment bindings through repeated `topic_pixi_environment_bindings` entries.
- Explicit Topic Workspace Pixi binding targets through repeated `topic_standalone_pixi_bindings` entries with `manifest_path_or_dir`, plus the implicit Topic Workspace directory default when no explicit standalone target exists.
- Project defaults such as the default Research Topic id and default Topic Workspace id.
- Path defaults such as the generated content root and default Topic Workspace base.
- Domain Agent Team Template refs, Topic Agent Team Profile refs, and Agent Team Instance refs.

Isomer never infers topic-to-environment relationships from Research Topic ids, Pixi environment names, or naming conventions such as `<topic-slug>-<env-purpose>`. Project-root bindings must be explicit. Topic Workspace bindings either use an explicit `manifest_path_or_dir` target or the registered Topic Workspace directory default, which Pixi resolves with `pixi info --json --manifest-path <target>`.

## Effective Topic Context

For a topic-scoped command, `isomer-cli` resolves an Effective Topic Context that includes:

- the validated Project and Project Manifest;
- the selected Research Topic and its Research Topic Config;
- the selected Topic Workspace;
- Project Manifest topic Pixi environment bindings when relevant;
- optional lifecycle refs such as Research Inquiry, Research Task, Run, Agent Team Instance, Agent Instance, and Topic Agent Team Profile;
- topic-level defaults such as Topic Agent Team Profile refs, Execution Adapter refs, Capability Binding refs, Skill Binding Projection refs, Research Operation Extension Point refs, and policy refs;
- source metadata so Workspace Path Resolution, Run initialization, Execution Adapter Command Requests, and provider-backed extension operations can trace where refs came from.

Effective Topic Context is process-local input. It is not a lifecycle object, not Workspace Runtime state, and not stored wholesale on every Run.

## Workspace Path Resolution

Workspace Path Resolution turns Effective Topic Context and a requested semantic label into concrete filesystem paths. Its read modes are side-effect-free: they compute paths without creating directories, writing runtime records, or launching agents.

Path surfaces include reserved labels such as `topic.workspace`, `topic.runtime.db`, `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.tracked.*`, `topic.agents_root`, `topic.records.*`, `topic.runtime`, `topic.tmp`, `topic.actors.output_root`, `agent.workspace`, `agent.output_root`, `agent.private_artifacts`, `agent.public_share`, `agent.links`, and `agent.tmp`. User-defined storage lives under `custom.*`, while additional topic repositories may use grouped `topic.repos.*` labels. Helper-created non-main topic repositories default under `repos/extern/...`, but the labels remain the storage API. Topic Workspace Manifest bindings use `label`, `path`, and explicit `storage_profile`; `storage_profile` supplies the context, lifecycle, visibility, safety, and Git semantics that a path string cannot safely imply.

The canonical `isomer-default.v1` Topic Workspace and Agent Workspace layout, including default paths such as `repos/topic-main`, `repos/extern/...` for helper-created non-main repositories, `repos/topic-main/isomer-managed/`, `agents/<agent-name>` worktrees, per-agent branch namespaces, tracked Isomer material, agent-owned untracked shares, topic-owned projections, generated links, topic-owned Pixi task channels, and launch cwd expectations, is defined in [Topic Workspace Definition](topic-workspace-definition.md).

`isomer-cli project paths preview` prints the computed path plan for a topic without creating files. `project paths get`, `project paths list`, `project paths default`, `project paths explain`, and `project outputs policy` are also read-only. Worker output trackedness is not a separate Isomer policy: `.gitignore` and Git status decide whether plain generated files are tracked or committable. Mutating storage commands are explicit: `project paths materialize-default`, `project paths materialize`, `project paths register`, `project paths update`, `project paths unregister`, `project paths reset`, and `project repos create`.

## Workspace Runtime

Workspace Runtime is the persistent substrate inside a Topic Workspace. It owns:

- `state.sqlite`, the SQLite database that stores runtime records;
- schema version metadata;
- Path Plan records for durable surfaces;
- lifecycle records for Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Topic Workspace, Topic Agent Team Profile, Artifact, Gate, Research Claim, Evidence Item, Decision Record, and Provenance Record;
- Agent Team Instance records, Agent Instance records, and Agent Workspace records;
- Topic Environment Readiness records;
- Validation Issue records;
- adapter manifest refs, reconciliation records, payload refs, command run records, materialization records, launch attempt records, inspection snapshots, and stop outcome records.

`isomer-cli project runtime init` creates or reopens the Workspace Runtime. Reopening a current-schema runtime is idempotent. Runtime initialization records the Topic Main Development Repository, `repos/topic-main/isomer-managed/`, and projection label path plans, but it does not replace topic environment setup and does not create per-agent untracked share directories before Agent Workspace setup. Unsupported older or newer runtime schemas produce diagnostics and do not create runtime directories or rewrite owner refs.

`isomer-cli project runtime prepare` records Topic Environment Readiness by checking explicit Project Manifest bindings and the implicit Topic Workspace directory default when no explicit standalone binding exists. Successful checks record `ready`; failed checks record `failed`; missing required topic binding intent records `blocked`. Repair remains explicit and should be represented as a Service Request rather than hidden inside `project runtime prepare`.

`isomer-cli project runtime inspect` and `isomer-cli project runtime validate` are read-only. They report metadata, record counts, readiness summaries, path-plan mismatches, broken refs, missing Agent Workspace directories, missing `isomer-managed/` support paths, stale legacy support refs, unsafe generated links, unpromoted dependencies on untracked shares, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, schema mismatches, and cross-topic leakage without repairing records or creating files.

## From Template to Profile to Instance

A **Domain Agent Team Template** is a reusable research-field method. It names default Agent Roles, Workflow Stages, Coordination Policy, Capability Binding slots, and template parameters, but it does not include a concrete research topic or project paths.

**Topic Team Specialization** adapts one Domain Agent Team Template for one Research Topic. It resolves topic context, template placeholders, role bindings, Workflow Stages, policy refs, and copied template material choices before the team becomes launch-facing runtime state.

A **Topic Agent Team Profile** specializes one Domain Agent Team Template for a user's Research Topic. It adapts roles and Workflow Stages to the topic context, records constraints and expected Artifacts, and can carry Capability Binding refs, Skill Binding Projections, allowed Research Operation Extension Points, and policy refs. It is a design-time artifact, not a running team.

An **Agent Team Instance** is a concrete runtime team created from a Topic Agent Team Profile. It contains launched Agent Instances, runtime refs, Agent Workspaces, and Run participation. `isomer-cli project team-instances create` writes the Agent Team Instance record, Agent Instance records, Agent Workspace records, Agent Workspace path plans, `isomer-managed/` support path plans, initial Workflow Stage Cursor records, and provenance refs, and materializes Agent Workspace directories. It does not launch backend agents or write adapter-specific launch material.

Topic-level Parallel Execution Scope means multiple Research Topics run concurrently, each researched by its own dedicated Agent Team Instance. It does not mean one Research Topic is handled by multiple competing teams. Task-level Parallel Execution Scope distributes one Research Task across multiple Agent Instances inside the selected topic team. Research Inquiry is not a Parallel Execution Scope.

## Operator Agent

The **Operator Agent** is the project-facing Agent Role and corresponding Agent Instance that acts as the main interaction point with the user. It performs Topic Team Specialization, launches Topic Agent Team Profiles into Agent Team Instances, controls or delegates Research Tasks, resolves fallback handling, and records task routing decisions.

Human users operate through the Operator Agent. User-origin commands, approvals, Gate decisions, and task-routing changes enter Isomer through the Operator Agent. The Operator Agent can handle a Research Task directly or delegate it to a team Agent Instance.

The Operator Agent is outside Agent Team Instance membership. Every other task Agent Instance should be a member of an Agent Team Instance.

## Execution Adapter Boundary

An **Execution Adapter** is a backend-specific bridge that maps Isomer's generic concepts onto a concrete execution engine. The current implementation provides a Houmao Execution Adapter. The adapter:

- maps Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instance records, Agent Profiles, and Agent Instances to Houmao launch material;
- invokes Houmao through the public `houmao-mgr --print-json` CLI boundary;
- stores command payloads and JSON manifests under the Topic Workspace;
- records adapter refs, manifest refs, reconciliation records, launch attempts, inspection snapshots, and stop outcomes in Workspace Runtime.

Execution Adapters must not change Isomer's core domain language. Houmao's specialist, project profile, native role, recipe, launch dossier, and managed-agent concepts belong inside the Houmao adapter; they are not promoted to generic Isomer terms.

## State Ownership Summary

| Domain object | Owned by | Notes |
|---|---|---|
| Project Config Directory | Project | configuration and discovery state |
| Project Manifest | Project Config Directory | discovery authority for topics, workspaces, bindings |
| Research Topic Config | Project Config Directory | topic defaults and refs, no runtime state |
| Topic Workspace | Research Topic | filesystem work area |
| Workspace Runtime | Topic Workspace | durable runtime substrate |
| Agent Workspace | Agent Instance | per-agent work area inside Topic Workspace |
| Agent Runtime | Agent Workspace under `isomer-managed/agent-owned/runtime/` | local execution state and support files |
| Agent Team Instance record | Workspace Runtime | runtime identity, refs, status |
| Agent Instance record | Workspace Runtime | runtime actor identity |
| Research Inquiry, Research Task, Run | Workspace Runtime | lifecycle records |
| Artifact, Evidence Item, Finding, Decision Record, Provenance Record | Workspace Runtime | durable research outputs and history |
| Adapter manifests and payloads | Topic Workspace files | durable adapter records |
| GUI Runtime State | GUI Backend | live UI state, not canonical research state |

## Roadmap Boundaries

The current Milestone 1-5 CLI focuses on Project discovery, Project Manifest validation, Effective Topic Context inspection, semantic Workspace Path Resolution, Domain Agent Team Template and Topic Agent Team Profile checks, Workspace Runtime records for topic environment readiness, pre-launch Agent Team Instance state, and Houmao-backed launch paths.

The following features exist in the domain language and roadmap but are not described here as implemented behavior:

- full Research Inquiry graph execution with Runs through Operator Agent dispatch;
- Operator Agent handoff normalization across adapters;
- GUI Backend and View Manifest runtime rendering;
- Service Request dispatch through launched Service Agent Instances;
- Gates, Decision Records, and Evidence Items beyond schema support;
- full research Artifact provenance chains.

When these features are mentioned in other pages, they are explicitly labeled as planned or partially implemented.
