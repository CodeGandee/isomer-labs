# Isomer Labs Roadmap

## Current Baseline

Isomer Labs now has a Milestone 1 `isomer-cli` implementation for Project discovery, Project Manifest validation, Effective Topic Context inspection, Workspace Path Resolution previews, built-in schema listing, and Project initialization. It also has Milestone 2 and 3 static validation for the `deepsci-org` Domain Agent Team Template, project-local template fixtures, and design-time Topic Agent Team Profiles for multiple Research Topics. Milestone 4 adds topic-scoped Workspace Runtime state with schema metadata, path plans, topic environment readiness records, pre-launch Agent Team Instance records, Agent Instance and Agent Workspace records, initial Workflow Stage Cursor records, validation, inspection, and two-topic isolation coverage. Milestone 5 adds the Houmao Execution Adapter launch, inspect, stop, reconciliation, adoption, manual handoff dispatch, Signal Observation, and Operator normalization path. The repo contains `teams/deepsci-org/`, a generated full-team Domain Agent Team Template, and `teams/deepsci-mini/`, a compact three-role Domain Agent Team Template for the first runnable research-direction slices.

The completed foundation made `deepsci-org` work inside the Isomer framework as the full research-organization template. The near-term acceptance path now uses `deepsci-mini` first, because UC-01 and UC-07 need a smaller Agent Team Instance to validate research recording, Gate handling, View Manifests, and Houmao-backed handoffs before the roadmap returns to `deepsci-org` parallelism, paper workflows, and capstone-scale coordination.

Houmao is the primary underlying implementation layer for Agent Team construction and management in this phase. Isomer keeps the generic domain language: Houmao roles, launch dossiers, mailboxes, gateway refs, specialists, and managed-agent details belong inside the Houmao Execution Adapter unless the canonical domain language explicitly promotes a term into Isomer core language.

## Use-Case Verification Plan

The use cases in `.imsight-arts/project-explore/use-cases/` are roadmap acceptance tests, not just examples. Each implementation milestone should either enable a new use-case test fixture, advance one use case from headless validation to live execution, or protect a previously enabled use case from regression.

- **UC-01 Explore a New Research Direction** becomes the first live vertical slice. It is pinned to Research Topic `flash-attention-gb10-peak-performance-optimization`, uses the `deepsci-mini` Domain Agent Team Template, and stops at a follow-up Research Inquiry Decision Record without requiring a GB10 measurement run.
- **UC-07 GB10 Feature-Driven Flash Attention 4 Optimization with deepsci-mini** becomes the next measured acceptance slice. It uses the same pinned topic and `deepsci-mini` team to record baseline measurement, candidate optimization experiments, accuracy checks, ranked GB10-specific optimization decisions, and final plan acceptance.
- **UC-02 Reproduce a Baseline and Optimize It** remains the generic measured-workflow regression after UC-07 proves the concrete GB10 optimization path.
- **UC-03 Plan and Execute a Paper Revision** verifies multi-task planning, claim-risk mapping, targeted analysis Runs, response drafting, final approval Gates, and reviewer audit records.
- **UC-04 Generate a Task-Specific GUI Component** verifies GUI Backend, View Manifest, GUI Component Registry, AG-UI Event Envelope, and gated executable component behavior.
- **UC-05 Mix Manual and Automatic Runs** verifies automatic baseline work, single-stage manual repair, automatic candidate Runs, multi-step manual handoffs, Completion Watcher Contracts, Signal Observations, and durable closeout.
- **UC-06 Capstone Roadmap Verification with Flash Attention 4 Runtime Prediction on DGX Spark GB10** is the final complete acceptance test. It stays at the end because it combines Project discovery, Pixi readiness, `deepsci-org` template validation, Topic Agent Team Profile specialization, Workspace Runtime, Houmao-backed Agent Team Instance launch, parallel topics, task-level fanout, Operator Agent handoffs, Service Requests, Gates, Artifacts, Evidence Items, Research Claims, CUDA/PTX/SASS-backed white-box execution-model records, component-time prediction views, model report packaging, GUI paths, mixed control, and a pass/fail roadmap verification verdict.

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

