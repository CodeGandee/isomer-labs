# Concept Mapping Ledger

## Status

draft

## Purpose

This ledger works through DeepScientist source concepts one by one and maps them to Isomer Labs terms for the research-paradigm skill migration.

The ledger is not allowed to create new Isomer concepts. Each row must use existing Isomer language, mark an unsettled concrete surface, classify a source detail for omission, or flag a candidate platform gap for later review.

## Classification

| Classification | Meaning |
| --- | --- |
| `accepted` | Existing Isomer concepts are enough for the migration text. |
| `tbd-surface` | Existing Isomer concepts are enough, but a concrete path, schema, API, provider, command, or policy is not settled. |
| `source-detail` | DeepScientist implementation detail. Do not carry into skill instructions except as provenance. |
| `review-needed` | Potential platform gap. Do not introduce a concept in the migrated skills before Isomer review. |
| `defer` | Outside the first research-paradigm extraction pass. |

## Research Lifecycle and Control

| DeepScientist source concept | Isomer framing | Classification | Open mapping decision |
| --- | --- | --- | --- |
| `quest` as lifecycle, pause, resume, archive, completion, and overall steering | Research Thread | accepted | None for skill text. Exact lifecycle enum remains `yet-to-be-determined:schema`. |
| `goal` and objective fields | Research Goal, with Measurable Objective or Exploratory Goal when needed | accepted | Launch schema remains `yet-to-be-determined:schema`. |
| `startup_contract` | Launch context that supplies Research Goal, constraints, expected Artifacts, Topic Agent Team Profile hints, Coordination Policy hints, and initial Run settings | tbd-surface | Need schema review. Do not create a new "startup contract" Isomer concept in skills. |
| `workspace_mode: autonomous` | Source runtime collaboration mode. In Isomer skill text, retain only that delegated Agent Team Instances may keep advancing under approved Coordination Policy while the Operator Agent remains the human-facing control boundary. | source-detail | Do not port as an Isomer mode. Concrete Agent Team Instance lifecycle and scheduler schemas are `yet-to-be-determined:schema`. |
| `decision_policy` | Coordination Policy and Gate policy | accepted | Exact policy fields are `yet-to-be-determined:schema`. |
| `research_intensity` | Topic Agent Team Profile constraint or Coordination Policy parameter | review-needed | Decide whether this is useful Isomer profile metadata or should stay a prompt-level instruction. |
| `need_research_paper` | Expected Artifact or Research Task output constraint | accepted | Exact field location is `yet-to-be-determined:schema`. |
| `active_anchor` | Active Workflow Stage cursor stored by Workspace Runtime | tbd-surface | Stage cursor schema is `yet-to-be-determined:schema`. |
| `baseline_gate` | Gate for accepting, waiving, or blocking comparator readiness | accepted | Gate record schema is `yet-to-be-determined:schema`. |
| `continuation_policy` | Source runtime scheduling detail. Decompose retained behavior into Agent Team Instance advancement under Coordination Policy, paused waiting for Operator Agent instruction, Workflow Stage recommendation, Gate, Decision Record, Completion Watcher Contract, or Signal Observation. | source-detail | Do not introduce an Isomer `continuation_policy`. Concrete pause/advancement state schema is `yet-to-be-determined:schema`. |
| `auto_continue` turn | Source daemon scheduling detail. In Isomer skill text, recommend next action instead of scheduling turns. | source-detail | Scheduler behavior is platform runtime design, not a research-paradigm skill requirement. |
| `turn intent` and `turn mode` | Run metadata, Workflow Stage context, Operator Agent input handling, or source scheduling detail depending on scope | tbd-surface | Run metadata and input-routing schemas are `yet-to-be-determined:schema`; do not port DeepScientist turn-mode enums. |
| `requested skill` | Capability Binding selecting a skill for an Agent Role or Workflow Stage | accepted | Binding/projection mechanics are `yet-to-be-determined:api`. |
| `status: active/stopped/paused/completed/errored` | Research Thread lifecycle state, Run status, and Decision Records depending on scope | tbd-surface | State enums are `yet-to-be-determined:schema`; do not reuse DeepScientist status names blindly. |
| `parked` and `wait_for_user_or_resume` | Source runtime waiting detail. In Isomer skill text, describe an Agent Team Instance paused and waiting for Operator Agent instruction, a Gate awaiting human resolution, or a handoff state depending on reason. | source-detail | Do not port `wait_for_user_or_resume`. Concrete pause and waiting-state enums are `yet-to-be-determined:schema`. |
| `completion approval` | Gate resolved by the human user through the Operator Agent, then Decision Record | accepted | Completion policy belongs to Gate and Coordination Policy, not to a DeepScientist completion API. |

