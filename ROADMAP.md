# Isomer Labs Roadmap

## Current Baseline

Isomer Labs is currently a design-heavy, implementation-light repository. The executable package under `src/isomer_labs/` is only a placeholder, while the strongest assets are the accepted platform language, manifested workspace engine design, manual mode design, OpenSpec contracts, the `skillset/research-paradigm/` skill bundle, the skillset validator, and the generated `teams/deepsci-org/execplan/` Domain Agent Team Template material.

The roadmap below turns those assets into an interactive, semi-automatic research-conduction platform where a human user works through the Operator Agent, Topic Workspaces hold durable research state, multi-agent teams execute bounded Research Tasks, and GUI views expose task-specific Artifacts, Gates, and next actions.

## Milestone 1: Platform Skeleton and Project Discovery

Goal: establish the smallest runnable Isomer core around Project discovery, Project Manifest validation, Research Topic Config loading, and Workspace Path Resolution.

Major steps:

- [x] Create an `isomer-cli` entrypoint with project-scoped commands for `init`, `validate`, `topics list`, `workspaces list`, and `schemas list`.
- [x] Define initial Python models for Project, Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Effective Topic Context, and Workspace Path Resolution.
- [x] Implement deterministic topic selection from explicit selectors, current directory, supported `ISOMER_*` identity refs, `.isomer-labs/local.toml`, and Project Manifest defaults.
- [x] Implement built-in Topic Workspace path defaults, supported path override handling, canonicalization, external-path rejection, and source reporting.
- [x] Convert the current design examples into fixture Projects and unit tests.
- [ ] Keep `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills` passing as the baseline quality gate.

Exit criteria:

- A user can create or validate a Project with one Research Topic and one Topic Workspace without launching agents.
- CLI errors name the neutral Isomer concept first and the concrete bad file, field, or path second.

## Milestone 2: Workspace Runtime and Research Records

Goal: make Topic Workspaces durable by adding SQLite-backed Workspace Runtime state plus file-backed research records.

Major steps:

- [ ] Implement Workspace Runtime creation with schema versioning, migration checks, and default directories for `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`.
- [ ] Add lifecycle tables and APIs for Research Topics, Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, Workflow Stage Cursors, and Agent Team Instance lifecycle state.
- [ ] Add minimal Artifact Core Records and recording APIs for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates.
- [ ] Record resolved paths and path sources before downstream Runs, Artifacts, logs, Agent Workspaces, or View Manifests depend on them.
- [ ] Add validation for missing Artifact files, broken refs, invalid lifecycle transitions, unresolved Gates, unsupported Research Claims, stale provenance, and schema-version mismatches.
- [ ] Add integration tests for creating, reopening, validating, and repairing a minimal Topic Workspace.

Exit criteria:

- A Topic Workspace can survive process restart with Research Topic, Research Inquiry, Research Task, Run, Artifact, Gate, and Provenance state intact.
- Validation reports durable workspace issues without silently deleting records.

## Milestone 3: Team Templates, Profiles, and Execution Adapters

Goal: turn the existing research-paradigm skills and `deepsci-org` generated package into launchable, provider-neutral team material.

Major steps:

- [ ] Define file formats and validators for Domain Agent Team Templates, Topic Agent Team Profiles, Agent Profiles, Agent Roles, Workflow Stages, Coordination Policies, Capability Bindings, and Skill Binding projections.
- [ ] Treat `teams/deepsci-org/execplan/` as the first seed Domain Agent Team Template, while preserving topic-specific values as placeholders until a Topic Agent Team Profile specializes them.
- [ ] Implement Topic Agent Team Profile specialization from a Research Topic, Effective Topic Context, selected roles, expected Artifacts, Gate policy refs, scheduler policy refs, Capability Binding refs, and Skill Binding projection refs.
- [ ] Add Agent Team Instance records and Agent Workspace creation with advisory Workspace Boundary files.
- [ ] Implement the provider-neutral Execution Adapter Command Request envelope for command execution, repository inspection, package management, service requests, agent launch, and other Research Operation Extension Points.
- [ ] Build a first Houmao-oriented adapter shim that maps Isomer records to maintained Houmao launch, mail, mailbox, gateway, and inspection surfaces without making Houmao terms core schema names.