## Milestone 6: UC-01 Headless Exploration Slice

Goal: enable Use Case 1, Explore a New Research Direction, as the first testable end-to-end `deepsci-mini` workflow without requiring custom GUI components or GB10 measurement.

Major steps:

- [ ] Add a UC-01 fixture Project for Research Topic `flash-attention-gb10-peak-performance-optimization`, one Topic Workspace, one `deepsci-mini` Topic Agent Team Profile, initial Research Inquiry `gb10-flash-attention-4-direction-selection`, Research Task `map-gb10-flash-attention-optimization-directions`, and one follow-up-inquiry Gate policy.
- [ ] Launch or simulate a manual-mode `deepsci-mini` Agent Team Instance that routes bounded scouting and synthesis-review work through the Houmao Execution Adapter.
- [ ] Record seed-source summaries, Flash Attention implementation notes, GB10 or Blackwell feature notes, claim candidates, Evidence Items, review notes, and inquiry options as Artifacts or provisional research records.
- [ ] Present a follow-up Research Inquiry Gate through CLI or Operator Agent text output and record the selected inquiry as a Decision Record.
- [ ] Emit minimal View Manifest records for literature matrix, claim graph, and inquiry comparison even when the first renderer is CLI-only.
- [ ] Add an integration or manual test script that runs the UC-01 path from Project initialization through the follow-up inquiry Decision Record.

Exit criteria:

- UC-01 can be run as a repeatable headless acceptance test against a local Houmao-backed or adapter-simulated `deepsci-mini` Agent Team Instance.
- The test leaves durable Workspace Runtime records for Research Topic, Research Inquiry, Research Task, Run, Agent Team Instance, Artifacts, Evidence Items, Gate, Decision Record, View Manifests, and Provenance Records.
- The selected follow-up inquiry is traceable to Evidence Items and explicitly chooses UC-07-style measured optimization, more scouting, or a different Flash Attention 4 investigation.

## Milestone 7: UC-07 GB10 Optimization Slice

Goal: enable Use Case 7 as the first measured optimization acceptance test, using the same pinned Flash Attention 4 on GB10 topic and the compact `deepsci-mini` team.

Major steps:

- [ ] Add or extend the UC-07 fixture Project with Research Topic `flash-attention-gb10-peak-performance-optimization`, explicit Pixi environment binding, `deepsci-mini` Domain Agent Team Template registration, and a Topic Agent Team Profile with lead, scout, and synthesis-reviewer Agent Workspaces.
- [ ] Run the CLI baseline for validation, topic listing, workspace listing, Effective Topic Context, Workspace Path Resolution, schema listing, doctor diagnostics, template inspection, and profile validation using root-level `--print-json` for machine-readable output.
- [ ] Launch or simulate a manual-mode `deepsci-mini` Agent Team Instance through the Houmao Execution Adapter and normalize at least one manual handoff round into Workspace Runtime.
- [ ] Record a GB10 feature inventory, Flash Attention 4 baseline scope, baseline measurement Artifact, candidate optimization Artifacts, speedup evidence, utilization evidence, and correctness checks.
- [ ] Open Gates for baseline measurement budget, top-candidate selection, and final optimization plan acceptance.
- [ ] Produce a ranked optimization table that ties each accepted recommendation to a concrete GB10-specific feature, speedup or validated lightweight model, risk, accuracy impact, and implementation effort.
- [ ] Add a simulated acceptance test and a live-gated manual validation path for real GB10 or Houmao execution, with skipped status recorded when live hardware or live Houmao gates are absent.

Exit criteria:

- UC-07 can be run as a repeatable focused optimization slice that records baseline measurement, candidate optimization experiments, synthesis-review ranking, final plan Artifacts, Gates, Decision Records, View Manifests, and Provenance Records.
- Every accepted optimization recommendation is traceable to a GB10-specific feature and supported by measured speedup or a validated lightweight model.
- Numerical correctness is checked for every candidate that changes precision or kernel layout, and failing candidates are rejected or repaired.
- Manual Mode and automatic replay or analysis can coexist in the same Topic Workspace without bypassing Gate Policy or completion normalization.