## Workspace, Runtime, and Files

| DeepScientist source concept | Isomer framing | Classification | Open mapping decision |
| --- | --- | --- | --- |
| `quest_root` as a filesystem area | Isomer Workspace when the storage scope is one Research Task | accepted | Concrete path is `yet-to-be-determined:path`. |
| `quest_root` as state authority | Workspace Runtime | accepted | Runtime storage schema is `yet-to-be-determined:schema`. |
| `quest.yaml` | Workspace Runtime records plus Research Thread, Research Task, Run, Gate, and Decision Record refs | tbd-surface | Do not create an Isomer `quest.yaml` equivalent. |
| `.ds/runtime_state.json` | Workspace Runtime state | tbd-surface | SQLite/file projection is `yet-to-be-determined:schema`. |
| `.ds/research_state.json` | Workspace Runtime state, Research Claims, Evidence Items, Findings, and Decision Records | tbd-surface | Split between DB records and Artifacts is unsettled. |
| `.ds/interaction_state.json` | Operator Agent handoff, Gate, and Signal Observation state | tbd-surface | Interaction schema is `yet-to-be-determined:schema`. |
| `.ds/cache/artifact_projection.v2.json` | Derived projection from Workspace Runtime, Artifacts, Evidence Items, and Provenance Records | source-detail | Do not port the cache format into skills. |
| `.ds/events.jsonl` | Provenance Records and Run logs | tbd-surface | Event retention format is `yet-to-be-determined:schema`. |
| `.ds/runs/<run_id>/prompt.md` | Run prompt Artifact or Agent Runtime record | tbd-surface | Prompt retention policy is `yet-to-be-determined:policy`. |
| `.ds/runs/<run_id>/command.json` | Provenance Record and Run execution metadata | tbd-surface | Command metadata schema is `yet-to-be-determined:schema`. |
| `.ds/runs/<run_id>/stdout.jsonl`, `stderr.txt`, `result.json` | Run logs, Artifacts, and Provenance Records | tbd-surface | Log and result paths are `yet-to-be-determined:path`. |
| runner history directories | Agent Runtime and Provenance Records | tbd-surface | Adapter-specific retention is `yet-to-be-determined:policy`. |
| `brief.md`, `plan.md`, `status.md`, `SUMMARY.md` | Artifacts, View Manifests, or Decision Records depending on content | tbd-surface | Do not reserve these filenames as Isomer defaults yet. |
| `active-user-requirements.md` | Research Goal constraints, Operator Agent context Artifact, or Finding | tbd-surface | Need schema/path review. |
| `artifacts/baselines/`, `artifacts/ideas/`, `artifacts/runs/`, `artifacts/decisions/`, `artifacts/reports/`, `artifacts/progress/`, `artifacts/milestones/` | Artifact categories with Evidence Item, Decision Record, Gate, and Provenance refs | tbd-surface | Do not guess artifact directory layout. |
| `paper/` | Report or manuscript Artifacts | tbd-surface | Publication layout is `yet-to-be-determined:path`. |
| `experiments/main/` and `experiments/analysis/` | Run Artifacts, Evidence Items, and analysis Artifacts | tbd-surface | Experiment output layout is `yet-to-be-determined:path`. |
| `memory/` | Findings, Evidence Items, prior durable context, or Artifact index | tbd-surface | Memory/query API is `yet-to-be-determined:api`. |
| uploaded attachments and userfiles | Artifacts, with Evidence Items only when used as evidence | accepted | Attachment storage path is `yet-to-be-determined:path`. |
| Git repository initialization | Source implementation detail unless Isomer explicitly uses Git for a task | source-detail | Git support remains an Execution Adapter capability, not a default research concept. |
| Git graph export | Provenance or View Manifest only if explicitly needed | source-detail | Do not port by default. |

