# Isomer Labs Roadmap

## Current Baseline

Isomer Labs now has a Milestone 1 `isomer-cli` implementation for Project discovery, Project Manifest validation, Effective Topic Context inspection, Workspace Path Resolution previews, built-in schema listing, and Project initialization. It also has Milestone 2 and 3 static validation for the `deepsci-org` Domain Agent Team Template, project-local template fixtures, and design-time Topic Agent Team Profiles for multiple Research Topics. Milestone 4 adds topic-scoped Workspace Runtime state with schema metadata, path plans, topic environment readiness records, pre-launch Agent Team Instance records, Agent Instance and Agent Workspace records, initial Workflow Stage Cursor records, validation, inspection, and two-topic isolation coverage. Milestone 5 adds the Houmao Execution Adapter launch, inspect, stop, reconciliation, adoption, manual handoff dispatch, Signal Observation, and Operator normalization path. The repo contains `teams/deepsci-org/`, a generated Domain Agent Team Template with intention source, execplan contracts, seven role profiles, generated skills, notifier prompts, a harness, a loop-local state contract, and an instantiation guide.

This version of Isomer Labs should make `deepsci-org` work inside the Isomer framework before broadening into other team templates. The main path is to register `deepsci-org` as a Domain Agent Team Template, specialize it into Topic Agent Team Profiles for different Research Topics, create pre-launch Agent Team Instance records inside Workspace Runtime, then let Milestone 5 map those records through a Houmao Execution Adapter and record the resulting Runs, handoffs, Artifacts, Gates, and Provenance Records inside topic-scoped Workspace Runtime state.

Houmao is the primary underlying implementation layer for Agent Team construction and management in this phase. Isomer keeps the generic domain language: Houmao roles, launch dossiers, mailboxes, gateway refs, specialists, and managed-agent details belong inside the Houmao Execution Adapter unless the canonical domain language explicitly promotes a term into Isomer core language.

## Use-Case Verification Plan

The use cases in `.imsight-arts/project-explore/use-cases/` are roadmap acceptance tests, not just examples. Each implementation milestone should either enable a new use-case test fixture, advance one use case from headless validation to live execution, or protect a previously enabled use case from regression.

- **UC-01 Explore a New Research Direction** becomes the first live vertical slice. It starts as a headless `deepsci-org` run with Project, Research Topic, Topic Agent Team Profile, Agent Team Instance, Artifacts, Evidence Items, a follow-up inquiry Gate, and CLI inspection before GUI polish.
- **UC-02 Reproduce a Baseline and Optimize It** verifies measured Runs, baseline acceptance or waiver Gates, optimization Research Tasks, Evidence Items, and Research Claims.
- **UC-03 Plan and Execute a Paper Revision** verifies multi-task planning, claim-risk mapping, targeted analysis Runs, response drafting, final approval Gates, and reviewer audit records.
- **UC-04 Generate a Task-Specific GUI Component** verifies GUI Backend, View Manifest, GUI Component Registry, AG-UI Event Envelope, and gated executable component behavior.
- **UC-05 Mix Manual and Automatic Runs** verifies automatic baseline work, single-stage manual repair, automatic candidate Runs, multi-step manual handoffs, Completion Watcher Contracts, Signal Observations, and durable closeout.
- **UC-06 Capstone Roadmap Verification with Flash Attention 4 Runtime Prediction on DGX Spark GB10** is the practical end-to-end acceptance test for this roadmap. It combines Project discovery, Pixi readiness, `deepsci-org` template validation, Topic Agent Team Profile specialization, Workspace Runtime, Houmao-backed Agent Team Instance launch, parallel topics, task-level fanout, Operator Agent handoffs, Service Requests, Gates, Artifacts, Evidence Items, Research Claims, CUDA/PTX/SASS-backed white-box execution-model records, component-time prediction views, model report packaging, and a pass/fail roadmap verification verdict.

## Milestone 1: Platform Skeleton and Project Discovery

