# research-idea-lineage Specification

## Purpose
TBD - created by archiving change add-research-idea-lineage. Update Purpose after archive.
## Requirements
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

### Requirement: Idea Realization Links
The system SHALL link Research Ideas to durable research records through Idea Realization records instead of treating one record as the whole idea.

#### Scenario: Idea appears in multiple records
- **WHEN** the same Research Idea is expressed by a candidate frontier entry, pre-idea draft, selected hypothesis, analysis follow-up, or paper-facing claim
- **THEN** the system records one Research Idea and multiple Idea Realizations that name the record id, source JSON path when known, realization stage, latest flag, and metadata

#### Scenario: Revised record updates same idea
- **WHEN** an accepted record revision changes the content that realizes an existing Research Idea
- **THEN** the system updates the same Research Idea in place and records the revised record as an Idea Realization without creating a new Research Idea or idea-level `revision_of` edge

#### Scenario: Idea detail opens records
- **WHEN** a GUI or CLI opens a Research Idea detail view
- **THEN** the system can return the latest realization and realization history with record detail refs, rendered Markdown refs when available, payload locators, and source JSON paths

### Requirement: Idea Lineage DAG
The system SHALL store typed idea-level lineage edges as a topic-scoped DAG between Research Ideas.

#### Scenario: Idea edge is recorded
- **WHEN** one Research Idea is derived from, selected from, merged from, follows up, alternates with, or subsumes another Research Idea
- **THEN** the system stores an Idea Lineage Edge with parent idea id, child idea id, lineage kind, optional parent role, generation id, decision record id, rationale, status, confidence when known, and metadata

#### Scenario: Subsumption is represented as edge
- **WHEN** one Research Idea intentionally covers another idea's mechanism, ablation, or test role
- **THEN** the system can store a `subsumes` Idea Lineage Edge so the GUI and CLI can show that conceptual relationship directly

#### Scenario: Idea lineage rejects cycles
- **WHEN** an idea lineage write would create a cycle in the non-archived Research Idea graph
- **THEN** validation rejects the edge and returns diagnostics naming the conflicting parent and child idea ids

#### Scenario: Idea revision edge is rejected
- **WHEN** a caller attempts to create an idea-level `revision_of` edge
- **THEN** validation rejects the edge and directs the caller to update the existing Research Idea and add or refresh an Idea Realization

### Requirement: Idea Generation Groups
The system SHALL represent sibling or alternative Research Ideas produced from the same idea pass through idea generation groups rather than pairwise sibling edges.

#### Scenario: Serious candidates share generation
- **WHEN** one idea pass creates several serious candidates from the same parent idea set
- **THEN** the system records an idea generation group with parent set digest, purpose, producer skill, optional decision record id, and member ideas linked through their lineage edges

#### Scenario: Sibling query returns alternatives
- **WHEN** a caller queries siblings for a Research Idea in a generation group
- **THEN** the system returns the other generated Research Ideas, the generation group metadata, and the common parent set without inventing pairwise `alternative_to` edges

#### Scenario: Sibling group does not imply subsumption
- **WHEN** several Research Ideas belong to the same idea generation group
- **THEN** the system does not infer `subsumes` edges unless an agent, operator, import, or repair action records those edges explicitly

### Requirement: Idea Maintenance CLI
The system SHALL expose deterministic CLI commands for creating, linking, querying, validating, importing, and repairing Research Idea lineage.

#### Scenario: Idea CLI writes canonical data
- **WHEN** an operator runs `isomer-cli --print-json ext research ideas upsert`, `realize`, `lineage add`, or `generation upsert`
- **THEN** the command writes canonical Workspace Runtime idea data, returns deterministic JSON, and does not write derived query-index rows directly

#### Scenario: Idea CLI validates data
- **WHEN** an operator runs `isomer-cli --print-json ext research ideas validate`
- **THEN** the command reports missing idea refs, missing realization records, cross-topic refs, invalid lineage kinds, duplicate primary ids, cycles, stale latest flags, and generation-group inconsistencies without mutating canonical data

#### Scenario: Idea CLI imports legacy records
- **WHEN** an operator runs `isomer-cli --print-json ext research ideas import-from-record <record-id>`
- **THEN** the command extracts explicit source labels, source paths, source raw idea ids, candidate ids, and authored lineage hints from structured payloads into a preview or applied canonical idea repair plan with semantic canonical `idea_id` values and preserved aliases

### Requirement: Primary Idea Graph View
The system SHALL provide an idea graph read model that defaults to canonical primary Research Ideas and their idea-level edges.

#### Scenario: Canonical idea graph is available
- **WHEN** a Topic Workspace has canonical Research Idea data
- **THEN** the idea-lineage graph returns primary Research Idea nodes, including raw time-parent ideas when marked primary, canonical idea lineage edges, generation-group metadata, diagnostics, and idea detail refs without using extracted record facets as primary nodes

#### Scenario: Supporting material is expanded on demand
- **WHEN** a caller requests supporting ideas or secondary material
- **THEN** the graph can include supporting Research Ideas, linked records, route decisions, claims, and realization details while preserving the primary idea DAG as the high-level structure

#### Scenario: Legacy fallback is diagnostic
- **WHEN** canonical Research Idea data is absent
- **THEN** the graph may use extracted record idea facets as a legacy fallback and MUST include diagnostics that the graph is heuristic rather than canonical

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