## Runtime APIs and Capabilities

| DeepScientist source concept | Isomer framing | Classification | Open mapping decision |
| --- | --- | --- | --- |
| `artifact.confirm_baseline(...)` | Decision Record resolving baseline readiness, with Artifact and Evidence Item refs | accepted | Operation API is `yet-to-be-determined:api`. |
| `artifact.waive_baseline(...)` | Decision Record resolving a Gate or justified exception | accepted | Operation API is `yet-to-be-determined:api`. |
| `artifact.overwrite_baseline(...)` | Decision Record replacing a baseline acceptance and preserving prior Provenance Records | tbd-surface | Refresh/overwrite policy is `yet-to-be-determined:policy`. |
| `artifact.submit_idea(...)` | Hypothesis or candidate-direction Artifact; Decision Record when selected; Research Branch when forked | accepted | Idea schema is `yet-to-be-determined:schema`. |
| `artifact.record_main_experiment(...)` | Run record, Artifact, Evidence Item, Research Claim update, and Provenance Record | accepted | Experiment record schema is `yet-to-be-determined:schema`. |
| `artifact.create_analysis_campaign(...)` | Analysis plan Artifact plus Workflow Stages, Research Tasks, or Runs when execution is needed | accepted | Campaign schema is `yet-to-be-determined:schema`. |
| `artifact.record_analysis_slice(...)` | Artifact and Evidence Item linked to a Research Claim, Run, paper claim, or reviewer concern | accepted | Slice schema is `yet-to-be-determined:schema`. |
| `artifact.submit_paper_outline(...)` | Paper-outline Artifact with scoped claims and evidence boundaries | accepted | Outline validation API is `yet-to-be-determined:api`. |
| `artifact.submit_paper_bundle(...)` | Report or manuscript Artifact bundle with Provenance and Evidence refs | accepted | Bundle schema is `yet-to-be-determined:schema`. |
| `artifact.interact(kind="decision_request", ...)` | Gate through the Operator Agent; Decision Record after resolution | accepted | Gate request API is `yet-to-be-determined:api`. |
| `artifact.complete_quest(...)` | Research Thread lifecycle transition after Gate resolution and Decision Record | accepted | Completion API is `yet-to-be-determined:api`; do not use the word quest in skill text. |
| `artifact.record(...)` for miscellaneous reports | Artifact plus Provenance Record; Evidence Item only if it supports or contradicts a Research Claim | accepted | Generic record API is `yet-to-be-determined:api`. |
| `artifact.get_optimization_frontier(...)` | Query over candidate Artifacts, Research Branches, Findings, and Evidence Items | review-needed | Decide whether "optimization frontier" is only an Artifact/View Manifest or a first-class Isomer model. |
| `artifact.git(...)` | Git capability exposed through an Execution Adapter and Capability Binding | tbd-surface | Git command API is `yet-to-be-determined:api`. |
| `artifact.science(...)` and Science Evidence Graph | Research Claims, Evidence Items, Findings, Artifacts, and Provenance Records | review-needed | Do not introduce "Science Evidence Graph" as a concept without review. |
| `artifact.validate_academic_outline(...)` | Validation rule for a paper-outline Artifact | tbd-surface | Validation API is `yet-to-be-determined:api`. |
| `artifact.compile_outline_to_writing_plan(...)` | Derived writing-plan Artifact or Workflow Stage plan | tbd-surface | Derived-artifact API is `yet-to-be-determined:api`. |
| `memory.search`, recent memory, and durable memory writes | Findings, Evidence Items, Artifacts, or prior durable context queries | tbd-surface | Query/write API is `yet-to-be-determined:api`. |
| `bash_exec(...)` | Execution capability from an Execution Adapter via Capability Binding | tbd-surface | Command API, permissions, logging, and long-running job behavior are `yet-to-be-determined`. |
| DeepXiv and `artifact.arxiv(...)` | Literature search and reading capability | tbd-surface | Provider and API are `yet-to-be-determined:provider`. |
| SSH, SLURM, GPU, solver, simulation, or HPC shell execution | Execution Adapter capability; Service Request only for environment or dependency support | tbd-surface | Provider support and operation policy are `yet-to-be-determined`. |

