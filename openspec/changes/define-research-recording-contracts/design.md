## Context

The manifested workspace engine defines Topic Workspaces, Workspace Runtime, file-backed Artifacts, Agent Workspaces, Runs, View Manifests, and Gates as core platform concepts. Workspace Path Resolution now settles where ordinary files, logs, and Artifact class directories live, but the research-paradigm skills still mark record APIs and schemas as TBD. As a result, an Agent Team Instance can know where to write an experiment output, but the platform still lacks a contract for turning that output into durable evidence, a claim update, a decision, a Gate, or a reusable Finding.

This change defines the core recording layer that other changes can build on. It should be concrete enough for skills and future engine code to name stable records and operations, while avoiding premature commitment to a final SQLite schema or complete lifecycle state machine.

## Goals / Non-Goals

**Goals:**

- Define durable record contracts for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates.
- Define host-facing APIs for recording Artifacts and Provenance Records, querying and writing Findings, and opening, resolving, and recording Gates.
- Define linkage rules among records so Research Claims, Decisions, Gates, and Findings can be audited through Evidence Items and Provenance Records.
- Define validation behavior for missing Artifact files, broken refs, unsupported Research Claims, contradictory Evidence Items, unresolved Gates, and stale Provenance Records.
- Give research-paradigm skills accepted names for formerly unsettled recording API and record-schema surfaces.

**Non-Goals:**

- Define the full SQLite table layout, indexes, migrations, or storage implementation.
- Define command execution, tool-call capture, prompt capture, literature provider behavior, scheduler policy, or Skill Binding.
- Define full Research Topic, Research Inquiry, Research Task, Run, Workflow Stage, or Agent Team Instance lifecycle transitions.
- Define GUI component rendering or View Manifest schema beyond the record refs a view can consume.
- Define external synchronization, multi-user conflict resolution, or remote service APIs.

## Decisions

### Decision 1: Use semantic records before storage tables

The first contract should define semantic record types and required fields, not final database tables. Each record should have an id, Topic Workspace scope, relevant lifecycle refs, actor refs when available, created and updated timestamps, status, content refs or short scalar fields, and Provenance Record links.

Minimum record families:

```text
Artifact
ProvenanceRecord
EvidenceItem
ResearchClaim
Finding
DecisionRecord
Gate
```

Rationale: skills and host APIs need stable record meaning before code needs a final table layout. A semantic contract can map to SQLite rows, JSON files, or a future service without changing the skill language.

Alternative considered: define table schemas immediately. Rejected for this change because lifecycle and execution contracts are still pending, and table details would force premature decisions about indexes, migrations, and denormalization.

### Decision 2: Make Evidence Items the support boundary

Research Claims, Decision Records, Gates, and Findings should cite Evidence Items when they rely on research evidence. An Evidence Item can reference an Artifact, measurement, result, source document, external reference, manual observation, or another durable record. Evidence Items and claim-evidence links carry relations such as support, contradiction, context, refutation, and withdrawal rationale. Research Claim status should stay focused on the claim lifecycle: `open`, `supported`, `refuted`, or `withdrawn`, unless a later accepted contract extends the status set. Research Claims should not cite raw files alone when the file is being used as evidence; the file should be represented through an Evidence Item.

Rationale: Artifacts are storage objects, while Evidence Items explain why a source supports, contradicts, or contextualizes a claim. Keeping contradiction and context on evidence links lets one claim carry mixed evidence without forcing the claim itself into an ambiguous status.

Alternative considered: let Research Claims point directly to Artifacts. Rejected because it makes a file both storage and epistemic support, which weakens contradiction handling and later writing/review workflows.

### Decision 3: Keep Provenance Records broad and append-oriented

A Provenance Record should describe how a record or Artifact was produced, updated, superseded, imported, repaired, or invalidated. It should link actors, source records, input refs, output refs, prompt or tool-call refs when those contracts exist, timestamps, and a concise action summary. Provenance Records should be append-oriented; corrections create new provenance rather than silently rewriting history.

Rationale: command execution, literature providers, manual edits, service-team support, and GUI actions will all need provenance later. A broad record shape avoids baking one execution backend into the core contract.

Alternative considered: one provenance subtype per producer. Rejected because the platform does not yet have stable command, literature, GUI, and service-team APIs.

### Decision 4: Separate Decisions from Gates

A Decision Record is the durable record of a meaningful choice and its rationale. A Gate is a blocking human decision point for irreversible or claim-shaping actions. A Gate may be resolved by a Decision Record, but a Decision Record does not always require a Gate, and a Gate does not create a Decision Record unless a meaningful choice was made.

