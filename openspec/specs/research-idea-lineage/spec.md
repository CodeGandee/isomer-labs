# research-idea-lineage Specification

## Purpose
TBD - created by archiving change add-research-idea-lineage. Update Purpose after archive.
## Requirements
### Requirement: Canonical Research Idea Identity
The system SHALL represent each durable topic-scoped research idea as a canonical Research Idea with stable identity, display key, human-readable title, human-readable summary, exploration state, decision state, evidence state, archive state, visibility, source refs, timestamps, and metadata.

#### Scenario: Primary idea is recorded
- **WHEN** an agent, operator, repair command, or import command records a top-level idea that should appear in the default idea map
- **THEN** the system stores a Research Idea with `visibility` set to `primary`, a stable semantic topic-scoped `idea_id`, a stable short `display_key`, non-empty `title`, non-empty `summary`, Research Topic ref, Topic Workspace ref, explicit state facets, source record ref when known, and provenance metadata
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
- **THEN** the system can store it as a Research Idea with non-empty `title` and `summary`, `visibility` set to `primary`, exploration state reflecting whether focused work began, decision state reflecting whether it remains open, deferred, or closed, and metadata that identifies the raw-slate generation

#### Scenario: Facets are not inferred from one another
- **WHEN** a caller writes or reads a canonical Research Idea
- **THEN** selection does not imply exploration, exploration does not imply evidence support, refutation does not imply closure, and archival does not erase any other facet

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
- **THEN** the system records an idea generation group with parent set digest, purpose, producer skill, optional Decision Record id, and member ideas linked through their lineage edges

#### Scenario: Sibling query returns alternatives
- **WHEN** a caller queries siblings for a Research Idea in a generation group
- **THEN** the system returns the other generated Research Ideas, the generation group metadata, and the common parent set without inventing pairwise `alternative_to` edges

#### Scenario: Sibling group does not imply subsumption
- **WHEN** several Research Ideas belong to the same idea generation group
- **THEN** the system does not infer `subsumes` edges unless an agent, operator, import, or repair action records those edges explicitly

#### Scenario: Generation membership does not imply decision membership
- **WHEN** a Decision Record considers some or all ideas from a generation group
- **THEN** the system records the considered option set explicitly
- **AND** it does not infer that every generation member was considered or rejected by that decision

### Requirement: Idea Maintenance CLI
The system SHALL expose deterministic CLI commands for creating, transitioning, linking, querying, traversing, validating, importing, migrating, and repairing Research Idea lineage and portfolio state.

#### Scenario: Idea CLI writes canonical data
- **WHEN** an operator runs `isomer-cli --print-json ext research ideas upsert`, `transition`, `realize`, `lineage add`, `generation upsert`, or a decision-option maintenance command
- **THEN** the command writes canonical Workspace Runtime idea data, returns deterministic JSON, and does not write derived query-index rows directly

#### Scenario: Transition records context
- **WHEN** an operator changes exploration, decision, evidence, archive, or visibility state through the CLI
- **THEN** the command requires the target value, actor, rationale or reason, and applicable durable refs
- **AND** it records previous and next values through canonical transition history

#### Scenario: Idea query filters portfolio state
- **WHEN** an operator queries Research Ideas by one or more exploration, decision, evidence, archive, visibility, generation, or Decision Record filters
- **THEN** the command returns every matching canonical Research Idea with its facet values and diagnostics
- **AND** it does not reduce the query to a legacy status comparison

#### Scenario: Idea traversal returns lineage
- **WHEN** an operator queries bounded ancestors or descendants for one or more Research Ideas with optional relation-kind and depth constraints
- **THEN** the command returns the traversed Research Ideas, canonical Idea Lineage Edges, completeness metadata, and diagnostics

#### Scenario: Decision context is queried
- **WHEN** an operator queries the decision context for a Research Idea or Decision Record
- **THEN** the command returns the complete recorded option set, selected options, other outcomes, rationale, consequence summaries, and supporting durable refs

#### Scenario: Idea CLI validates data
- **WHEN** an operator runs `isomer-cli --print-json ext research ideas validate`
- **THEN** the command reports missing idea refs, missing realization records, cross-topic refs, invalid lineage kinds, invalid facet values, incomplete transitions, conflicting compatibility status, missing decision options, duplicate primary ids, cycles, stale latest flags, and generation-group inconsistencies without mutating canonical data