## Research Objects and Durable Outputs

| DeepScientist source concept | Isomer framing | Classification | Open mapping decision |
| --- | --- | --- | --- |
| baseline as comparator | Domain noun inside Artifacts, Evidence Items, and Decision Records | accepted | Do not introduce a first-class Baseline concept yet. |
| metric contract | Artifact that defines task, dataset, split, metrics, direction, evaluator, source identity, and caveats | accepted | Contract schema is `yet-to-be-determined:schema`. |
| accepted baseline | Decision Record that accepts comparator evidence for later comparison | accepted | Gate/Decision fields are `yet-to-be-determined:schema`. |
| waived baseline | Decision Record that records why comparator evidence is bypassed | accepted | Waiver policy is `yet-to-be-determined:policy`. |
| blocker | Gate when user decision blocks progress; Finding, Run status, or Decision Record otherwise | accepted | Blocker taxonomy is `yet-to-be-determined:schema`. |
| candidate idea | Hypothesis or candidate-direction Artifact | accepted | Candidate schema is `yet-to-be-determined:schema`. |
| selected idea | Decision Record selecting a candidate; Research Branch when work forks | accepted | Selection schema is `yet-to-be-determined:schema`. |
| optimization candidate brief | Artifact used by optimize skill | accepted | Do not make it a concept unless later review accepts it. |
| durable optimization line | Research Branch if it forks a line of work; otherwise Artifact plus Decision Record | accepted | Branching threshold policy is `yet-to-be-determined:policy`. |
| implementation-level candidate attempt | Run or Artifact inside a Research Branch or Research Task | accepted | Attempt schema is `yet-to-be-determined:schema`. |
| run contract | Artifact plus Run metadata that fixes question, baseline, stop rules, output schema, and comparability rules | accepted | Contract schema is `yet-to-be-determined:schema`. |
| main experiment result | Run record, Evidence Item, Research Claim update, Artifact, and Provenance Record | accepted | Result schema is `yet-to-be-determined:schema`. |
| evaluation summary, claim update, baseline relation, failure mode, next action | Fields in result Artifact, Evidence Item, Research Claim, Decision Record, or Finding | tbd-surface | Field schema is `yet-to-be-determined:schema`. |
| analysis campaign | Workflow Stage behavior plus analysis-plan Artifact; may create Research Tasks or Runs | accepted | Do not add a first-class campaign concept yet. |
| analysis slice | Evidence Item and Artifact linked to a claim, result, paper row, or reviewer concern | accepted | Slice schema is `yet-to-be-determined:schema`. |
| paper outline | Artifact | accepted | Outline schema and validation are `yet-to-be-determined`. |
| writing plan | Artifact or Workflow Stage plan | accepted | Schema is `yet-to-be-determined:schema`. |
| paper bundle or report package | Artifact bundle | accepted | Bundle layout is `yet-to-be-determined:path`. |
| review matrix | Artifact that records findings, evidence gaps, severity, and next routing | accepted | Review schema is `yet-to-be-determined:schema`. |
| rebuttal matrix | Artifact that maps reviewer concerns to evidence, experiments, manuscript deltas, and response text | accepted | Rebuttal schema is `yet-to-be-determined:schema`. |
| milestone chart, progress graph, or git graph | Artifact or View Manifest; AG-UI Render Payload only for live GUI updates | accepted | Visualization payload and storage are `yet-to-be-determined`. |

## Agent, Skill, and Team Mapping

