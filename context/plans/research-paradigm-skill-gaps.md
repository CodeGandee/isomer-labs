# Research Paradigm Skill Gaps Plan

This plan tracks what remains before `skillset/research-paradigm` can move from method guidance to executable Isomer research workflows. The workspace path layer is treated as settled by Workspace Path Resolution, durable recording surfaces are treated as settled by Research Recording Contracts, lifecycle state is treated as settled by Research Lifecycle State, CLI topic context is treated as settled by CLI Topic Context Resolution, and execution/provider extension refs are settled by Research Execution and Extension Contract; this plan now focuses on validation, golden examples, and optional asset contracts.

## Remaining Placeholder Summary

The formerly remaining registered placeholders are `api-execution-command`, `policy-scheduler`, `policy-cost-privacy-gate`, `schema-skill-binding`, `policy-baseline-waiver`, and `provider-literature-search`. `define-research-execution-extension-contract` mapped them to accepted Research Operation Extension Points, Execution Adapter Command Requests, Capability Binding and Skill Binding projections, scheduler policy refs, Gate policy refs, baseline-waiver policy refs, and literature provider bindings. Those terms have been applied across `skillset/research-paradigm`; the next major step is adding validation so stale placeholders do not return as active guidance.

## Current Completion Status

- [x] Stage 1: Core Research Recording Contracts are implemented in main specs and research-paradigm skill references.
- [x] Stage 2: Research Lifecycle State is implemented, validated, and reflected in shared and local research skill contracts.
- [x] CLI Topic Context Resolution is implemented, validated, and reflected in main specs, architecture notes, domain language, and shared/local research skill contracts.
- [x] Archive the completed `define-research-lifecycle-state` and `define-cli-topic-context-resolution` OpenSpec changes after final review.
- [x] Stage 3 through Stage 5 contracts are defined and applied by `define-research-execution-extension-contract`; manual validation checks confirmed that stale placeholders do not remain active guidance.
- [x] Archive the completed `define-research-execution-extension-contract` OpenSpec change after final review.

## Stage 1: Define Core Research Recording Contracts

- [x] Define the Artifact and Provenance recording API currently represented by `[[tbd-surface:api-artifact-record]]`.
- [x] Define the Finding query/write API currently represented by `[[tbd-surface:api-finding-query]]`.
- [x] Define the Gate open/resolve/record API currently represented by `[[tbd-surface:api-gate]]`.
- [x] Define durable schemas for Decision Records, Evidence Items, Research Claims, and Gates.
- [x] Specify validation rules for broken refs, missing files, unsupported Research Claims, unresolved Gates, and stale Provenance Records.
- [x] Update research-paradigm skill references to replace recording/schema TBDs where the accepted contracts apply.

## Stage 2: Define Research Lifecycle State

- [x] Define lifecycle state for Research Topic, Research Inquiry, Research Task, Run, and Workflow Stage Cursor.
- [x] Define how a Research Inquiry Relationship is recorded without forcing all exploration paths into a tree.
- [x] Define Research Inquiry Relationship, pause, resume, supersede, block, finalize, and archive transitions through Research Lifecycle State.
- [x] Define Agent Team Instance lifecycle state, including how it maps to Topic-level and Task-level parallel execution.
- [x] Map the former `policy-branching` surface to Research Inquiry Relationship policy through Research Lifecycle State.
- [x] Update skills that route between scout, baseline, idea, experiment, analysis, decision, write, review, rebuttal, and finalize to use the accepted lifecycle terms.

## Stage 3: Define Execution Adapter Command Surface

- [x] Define the command execution surface formerly represented by `api-execution-command` as Execution Adapter Command Request.
- [x] Specify how commands declare permissions, working directory, environment variables, inputs, outputs, logs, and expected Artifacts through the provider-neutral request envelope and semantic workspace targets.
- [x] Specify how execution records map to Runs, Run logs, Evidence Items, and Provenance Records through Research Recording Contracts.
- [x] Define long-running execution behavior for experiments, baseline recovery, package checks, HPC jobs, and manual checkpoints through Scheduler Policy refs, Completion Watcher Contracts, Run observations, and Gate Policy preflight.
- [x] Define the scheduler and continuation policy formerly represented by `policy-scheduler` as Scheduler Policy refs that do not replace Workflow Stage Cursor or Agent Team Instance lifecycle state.
- [x] Define cost, credential, privacy, data-export, external-upload, long-compute, destructive-change, and publication-facing Gate thresholds formerly represented by `policy-cost-privacy-gate` as Gate Policy preflight.

