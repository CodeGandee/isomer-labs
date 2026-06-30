# Required Storage Support for Research-Paradigm Skills

This report maps the storage tasks implied by `skillset/research-paradigm/*` to the current Isomer Labs storage layer, then lists the support missing from the storage layer. It treats the research-paradigm skills as consumers of platform storage contracts, not as the place to define concrete runtime APIs or layouts.

The audit combines a local review with a GPT-5.5 high subagent cross-check. The subagent inspected the full `skillset/research-paradigm` tree read-only and returned the same main conclusion: path resolution and generic lifecycle storage exist, but the typed research recording layer expected by the skills is mostly not yet exposed.

## Source Lineage

The `isomer-rsch-*` skills are modified from DeepScientist research workflow skills and translated into Isomer Labs domain language, storage concepts, and Agent Workspace boundaries. The local source checkout inspected for this report is [`../../../extern/orphan/DeepScientist`](../../../extern/orphan/DeepScientist), with source skill material under [`../../../extern/orphan/DeepScientist/src/skills`](../../../extern/orphan/DeepScientist/src/skills). The source checkout lives under `extern/orphan/`, so it is local-only context rather than a committed or runtime dependency. DeepScientist is licensed under Apache 2.0 in [`../../../extern/orphan/DeepScientist/LICENSE`](../../../extern/orphan/DeepScientist/LICENSE).

This report also depends on earlier source-system analysis under [`../../../.imsight-arts/project-explore`](../../../.imsight-arts/project-explore). That analysis records the decision to learn from DeepScientist without inheriting its quest model in [`0006-manifested-workspace-engine.md`](../../../.imsight-arts/project-explore/adrs/0006-manifested-workspace-engine.md), the decision that research skills request semantic workspace labels instead of paths in [`0018-workspace-path-resolver.md`](../../../.imsight-arts/project-explore/adrs/0018-workspace-path-resolver.md), the canonical term mapping away from DeepScientist reference language in [`dc-isomer-platform-language.md`](../../../.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md), and the open design question about adapting DeepScientist skill and Artifact structure in [`2026-06-15-manifested-workspace-engine-design.md`](../../../.imsight-arts/project-explore/designs/2026-06-15-manifested-workspace-engine-design.md).

## Sources Inspected

- Research-paradigm skill instructions: `isomer-rsch-analysis`, `isomer-rsch-baseline`, `isomer-rsch-decision`, `isomer-rsch-experiment`, `isomer-rsch-figure-polish`, `isomer-rsch-finalize`, `isomer-rsch-idea`, `isomer-rsch-intake`, `isomer-rsch-optimize`, `isomer-rsch-paper-outline`, `isomer-rsch-paper-plot`, `isomer-rsch-rebuttal`, `isomer-rsch-review`, `isomer-rsch-science`, `isomer-rsch-scout`, `isomer-rsch-shared`, and `isomer-rsch-write`.
- Local DeepScientist source skill material: [`../../../extern/orphan/DeepScientist/src/skills`](../../../extern/orphan/DeepScientist/src/skills), including the source `analysis-campaign`, `baseline`, `decision`, `experiment`, `figure-polish`, `finalize`, `idea`, `intake-audit`, `optimize`, `paper-outline`, `paper-plot`, `rebuttal`, `review`, `science`, `scout`, and `write` skills.
- Prior Isomer project exploration: [`../../../.imsight-arts/project-explore/adrs/0006-manifested-workspace-engine.md`](../../../.imsight-arts/project-explore/adrs/0006-manifested-workspace-engine.md), [`../../../.imsight-arts/project-explore/adrs/0018-workspace-path-resolver.md`](../../../.imsight-arts/project-explore/adrs/0018-workspace-path-resolver.md), [`../../../.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`](../../../.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md), and [`../../../.imsight-arts/project-explore/designs/2026-06-15-manifested-workspace-engine-design.md`](../../../.imsight-arts/project-explore/designs/2026-06-15-manifested-workspace-engine-design.md).
- Research-paradigm reference material under each skill's `references/` directory, especially run records, campaign records, baseline contracts, science evidence recording, figure export recording, review/rebuttal matrices, package inventories, claim ledgers, and shared source-term mappings.
- Storage design and docs: [`../../../docs/storage-layer.md`](../../../docs/storage-layer.md), [`../../../docs/runtime-and-files.md`](../../../docs/runtime-and-files.md), [`../../../docs/topic-workspace-definition.md`](../../../docs/topic-workspace-definition.md), [`../../../docs/system-design.md`](../../../docs/system-design.md), and [`../../../docs/isomer-cli.md`](../../../docs/isomer-cli.md).
- Runtime and semantic-surface implementation anchors: [`../../../src/isomer_labs/semantic_surfaces.py`](../../../src/isomer_labs/semantic_surfaces.py), [`../../../src/isomer_labs/runtime/models.py`](../../../src/isomer_labs/runtime/models.py), [`../../../src/isomer_labs/runtime/schema.py`](../../../src/isomer_labs/runtime/schema.py), [`../../../src/isomer_labs/runtime/store.py`](../../../src/isomer_labs/runtime/store.py), and [`../../../src/isomer_labs/runtime/validation_checks.py`](../../../src/isomer_labs/runtime/validation_checks.py).