| DeepScientist source concept | Isomer framing | Classification | Open mapping decision |
| --- | --- | --- | --- |
| stage skill | Workflow Stage capability attached through Capability Binding | accepted | Exact binding file/schema is `yet-to-be-determined:schema`. |
| companion skill | Capability available to one or more Agent Roles or Workflow Stages | accepted | Do not make companion status a core Isomer concept. |
| custom skill | Optional Capability Binding when included by a profile | accepted | Discovery/install mechanism is `yet-to-be-determined:api`. |
| fixed DeepScientist skill registry | Domain Agent Team Template defaults plus Capability Bindings | accepted | Template schema is outside this skill extraction. |
| quest-local skill copy/projection | Execution Adapter projection of Capability Bindings into backend-specific locations | tbd-surface | Projection mechanism and paths are `yet-to-be-determined`. |
| `.codex/skills`, `.kimi/skills`, `.opencode/skills`, `.claude/agents` | Backend-specific adapter targets | source-detail | Do not put these paths in migrated skill requirements except as source notes. |
| prompt builder injecting skill paths | Execution Adapter prompt assembly and Provenance Record behavior | tbd-surface | Prompt injection mechanism is `yet-to-be-determined:api`. |
| runner adapter | Execution Adapter | accepted | Adapter contracts are outside this skill extraction. |
| runner subprocess | Agent Instance execution through Execution Adapter, or tool execution when no agent is launched | tbd-surface | Runtime model is `yet-to-be-determined:policy`. |
| generic research agent names | Agent Role kinds used in Domain Agent Team Template or Topic Agent Team Profile | accepted | Team docs can use research-lead, research-scout, research-designer, research-executor, research-writer, and research-reviewer. |
| one DeepScientist skill per specialist | Rejected topology assumption | source-detail | Do not encode one-skill-one-agent in skills. |
| Houmao specialist, mailbox, gateway, launch dossier, recipe | Execution Adapter details | source-detail | Keep out of research-paradigm skill requirements. |

## Route and Handoff Mapping

| DeepScientist source concept | Isomer framing | Classification | Open mapping decision |
| --- | --- | --- | --- |
| next anchor | Next recommended Workflow Stage, Decision Record, or Gate outcome | accepted | Stage transition schema is `yet-to-be-determined:schema`. |
| route decision | Decision Record, possibly resolving a Gate or selecting a Research Branch | accepted | Route is not a first-class concept. |
| autonomous redirect of normal route questions | Coordination Policy allowing Operator Agent or delegated agent to decide from evidence | review-needed | Need policy decision before migrating this as behavior. |
| user question for preference, scope, cost, or safety | Gate through Operator Agent | accepted | Gate categories are `yet-to-be-determined:schema`. |
| queued user messages | Operator Agent input queue or handoff state | tbd-surface | Input queue model is `yet-to-be-determined:api`. |
| direct runner continuation from durable state | Source scheduling detail. In Isomer skill text, emit a next recommended Workflow Stage, Gate, or Decision Record; platform runtime may later initialize a Run from Workspace Runtime state. | source-detail | Scheduling policy is `yet-to-be-determined:policy`; not required by research-paradigm skills. |
| manual handoff completion by file or channel signal | Signal Observation, then Operator Agent normalization into Workspace Runtime | accepted | Completion Watcher Contract schema is `yet-to-be-determined:schema`. |

## First Review Queue

These are the rows most likely to need user or architecture review before implementation hardens them:

1. Whether `research_intensity` should become Topic Agent Team Profile metadata, Coordination Policy metadata, or stay a prompt-level hint.
2. Whether concrete Agent Team Instance pause/advancement states should be standardized in platform schemas.
3. Whether "optimization frontier" should remain a derived Artifact/View Manifest or become a first-class Isomer model.
4. Whether DeepScientist's Science Evidence Graph should map entirely to Research Claims, Evidence Items, Findings, Artifacts, and Provenance Records.
5. Whether baseline remains only a domain noun inside Artifacts and Decision Records, or later deserves a first-class Isomer concept.
6. Whether source-level autonomous route-choice behavior should be preserved as Coordination Policy behavior.
7. Which concrete schemas and APIs will eventually replace artifact operations, memory queries, execution commands, literature search, prompt injection, and skill projection.