Exit criteria:

- A user can specialize the `deepsci-org` Domain Agent Team Template into a Topic Agent Team Profile and validate it before launch.
- The system can prepare an Agent Team Instance plan and Agent Workspaces without requiring automatic execution.

## Milestone 4: Operator Control Loop and Manual Mode

Goal: implement the user-steered research loop where the Operator Agent controls Runs, opens handoffs, normalizes completion, and records decisions.

Major steps:

- [ ] Implement Run creation with `control_mode` values `manual` and `automatic`, plus manual prompt-scope metadata for `single_stage` and `multi_step`.
- [ ] Add handoff-before-send behavior for manual direct messages to delegated Agent Instances.
- [ ] Resolve Completion Watcher Contracts from Coordination Policy and copy the resolved contract onto each handoff.
- [ ] Implement Signal Observation records for agent inspection, file observation, channel replies, and adapter events.
- [ ] Implement completion normalization so downstream state changes only after the Operator Agent accepts a result and records produced Artifact refs and Provenance Records.
- [ ] Add Gate handling for baseline waiver, credential use, cost, private data, destructive mutation, publication-facing output, claim strengthening, finalization, and archival actions.
- [ ] Add CLI commands for listing, inspecting, retrying, rerouting, closing, or parking Runs and handoffs.
- [ ] Add Service Team and Service Request support for environment setup, dependency repair, diagnostics, and workspace maintenance.

Exit criteria:

- A manual Run can dispatch one bounded Research Task, observe completion, record outputs, stop at Gates, and recover after restart.
- Multi-step manual prompts continue only through user-declared steps and stop for ambiguity, failure, stale handoffs, or governed actions.

## Milestone 5: Task-Specific GUI and End-to-End Research Loops

Goal: expose the research engine through task-specific views while keeping Workspace Runtime and the Operator Agent as the semantic authority.

Major steps:

- [ ] Define and validate the initial View Manifest schema for Artifact lists, Run timelines, Research Claim graphs, experiment matrices, decision queues, figure review, and next-action panels.
- [ ] Build the GUI Backend started by `isomer-cli`, with Project resolution, Workspace Runtime reads, View Manifest loading, GUI Runtime State, and authenticated GUI Backend APIs.
- [ ] Build the predefined GUI Renderer with Built-in GUI Components for tables, timelines, markdown Artifacts, evidence links, Gate resolution, and Run or handoff status.
- [ ] Implement GUI Component Registry validation for Built-in GUI Components, Declarative GUI Component Specs, Project GUI Components, and Executable GUI Components.
- [ ] Implement AG-UI Render Payload routing, GUI Component Instance updates, GUI Layout Specs, AG-UI Event Envelope persistence, publisher authentication, and explicit full-payload retention opt-in.
- [ ] Add project-scoped GUI Component Approve-All Policy with validation, revocation, and audit records.
- [ ] Drive one end-to-end use case from `.imsight-arts/project-explore/use-cases/`: create a Research Topic, specialize a team, run manual handoffs, record Artifacts and Gates, emit View Manifests, and inspect the result in the GUI.

Exit criteria:

- A user can run a complete observable research pass from CLI or GUI, inspect durable Artifacts and decisions, resolve Gates through the Operator Agent path, and resume from Workspace Runtime state.
- GUI live updates remain separate from canonical research state, with AG-UI Event Envelopes retained by default and full payloads retained only by explicit user instruction.

## Cross-Cutting Work

- [ ] Keep the canonical domain language in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` aligned with schemas, CLI labels, GUI labels, and code identifiers.
- [ ] Promote OpenSpec contracts into tests before implementing each major API.
- [ ] Preserve research-paradigm skillset validation as a release gate.
- [ ] Prefer small, inspectable records over opaque automation, especially around Gates, Evidence Items, Research Claims, and Provenance Records.
- [ ] Keep user-owned Project files first-class: Isomer should manage Topic Workspaces and records without forcing all research work into a hidden platform directory.