## Executive Summary

The research-paradigm skills assume two storage capabilities. First, agents can resolve semantic workspace labels, then put and read durable bodies such as run logs, figures, manuscripts, reviews, and package inventories. Second, agents can record typed research objects such as Artifacts, Evidence Items, Findings, Research Claims, Decision Records, Gates, Provenance Records, Runs, Research Tasks, Workflow Stage Cursors, and Research Inquiry Relationships.

The current storage layer substantially supports the first capability. It provides Project and Topic Workspace surfaces, semantic labels, Workspace Path Resolution, Path Plans, runtime initialization and validation, Agent Workspace labels, handoff records, adapter payload records, and generic lifecycle rows in `state.sqlite`.

The current storage layer only partially supports the second capability. The runtime has generic lifecycle record kinds for many research objects, and validation already understands some artifact, Gate, Research Claim, Evidence Item, and Provenance Record checks. However, the platform does not yet expose accepted recording APIs or CLI commands for most typed research records. The skills therefore cannot reliably create, link, query, promote, validate, or hand off research evidence through the storage layer without ad hoc files.

The highest-priority missing support is a typed research recording layer over the existing path and runtime storage: `project records artifact`, `project records evidence`, `project records claim`, `project records decision`, `project records gate`, `project records finding`, `project records provenance`, and `project records run` style operations, plus artifact kind profiles and validation rules aligned with these skills.

## Current Storage Layer Baseline

The storage layer already supports label-first file placement. Durable topic-level bodies can be placed below labels such as `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, and `topic.records.logs`; agent-local work maps to labels such as `agent.private_artifacts`, `agent.scratch`, `agent.runtime`, `agent.logs`, and `agent.public_share`.

The storage layer already stores Path Plans and lifecycle rows in the Workspace Runtime database. `RuntimeLifecycleRecord` supports generic `record_kind` values including `research_topic`, `research_inquiry`, `research_task`, `run`, `workflow_stage_cursor`, `artifact`, `gate`, `finding`, `research_claim`, `evidence_item`, `decision_record`, `view_manifest`, and `provenance_record`.

The CLI is currently path-, runtime-, team-, handoff-, and adapter-oriented. The practical command surface covers path resolution and mutation, runtime init/prepare/inspect/validate, team instance creation, adapter launch/inspection records, and handoff dispatch/normalization.

The runtime validators already check several research-storage concerns: missing Artifact content paths, unpromoted Isomer-managed dependencies, unresolved Gates, supported Research Claims without linked Evidence Items, and stale Provenance Records.

The storage layer does not yet provide a first-class `project records` command family, typed record models beyond generic lifecycle rows, artifact kind profiles for research outputs, a general research execution recorder, a promotion workflow from Agent Workspace material to durable topic records, or query APIs that agents can use as the first truth source before scanning files.

## Proposed Storage Design

The default storage design should keep a two-layer separation. Agents work inside the Topic Main Development Repository or an Agent Workspace worktree, but accepted research state belongs to the Topic Workspace record store. The storage authority is the semantic label or typed record ref, not the agent's current working directory and not a hard-coded relative path.

Layout markers:

- `[exist.reuse]`: already present and reused by the research-paradigm skills as a work surface, staging surface, runtime index, or durable record surface.
- `[exist.unused]`: already present, but not a storage target for research-paradigm outputs; it may still support Isomer operation, boundaries, manifests, tooling, or adapter internals.
- `[new]`: recommended storage support needed by the research-paradigm skills.
- `[profile under existing]`: recommended Artifact or Run organization inside an existing storage label, not a new semantic label.
- `[optional.new]`: add only if the storage behavior proves distinct from ordinary Artifacts or custom labels.

Recommended default layout:

```text
<topic-workspace>/
  state.sqlite                         # [exist.reuse] topic.runtime.db, lifecycle record store
  runtime/                             # [exist.unused] topic.runtime, runtime-owned private support
    adapters/                          # [exist.unused] adapter-owned runtime material
    execution/                         # [new] generic research execution recorder support
  records/                             # [exist.reuse] topic.records, canonical owner-preserved record store
    artifacts/                         # [exist.reuse] topic.records.artifacts
    evidence/                          # [new] proposed topic.records.evidence
    provenance/                        # [new] proposed topic.records.provenance
    packages/                          # [new] proposed topic.records.packages
    datasets/                          # [optional.new] proposed topic.records.datasets
    tasks/                             # [exist.reuse] topic.records.tasks
    runs/                              # [exist.reuse] topic.records.runs
    views/                             # [exist.reuse] topic.records.views
    logs/                              # [exist.reuse] topic.records.logs
  repos/
    topic-main/                        # [exist.reuse] work surface, not record authority
      isomer-managed/
        tracked/                       # [exist.unused] small Git-shared coordination material, not record authority
          shared/                      # [exist.reuse] lightweight shared notes only
          artifacts/                   # [exist.reuse] small reviewable Artifact pointers or stubs only
          tasks/                       # [exist.reuse] small task coordination only
          runs/                        # [exist.reuse] small run pointers only
          views/                       # [exist.reuse] small board/view pointers only
          tools/                       # [exist.unused] topic tooling support
          boundaries/                  # [exist.unused] workspace boundary support
          manifests/                   # [exist.unused] projection/runtime manifest support
  agents/
    <agent-name>/                      # [exist.reuse] agent.workspace, launch cwd and worktree
      isomer-managed/
        tracked/                       # [exist.unused] same Git-tracked material through the worktree, not record authority
        agent-owned/
          runtime/                     # [exist.unused] agent.runtime, recovery/runtime support
          scratch/                     # [exist.reuse] agent.scratch, pre-promotion drafts
          logs/                        # [exist.reuse] agent.logs, pre-promotion diagnostics
          artifacts/                   # [exist.reuse] agent.private_artifacts, pre-promotion outputs
          public/                      # [exist.reuse] agent.public_share, peer-readable pre-promotion material
        links/
          topic/
            records -> <topic-workspace>/records
                                        # [new] generated convenience link, not storage authority
