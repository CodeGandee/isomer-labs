## ADDED Requirements

### Requirement: Idea-producing Records Persist Portfolio Intent
Idea-bearing structured research record writes SHALL persist canonical Research Idea facets, Idea Realizations, lineage, generation membership, decision context, and transition provenance when the producer claims those effects and has enough authored intent to do so.

#### Scenario: Raw idea slate is accepted
- **WHEN** an accepted structured record profile declares a set of durable proposed Research Ideas
- **THEN** the write records each canonical Research Idea, its exact object-valued Idea Realization path, known visibility and state facets, generation membership, and provenance in the same accepted operation
- **AND** it does not rely on later Markdown parsing or GUI facet extraction to create those ideas

#### Scenario: Candidate is investigated
- **WHEN** an accepted analysis, experiment, or focused exploration record establishes that work began or completed for a Research Idea
- **THEN** the producer explicitly records the justified exploration transition and links the record, Research Task, Run, Evidence Item, Finding, or Provenance Record refs that support it
- **AND** it does not change decision or evidence state unless the accepted output also justifies those independent changes

#### Scenario: Evidence assessment changes
- **WHEN** an accepted result or decision explicitly assesses evidence for a Research Idea
- **THEN** the producer records the justified evidence transition with supporting Evidence Item, Artifact, Finding, Research Claim, Run, or Decision Record refs
- **AND** it does not automatically close a refuted idea or select a supported idea

#### Scenario: Record lacks enough intent
- **WHEN** an idea-bearing record cannot justify one or more canonical facets, lineage edges, or decision options
- **THEN** the producer records `unknown` for required unknown facets or omits optional effects according to the profile contract
- **AND** it emits diagnostics naming the missing intent rather than guessing from nearby prose or timestamps

### Requirement: Idea Decision Records Preserve Considered Options
Record-write paths that accept a meaningful Research Idea selection, deferral, closure, or reopening SHALL preserve the complete authored option set and its outcomes.

#### Scenario: Selection output is accepted
- **WHEN** a selected hypothesis, selected idea draft, route decision, or equivalent structured record selects an idea from authored alternatives
- **THEN** the accepted operation records the Decision Record, every authored considered Research Idea option, selected and non-selected outcomes, rationale, consequences, and supporting refs
- **AND** it links the resulting decision-state transitions to that Decision Record

#### Scenario: Rejected and deferred ledger is accepted
- **WHEN** a structured record explicitly records rejected, deferred, or closed Research Ideas and their reasons
- **THEN** the accepted operation records the corresponding decision option membership and decision-state transitions
- **AND** it preserves closure reason codes separately from freeform rationale

#### Scenario: Decision set differs from generation group
- **WHEN** a decision record considers only part of a generation group or combines ideas from multiple generations
- **THEN** the recording path writes the exact authored decision option set
- **AND** it does not substitute generation membership for decision membership

### Requirement: Promised Canonical Idea Effects Are Atomic With Record Acceptance
The recording API SHALL commit an accepted structured record and the canonical Research Idea effects promised by its profile as one atomic operation.

#### Scenario: Canonical idea effects succeed
- **WHEN** a profile-valid record write declares canonical idea effects and every referenced idea, record, path, lineage edge, decision, and transition validates
- **THEN** the recording API commits the record and all promised idea effects together
- **AND** the response returns the created or updated Research Idea, Idea Realization, lineage, decision, and transition refs

#### Scenario: Canonical idea effect fails
- **WHEN** a promised Research Idea effect has an invalid facet, missing exact source path, missing parent, cross-topic ref, incomplete transition, or incomplete required decision option set
- **THEN** the recording API rejects the accepted operation without committing a partial record or partial canonical idea mutation
- **AND** it returns deterministic diagnostics for repair

#### Scenario: Non-idea-bearing record omits idea metadata
- **WHEN** a structured record profile does not claim canonical Research Idea effects
- **THEN** the recording API can accept the record without idea metadata
- **AND** it does not invent Research Ideas from general research prose

### Requirement: System Skills Teach Canonical Idea Portfolio Recording
Packaged and source Research Idea-producing system skills SHALL instruct agents to record canonical portfolio state and verify durable refs before declaring their idea-bearing outputs accepted.

#### Scenario: Idea-producing skill records output
- **WHEN** a DeepSci or other system skill produces a raw slate, candidate frontier, pre-idea draft, selected hypothesis, selected idea, rejected or deferred ledger, route decision, analysis follow-up, optimization line, or paper-facing idea seed
- **THEN** its workflow names the required Research Idea upsert, exact realization, lineage, generation, transition, and decision-option operations for that output
- **AND** it requires the operation result refs in the accepted terminal report or equivalent durable output

#### Scenario: Shared guidance owns common intent
- **WHEN** several system skills need the same Research Idea recording rules
- **THEN** they route to one shared Research Idea Recording reference and add only profile-specific mappings
- **AND** copied skill text does not redefine canonical state vocabulary independently

#### Scenario: Skill cannot record promised effects
- **WHEN** an idea-producing skill cannot complete or validate required canonical idea writes
- **THEN** it reports the output as paused, blocked, or incomplete with a precise resume point
- **AND** it does not claim that a generated file or operation-set output alone completed durable idea recording
