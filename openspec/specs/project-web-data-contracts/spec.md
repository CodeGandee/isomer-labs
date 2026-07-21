# project-web-data-contracts Specification

## Purpose
Define GUI-usable Project Web data contracts and permissive validation rules for read payloads rendered by the Isomer Labs GUI.
## Requirements
### Requirement: UI Contract Documentation
The system SHALL document GUI-usable data contracts under `docs/ui/contracts/` as separate pages organized by Project Web view or shared payload shape.

#### Scenario: Contract pages exist
- **WHEN** a developer or agent needs to understand the data required by a Project Web view
- **THEN** `docs/ui/contracts/` SHALL contain an index page and focused contract pages for the relevant GUI payloads
- **AND** each page SHALL describe required fields, optional useful fields, extra-field handling, and a concrete example

#### Scenario: Contract docs distinguish storage from viewing
- **WHEN** a contract page describes a GUI payload
- **THEN** it SHALL state that the payload is a UI read contract unless it is explicitly documenting an existing canonical storage contract
- **AND** it SHALL NOT imply that extra agent-authored metadata must be removed from Workspace Runtime records

### Requirement: Permissive Python GUI Schemas
The system SHALL provide Python schemas for GUI-facing read models that validate required Project Web fields while allowing additional fields.

#### Scenario: Required fields are present
- **WHEN** backend code, tests, or fixture checks validate a GUI payload with all required fields and additional unknown fields
- **THEN** schema validation SHALL pass
- **AND** the caller SHALL be able to preserve or ignore unknown fields according to its use case

#### Scenario: Required fields are missing
- **WHEN** a GUI payload omits fields required for the corresponding Project Web view to render safely
- **THEN** schema validation SHALL fail with a deterministic validation error that identifies the missing or invalid field

#### Scenario: Nested payloads contain richer agent metadata
- **WHEN** a payload includes nested metadata that is not required by the GUI contract
- **THEN** schema validation SHALL NOT reject the payload solely because of those extra fields

### Requirement: Initial Contract Coverage
The initial GUI contract set SHALL cover the read models currently needed by Project Web topic inspection flows.

#### Scenario: Topic overview contract is covered
- **WHEN** the topic overview panel consumes a topic overview response
- **THEN** a documented contract and Python schema SHALL cover `ok`, `mutated`, topic identity, overview source metadata, Markdown content availability, supporting JSON payloads, and diagnostics

#### Scenario: Graph view contract is covered
- **WHEN** the idea lineage or artifact graph panels consume a graph response
- **THEN** a documented contract and Python schema SHALL cover graph identity fields, nodes, edges, groups, facets, paging, diagnostics, and renderer hints needed by Project Web

#### Scenario: Idea detail contract is covered
- **WHEN** the idea detail panel consumes an idea detail response
- **THEN** a documented contract and Python schema SHALL cover idea identity, canonical idea metadata, realizations, source provenance, source JSON availability, lineage edges, generation groups, diagnostics, and optional exact source JSON

#### Scenario: Record inspection contracts are covered
- **WHEN** record tabs consume viewer descriptors, rendered record payloads, file lists, lineage, siblings, or facets
- **THEN** documented contracts and Python schemas SHALL cover the fields required to choose a viewer, open canonical detail, display rendered Markdown, display file openability, group raw JSON modal payloads, report diagnostics, and copy an absolute artifact filepath when available
- **AND** record detail contracts SHALL cover optional Topic Workspace-relative path, absolute artifact filepath, and direct parent idea metadata when those values can be derived from structured read-model data

### Requirement: Contract Validation Tests
The system SHALL include tests that exercise GUI contract schema validation with representative Project Web payloads.

#### Scenario: Extra fields are accepted in tests
- **WHEN** a test validates a representative GUI payload that includes unknown top-level and nested fields
- **THEN** the test SHALL pass if all required GUI fields are present

#### Scenario: Missing required fields are rejected in tests
- **WHEN** a test validates a representative GUI payload with a required field removed
- **THEN** the test SHALL assert that validation fails

#### Scenario: Current backend payloads remain compatible
- **WHEN** tests build representative payloads from current Project Web read-model shapes
- **THEN** those payloads SHALL validate without requiring database migration or removal of extra metadata

### Requirement: Idea Timeline Contract Coverage
The Project Web UI contract set SHALL document and validate the payload shape consumed by the Idea Timeline view.

#### Scenario: Timeline contract is documented
- **WHEN** a developer or agent needs to implement or review the Idea Timeline view
- **THEN** `docs/ui/contracts/` contains contract documentation for the timeline payload or an updated topic graph contract that explicitly covers timeline use
- **AND** the documentation identifies required fields, optional useful fields, extra-field handling, and a concrete example

