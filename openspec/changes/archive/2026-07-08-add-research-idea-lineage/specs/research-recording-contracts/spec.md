## ADDED Requirements

### Requirement: Records Declare Idea Realizations
Structured research records SHALL be able to declare which Research Ideas they realize without overloading canonical record lineage.

#### Scenario: Record realizes an idea
- **WHEN** an idea-bearing structured record is created or updated with explicit idea realization metadata
- **THEN** the recording API writes or updates the canonical Research Idea and Idea Realization through Workspace Runtime and still records record lineage separately through `parents-json`

#### Scenario: Multiple ideas in one record
- **WHEN** one structured record contains several raw ideas, serious candidates, or alternatives
- **THEN** the recording API can create multiple Idea Realizations that point to the same record with distinct idea ids, stages, source JSON paths, and metadata

#### Scenario: Idea metadata does not create record parents
- **WHEN** a record declares idea parents or idea lineage
- **THEN** the system records idea-level lineage and does not invent `research_record_lineage_edges` unless explicit record parent refs are also supplied

### Requirement: Records Preserve Idea Hints for Repair
Structured research payloads SHALL preserve explicit idea ids, source raw idea ids, source candidate ids, sibling group ids, and collapse rationale when the producing skill knows them.

#### Scenario: Candidate frontier carries source hints
- **WHEN** a candidate frontier payload is written
- **THEN** it includes stable candidate idea ids, status, primary/supporting visibility intent when known, source raw idea ids when known, generation group id when known, and selection or collapse rationale when known

#### Scenario: Source labels are not canonical ids
- **WHEN** a structured payload uses local labels such as `R1`, `R8`, `C1`, or `C3`
- **THEN** the recording API preserves those labels as source aliases or realization metadata and maps them to semantic topic-scoped canonical Research Idea ids

#### Scenario: Selected hypothesis carries realized idea
- **WHEN** a selected hypothesis or selected idea draft is written
- **THEN** it identifies the Research Idea it realizes and records whether the record selects, updates in place, follows up from, or merely elaborates that idea

### Requirement: Idea Recording Validation
The recording API SHALL validate explicit idea recording metadata before accepting durable record writes that claim canonical idea effects.

#### Scenario: Invalid idea metadata blocks canonical idea write
- **WHEN** a record write supplies malformed idea ids, unsupported idea lineage kinds, missing parent ideas, or cross-topic idea refs
- **THEN** the system rejects the canonical idea mutation with diagnostics and does not write partial idea rows

#### Scenario: Record can still omit idea metadata
- **WHEN** a durable record is not idea-bearing or lacks enough context to claim canonical idea effects
- **THEN** the system can accept the record without idea metadata and may report a diagnostic only when the record profile normally requires idea lineage
