# Refactor Isomer Research Skills and Storage Support

This plan tracks the work needed to make `skillset/research-paradigm/isomer-rsch-*` skills executable against the Isomer Labs storage system instead of depending on conceptual storage contracts or ad hoc files.

The supporting audit and proposed storage design now live in [`required-storage-support.md`](required-storage-support.md). Treat that document as the source analysis for storage needs, default layout decisions, and the `[exist.reuse]`, `[exist.unused]`, `[new]`, and `[optional.new]` storage-surface classification.

## Source Lineage

The `isomer-rsch-*` skills are Isomer-native adaptations of research workflow skills from the DeepScientist system. The local source checkout inspected for this plan is [`../../../extern/orphan/DeepScientist`](../../../extern/orphan/DeepScientist), with source skills under [`../../../extern/orphan/DeepScientist/src/skills`](../../../extern/orphan/DeepScientist/src/skills). That source checkout is local-only material under `extern/orphan/`; it is not a runtime dependency and should not be referenced by active skill instructions. DeepScientist is licensed under Apache 2.0 in [`../../../extern/orphan/DeepScientist/LICENSE`](../../../extern/orphan/DeepScientist/LICENSE).

This plan also builds on earlier DeepScientist-to-Isomer analysis under [`../../../.imsight-arts/project-explore`](../../../.imsight-arts/project-explore). Relevant prior notes include the manifested workspace decision in [`0006-manifested-workspace-engine.md`](../../../.imsight-arts/project-explore/adrs/0006-manifested-workspace-engine.md), the Workspace Path Resolver decision in [`0018-workspace-path-resolver.md`](../../../.imsight-arts/project-explore/adrs/0018-workspace-path-resolver.md), the canonical domain-language mapping in [`dc-isomer-platform-language.md`](../../../.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md), and the open design question about how much DeepScientist skill and Artifact structure should be adapted in [`2026-06-15-manifested-workspace-engine-design.md`](../../../.imsight-arts/project-explore/designs/2026-06-15-manifested-workspace-engine-design.md).

## Objective

Refactor the research-paradigm skills so each durable output maps to an implemented Isomer storage surface, typed Workspace Runtime record, or explicitly planned storage addition. Patch the storage system enough that agents can create, promote, link, query, and validate the records the skills require.

## Sequencing Rule

Patch the storage system before tightening skill requirements. A skill should not require a command, label, record type, status, or validation rule that does not exist unless the skill marks it as a planned platform surface and routes through a Gate or blocker.

After Topic Team Specialization and standard Topic Workspace initialization, use `isomer-rsch-workspace-mgr-v2` as the research-specific bootstrap manager. It prepares the selected Topic Workspace context, placeholder binding registry, semantic label readiness plan, Agent Workspace access posture, validation report, and blocker record before ordinary v2 research skills rely on durable placeholder outputs.

## Workstreams

### A. Storage Surface and Layout Patch

- [ ] Add built-in semantic labels for `topic.records.evidence`, `topic.records.provenance`, and `topic.records.packages` with `storage_profile = "topic_records_dir"` and default paths `records/evidence`, `records/provenance`, and `records/packages`.
- [ ] Defer `topic.records.datasets` until a concrete dataset retention, size, provenance, or tracking rule cannot be represented by `custom.datasets.*` or an Artifact profile.
- [ ] Do not add `topic.records.execution`; use `topic.records.runs`, `topic.records.logs`, runtime adapter material, and future execution records instead.
- [ ] Update standard topic materialization so the new required record directories are created by runtime initialization or an explicit materialization path.
- [ ] Update path docs and CLI path examples only after implementation lands.

### B. Typed Research Record API

- [ ] Add a `project records` CLI/API family backed by Workspace Path Resolution and Workspace Runtime lifecycle rows.
- [ ] Implement initial commands for `artifact create/list/show/update/promote`, `evidence create/link`, `claim create/link/update`, `decision create`, `gate open/resolve`, `finding put/query`, `provenance create/link`, `run create/update/attach-output`, and `cursor update`.
- [ ] Keep the first implementation thin: generic lifecycle rows plus typed metadata and content paths are acceptable if command outputs are stable and validators can inspect them.
- [ ] Add stable JSON refs for all record commands so skills can cite refs rather than relative paths.
- [ ] Add tests for command output shape, path resolution, idempotent writes, missing content paths, and invalid cross-record links.

### C. Record Links, Statuses, and Validation

- [ ] Align `ResearchClaim` statuses with the skills: at least `open`, `supported`, `refuted`, and `withdrawn`.
- [ ] Align Gate statuses with skill routing: at least open, blocked, resolved, superseded, waived, and failed.
- [ ] Add typed link metadata for supports, contradicts, contextualizes, derived-from, validates, invalidates, supersedes, blocks, resolves, selected-by, and produced-by.
- [ ] Add `Research Inquiry Relationship` as a first-class lifecycle or relationship record so branching, fusion, route-back, and supersession can be durable.
- [ ] Extend runtime validation for missing Artifact bodies, unsupported supported claims, unresolved Gates, stale Provenance Records, scratch-backed durable refs, missing metric contracts, missing run contracts, and finalization without package inventory.

### D. Promotion and Agent Workspace Flow