#### Scenario: Timeline payload validates required fields
- **WHEN** tests validate a representative Idea Timeline payload
- **THEN** validation passes when required topic identity, idea identity, display key, title, timestamp or fallback ordering fields, parent relationship identity, visibility or supporting-row metadata, diagnostics, and mutation state are present

#### Scenario: Timeline filter contract validates required fields
- **WHEN** tests validate Idea Timeline search or filter state and payloads
- **THEN** validation covers search text, status filter, relation filter, Supporting Records state, and enough row metadata to apply those filters safely

#### Scenario: Timeline sort and entry-count contract validates required fields
- **WHEN** tests validate Idea Timeline sort state, entry-count state, and payloads
- **THEN** validation covers active sort column, sort direction, entry-count limit, and enough row metadata to sort each visible column deterministically

#### Scenario: Timeline settings contract covers row coloring
- **WHEN** tests validate Project Web settings used by Idea Timeline
- **THEN** validation covers whether row category coloring is enabled and the configured Primary Idea and supporting idea row colors

#### Scenario: Timeline payload rejects unsafe omissions
- **WHEN** tests validate a representative Idea Timeline payload missing fields required for safe table rendering or row opening
- **THEN** validation fails with a deterministic error or the GUI reports a safe empty/diagnostic state

#### Scenario: Display key uniqueness is database-backed
- **WHEN** backend contract tests exercise Research Idea persistence
- **THEN** they verify topic-scoped `display_key` uniqueness is enforced by Workspace Runtime database constraints

### Requirement: Graph View Metadata Contract Coverage
The Project Web UI contract set SHALL document metadata needed to distinguish idea graph and idea timeline views.

#### Scenario: View metadata is documented
- **WHEN** a graph-section openable descriptor or graph payload identifies an idea view
- **THEN** the contract documentation describes the field or identifier that separates relationship graph presentation from timeline/table presentation

#### Scenario: Extra graph fields remain accepted
- **WHEN** graph or timeline payloads include additional metadata for future timeline growth
- **THEN** contract validation accepts those extra fields as long as required GUI fields are present

### Requirement: Recent Errors Contract Coverage
The Project Web UI contract set SHALL document and validate the recent-errors response used by graph and timeline warning surfaces.

#### Scenario: Recent errors contract is documented
- **WHEN** a developer or agent needs to implement or review the recent-errors query
- **THEN** `docs/ui/contracts/` contains contract documentation for recent errors or an updated diagnostics contract that explicitly covers recent read-model errors

#### Scenario: Recent errors payload validates required fields
- **WHEN** tests validate a representative recent-errors payload
- **THEN** validation passes when bounded list metadata, timestamp, severity, code, message, source view or operation, diagnostics, and `mutated: false` are present

### Requirement: Hyphenated Display Key Contract
Project Web data contracts SHALL document and validate Research Idea display keys as GUI-visible labels in the `I-<index>` format.

#### Scenario: Graph node contract carries display key
- **WHEN** a topic graph node represents a canonical Research Idea with a display key
- **THEN** the graph payload exposes `display_key` using the `I-<index>` format
- **AND** UI contract schemas accept the field without requiring consumers to parse canonical `idea_id`

#### Scenario: Timeline contract uses display key as visible identity
- **WHEN** the Idea Timeline derives rows from graph data
- **THEN** the timeline contract identifies `display_key` as the short visible key
- **AND** it states that `idea_id` remains the stable row identity

### Requirement: Timeline Fuzzy Search Contract
Project Web data contracts SHALL document the Idea Timeline fuzzy search state and matching surface.

#### Scenario: Search state is one text value
- **WHEN** the Idea Timeline view stores or restores search state
- **THEN** the contract represents search as one text query value
- **AND** it does not require separate status, relation, or field-specific query values

#### Scenario: Search surface includes supporting rows
- **WHEN** the contract describes timeline search behavior
- **THEN** it states that search can match primary and supporting Research Idea row fields
- **AND** it states that the Supporting Records flag controls whether supporting rows are visible

### Requirement: Project Web Display Contracts Use Summary
Project Web graph, timeline, hover, detail, and record read contracts SHALL expose `summary` as the brief display field and SHALL NOT require `one_liner`.

#### Scenario: Graph node uses summary
- **WHEN** the Project Web idea graph consumes a graph response
- **THEN** each graph node exposes `title`, `summary`, material kind, status, refs, and diagnostics needed for rendering
- **AND** canonical Research Idea nodes also expose `display_key`, visibility, and parent refs
- **AND** the node contract does not expose `one_liner`

#### Scenario: Timeline row uses summary
- **WHEN** the Project Web idea timeline consumes a timeline row response
- **THEN** the row exposes creation time, display index, display key, title, summary, parent display keys or indexes, visibility, status, and diagnostics needed for table rendering
- **AND** the row contract does not expose `one_liner`