Goal: establish the smallest runnable Isomer core around Project discovery, Project Manifest validation, Research Topic Config loading, and Workspace Path Resolution.

Major steps:

- [x] Create an `isomer-cli` entrypoint with project-scoped commands for `init`, `validate`, `topics list`, `workspaces list`, and `schemas list`.
- [x] Define initial Python models for Project, Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Effective Topic Context, and Workspace Path Resolution.
- [x] Implement deterministic topic selection from explicit selectors, current directory, supported `ISOMER_*` identity refs, `.isomer-labs/local.toml`, and Project Manifest defaults.
- [x] Implement built-in Topic Workspace path defaults, supported path override handling, canonicalization, external-path rejection, and source reporting.
- [x] Convert the current design examples into fixture Projects and unit tests.
- [x] Keep `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills` passing as the baseline quality gate.

Exit criteria:

- A user can create or validate a Project with one Research Topic and one Topic Workspace without launching agents.
- CLI errors name the neutral Isomer concept first and the concrete bad file, field, or path second.

## Milestone 2: deepsci-org Template Registration and Validation

Goal: make `teams/deepsci-org/execplan/` a first-class, validated Domain Agent Team Template that Isomer can discover and reason about.

Major steps:

- [x] Register or reference `teams/deepsci-org/execplan/` from Project Manifest or built-in template discovery without copying runtime state into a Topic Workspace.
- [x] Validate the generated package manifest, participant contract, role profiles, notifier prompts, generated skills, harness schemas, state contract, workspace contract, and run contract.
- [x] Map the seven template roles (`deepsci-org-master`, `framer`, `designer`, `experimenter`, `analyzer`, `publisher`, and `reviewer`) to Isomer Agent Roles, Workflow Stages, Capability Binding slots, and Skill Binding Projection slots.
- [x] Verify that topic-specific placeholders remain unresolved at the Domain Agent Team Template layer and are only filled by a Topic Agent Team Profile.
- [x] Add CLI and unit-test coverage for listing, inspecting, and validating Domain Agent Team Templates, with `deepsci-org` as the seed fixture.
- [x] Keep the generated `teams/deepsci-org/execplan/harness/bin/deepsci-org` validation path useful as a template-level diagnostic input.

Exit criteria:

- Isomer can report whether the `deepsci-org` Domain Agent Team Template is internally consistent.
- Validation rejects template material that already contains concrete Research Topic, Topic Workspace, Agent Team Instance, credential, launch, mailbox, or runtime truth.

## Milestone 3: Topic Agent Team Profile Specialization

Goal: specialize `deepsci-org` into separate Topic Agent Team Profiles for concrete Research Topics without starting any agents.

Major steps:

- [x] Extend Project Manifest and Research Topic Config loading to reference Domain Agent Team Templates, default Topic Agent Team Profiles, Execution Adapter refs, Capability Binding refs, Skill Binding Projection refs, Gate Policy refs, Scheduler Policy refs, provider refs, and baseline-waiver policy refs.
- [x] Implement Topic Agent Team Profile generation from `teams/deepsci-org/execplan/docs/instantiation-guide.md` and the execplan placeholder contracts.
- [x] Replace topic placeholders with Effective Topic Context refs, selected roles, expected Artifacts, Agent Profile refs, Capability Binding refs, Skill Binding Projection refs, Agent Workspace refs, policy refs, and provider refs.
- [x] Support multiple Research Topics in one Project, each with its own `deepsci-org` Topic Agent Team Profile and Topic Workspace.
- [x] Validate role activation, scalable `experimenter` and `analyzer` fanout policy, reviewer read-access policy, manual-mode default, and automatic-mode opt-in requirements.
- [x] Add fixture Projects for UC-01, UC-02, UC-03, and UC-05 that specialize the same `deepsci-org` Domain Agent Team Template differently without launching agents.

Exit criteria:

- A user can create and validate two different Topic Agent Team Profiles from `deepsci-org` in one Project.
- The profiles share template identity but do not share topic-specific refs, Agent Workspaces, policy choices, or launch facts.
- UC-01 through UC-03 and UC-05 have static profile fixtures that fail validation when topic-specific placeholders, policy refs, or Agent Workspace refs leak across topics.

## Milestone 4: Workspace Runtime for Multi-Team Instantiation

Goal: add enough Workspace Runtime to create, reopen, inspect, and validate multiple Agent Team Instance records across Topic Workspaces.

Major steps:

- [x] Implement Workspace Runtime creation with schema versioning, migration checks, and default directories for `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`.
- [x] Add durable records for Research Topics, Research Inquiries, Research Tasks, Runs, Workflow Stage Cursors, Topic Agent Team Profiles, Agent Team Instances, Agent Instances, Agent Workspaces, and handoff state.
- [x] Record resolved paths and path sources before Agent Workspaces, Run logs, Artifacts, View Manifests, or Houmao launch material depend on them.
- [x] Treat the `deepsci-org` loop-local state contract as adapter bookkeeping input, not as a replacement for canonical Workspace Runtime state.
- [x] Add validation for broken refs, missing Agent Workspaces, invalid lifecycle transitions, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, and schema-version mismatches.
- [x] Add integration tests that create two Research Topics, specialize `deepsci-org` for both, and instantiate separate Agent Team Instance records under separate Topic Workspaces.

Exit criteria:

- A Project can persist multiple topic-scoped `deepsci-org` Agent Team Instance records and recover them after process restart.
- Topic Workspace validation proves that one topic's Agent Team Instance, Agent Workspaces, Runs, and Artifacts do not leak into another topic.

## Milestone 5: Houmao Execution Adapter and First Real Team Launch

Goal: use the local Houmao build to launch and manage a `deepsci-org` Agent Team Instance from an Isomer Topic Agent Team Profile.

Major steps:

- [x] Implement a Houmao Execution Adapter that maps Isomer Domain Agent Team Template, Topic Agent Team Profile, Agent Team Instance, Agent Profile, Agent Instance, Agent Workspace, Run, and Artifact refs onto Houmao launch, mailbox, gateway, notifier, and inspection surfaces.
- [x] Use `extern/orphan/houmao` as the local Houmao source and build target while keeping Houmao source changes in the Houmao checkout.
- [x] Materialize Houmao launch material from `teams/deepsci-org/execplan/agents/`, generated skills, notifier prompts, topology, and communication templates.
- [x] Launch a manual-mode `deepsci-org` Agent Team Instance for one Research Topic and record Houmao refs without exposing Houmao terms as Isomer core schema fields.
- [x] Dispatch one handoff from `deepsci-org-master` to a specialist, receive the result through Houmao mail or gateway surfaces, and normalize it into Workspace Runtime.
- [x] Fix Houmao defects discovered during launch in the Houmao repo when any are found, validate them with Houmao's own commands, and document the local build expectation in Isomer adapter tests. This pass found no required Houmao source changes; live validation remains gated by `ISOMER_MANUAL_LIVE_HOUMAO=1`.

Exit criteria:

- [x] Isomer can start, inspect, and stop one Houmao-backed `deepsci-org` Agent Team Instance from a Topic Agent Team Profile.
- [x] A manual handoff round produces a recorded Run, handoff state, Agent Instance refs, Adapter refs, and Provenance Records in the Topic Workspace.

## Milestone 6: UC-01 Headless Vertical Slice

Goal: enable Use Case 1, Explore a New Research Direction, as the first testable end-to-end `deepsci-org` workflow without requiring custom GUI components.

Major steps:

- [ ] Add a UC-01 fixture Project with one Research Topic, one Topic Workspace, one `deepsci-org` Topic Agent Team Profile, and one follow-up-inquiry Gate policy.
- [ ] Launch or simulate a manual-mode `deepsci-org` Agent Team Instance that routes bounded scouting, analysis, and review work through the Houmao Execution Adapter.
- [ ] Record seed-source summaries, literature notes, claim candidates, Evidence Items, review notes, and inquiry options as Artifacts or provisional research records.
- [ ] Present a follow-up Research Inquiry Gate through CLI or Operator Agent text output and record the selected inquiry as a Decision Record.
- [ ] Emit minimal View Manifest records for literature matrix, claim graph, and inquiry comparison even if the first renderer is CLI-only.
- [ ] Add an integration or manual test script that runs the UC-01 path from Project initialization through the follow-up inquiry Decision Record.

