## ADDED Requirements

### Requirement: Production DeepSci Artifact Lineage Workflow
Production DeepSci skills SHALL identify canonical artifact lineage before writing or revising durable research records.

#### Scenario: Skill creates a durable record
- **WHEN** a production DeepSci skill creates a durable Artifact, Evidence Item, Decision Record, Run, View Manifest, or related structured research record
- **THEN** the skill workflow tells the agent to identify parent records, lineage kind, parent roles, generation group when relevant, decision record when relevant, and revision parent when relevant before calling the recording CLI

#### Scenario: Skill cannot identify parents
- **WHEN** a production DeepSci skill cannot responsibly identify lineage parents for a durable record
- **THEN** the skill records the omission as a blocker, diagnostic, or explicit no-parent/root-lineage reason rather than inventing parentage

#### Scenario: Skill revises accepted content
- **WHEN** a production DeepSci skill changes accepted record content in a way that should remain historically visible
- **THEN** the skill uses the record revision path and preserves the prior record as the immediate revision parent

### Requirement: DeepSci Idea Flow Records Artifact DAG
The DeepSci idea flow SHALL record parent-child lineage across raw ideas, candidate frontiers, pre-idea drafts, route decisions, and selected hypotheses.

#### Scenario: Raw slate is produced
- **WHEN** `isomer-deepsci-idea` records a raw idea slate
- **THEN** it records lineage parents such as objective contract, current board, literature survey, limitations map, and mechanism framing when those records exist

#### Scenario: Serious candidates are produced
- **WHEN** `isomer-deepsci-idea` promotes serious candidates into candidate frontier or pre-idea draft records
- **THEN** it records those candidates as children of the raw slate or candidate frontier and associates sibling alternatives with a generation group

#### Scenario: Selected hypothesis is produced
- **WHEN** `isomer-deepsci-idea` records a selected hypothesis
- **THEN** it records the selected hypothesis as a child of the selected pre-idea draft or candidate record and the route decision that selected it

### Requirement: DeepSci Downstream Flows Continue Artifact DAG
Downstream DeepSci flows SHALL continue canonical artifact lineage after idea selection.

#### Scenario: Experiment flow creates records
- **WHEN** `isomer-deepsci-experiment` creates an experiment contract, run record, artifact manifest, result summary, or route decision
- **THEN** it records lineage from the selected hypothesis, comparator contract, prior run, and relevant decision records according to the artifact's actual parents

#### Scenario: Analysis flow creates records
- **WHEN** `isomer-deepsci-analysis` creates context briefs, slice records, campaign plans, findings, summaries, or route decisions
- **THEN** it records lineage from parent results, parent claims, runs, evidence, and decisions according to the artifact's actual parents

#### Scenario: Decision flow changes route
- **WHEN** `isomer-deepsci-decision` records a route-changing decision or checkpoint memory
- **THEN** it records lineage from the evidence packet, route question, selected target record, and superseded or rejected route records when those refs are explicit