## Stage 4: Define Capability and Skill Binding Contracts

- [x] Define the Skill Binding surface formerly represented by `schema-skill-binding` as Skill Binding projection refs under Capability Binding, Agent Profile, Topic Agent Team Profile, or Run context.
- [x] Define how Capability Bindings expose tools, credentials, skills, search providers, command execution, package managers, GUI publishing, and allowed Research Operation Extension Points to Agent Roles.
- [x] Define how Domain Agent Team Templates specialize into Topic Agent Team Profiles with per-topic skill and capability bindings.
- [x] Define how an Agent Team Instance records the concrete Agent Instances, bindings, workspace refs, Run participation, and launch refs while launch dispatch uses Execution Adapter Command Requests.
- [x] Update shared and per-skill references so they can name accepted bindings instead of generic host API placeholders.

## Stage 5: Define Literature and Citation Provider Contract

- [x] Define the literature search and paper-reading provider surface formerly represented by `provider-literature-search` as Literature Provider Binding refs.
- [x] Specify citation metadata, source provenance, paper Artifact refs, repository refs, benchmark refs, and confidence labels.
- [x] Define how literature provider output starts as provider-output Artifacts for context-only use, becomes Findings when distilled, and becomes Evidence Items only when linked by evidence-use intent.
- [x] Define provider behavior for scout, review, rebuttal, write, paper-outline, and baseline route selection.
- [x] Update literature-facing references after the provider contract is accepted.

## Stage 6: Add Skillset Validation Harness

- [ ] Add a validation check for stale terms such as Research Goal, Research Thread, Research Branch, and Isomer Workspace.
- [ ] Add a validation check that ordinary workspace path TBDs are not reintroduced.
- [ ] Add a validation check that every `[[tbd-surface:*]]` id is registered.
- [ ] Add a validation check for hard-coded absolute paths and source-analysis paths.
- [ ] Add a validation check for broken local reference links from each `SKILL.md`.
- [ ] Add a validation check that `agents/openai.yaml` display names match skill names.
- [ ] Add CI or repository commands for running the skillset validation harness.

## Stage 7: Add Golden Research Workflow Examples

- [ ] Create a minimal Research Topic example with Topic Workspace, Research Inquiry, Research Task, Run, Artifact, Evidence Item, Decision Record, and Gate refs.
- [ ] Create an experiment-oriented example that flows through scout, baseline, idea, experiment, analysis, and decision.
- [ ] Create a paper-oriented example that flows through paper-outline, paper-plot, figure-polish, write, review, rebuttal, and finalize.
- [ ] Show Topic-level parallel execution across different Agent Team Instances.
- [ ] Show Task-level parallel execution distributed to multiple Agent Instances within one Agent Team Instance.
- [ ] Show that Research Inquiry is not a parallel execution scope.

## Stage 8: Import or Generate Optional Skill Assets

- [ ] Decide whether venue LaTeX templates should be imported as sanitized optional assets, project-provided templates, or external Capability Bindings.
- [ ] Sanitize any accepted venue templates by removing sample content, source-local notes, TODO macros, and unclear licensing.
- [ ] Decide whether paper-plot scripts should be imported as reusable parameterized generators under `scripts/`.
- [ ] Sanitize accepted plotting scripts so they take explicit input/output arguments, avoid local paths, declare dependencies, and write through resolved figure Artifacts.
- [ ] Decide whether the science package-card catalog should be imported as local references, generated assets, or a Capability Binding.
- [ ] Define package-card freshness, source URL, license, and Provenance Record behavior before importing catalog material.
- [ ] Consider a separate publication-extension change for Nature-specific helpers.

## Stage 9: Reconcile Skills After Contracts Land

- [x] Replace resolved TBD placeholders across `skillset/research-paradigm`.
- [x] Remove local workaround text that only exists because a platform contract was missing.
- [x] Keep unresolved placeholders only for genuinely unsettled surfaces.
- [x] Run OpenSpec validation.
- [ ] Run skillset validation once the validation harness exists.
- [x] Review the final skillset for consistency with Topic Workspace, Agent Workspace, Research Topic, Research Inquiry, and Research Task terminology.
- [x] Archive the completed OpenSpec changes in dependency order.