Exit criteria:

- UC-01 can be run as a repeatable headless acceptance test against a local Houmao-backed or adapter-simulated `deepsci-org` Agent Team Instance.
- The test leaves durable Workspace Runtime records for Research Topic, Research Inquiry, Research Task, Run, Agent Team Instance, Artifacts, Evidence Items, Gate, Decision Record, and Provenance Records.

## Milestone 7: Parallel Topics and Repeated Team Instantiation

Goal: prove that Isomer can instantiate multiple `deepsci-org` Agent Team Instances for different Research Topics in the same Project.

Major steps:

- [ ] Add commands or APIs for preparing, launching, listing, inspecting, parking, resuming, and stopping Agent Team Instances by Research Topic and Topic Workspace.
- [ ] Launch two or more `deepsci-org` Agent Team Instances with different Topic Agent Team Profiles, separate Topic Workspaces, separate Agent Workspaces, and separate Houmao runtime refs.
- [ ] Support topic-level Parallel Execution Scope where different Agent Team Instances explore different Research Topics or different approved strategy profiles.
- [ ] Support task-level Parallel Execution Scope for scalable `deepsci-org-experimenter` and `deepsci-org-analyzer` roles inside one selected Agent Team Instance.
- [ ] Add collision checks for mailbox ids, Agent Workspace paths, Run ids, Artifact refs, Gate refs, and provider or credential refs.
- [ ] Add recovery tests for one completed team, one parked team, and one failed or stale team without corrupting other topics.
- [ ] Run two UC-01-style research-direction fixtures side by side to prove topic-level isolation before adding heavier use cases.

Exit criteria:

- One Project can run multiple independent `deepsci-org` Agent Team Instances against different Research Topics.
- Stopping, repairing, or replaying one Agent Team Instance does not disturb another topic's Workspace Runtime state or Houmao-managed agents.

## Milestone 8: Operator Control Loop, Research Records, and Built-In Views

Goal: make launched `deepsci-org` teams produce durable, inspectable research state through the Operator Agent path.

Major steps:

- [ ] Implement Run creation with `control_mode` values `manual` and `automatic`, plus manual prompt-scope metadata for `single_stage` and `multi_step`.
- [ ] Add Artifact Core Records and recording APIs for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates.
- [ ] Resolve Completion Watcher Contracts from Coordination Policy and copy the resolved contract onto each handoff.
- [x] Implement Signal Observation records for Houmao mail, gateway events, file observations, and bounded agent inspection.
- [x] Implement handoff completion normalization so downstream Run state changes only after the Operator Agent accepts a result and records produced Artifact refs and Provenance Records.
- [ ] Extend Signal Observation records to adapter events and broader Operator Control Loop views.
- [ ] Extend completion normalization across automatic/manual Control Mode, Gates, and built-in views.
- [ ] Add Gate handling for baseline waiver, credential use, cost, private data, destructive mutation, publication-facing output, claim strengthening, finalization, and archival actions.
- [ ] Define View Manifests and GUI Backend reads for Agent Team Instance status, Run timelines, handoff queues, Artifact lists, Research Claim graphs, decision queues, and pending Gates.
- [ ] Promote the UC-01 headless test to a built-in-view acceptance test with literature matrix, claim graph, inquiry comparison, Run timeline, and pending Gate inspection.

Exit criteria:

- A `deepsci-org` Agent Team Instance can complete a bounded Research Task, return through the Operator Agent path, and leave durable Artifacts, decisions, evidence, and provenance.
- GUI or CLI inspection can show what each topic-level team did, what is blocked, what is trustworthy, and what can safely happen next.
- UC-01 is enabled as a full built-in-view regression test.