```

Do not move canonical `records/` into `repos/topic-main/`. The Topic Main Development Repository is the source and coordination surface; the Topic Workspace record store is the accepted research record surface. Putting accepted Evidence Items, large outputs, final packages, or provenance graphs inside the repository would tie durable research truth to Git branches and duplicate it across Agent Workspace worktrees.

Use `repos/topic-main/isomer-managed/tracked/*` only for small, Git-reviewable coordination material: task notes, small pointer manifests, lightweight views, and integration stubs that benefit from branch review. Do not use tracked repo support dirs as the accepted storage location for Evidence Items, large outputs, final packages, or provenance graphs. Use `records/*` for accepted durable research material: Evidence Item bodies, Provenance Records, Run outputs, final figures, manuscripts, review packages, rebuttal packages, claim ledgers, and package inventories.

Agent-local work should start under `agent.private_artifacts`, `agent.scratch`, `agent.logs`, or `agent.public_share` according to ownership and visibility. That material is not accepted topic evidence until a promotion workflow records it as an Artifact, Evidence Item, Provenance Record, Decision Record, or package entry under `records/*`.

The generated `agents/<agent-name>/isomer-managed/links/topic/records` link is an ergonomic read path only. Agents may inspect it, but they should cite semantic labels and typed record refs. Future record commands should resolve `topic.records.*` labels and return stable refs so a skill can say "use Evidence Item `evi-...`" rather than "read `../../records/evidence/...`".

Relevant existing and proposed labels:

| Label | Status | Default path | Role for `isomer-rsch-*` |
|---|---|---|---|
| `topic.runtime.db` | `[exist.reuse]` | `state.sqlite` | Stores typed lifecycle rows and future record refs; agents should not write it directly. |
| `topic.runtime` | `[exist.unused]` | `runtime` | Runtime-owned private support; use for adapter/runtime internals, not accepted research bodies. |
| `topic.records.artifacts` | `[exist.reuse]` | `records/artifacts` | General durable Artifact bodies already have a topic-level records surface. |
| `topic.records.tasks` | `[exist.reuse]` | `records/tasks` | Durable task records already have a topic-level records surface. |
| `topic.records.runs` | `[exist.reuse]` | `records/runs` | Run-centered execution material should build on this existing surface. |
| `topic.records.views` | `[exist.reuse]` | `records/views` | Durable boards, frontiers, and View Manifests should build on this existing surface. |
| `topic.records.logs` | `[exist.reuse]` | `records/logs` | Durable logs already have a topic-level records surface. |
| `topic.repos.main` | `[exist.reuse]` | `repos/topic-main` | Agent work surface and source repository; not accepted research record storage. |
| `topic.repos.main.tracked.tools` | `[exist.unused]` | `repos/topic-main/isomer-managed/tracked/tools` | Topic tooling support, not a research output destination. |
| `topic.repos.main.tracked.boundaries` | `[exist.unused]` | `repos/topic-main/isomer-managed/tracked/boundaries` | Workspace boundary support, not a research output destination. |
| `topic.repos.main.tracked.manifests` | `[exist.unused]` | `repos/topic-main/isomer-managed/tracked/manifests` | Projection and support manifests, not a research output destination. |
| `agent.workspace` | `[exist.reuse]` | `agents/<agent-name>` | Agent cwd and worktree. |
| `agent.private_artifacts` | `[exist.reuse]` | `agents/<agent-name>/isomer-managed/agent-owned/artifacts` | Agent-owned outputs before promotion. |
| `agent.scratch` | `[exist.reuse]` | `agents/<agent-name>/isomer-managed/agent-owned/scratch` | Draft and intermediate material before promotion. |
| `agent.logs` | `[exist.reuse]` | `agents/<agent-name>/isomer-managed/agent-owned/logs` | Agent-local diagnostics before promotion. |
| `agent.public_share` | `[exist.reuse]` | `agents/<agent-name>/isomer-managed/agent-owned/public` | Peer-readable pre-promotion material. |
| `agent.runtime` | `[exist.unused]` | `agents/<agent-name>/isomer-managed/agent-owned/runtime` | Agent recovery/runtime support, not accepted research state. |
| `topic.records.evidence` | `[new]` | `records/evidence` | Evidence Items need first-class query, claim-link, validation, and promotion semantics. |
| `topic.records.provenance` | `[new]` | `records/provenance` | Provenance graphs, snapshots, hashes, and import records need durable inspection outside ordinary Artifacts. |
| `topic.records.packages` | `[new]` | `records/packages` | Manuscript, review, rebuttal, figure-export, final-report, and closure bundles need package-level inventory and validation. |
| `topic.records.datasets` | `[optional.new]` | `records/datasets` | Add only when datasets need storage policy, size, retention, or provenance behavior that does not fit `custom.datasets.*` or ordinary Artifacts. |

Do not add a top-level `topic.records.execution` label yet. Execution-derived material should usually belong to a Run under `records/runs/<run-id>/`, with logs also queryable through `topic.records.logs` when needed. Adapter-private payloads and manifests should stay under `runtime/adapters/*`; curated execution evidence should be promoted into `records/runs/*`, `records/evidence/*`, or `records/artifacts/*`.

The proposed `runtime/execution` support is different from a durable `records/execution` surface. It is needed for runtime-private execution bookkeeping: pending command requests, adapter leases, cancellation state, watchdog checkpoints, streamed stdout/stderr cursors, process ids or scheduler ids, retry state, and recovery metadata. The durable research question is not "where did the process manager put its temporary files?" but "which Run produced which command, log, metric, output, validation, environment snapshot, and Provenance Record?" For that reason, `runtime/execution` may exist as an implementation support area, but agents and skills should cite `records/runs/<run-id>`, Evidence Item refs, Artifact refs, and Provenance Record refs.

Isomer Labs should also not copy DeepScientist's per-quest `.venv` pattern. The inspected DeepScientist run duplicated large local Python/CUDA environments under both `baselines/local/.../.venv` and `experiments/.../.venv`; this is source-system behavior, not an Isomer storage requirement. Isomer's default execution environment is Pixi, so Run records should capture the Pixi environment identity instead: `pixi.toml` or `pyproject.toml`, `pixi.lock` hash, Pixi environment name, invoked `pixi run ...` command, relevant environment variables, selected GPU/HPC scheduler metadata, and package/tool version summaries. The Pixi environment cache itself should remain external runtime material, not a durable Topic Workspace record body, unless a specific package/build artifact is promoted as evidence.

Artifact kinds should remain profiles inside `topic.records.artifacts` unless they need separate lifecycle behavior. A practical default organization is:

```text
records/artifacts/                    # [exist.reuse] topic.records.artifacts
  contracts/                          # [profile under existing]
  provider-outputs/                   # [profile under existing]
  literature/                         # [profile under existing]
  analysis/                           # [profile under existing]
  figures/                            # [profile under existing]
  paper/                              # [profile under existing]
  reviews/                            # [profile under existing]
  rebuttals/                          # [profile under existing]
  final/                              # [profile under existing]
  handoffs/                           # [profile under existing]
```

Run-centered execution material should be grouped by Run:

```text
records/runs/<run-id>/                # [exist.reuse] topic.records.runs
  contract/                           # [profile under existing]
  commands/                           # [profile under existing]
  configs/                            # [profile under existing]
  logs/                               # [profile under existing]
  metrics/                            # [new] metric record support
  environment/                        # [new] Pixi/env snapshot support, not copied environments
  outputs/                            # [profile under existing]
  validation/                         # [new] validation Evidence Item support
```

This design satisfies the research-paradigm skills by giving agents a stable working cwd in the repository while keeping durable research truth in one topic-level record store. The missing implementation work is the typed API that promotes from Agent Workspace material to `records/*`, creates lifecycle records in `state.sqlite`, and returns refs that later skills can query.

## Support Level Key

- Implemented command: user-facing CLI or documented operational command exists.
- Internal record only: runtime schema/model/store support exists, but no stable user-facing recording surface exists.
- Documented concept: docs or skills name the concept, but the implementation is not yet a usable storage surface.
- Missing: the storage layer does not expose a clear concept, record kind, command, or validation path.

## Storage Task Map by Skill

| Skill | Storage tasks described by the skill | Best current mapping | Missing or weak support |
|---|---|---|---|
| `isomer-rsch-shared` | Establishes truth-source order; resolves ordinary paths through Workspace Path Resolution; treats Artifacts, Evidence Items, Findings, Research Claims, Decision Records, Gates, Provenance Records, Workflow Stage Cursors, Runs, Research Tasks, and Research Inquiry Relationships as durable surfaces. | Path labels, Path Plans, Workspace Runtime, generic lifecycle records, and validation checks cover part of the contract. | Accepted recording APIs are not exposed; Research Inquiry Relationship is not a runtime record kind; query/write semantics for Findings, Claims, Evidence Items, Decisions, Gates, and Provenance are not typed. |
| `isomer-rsch-scout` | Stores task frame, evaluation contract, comparator shortlist, route justification, route-changing literature notes, next Workflow Stage Cursor, and optional Decision Record. | Task frame and comparator notes can be Artifacts under `topic.records.artifacts`; Workflow Stage Cursor and Decision Record can be generic lifecycle rows. | No command to create an evaluation-contract Artifact, comparator shortlist, Workflow Stage Cursor update, literature-note Evidence Item, or Decision Record. |
| `isomer-rsch-intake` | Reads durable state before files; inventories baselines, Runs, analysis, writing, review packages, provenance, blockers; emits state audit Artifact, current-board packet, repair notes, optional Provenance Records. | Existing runtime inspect/validate can read some state; Artifacts can be placed under records labels; Provenance Record is an internal lifecycle kind. | No durable context query API, no package/import inventory recorder, no typed repair-note or state-audit Artifact profile, no Provenance Record creation command. |
| `isomer-rsch-idea` | Stores objective contract, current-board packet, literature provider-output Artifacts, literature survey Artifacts, related-work Findings/Evidence Items, candidate frontier, rejected notes, pre-idea drafts, selected route Artifact, Decision Record, optional paper-outline seed. | Files can live under artifact/view labels; `finding`, `evidence_item`, `decision_record`, and `view_manifest` exist as generic lifecycle kinds. | No Literature Provider Binding storage, provider-output recorder, Finding query/write API, candidate frontier View Manifest API, selected-route Decision Record API, or paper-outline seed Artifact kind. |
| `isomer-rsch-baseline` | Stores metric-contract Artifact, comparator/source identity, accepted deviations, verification Evidence Items for logs/outputs/source docs/package records/local evaluations/Run records, Gate state, Decision Record, and next cursor. | Metric contract can be a file Artifact; Evidence Item, Gate, Decision Record, Run, and Workflow Stage Cursor can be generic lifecycle rows. | No baseline acceptance/waiver storage, comparator identity schema, metric-contract Artifact profile, Evidence Item link API, Gate open/resolve command, or baseline-specific validation. |
| `isomer-rsch-experiment` | Stores Run contract Artifact, commands, configs, logs, outputs, metrics, environment notes, Run log Artifact or Evidence Item, metric records, evaluation summary, Research Claim update, next-route Decision Record, Provenance Records, optional plan/checklist/run-record Artifacts. | `topic.records.runs`, `topic.records.logs`, and `topic.records.artifacts` can hold files; `run`, `research_claim`, `decision_record`, and `provenance_record` are generic lifecycle kinds; adapter command records exist for some Houmao-backed operations. | No general Run recorder, Run contract schema, metric record schema, command/config/log/output refs, Research Claim transition API, generic Execution Adapter Command Request, or execution provenance graph. |
| `isomer-rsch-analysis` | Stores per-slice status, evidence path, claim update, comparability verdict, caveat, next action, Slice Evidence Items/Artifacts, campaign interpretation, Research Claim updates, next-route Decision Record, optional campaign record/frontier/checklist/writing-map Artifact. | Slice and campaign bodies can be Artifacts; `evidence_item`, `research_claim`, `decision_record`, and `view_manifest` exist internally. | No analysis-slice Artifact kind, comparability verdict schema, campaign record profile, claim-evidence update API, or analysis-to-writing map profile. |
| `isomer-rsch-optimize` | Stores refreshed frontier Artifact or View Manifest, method brief Artifacts, candidate board, ranking, checklist, optimization memory, route Decision Records, implementation-attempt Evidence Items, Run references, and Provenance Records. | Frontier and boards can be files; `view_manifest`, `decision_record`, `evidence_item`, `run`, and `provenance_record` exist as generic lifecycle records. | No frontier View Manifest writer, candidate board schema, method-brief Artifact kind, implementation-attempt Evidence Item profile, or Research Inquiry Relationship graph for route branching and fusion. |
| `isomer-rsch-science` | Stores package/environment check Artifact, computational Run or dataset analysis Evidence Item, parameter sweep and HPC job Evidence Items, validation Evidence Item, source data Artifact, Research Claims, blockers, Gates, Decision Records, and Provenance Records. | Files can go under records labels; lifecycle kinds cover Run, Evidence Item, Research Claim, Gate, Decision Record, and Provenance Record; validation can check some claim/evidence relationships. | No package/environment check recorder, source data Artifact profile, parameter/units/version/tolerance/seeds schema, HPC job record support, validation Evidence Item schema, or general science execution adapter storage. |
| `isomer-rsch-paper-plot` | Stores source data Artifact or linked Evidence Item, figure-generation Artifact with script/notebook path, first rendered figure, inspection note, and optional handoff to figure polish. | Figure files and scripts can live under artifacts; handoff dispatch/normalize exists; Evidence Item and Artifact lifecycle kinds exist internally. | No source data Artifact kind, figure-generation Artifact kind, render-inspection note schema, plot output registration command, or handoff-to-figure-polish package profile. |
| `isomer-rsch-figure-polish` | Stores final figure exports as figure output Artifacts, source plotting Artifact/generation path, visual inspection note, self-review delta, and links to Evidence Items, Research Claims, report sections, reviewer items, Decisions, Gates, and Provenance. | Figure bodies can live under `topic.records.artifacts`; generic lifecycle records can represent Artifacts and links through metadata. | No figure output Artifact kind, export manifest, visual inspection note type, figure-to-claim/reviewer/section link API, or provenance chain recorder for exported figures. |
| `isomer-rsch-paper-outline` | Stores candidate, selected, and revised outline Artifacts, paper view, evidence view, section-level writing plan, claim-evidence boundary list, reviewer objection list, analysis-plan roles, and Decision/Gate for unresolved route or paper scope. | Outlines and views can be files; `view_manifest`, `decision_record`, and `gate` exist internally. | No outline Artifact kind, paper/evidence View Manifest writer, claim-boundary list schema, reviewer objection profile, or scope Gate command. |
| `isomer-rsch-write` | Stores updated paper, report, section, or manuscript package Artifact; aligned claim-evidence map; experiment or analysis matrix; bibliography; figure/table status; appendix bridge map; bundle status; optional rewrite plans; Decision Record for claim narrowing, route-back, blocker, review package, or submission-readiness Gate. | Manuscript files can be Artifacts; generic `decision_record` and `gate` rows can represent route decisions; `topic.records.artifacts` can contain bundle material. | No manuscript package Artifact kind, claim-evidence map API, bibliography status record, figure/table status schema, paper bundle inventory, review package handoff profile, or submission-readiness Gate workflow. |
| `isomer-rsch-review` | Stores review report Artifact, revision log Artifact, Evidence TODO Artifact, literature benchmark/comparison matrix, and Gate/Decision for route choice, claim downgrade, stop, review closure, and finalization readiness. | Review files can be Artifacts; `gate`, `decision_record`, and `evidence_item` exist internally. | No review report Artifact profile, revision-log schema, Evidence TODO profile, literature benchmark matrix profile, or review closure Gate command. |
| `isomer-rsch-rebuttal` | Stores reviewer item matrix, rebuttal action plan, evidence update, text delta, response letter or revision package, and Gate/Decision for supplementary evidence, baseline recovery, claim downgrade, and final handoff. | Rebuttal files can be Artifacts; Decision Record and Gate can be generic lifecycle rows; handoff records exist. | No reviewer item matrix schema, response package Artifact kind, evidence update link API, text delta profile, rebuttal handoff package, or claim downgrade workflow. |
| `isomer-rsch-decision` | Stores Decision Record, optional Gate or milestone, next Workflow Stage Cursor, pause/blocker, and checkpoint or resume packet when the authoritative active node changes. | `decision_record`, `gate`, and `workflow_stage_cursor` exist internally; resume packets can be Artifacts. | No Decision Record creation command, no cursor update command, no pause/blocker record workflow, no checkpoint/resume packet profile, and no actor/approval capture for Gate-linked decisions. |
| `isomer-rsch-finalize` | Stores final claim ledger or status summary, final report/handoff Artifact, final Decision Record, completion Gate when required, resume packet, closure handoff, and package inventory. | Final reports and inventories can be Artifacts; handoff records exist; `research_claim`, `decision_record`, and `gate` are internal lifecycle kinds. | No claim-ledger API, package inventory recorder, finalization Gate workflow, closure handoff package profile, or final report bundle validation. |

## Cross-Skill Storage Object Map

| Storage object or task | Current storage layer support | Gap |
|---|---|---|
| Durable Artifact bodies | Implemented through semantic paths such as `topic.records.artifacts`; generic `artifact` lifecycle rows exist internally. | No typed Artifact creation/list/show/update/promote command, artifact kind registry, required metadata, content hashing, format profile refs, or extension refs. |
| Evidence Items | Generic `evidence_item` lifecycle rows exist internally; validation knows a supported Research Claim should link to an Evidence Item. | No Evidence Item creation command, support/contradict/context relation model, validation-status field, source/run/output links, or claim-evidence link table. |
| Findings | Generic `finding` lifecycle rows exist internally. | No Finding query/write API, Research Inquiry scope rules, or source Evidence Item linkage. |
| Research Claims | Generic `research_claim` lifecycle rows exist internally; validation checks one supported-claim condition. | Skill statuses include `open`, `supported`, `refuted`, and `withdrawn`, but runtime statuses are broader and incomplete for this lifecycle; no transition API, evidence graph, or claim downgrade workflow. |
| Decision Records | Generic `decision_record` lifecycle rows exist internally. | No typed Decision Record schema for options, chosen route, rationale, evidence refs, policy refs, actor, timestamp, next cursor, or Gate link. |
| Gates | Generic `gate` lifecycle rows exist internally; validation can report unresolved Gates. | No Gate open/resolve/record command, approval actor capture, policy refs, blocking semantics, or option set recording. |
| Provenance Records | Generic `provenance_record` lifecycle rows exist internally; stale provenance validation exists. | No provenance graph model, record/link command, hash/snapshot support, or consistent links among inputs, execution, outputs, validation, and interpretation. |
| Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor | Several lifecycle kinds exist internally and runtime init/team operations create some rows. | No public lifecycle command family for creating/querying/updating these records; no Research Inquiry Relationship record kind; no durable route graph commands. |
| View Manifests | Generic `view_manifest` lifecycle rows exist internally; `topic.records.views` can hold files. | No View Manifest writer/validator for current boards, frontiers, evidence views, paper views, route boards, or package inventories. |
| Run logs, metrics, configs, outputs | `topic.records.runs` and `topic.records.logs` can hold files; adapter command records exist for some Houmao-backed operations. | No general Run contract model, metric row schema, command/config/log/output pointer schema, environment capture, or research execution recorder. |
| Execution Adapter Command Requests | Named by shared research contracts and partly present through Houmao adapter command records. | No generic execution request surface for package checks, notebook execution, local commands, HPC jobs, document builds, figure rendering, provider search, or data export. |
| Literature provider outputs | Can be stored as ordinary Artifacts. | No Literature Provider Binding storage, provider-output Artifact kind, search ledger, citation/result identity schema, or provider-output-to-Finding conversion path. |
| Baseline package and waiver records | Baseline concepts can be stored as Artifacts or Decision Records. | No Baseline-Waiver Policy storage, comparator package identity schema, accepted-deviation schema, or baseline-dependent claim validation. |
| Agent Artifact promotion | Agent labels exist; docs distinguish Agent Workspace material from durable topic records. | No promotion command that copies or registers agent-local material into topic records, creates Artifact/Evidence/Provenance records, and prevents durable records from depending on scratch. |
| Manuscript, figure, rebuttal, review, and final packages | Bodies can live under `topic.records.artifacts`; handoff records exist. | No package inventory recorder, package-level validation, bundle manifest, figure export manifest, response package profile, review package profile, or final closure package profile. |

## Required Storage Support

### P0: Research Recording API and CLI

Add a typed research recording layer over Workspace Path Resolution and Workspace Runtime. The minimum command family should support `artifact create/list/show/update/promote`, `evidence create/link`, `finding put/query`, `claim create/link/update`, `decision create`, `gate open/resolve`, `provenance create/link`, `run create/update/attach-output`, and `cursor update`.

Each command should resolve its storage target through semantic labels, write or register a durable body when needed, create or update lifecycle records in `state.sqlite`, emit stable JSON refs, and support read-only query modes for agents. The implementation can start by wrapping generic lifecycle rows, but the public contract should be typed enough that skills can stop inventing files.

### P0: Artifact Kind Profiles

Define Artifact Format Profiles and Artifact Extension refs for the repeated research outputs rather than adding ad hoc path names into the skills. The first profile set should cover objective contract, current board, task frame, evaluation contract, metric contract, provider output, literature survey, selected route, run contract, run log, experiment output, analysis slice, campaign record, frontier, method brief, source data, package check, validation record, figure generation, figure export, paper outline, paper or manuscript package, bibliography, review report, revision log, reviewer item matrix, rebuttal package, claim ledger, package inventory, resume packet, and final report.

These profiles should define required metadata, expected body location, link fields, allowed lifecycle status, and validation rules. They should not force one physical directory structure; they should bind to Workspace Path Resolution.

### P0: Run and Execution Recording

Add a general research execution recorder for command execution, notebook execution, package/environment checks, HPC jobs, document builds, figure rendering, literature provider searches, data export, and local script runs. This recorder should store Execution Adapter Command Requests, command payload refs, stdout/stderr/log Artifacts, output Artifact refs, metric records, environment records, seeds, parameters, tolerances, queue/job ids, scheduler checkpoints, and policy/Gate refs.

This support is required by `experiment`, `science`, `paper-plot`, `figure-polish`, `baseline`, and `analysis`. The existing Houmao adapter command records are useful but too narrow because the research skills need execution storage outside agent-team launch and handoff flows.

For Isomer Labs, "environment records" should mean reproducibility metadata, not a copied environment directory. The default case should capture Pixi facts such as the environment name, command invocation, lockfile hash, resolved package summary, Python/CUDA/tool versions, GPU selection, and relevant env vars. Full Pixi caches, `.pixi/`, venvs, build caches, downloaded wheels, and compiler intermediates should stay outside durable records unless explicitly promoted as an Artifact or Evidence Item. This keeps Run records small while preserving enough information to reproduce or audit the execution.

### P0: Research Lifecycle Graph

Add first-class support for Research Inquiry Relationship and public lifecycle operations for Research Inquiry, Research Task, Run, and Workflow Stage Cursor records. Skills need to route between scout, idea, baseline, experiment, analysis, optimize, write, review, rebuttal, decision, and finalize without relying on conversation state.

The graph should record parent/child, supports, competes-with, supersedes, blocks, merges, fuses, and route-back relationships. Workflow Stage Cursor updates should link to the Decision Record or Gate that made the route authoritative.

### P0: Claims, Evidence, Decisions, Gates, and Provenance Links

Implement typed link semantics among Research Claims, Evidence Items, Decision Records, Gates, Runs, Artifacts, Findings, and Provenance Records. The core link types should include supports, contradicts, contextualizes, derived-from, validates, invalidates, supersedes, blocks, resolves, selected-by, and produced-by.

Research Claim statuses should align with the skills: at least `open`, `supported`, `refuted`, and `withdrawn`, with room for `candidate`, `partial`, or `blocked` if the platform needs them. Gate statuses should distinguish open, blocked, resolved, superseded, waived, and failed states.

### P1: Promotion from Agent Workspace to Topic Records

Add a promotion workflow for agent-local material. The workflow should take an Agent Artifact, scratch file, log, or generated output; register or copy it into the resolved Topic Workspace durable surface; create Artifact, Evidence Item, or Provenance Record entries; and return stable refs for the agent to cite.

Validation should continue to warn when durable records depend on `agent.scratch`, `agent.private_artifacts`, ignored `tmp/` paths, or unpromoted Isomer-managed material.

### P1: Baseline, Literature, and Policy Records

Add storage surfaces for Baseline-Waiver Policy decisions, comparator package identity, accepted deviations, Literature Provider Binding refs, provider-output identities, Gate Policy refs, Scheduler Policy refs, Capability Binding refs, and Skill Binding projections. These do not need to expose every implementation detail, but agents need stable refs that can appear in Evidence Items, Decision Records, and Provenance Records.

This support is especially important for `baseline`, `idea`, `science`, `experiment`, `decision`, and `optimize`.

### P1: Package, Bundle, and Handoff Inventory

Add a package inventory recorder for manuscript packages, review packages, rebuttal packages, figure export sets, final reports, and closure handoffs. The recorder should capture included Artifact refs, claim coverage, evidence coverage, missing items, external dependencies, build/render status, and handoff target.

This support lets `write`, `review`, `rebuttal`, and `finalize` produce durable packages that later agents can inspect without rebuilding the context from filenames.

### P1: Query Surface for Durable Context

Expose a read-only query surface over records before file search. Agents should be able to query by Research Topic, Research Inquiry, Research Task, Run, record kind, Artifact kind, status, claim id, evidence id, Decision Record id, Gate id, provenance source, and time range.

This should become the operational version of the shared skill's truth-source order: durable records first, runtime state second, agent notes third, conversation last.

### P2: Skill-Aligned Validators

Extend validation with skill-facing checks: missing Artifact body, missing Evidence Item for a supported claim, claim evidence that points to scratch, stale current board, stale frontier, unresolved Gate, unsupported baseline-dependent claim, missing metric contract, experiment without run contract, figure export without inspection note, manuscript package without bibliography or claim map, rebuttal package without reviewer item matrix, and finalization without package inventory or closure handoff.

The validators should report semantic object refs and suggested storage commands, not only filesystem paths.

## Recommended Implementation Slices

1. Build the typed record wrapper first: Artifact, Evidence Item, Research Claim, Decision Record, Gate, Finding, and Provenance Record commands backed by existing lifecycle rows and content paths.
2. Add Artifact Format Profiles for the highest-traffic outputs: metric contract, run contract, run log, experiment output, analysis slice, figure export, paper package, review report, rebuttal package, claim ledger, package inventory, and resume packet.
3. Add Run and Execution Adapter Command Request recording for local commands, package checks, notebook/script execution, figure rendering, and HPC job refs.
4. Add Research Inquiry Relationship and Workflow Stage Cursor update operations, then make Decision Records the durable source for route changes.
5. Add promotion from Agent Workspace material to Topic Workspace records, with validation against unpromoted dependencies.
6. Add durable query commands and skill-aligned validators once typed records and promotion are usable.

## Open Design Questions

- Should typed research records remain generic lifecycle rows with typed metadata, or should high-traffic objects such as Evidence Items, Claims, Gates, Decisions, Runs, and Provenance Records receive dedicated tables?
- Should Artifact bodies be versioned by content hash at creation time, or should initial support store paths first and add hash snapshots during promotion/finalization?
- How much of the Artifact kind taxonomy should be built into platform defaults, and how much should live in Artifact Format Profile refs supplied by skillsets or Topic Workspace profiles?
- Which actor model should Gates and Decision Records use for human approval, agent approval, policy approval, and service approval?
- How should literature provider credentials and provider-output caching be represented without leaking provider-specific implementation details into the research skills?
- Should package inventories be ordinary Artifacts with a profile, a typed record kind, or both?

## Bottom Line

The storage layer already has the right foundation: semantic path resolution, Topic Workspace storage, Agent Workspace storage, runtime state, Path Plans, generic lifecycle rows, handoffs, and validation hooks. To support the research-paradigm skills, it needs a typed recording layer that turns those foundations into durable research objects agents can create, link, query, validate, and promote.

The first useful milestone is not a new directory tree. It is a stable `project records` API/CLI that writes bodies through existing semantic labels and records typed research state in the Workspace Runtime.