#### Scenario: Idea CLI imports legacy records
- **WHEN** an operator runs `isomer-cli --print-json ext research ideas import-from-record <record-id>`
- **THEN** the command extracts explicit source labels, source paths, source raw idea ids, candidate ids, authored state facets, decision membership, and lineage hints from structured payloads into a preview or applied canonical idea repair plan with semantic canonical `idea_id` values and preserved aliases

#### Scenario: Legacy status migration previews changes
- **WHEN** an operator runs the Research Idea portfolio migration command without an apply flag
- **THEN** the command returns a deterministic plan containing every proposed facet, compatibility status, transition, diagnostic, and affected idea id
- **AND** it does not mutate Workspace Runtime, payload files, generated views, or query-index rows

### Requirement: Primary Idea Graph View
The system SHALL provide an idea graph read model that defaults to canonical primary Research Ideas and their idea-level edges while exposing canonical portfolio facets and diagnostics.

#### Scenario: Canonical idea graph is available
- **WHEN** a Topic Workspace has canonical Research Idea data
- **THEN** the idea-lineage graph returns primary Research Idea nodes, including raw time-parent ideas when marked primary, canonical portfolio facets, canonical Idea Lineage Edges, generation-group metadata, decision summary refs, diagnostics, and idea detail refs without using extracted record facets as primary nodes

#### Scenario: Supporting material is expanded on demand
- **WHEN** a caller requests supporting ideas or secondary material
- **THEN** the graph can include supporting Research Ideas, linked records, route decisions, claims, and realization details while preserving the primary idea DAG as the high-level structure

#### Scenario: Legacy fallback is diagnostic
- **WHEN** canonical Research Idea data is absent
- **THEN** the graph may use extracted record idea facets as a legacy fallback and MUST include diagnostics that the graph is heuristic rather than canonical

#### Scenario: Unknown classification remains visible
- **WHEN** a primary Research Idea has one or more `unknown` state facets
- **THEN** the default graph keeps the idea visible unless the user explicitly filters it out
- **AND** it labels the idea as needing classification instead of mapping it silently to a known state

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

### Requirement: Research Idea Decision Option Membership
The system SHALL link a Decision Record to every Research Idea explicitly considered by that decision without treating generation or lineage as a substitute for option membership.

#### Scenario: Selection decision records all considered ideas
- **WHEN** a user, operator, or agent selects one or more Research Ideas from a considered set
- **THEN** the system records an option membership row for every considered Research Idea
- **AND** each row records its outcome or role, ordering when meaningful, rationale or consequence when present, and generation ref when relevant

#### Scenario: Deferral or closure is explained
- **WHEN** a decision defers or closes a Research Idea
- **THEN** its option membership and state transition link to the Decision Record that records the reason, actor, timestamp, consequences, and supporting Evidence Item or Artifact refs

#### Scenario: Idea is reopened
- **WHEN** a later decision reopens a deferred or closed Research Idea
- **THEN** the new Decision Record and transition reference the prior disposition and preserve both decisions in history

#### Scenario: Partial historical option set is preserved honestly
- **WHEN** migration can identify a selected idea but cannot identify every considered alternative
- **THEN** the system records only the known option membership
- **AND** it emits an incomplete-decision-context diagnostic rather than inventing alternatives

### Requirement: Legacy Research Idea Portfolio Migration
The system SHALL migrate overloaded Research Idea status values into canonical facets conservatively through explicit preview and apply operations.

#### Scenario: Legacy value maps only justified meaning
- **WHEN** migration interprets `raw`, `candidate`, `selected`, `active`, `supported`, `refuted`, `deferred`, `rejected`, `superseded`, or `archived`
- **THEN** it assigns only directly justified exploration, decision, evidence, or archive values
- **AND** it sets every unsupported facet to `unknown`

#### Scenario: Legacy rejection becomes explained closure
- **WHEN** migration applies a legacy `rejected` or `superseded` status
- **THEN** it sets decision state to `closed` with a legacy rejection or legacy supersession reason code
- **AND** it preserves the original status in migration metadata

#### Scenario: Migration does not invent history
- **WHEN** no historical actor, rationale, decision, evidence, or transition timestamp is available
- **THEN** migration records its own provenance and classification timestamp
- **AND** it does not fabricate the missing historical context

#### Scenario: Applied migration keeps compatibility reads
- **WHEN** an explicit apply operation migrates a Research Idea
- **THEN** canonical reads use the new facets
- **AND** compatibility reads continue to return a deterministic deprecated status projection for the supported migration window

