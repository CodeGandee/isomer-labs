## MODIFIED Requirements

### Requirement: Canonical Research Idea Identity
The system SHALL represent each durable topic-scoped research idea as a canonical Research Idea with stable identity, display key, human-readable title, human-readable summary, status, visibility, source refs, timestamps, and metadata.

#### Scenario: Primary idea is recorded
- **WHEN** an agent, operator, repair command, or import command records a top-level idea that should appear in the default idea map
- **THEN** the system stores a Research Idea with `visibility` set to `primary`, a stable semantic topic-scoped `idea_id`, a stable short `display_key`, non-empty `title`, non-empty `summary`, Research Topic ref, Topic Workspace ref, status, source record ref when known, and provenance metadata
- **AND** the stored Research Idea does not use `one_liner` as a first-class display field

#### Scenario: Source label is preserved as alias
- **WHEN** a source record names an idea with a local label such as `R1`, `R8`, `C1`, or `C3`
- **THEN** the system preserves that source label as an alias or realization metadata and does not require the source label to become the canonical `idea_id` or display key

#### Scenario: Reused source label does not collide
- **WHEN** a later idea pass reuses a source-local label that appeared in an earlier pass
- **THEN** validation allows the alias reuse only when the canonical semantic `idea_id` values remain distinct within the Research Topic

#### Scenario: Supporting idea is recorded
- **WHEN** an idea is a raw component, ablation term, or detail that supports a primary idea but should not appear in the default map
- **THEN** the system stores it as a Research Idea with non-empty `title` and `summary` and with `visibility` set to `supporting` or `hidden` instead of forcing it into the primary graph

#### Scenario: Raw time-parent idea is recorded
- **WHEN** a raw idea slate entry explains how later candidate ideas branched over time
- **THEN** the system can store it as a Research Idea with non-empty `title` and `summary`, `visibility` set to `primary`, `status` reflecting raw, deferred, or rejected state, and metadata that identifies the raw-slate generation

## ADDED Requirements

### Requirement: Research Idea Summary Migration
The system SHALL provide deterministic migration and validation behavior for Research Ideas that still contain legacy `one_liner` data.

#### Scenario: Legacy one-liner is migrated
- **WHEN** a migration or repair apply command encounters a Research Idea with `one_liner` and no canonical `summary`
- **THEN** it writes the legacy value to `summary` when the value is usable
- **AND** it records migration diagnostics or provenance for the affected idea

#### Scenario: Normal idea reads use stored summary
- **WHEN** graph, timeline, hover, detail, CLI, or API read paths return a Research Idea after migration support exists
- **THEN** they read the stored `summary` field directly
- **AND** they do not convert `one_liner` to `summary` on the fly for normal display

#### Scenario: Damaged idea data is non-fatal
- **WHEN** an idea is missing display fields, has broken parent refs, points to deleted source records, or contains lineage that cannot be fully interpreted
- **THEN** validation and read models report diagnostics for the damaged data
- **AND** they return all safely interpretable idea nodes, edges, rows, and recent errors instead of crashing