#### Scenario: Hover and detail use summary
- **WHEN** the Project Web hover preview or idea detail panel opens a Research Idea
- **THEN** the read payload exposes canonical idea `title` and `summary` and exact source-fragment `title` and `summary` when available
- **AND** source aliases remain separate from display fields

#### Scenario: Fuzzy search includes summary
- **WHEN** a GUI user performs fuzzy text search in idea graph or timeline views
- **THEN** search matching includes `summary` and the other visible/searchable row or node fields
- **AND** visibility flags still control whether supporting or hidden ideas are shown in results

### Requirement: Project Web Display Diagnostics Are Non-fatal
Project Web read contracts SHALL carry display-contract diagnostics so damaged data does not crash the GUI.

#### Scenario: Missing summary reaches GUI as diagnostic
- **WHEN** a backend graph, timeline, hover, or detail response encounters an idea without a usable `summary`
- **THEN** the response includes a diagnostic naming the affected idea and missing field
- **AND** the GUI can render the remaining interpretable data without reading `one_liner`

#### Scenario: Recent errors include display issues
- **WHEN** Project Web records display-contract warnings or errors while building read models
- **THEN** the recent-errors read contract exposes those issues for operator inspection
- **AND** the recent-errors contract remains a process-local recent diagnostic query rather than durable Workspace Runtime storage for this change

### Requirement: Research Idea Portfolio Facet Contract
Project Web data contracts SHALL document and validate canonical Research Idea exploration, decision, evidence, archive, and visibility facets for graph nodes, timeline rows, hover previews, and idea details.

#### Scenario: Canonical facet payload validates
- **WHEN** a representative canonical Research Idea payload contains stable identity, display fields, `exploration_state`, `decision_state`, `evidence_state`, `archive_state`, `visibility`, detail refs, and diagnostics
- **THEN** the corresponding permissive Python schema validates the payload
- **AND** extra agent-authored metadata remains allowed

#### Scenario: Required facet is missing
- **WHEN** a canonical Research Idea payload for the new portfolio contract omits a required state facet
- **THEN** schema validation fails with a deterministic field error or the backend marks the payload as a legacy fallback with explicit diagnostics
- **AND** Project Web does not silently derive the missing facet from deprecated status

#### Scenario: Unknown facet validates
- **WHEN** exploration, decision, or evidence state is `unknown`
- **THEN** schema validation accepts the canonical value
- **AND** the contract documents how clients identify the idea as needing classification

#### Scenario: Deprecated status is present
- **WHEN** a payload includes the compatibility `status` field together with canonical facets
- **THEN** schema validation permits it as an extra or explicitly deprecated field
- **AND** contract documentation states that clients use canonical facets for portfolio behavior

### Requirement: Idea Portfolio Preset and Filter Contract
Project Web data contracts SHALL document and validate semantic preset metadata, explicit facet filters, applied predicates, source counts, visible counts, and topology completeness.

#### Scenario: Preset metadata validates
- **WHEN** a graph or timeline response identifies a supported portfolio preset
- **THEN** schema validation covers preset id, canonical predicate, explicit filter values, source facet counts, visible counts, index revision, and completeness metadata

#### Scenario: Composed filter state validates
- **WHEN** Project Web stores or restores a preset plus exploration, decision, evidence, archive, visibility, relation-kind, text, generation, or decision filters
- **THEN** the UI-state contract validates supported values and composition order
- **AND** it keeps browser view state distinct from canonical Research Idea state

#### Scenario: Unsupported preset is rejected
- **WHEN** a response or restored view state names an unsupported semantic preset
- **THEN** validation reports the invalid preset deterministically
- **AND** Project Web falls back to a safe documented view without mutating research data

### Requirement: Research Idea Decision Context Contract
Project Web data contracts SHALL document and validate the read payload used to explain Research Idea selection, deferral, closure, and reopening.

#### Scenario: Complete decision context validates
- **WHEN** a decision-context payload contains Decision Record identity, considered Research Idea options, option outcomes, selected options, rationale, consequences, actor refs, timestamps, transition refs, supporting refs, mutation state, and diagnostics
- **THEN** the permissive Python schema validates the payload
- **AND** extra decision metadata remains allowed

#### Scenario: Incomplete historical context validates with diagnostics
- **WHEN** a historical Decision Record has an incomplete option set or missing rationale
- **THEN** the payload validates only when it includes diagnostics that identify the incomplete fields
- **AND** clients are not required to invent placeholder alternatives

