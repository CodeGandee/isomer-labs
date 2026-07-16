## ADDED Requirements

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
