## ADDED Requirements

### Requirement: Kaoju Direction Set Binding Declares Canonical Research Idea Effects
The versioned `KAOJU:DIRECTION-SET` binding and structured payload profile for new accepted writes SHALL declare and validate the canonical Research Idea effects promised for every durable survey-direction proposal while retaining prior Direction Set payloads as readable migration inputs.

#### Scenario: Idea-bearing Direction Set profile is resolved
- **WHEN** a Kaoju producer resolves the active Direction Set binding for a new accepted write
- **THEN** the binding identifies a versioned structured Decision Record profile whose proposal mappings carry or receive stable canonical `idea_id` values, exact proposal paths, generation membership, authored decision option outcomes, and applicable state-transition context
- **AND** the profile remains storage-neutral and does not embed Project Web behavior or a Kaoju-specific database path

#### Scenario: Direction proposal mapping validates
- **WHEN** a Direction Set payload claims canonical Research Idea effects
- **THEN** validation resolves each `idea_id` to exactly one object-valued proposal path, retains the direction id as a source-local alias, validates proposal and decision membership uniqueness, and validates required closure or deferral rationale
- **AND** collection paths, rendered Markdown, selection arrays, and whole-record paths cannot serve as the proposal's Idea Realization path

#### Scenario: Direction Set acceptance is atomic
- **WHEN** a valid idea-bearing Direction Set, its Decision Record option set, and every promised Research Idea effect validate
- **THEN** the artifact service commits the Direction Set record, canonical Research Ideas, Idea Realizations, generation membership, decision options, lineage, and transitions in one transaction
- **AND** it returns all resulting refs to the Kaoju frame and pipeline skills

#### Scenario: Promised direction effect fails
- **WHEN** a Direction Set has a duplicate or missing canonical identity, invalid exact path, unresolved parent, incomplete authored option set, invalid facet, missing closure reason, or cross-topic ref
- **THEN** the artifact service rejects the accepted write without leaving a Direction Set or partial canonical Research Idea effects committed
- **AND** deterministic diagnostics identify the proposal and failed effect

#### Scenario: Legacy Direction Set remains readable
- **WHEN** a Direction Set written under the prior profile contains proposals, selections, and confirmation but lacks canonical idea identity or per-proposal disposition
- **THEN** the binding remains readable and eligible for an explicit previewable migration
- **AND** ordinary reads do not infer current disposition, rationale, exploration, evidence, or idea lineage from omission or nearby prose

#### Scenario: Legacy Direction Set migration is applied
- **WHEN** an actor approves a validated migration plan for a legacy Direction Set
- **THEN** the migration creates one canonical Research Idea per durable proposal, preserves the direction id as an alias, records exact realizations and any decision outcomes directly justified by selections and confirmation, and records migration provenance
- **AND** ambiguous facets, reasons, and lineage remain `unknown` or diagnosed rather than fabricated