#### Scenario: Closure detail validates
- **WHEN** an idea detail payload describes a closed disposition
- **THEN** the contract covers closure reason code, rationale, deciding actor, timestamp, Decision Record ref, transition ref, supporting refs, and later reopen refs when present

### Requirement: Research Idea Traversal Contract
Project Web data contracts SHALL document and validate bounded ancestor and descendant traversal request and response payloads.

#### Scenario: Traversal request validates
- **WHEN** a client requests lineage traversal
- **THEN** the request contract validates root idea ids, ancestor or descendant direction, relation kinds, optional maximum depth, and supported safety-bound parameters

#### Scenario: Complete traversal response validates
- **WHEN** a traversal response is complete
- **THEN** the response contract validates roots, direction, relation kinds, nodes, edges, observed depth, source revision, counts, `topology_complete: true`, `mutated: false`, and diagnostics

#### Scenario: Incomplete traversal response validates
- **WHEN** a traversal response reaches a safety bound
- **THEN** the response contract requires incomplete status, limiting-bound metadata, returned counts, source counts when known, and actionable continuation or refinement metadata

### Requirement: Research Idea Steering Action Contract
Project Web data contracts SHALL document and validate separate request and response payloads for `Explore this idea` and `Explore instead` actions.

#### Scenario: Explore alongside request validates
- **WHEN** Project Web submits `Explore this idea`
- **THEN** the request contract validates topic identity, target idea id, expected index revision, idempotency key, user prompt or rationale, and reopening confirmation when required
- **AND** it does not require replaced idea ids

#### Scenario: Explore instead request validates
- **WHEN** Project Web submits `Explore instead`
- **THEN** the request contract validates topic identity, target idea id, exact replaced idea ids, proposed replaced-idea dispositions, rationale, expected index revision, idempotency key, and Gate resolution ref when required

#### Scenario: Accepted steering response validates
- **WHEN** a steering action is accepted
- **THEN** the response contract validates mutation state, operation id, Decision Record ref when present, transition refs, Research Inquiry ref, Research Task ref, handoff or dispatch ref, resulting idea facets, new index revision or pending revision state, and dispatch status

#### Scenario: Pending or blocked dispatch response validates
- **WHEN** canonical steering effects commit but actor dispatch is pending or blocked
- **THEN** the response contract distinguishes canonical acceptance from dispatch state
- **AND** it includes actionable diagnostics and an idempotent retry ref without reporting the canonical action as rolled back

#### Scenario: Conflict response validates
- **WHEN** a steering action conflicts with current canonical state
- **THEN** the response contract includes current idea facets, current index revision, conflicting refs, `mutated: false`, and diagnostics needed for user review

### Requirement: Portfolio Contract Fixtures Cover Cross-view Semantics
Contract tests SHALL prove that Python read models and TypeScript Project Web predicates interpret portfolio state consistently.

#### Scenario: Shared preset fixture is evaluated
- **WHEN** Python and TypeScript tests evaluate the same complete Research Idea fixture for every supported semantic preset
- **THEN** both implementations produce the same eligible idea ids and facet counts

#### Scenario: Independent facets are combined
- **WHEN** a fixture includes selected plus unexplored, explored plus deferred, supported plus closed, refuted plus open, and unknown legacy combinations
- **THEN** contract and UI tests preserve every independent facet
- **AND** no implementation replaces the combination with one authoritative status

#### Scenario: Decision and traversal fixtures are evaluated
- **WHEN** tests validate considered option sets, closure history, reopening history, ancestors, descendants, and incomplete traversal
- **THEN** Python schemas and TypeScript consumers preserve stable ids, completeness, mutation state, and diagnostics

#### Scenario: Kaoju-only portfolio fixture is evaluated
- **WHEN** Python and TypeScript tests evaluate a topic containing only canonical Research Ideas realized by a Kaoju Direction Set
- **THEN** the shared graph, timeline, preset, decision-context, realization-detail, and steering contracts validate without a Kaoju-specific client schema
- **AND** every durable proposal appears with the actor-authored selected, open, deferred, or closed meaning

#### Scenario: Mixed-paradigm portfolio fixture is evaluated
- **WHEN** Python and TypeScript tests evaluate one topic containing DeepSci-realized and Kaoju-realized canonical Research Ideas
- **THEN** both implementations return the same union of eligible idea ids, edges, facet counts, decision summaries, and topology completeness for the same predicate and revision
- **AND** neither implementation chooses one artifact family as the authoritative source scope

#### Scenario: Unprojected legacy Kaoju fixture is evaluated
- **WHEN** a legacy Direction Set lacks canonical Research Idea effects
- **THEN** backend and TypeScript contracts preserve the incomplete-portfolio diagnostic and migration or repair metadata
- **AND** Project Web does not validate transient payload-parsed direction nodes as canonical ideas