- [ ] Implement promotion from `agent.private_artifacts`, `agent.scratch`, `agent.logs`, and `agent.public_share` into topic-level `records/*`.
- [ ] Promotion must create or update Artifact, Evidence Item, Provenance Record, Decision Record, or package refs as appropriate.
- [ ] Add validation that durable records do not depend on unpromoted Agent Workspace scratch, ignored `tmp/`, or adapter-private payload paths.
- [ ] Add an optional generated advisory link from each Agent Workspace to topic records only after the storage authority remains Workspace Path Resolution and typed refs.

### E. Run and Execution Recording

- [ ] Add a generic research execution recorder for local commands, package checks, notebook/script execution, document builds, figure rendering, provider search, and HPC job refs.
- [ ] Store Execution Adapter Command Requests, command payload refs, logs, metrics, output refs, parameters, seeds, environment notes, validation refs, scheduler refs, and Gate refs.
- [ ] Keep adapter-private material under `runtime/adapters/*`; promote curated execution evidence to `records/runs/*`, `records/evidence/*`, or `records/artifacts/*`.
- [ ] Add tests for a minimal recorded Run with command refs, log refs, metric refs, output refs, validation refs, and Provenance Records.

### F. Skill Refactor

- [ ] Keep `isomer-rsch-workspace-mgr-v2` as the post-specialization bootstrap skill while the typed storage layer is still incomplete; once record commands exist, revise it to call those commands directly.
- [ ] Start with `isomer-rsch-shared`: replace conceptual "accepted recording APIs" language with the implemented `project records` contract and the new semantic labels.
- [ ] Refactor execution-heavy skills next: `isomer-rsch-experiment`, `isomer-rsch-science`, `isomer-rsch-baseline`, `isomer-rsch-analysis`, and `isomer-rsch-optimize`.
- [ ] Refactor publication-heavy skills after package support exists: `isomer-rsch-paper-plot`, `isomer-rsch-figure-polish`, `isomer-rsch-paper-outline`, `isomer-rsch-write`, `isomer-rsch-review`, `isomer-rsch-rebuttal`, and `isomer-rsch-finalize`.
- [ ] Refactor routing skills last: `isomer-rsch-scout`, `isomer-rsch-idea`, `isomer-rsch-intake`, and `isomer-rsch-decision`, once lifecycle graph and cursor updates are implemented.
- [ ] Remove guidance that tells agents to invent storage locations; require semantic labels, typed refs, Artifact Format Profiles, or a blocker.
- [ ] Keep skills at the domain-contract level. Do not bake implementation-only paths, adapter internals, credentials, mailbox routes, gateway routes, or team topology into skill instructions.

### G. Docs, Examples, and Validation

- [ ] Add examples for a minimal topic record flow: Artifact, Evidence Item, Research Claim, Decision Record, Gate, Provenance Record, Run, and Workflow Stage Cursor.
- [ ] Add an experiment flow example covering scout, baseline, experiment, analysis, and decision.
- [ ] Add a paper flow example covering paper-plot, figure-polish, write, review, rebuttal, and finalize.
- [ ] Update docs only after implementation lands so user-facing pages describe real commands.
- [ ] Extend `scripts/validate_research_paradigm_skillset.py` so it rejects stale conceptual storage placeholders once implemented storage contracts exist.

## Milestones

### Milestone 1: Storage Labels and Runtime Scaffolding

- [ ] New required labels materialize in default Topic Workspaces.
- [ ] Workspace Runtime can store typed metadata for core research records through existing lifecycle rows or new typed tables.
- [ ] Validation reports broken refs and scratch-backed durable records.

### Milestone 2: Core Record Commands

- [ ] Agents can create and query Artifacts, Evidence Items, Research Claims, Decision Records, Gates, Findings, and Provenance Records.
- [ ] Commands return stable refs and JSON output under the existing `isomer-cli-output.v1` wrapper.
- [ ] Unit tests cover happy paths and common invalid links.

### Milestone 3: Runs, Execution, and Promotion

- [ ] Agents can record a Run with command refs, logs, metrics, outputs, validation refs, and provenance.
- [ ] Agents can promote local Agent Workspace outputs into topic records.
- [ ] Runtime validation catches unpromoted dependencies.

### Milestone 4: Skill Refactor

- [ ] Shared research contract points at implemented labels, record commands, and validators.
- [ ] Each `isomer-rsch-*` skill maps its durable outputs to implemented storage support.
- [ ] No skill instructs agents to depend on conversation memory, hard-coded paths, or unpromoted scratch for durable research state.

### Milestone 5: End-to-End Examples

- [ ] Minimal record example passes validation.
- [ ] Experiment workflow example passes validation.
- [ ] Paper workflow example passes validation.

## Definition of Done

- [ ] `pixi run lint` passes.
- [ ] `pixi run typecheck` passes.
- [ ] `pixi run test` passes.
- [ ] `pixi run python scripts/validate_research_paradigm_skillset.py` passes.
- [ ] `pixi run python scripts/validate_skillsets.py --scope research` passes.
- [ ] The moved storage support report remains linked from this plan and has no broken relative links.

## Open Questions

- Should high-traffic records such as Evidence Items, Claims, Gates, Decisions, Runs, and Provenance Records stay as generic lifecycle rows with typed metadata, or receive dedicated tables?
- Should Artifact bodies be content-hashed at creation time or only during promotion and finalization?
- Should package inventories be Artifact profiles, typed records, or both?
- How should human approval, agent approval, policy approval, and service approval be represented on Gate and Decision Record refs?
- How much of the literature provider and baseline-waiver support should live in storage records versus provider/policy binding records?