## Milestone 8: Operator Control, Research Records, and Built-In Inspection

Goal: harden the Operator Agent path and built-in inspection surfaces using the records produced by UC-01 and UC-07.

Major steps:

- [ ] Implement Run creation with `control_mode` values `manual` and `automatic`, plus manual prompt-scope metadata for `single_stage` and `multi_step`.
- [ ] Complete Artifact Core Records and recording APIs for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, Gates, View Manifests, and research-record links used by UC-01 and UC-07.
- [ ] Resolve Completion Watcher Contracts from Coordination Policy and copy the resolved contract onto each handoff.
- [x] Implement Signal Observation records for Houmao mail, gateway events, file observations, and bounded agent inspection.
- [x] Implement handoff completion normalization so downstream Run state changes only after the Operator Agent accepts a result and records produced Artifact refs and Provenance Records.
- [ ] Extend Signal Observation records to adapter events and broader Operator Control Loop views.
- [ ] Extend completion normalization across automatic/manual Control Mode, Gates, built-in views, and replayed simulated handoffs.
- [ ] Add Gate handling for baseline waiver, credential use, cost, private data, destructive mutation, publication-facing output, claim strengthening, finalization, and archival actions.
- [ ] Define built-in CLI or GUI-readable View Manifests for Agent Team Instance status, Run timelines, handoff queues, Artifact lists, Research Claim graphs, decision queues, ranked optimization tables, baseline-to-optimized comparisons, and pending Gates.

Exit criteria:

- UC-01 and UC-07 are inspectable after process restart through deterministic CLI output and durable View Manifest records.
- CLI or GUI inspection can show what each topic-level team did, what is blocked, what is trustworthy, and what can safely happen next.
- Manual and automatic work can share one Topic Workspace while preserving Gate Policy, Completion Watcher Contract, Signal Observation, and Provenance Record boundaries.

## Milestone 9: UC-04 GUI and Project-Specific Component Path

Goal: enable built-in and project-specific GUI inspection after UC-07 has real optimization Artifacts to visualize.

Major steps:

- [ ] Implement the GUI Backend, GUI Component Registry, Project GUI Component registration, Declarative GUI Component Spec validation, GUI Layout Spec records, GUI Component Instances, and AG-UI Event Envelope persistence needed by UC-04.
- [ ] Add executable component Gates for UC-04, including per-component approval, project-scoped approve-all policy, revocation, and audit records.
- [ ] Run UC-04 against UC-07 Artifacts so the task-specific component has baseline measurements, candidate optimization results, ranked tables, accuracy checks, and source Artifact refs.
- [ ] Support create-on-message and targeted-update GUI Component Instance lifecycles with rejected update records for non-updatable instances.
- [ ] Route GUI actions that would accept claims, approve downstream work, or change research direction through the Operator Agent as Gates.

Exit criteria:

- UC-04 can load a project-specific visualization over UC-07 optimization Artifacts while preserving Gate and provenance rules.
- Built-in and project-specific GUI paths can render ranked optimization tables, baseline-to-optimized comparisons, Run timelines, Artifact refs, and pending Gates from durable View Manifests.

## Milestone 10: Full deepsci-org Expansion and Workflow Breadth

Goal: return to the full `deepsci-org` template for workflows that need parallel topics, task-level fanout, writing, publication surfaces, mixed manual/automatic service work, or independent full review loops.

Major steps:

- [ ] Add commands or APIs for preparing, launching, listing, inspecting, parking, resuming, and stopping multiple Agent Team Instances by Research Topic and Topic Workspace.
- [ ] Launch two or more `deepsci-org` Agent Team Instances with different Topic Agent Team Profiles, separate Topic Workspaces, separate Agent Workspaces, and separate Houmao runtime refs.
- [ ] Support topic-level Parallel Execution Scope where different Agent Team Instances explore different Research Topics or different approved strategy profiles.
- [ ] Support task-level Parallel Execution Scope for scalable `deepsci-org-experimenter` and `deepsci-org-analyzer` roles inside one selected Agent Team Instance.
- [ ] Add collision checks for mailbox ids, Agent Workspace paths, Run ids, Artifact refs, Gate refs, provider refs, credential refs, calibration splits, and model refs.
- [ ] Implement the generic UC-02 baseline reproduction path as a regression over the concrete UC-07 measured optimization path.
- [ ] Implement the UC-03 paper revision path with manuscript and review Artifacts, feedback mapping, claim-risk view data, targeted analysis Research Tasks, writer output, reviewer audit, and final approval Gate.
- [ ] Implement the UC-05 mixed manual and automatic path with automatic baseline validation, single-stage manual Service Request repair, automatic candidate Runs, multi-step manual error analysis, Completion Watcher Contracts, Signal Observations, Service Dispatch Forms, and next-action Gate.