## Milestone 9: UC-02 and UC-03 Research Workflow Verification

Goal: enable the baseline optimization and paper revision use cases as repeatable `deepsci-org` workflow tests.

Major steps:

- [ ] Implement the UC-02 baseline reproduction path with Measurable Objective, metric tolerance, baseline acceptance or waiver Gate, optimization Research Task, result tables, Evidence Items, and Research Claims.
- [ ] Route UC-02 through `deepsci-org-framer`, `deepsci-org-experimenter`, `deepsci-org-analyzer`, and `deepsci-org-reviewer` roles with separate Agent Workspaces and durable Run records.
- [ ] Implement the UC-03 paper revision path with manuscript and review Artifacts, feedback mapping, claim-risk view data, targeted analysis Research Tasks, writer output, reviewer audit, and final approval Gate.
- [ ] Validate that targeted analyses created during UC-03 stay inside the same Topic Workspace and preserve links to the originating review issues and Research Claims.
- [ ] Add View Manifests for UC-02 Run timeline, result table, baseline Gate, and experiment decision views.
- [ ] Add View Manifests for UC-03 response matrix, claim-risk view, Run timeline, and final approval view.

Exit criteria:

- UC-02 can run from baseline setup through a continue, follow-up inquiry, or stop Decision Record.
- UC-03 can run from review import through final response package Gate with Artifacts, Evidence Items, Research Claims, and Provenance Records intact.

## Milestone 10: UC-04 and UC-05 Interactive Operation Verification

Goal: enable project-specific GUI component generation and mixed manual or automatic control as the highest-risk interactive acceptance tests.

Major steps:

- [ ] Implement the GUI Backend, GUI Component Registry, Project GUI Component registration, Declarative GUI Component Spec validation, GUI Layout Spec records, GUI Component Instances, and AG-UI Event Envelope persistence needed by UC-04.
- [ ] Add executable component Gates for UC-04, including per-component approval, project-scoped approve-all policy, revocation, and audit records.
- [ ] Run UC-04 against experiment Artifacts produced by UC-02 or UC-05 so the task-specific component has real metrics, clusters, examples, and source Artifact refs.
- [ ] Implement UC-05 automatic baseline validation, single-stage manual Service Request repair, automatic candidate experiment Runs, multi-step manual error analysis, and next-action Gate.
- [ ] Record Completion Watcher Contracts, Signal Observations, manual prompt-scope metadata, Service Dispatch Forms, Service Requests, and manual handoff completion for UC-05.
- [ ] Add regression tests that switch between automatic and manual Runs without losing Agent Team Instance state or bypassing Gates.

Exit criteria:

- UC-04 can load a project-specific visualization through the GUI path while preserving Gate and provenance rules.
- UC-05 can mix automatic and manual `deepsci-org` work in one Topic Workspace and close out with a durable next-action Decision Record.

## Cross-Cutting Work

- [ ] Keep the canonical domain language in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` aligned with schemas, CLI labels, GUI labels, and code identifiers.
- [ ] Keep Houmao terms inside the Houmao Execution Adapter unless the domain language explicitly promotes them.
- [ ] Promote OpenSpec contracts into tests before implementing each major API.
- [ ] Treat `.imsight-arts/project-explore/use-cases/` as acceptance-test source material and update the relevant roadmap milestone whenever a use case becomes runnable.
- [ ] Treat UC-06 as the capstone roadmap verification fixture once Milestone 10 surfaces are available, and require its roadmap verdict to link concrete pass/fail evidence for Milestones 1 through 10.
- [ ] Preserve research-paradigm skillset validation as a release gate.
- [ ] Prefer small, inspectable records over opaque automation, especially around Gates, Evidence Items, Research Claims, Agent Team Instance lifecycle state, and Provenance Records.
- [ ] Keep user-owned Project files first-class: Isomer should manage Topic Workspaces and records without forcing all research work into a hidden platform directory.