Gate statuses should include at least `open`, `resolved`, `cancelled`, and `superseded`. A `resolved` Gate should create or link a Decision Record when the user made a meaningful choice. A `cancelled` or `superseded` Gate can close without a Decision Record, but it still needs a Provenance Record. Decision Records should include selected option, rejected alternatives when material, rationale, evidence refs, actor, timestamp, consequence summary, and optional follow-up refs.

Rationale: this preserves the current domain language: Gates are human-return control points, while Decision Records are broader research records. It also prevents routine routing choices from becoming unnecessary Gates.

Alternative considered: model all decisions as Gates. Rejected because it would over-gate ordinary workflow progress and make automation harder without improving auditability.

### Decision 5: Use reference fields for lifecycle objects

Records should include optional or required refs to `research_topic_id`, `research_inquiry_id`, `research_task_id`, `run_id`, `topic_workspace_id`, `agent_team_instance_id`, `agent_instance_id`, and `workflow_stage_id` where applicable. This change defines how records may refer to those objects, not the full lifecycle state machine for those objects.

Rationale: recording cannot wait for every lifecycle transition to be settled, but later lifecycle work needs records to carry stable refs.

Alternative considered: block recording contracts until lifecycle is fully specified. Rejected because Evidence Items, Findings, Decision Records, and Gates are the next dependency for execution and literature contracts.

### Decision 6: Scope Findings to Research Inquiries first

Findings should be primarily owned by a Research Inquiry when an applicable inquiry exists. A Finding can still carry refs to Research Topic, Research Task, Run, Evidence Items, Research Claims, and tags for broader retrieval. Topic-level Findings are allowed only when the platform has not yet created a more specific Research Inquiry.

Rationale: Findings are reusable insights, but they usually answer or steer a question. Primary Research Inquiry ownership keeps Findings tied to the inquiry graph while allowing topic-level and workspace-level query surfaces.

Alternative considered: scope Findings primarily to Research Topic or Topic Workspace. Rejected because Topic scope is too broad for many reusable insights, and Topic Workspace scope is storage-oriented rather than research-semantic.

### Decision 7: Validate records as a graph

The recording layer should expose validation that can inspect record links and path-backed Artifacts together. Validation should report issues without silently deleting records. Missing files, unsupported claims, unresolved Gates, stale provenance, and contradictory evidence should stay visible until repaired, superseded, withdrawn, or resolved.

Rationale: research workflows need recoverability and auditability more than hidden cleanup. The user and Operator Agent should see the problem and choose a correction.

Alternative considered: automatically prune invalid refs. Rejected because pruning can erase why a claim, decision, or Gate was made.

## Risks / Trade-offs

- [Risk] A semantic contract may be too abstract for implementation. -> Mitigation: require minimum fields and host API scenarios, but defer only storage mechanics.
- [Risk] Evidence Items may feel heavy for simple outputs. -> Mitigation: allow lightweight Evidence Items with a concise summary and one source ref when the evidence is straightforward.
- [Risk] Keeping lifecycle refs without full lifecycle state can leave edge cases unsettled. -> Mitigation: limit this change to reference integrity and leave transitions to the planned lifecycle change.
- [Risk] Gate semantics can block too much work if validation treats every open Gate globally. -> Mitigation: Gates block only the governed action named in the Gate, not unrelated inspection or safe edits.
- [Risk] Updating skill TBDs too aggressively could imply command or provider contracts are settled. -> Mitigation: remove only recording API and record-schema TBDs covered by this change; keep execution, literature, scheduler, Skill Binding, Agent Team State, and policy TBDs.

## Migration Plan

1. Add `research-recording-contracts` specs for record identity, linkage, host APIs, Gate behavior, and validation.
2. Update `research-paradigm-skills` specs so skill references consume accepted recording contracts instead of record API/schema TBD placeholders.
3. Implement documentation changes in the shared TBD registry and local research contracts.
4. Leave concrete command execution, literature search, lifecycle state, and scheduler TBDs in place.
5. Run OpenSpec validation and scans for resolved TBD ids.

Rollback is documentation-only for this change: restore the prior TBD registry entries and remove the new recording contract spec if the contract proves too broad.

## Open Questions

- Should the first implementation use one generic `record_ref` table plus typed payloads, or separate tables per record family?
- Which validation issues are warnings, which are blockers, and which require an Operator Agent Gate to resolve?
