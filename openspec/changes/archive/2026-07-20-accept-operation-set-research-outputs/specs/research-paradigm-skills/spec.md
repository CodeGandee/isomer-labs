## ADDED Requirements

### Requirement: Production DeepSci Workflows Close Operation Sets Durably
Active production DeepSci skills that write operation-set files SHALL apply the shared Operation Set Closeout contract after end callbacks and before final response, handoff, or successful completion.

#### Scenario: Focused skill accepts generated outputs
- **WHEN** a production DeepSci skill writes a payload staging file, report, code deliverable, table, figure, note, log, or other material file under an operation set
- **THEN** its numbered workflow invokes the focused operation-set recording route, verifies a complete receipt, and returns durable record refs rather than file paths alone

#### Scenario: End callback output is included
- **WHEN** an end callback creates or changes a material operation-set file
- **THEN** closeout runs after that callback and reconciles the callback output before completion

#### Scenario: Idea-bearing output records both lineage layers
- **WHEN** a DeepSci operation set contains an idea-bearing accepted payload
- **THEN** closeout passes explicit Research Idea effects with exact realization paths through the existing atomic record transaction and verifies canonical record parents and returned idea refs
- **AND** it does not derive Idea Lineage Edges from record lineage alone

#### Scenario: Closeout failure pauses the skill
- **WHEN** acceptance or verification finds an unclassified file, invalid payload, missing parent, failed record action, or missing idea effect
- **THEN** the skill returns a paused result with accepted refs, partial receipt when present, diagnostics, and a resume command

#### Scenario: No plain output is explicit
- **WHEN** a production DeepSci skill completes using only already durable records and creates no operation set
- **THEN** its terminal result records `closeout: not_applicable` and identifies the durable refs it used or created

### Requirement: DeepSci Validation Enforces Operation Set Closeout
The research-paradigm validation harness SHALL reject active DeepSci guidance that can report successful completion from plain operation-set files without verified durable acceptance.

#### Scenario: Missing closeout step is reported
- **WHEN** an active non-shared DeepSci skill writes or describes material plain outputs but lacks a numbered closeout step after end callbacks
- **THEN** validation reports the skill and the missing Operation Set Acceptance gate

#### Scenario: File-only terminal output is reported
- **WHEN** active DeepSci guidance treats a worker output path, terminal summary, rendered Markdown, or Git commit as sufficient successful output
- **THEN** validation reports that durable record refs and a complete receipt are required

#### Scenario: Shared guidance owns command details
- **WHEN** a focused DeepSci skill references the shared closeout contract and focused core recording skill
- **THEN** validation does not require it to duplicate the full manifest and CLI procedure

#### Scenario: Closeout order is validated
- **WHEN** validation inspects a DeepSci workflow that participates in end callbacks
- **THEN** it confirms operation-set closeout occurs after end callbacks and before final success or handoff