Exit criteria:

- One Project can run multiple independent `deepsci-org` Agent Team Instances against different Research Topics.
- Stopping, repairing, replaying, or parking one Agent Team Instance does not disturb another topic's Workspace Runtime state or Houmao-managed agents.
- UC-02, UC-03, and UC-05 can run as repeatable workflow breadth tests without weakening the UC-01 and UC-07 acceptance paths.

## Final Capstone: UC-06 Roadmap Verification

Goal: run Use Case 6 as the complete final test for the roadmap after the smaller `deepsci-mini` slices, built-in views, GUI path, mixed control, and full `deepsci-org` breadth are available.

Major steps:

- [ ] Build the UC-06 fixture Project with primary Research Topic `flash-attention-gb10-runtime-prediction`, at least one companion topic, explicit Pixi environment bindings, `deepsci-org` Domain Agent Team Template registration, and topic-specific Topic Agent Team Profiles.
- [ ] Verify Project discovery, doctor diagnostics, template validation, profile validation, Workspace Runtime creation, Houmao-backed launch, handoff normalization, topic-level parallelism, and task-level fanout in one Project.
- [ ] Record CUDA source, PTX, SASS, compiler flags, target architecture, calibration splits, held-out validation inputs, profiler traces, correctness outputs, component-time model Artifacts, uncertainty records, Evidence Items, Findings, Research Claims, Gates, Decision Records, View Manifests, GUI Component records, and Provenance Records.
- [ ] Produce a white-box Flash Attention 4 runtime-prediction model that returns `predicted_runtime_ms`, uncertainty or validity scope, and a component-time explanation without measuring the exact prediction-query input.
- [ ] Emit a roadmap verification verdict with concrete pass/fail evidence for Milestones 1 through 10 and all cross-cutting release gates.

Exit criteria:

- UC-06 proves the whole system works together: `deepsci-org`, multiple topics, Houmao, manual and automatic control, service requests, Gates, Artifacts, Evidence Items, Research Claims, View Manifests, GUI, project-specific components, and a final report package.
- The capstone can fail honestly when white-box traceability, GB10 evidence, topic isolation, model validity, GUI state, or Gate policy evidence is missing.

## Cross-Cutting Work

- [ ] Keep the canonical domain language in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` aligned with schemas, CLI labels, GUI labels, and code identifiers.
- [ ] Keep Houmao terms inside the Houmao Execution Adapter unless the domain language explicitly promotes them.
- [ ] Promote OpenSpec contracts into tests before implementing each major API.
- [ ] Treat `.imsight-arts/project-explore/use-cases/` as acceptance-test source material and update the relevant roadmap milestone whenever a use case becomes runnable.
- [ ] Treat UC-06 as the capstone roadmap verification fixture once Milestone 10 surfaces are available, and require its roadmap verdict to link concrete pass/fail evidence for Milestones 1 through 10.
- [ ] For testing agents that need an external coding LLM, use `scripts/claude-kimi.sh` with the prefixed `CLAUDE_KIMI_*` settings documented in `.env.example`; real `.env` values stay local, and tests or fixtures must not copy API keys into repository files.
- [ ] Preserve research-paradigm skillset validation as a release gate.
- [ ] Prefer small, inspectable records over opaque automation, especially around Gates, Evidence Items, Research Claims, Agent Team Instance lifecycle state, and Provenance Records.
- [ ] Keep user-owned Project files first-class: Isomer should manage Topic Workspaces and records without forcing all research work into a hidden platform directory.
