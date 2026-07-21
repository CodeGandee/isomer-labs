## ADDED Requirements

### Requirement: Idea Graph Read Models Expose Portfolio Facets
The Topic Graph read API SHALL expose canonical Research Idea portfolio facets and facet diagnostics without requiring clients to interpret the deprecated compatibility status.

#### Scenario: Canonical idea node is returned
- **WHEN** the API returns a graph node or timeline row for a canonical Research Idea
- **THEN** the payload includes `exploration_state`, `decision_state`, `evidence_state`, `archive_state`, `visibility`, stable identity, display fields, and detail refs
- **AND** any deprecated compatibility `status` is labeled or documented as non-authoritative

#### Scenario: Facet counts are returned
- **WHEN** the API builds an Idea Graph or Idea Timeline source read model
- **THEN** it returns counts for each exploration, decision, evidence, archive, and visibility value over the declared source scope
- **AND** it identifies whether the counts describe complete or incomplete source topology

#### Scenario: Unknown facet is returned
- **WHEN** a Research Idea has an `unknown` exploration, decision, or evidence state
- **THEN** the API returns `unknown` unchanged and includes a needs-classification indicator or diagnostic
- **AND** it does not map the idea to a known state from title, summary, lineage, record kind, or timestamp

#### Scenario: Facet read remains lightweight
- **WHEN** graph or timeline list data includes portfolio facets and decision summaries
- **THEN** the response omits full realization payloads, rendered Markdown, transition rationale bodies, Decision Record bodies, Evidence Item bodies, and file content
- **AND** those details remain available through lazy detail requests

### Requirement: Semantic Idea Portfolio Presets
The Topic Graph read API SHALL support fixed semantic portfolio presets and return the exact predicate applied to each response.

#### Scenario: Current preset is requested
- **WHEN** a caller requests preset `current`
- **THEN** the response contains active Primary Ideas whose decision state is `unknown`, `open`, `shortlisted`, or `selected`
- **AND** unknown ideas remain visible with classification diagnostics

#### Scenario: All proposed preset is requested
- **WHEN** a caller requests preset `all-proposed`
- **THEN** the response contains every non-hidden canonical Research Idea in the source scope, including supporting and archived ideas
- **AND** visibility and archive state remain explicit

#### Scenario: Open for exploration preset is requested
- **WHEN** a caller requests preset `open-for-exploration`
- **THEN** the response contains active ideas whose decision state is `open`, `shortlisted`, or `selected`
- **AND** it does not treat `unknown`, `deferred`, or `closed` as explicitly open

#### Scenario: Lifecycle preset is requested
- **WHEN** a caller requests `unexplored`, `exploring`, `explored`, `selected`, `deferred`, or `closed`
- **THEN** the API applies the corresponding canonical exploration or decision facet predicate
- **AND** it reports that predicate in response metadata

#### Scenario: Needs classification preset is requested
- **WHEN** a caller requests preset `needs-classification`
- **THEN** the response contains non-hidden ideas with `unknown` exploration, decision, or evidence state
- **AND** diagnostics identify which facets require classification

#### Scenario: Explicit filters refine a preset
- **WHEN** a caller combines a supported preset with explicit facet, visibility, archive, relation-kind, generation, or decision filters
- **THEN** the API applies the documented composition order and returns the complete applied predicate
- **AND** invalid or contradictory filters produce deterministic diagnostics instead of silent remapping

#### Scenario: Filtered graph preserves coherent edges
- **WHEN** a preset or explicit filter omits Research Idea nodes
- **THEN** the response includes only canonical Idea Lineage Edges whose source and target nodes are present
- **AND** it reports omitted cross-boundary edge counts or diagnostics when known

### Requirement: Research Idea Decision Context Read Model
The Topic Graph read API SHALL expose read-only decision context for a Research Idea or Decision Record.

#### Scenario: User inspects why an idea was selected
- **WHEN** a caller requests decision context for a selected Research Idea
- **THEN** the response includes the relevant Decision Record refs, complete recorded considered option sets, selected and non-selected outcomes, rationale, consequence summaries, actor refs, timestamps, and supporting Evidence Item or Artifact refs
- **AND** it identifies incomplete historical option sets with diagnostics

#### Scenario: User inspects deferred or closed idea
- **WHEN** a caller requests decision context for a deferred or closed Research Idea
- **THEN** the response includes its current disposition reason code, rationale, transition refs, deciding actor and timestamp, supporting refs, and later reopening decisions when present

#### Scenario: User inspects decision by id
- **WHEN** a caller requests one Decision Record's Research Idea context
- **THEN** the response includes every recorded Research Idea option and outcome for that decision
- **AND** it does not expand generation siblings that were not recorded as decision options

#### Scenario: Decision context read is non-mutating
- **WHEN** decision context is listed, opened, filtered, or refreshed
- **THEN** the response reports `mutated: false`
- **AND** the operation does not create, repair, migrate, or backfill decision membership or state transitions

### Requirement: Bounded Research Idea Ancestor and Descendant Traversal
The Topic Graph read API SHALL provide bounded read-only ancestor and descendant traversal over canonical Idea Lineage Edges.

#### Scenario: Descendants are requested
- **WHEN** a caller supplies one or more valid root Research Idea ids, direction `descendants`, eligible relation kinds, and optional maximum depth
- **THEN** the API traverses canonical edges from parent to child and returns every reachable idea and induced eligible edge within the requested and configured bounds

#### Scenario: Ancestors are requested
- **WHEN** a caller supplies one or more valid root Research Idea ids, direction `ancestors`, eligible relation kinds, and optional maximum depth
- **THEN** the API traverses canonical edges from child to parent and returns every reachable idea and induced eligible edge within the requested and configured bounds

#### Scenario: Traversal is complete
- **WHEN** every eligible reachable node and edge fits within configured depth, node, and edge limits
- **THEN** the response reports traversal complete, root ids, direction, relation kinds, maximum observed depth, node count, edge count, and source index revision

#### Scenario: Traversal exceeds a bound
- **WHEN** eligible traversal exceeds a configured depth, node, edge, or response bound
- **THEN** the response reports incomplete traversal and the limiting bound with actionable continuation or refinement metadata
- **AND** it does not silently report a partial result as complete

#### Scenario: Root idea is unknown
- **WHEN** one or more requested root ids do not identify canonical Research Ideas in the selected Topic Workspace
- **THEN** the response reports unresolved-root diagnostics
- **AND** it traverses any remaining valid roots without inventing nodes

#### Scenario: Traversal remains canonical and read-only
- **WHEN** the backend calculates ancestor or descendant traversal
- **THEN** it uses canonical Idea Lineage Edges and does not infer authority from record lineage or generated Markdown
- **AND** it reports `mutated: false` and writes no graph, filter, selection, or layout state to Workspace Runtime

### Requirement: Canonical Portfolio Read Models Are Paradigm Independent
The Topic Graph read API SHALL combine all topic-scoped canonical Research Ideas into one portfolio regardless of producing research paradigm, artifact family, or installed extension set.

#### Scenario: Kaoju-only topic is read
- **WHEN** a Topic Workspace contains canonical Research Ideas realized by Kaoju Direction Set proposals and no DeepSci extension or DeepSci records
- **THEN** Idea Graph and Idea Timeline read models return those directions with the same facets, decision summaries, lineage, detail refs, presets, and steering eligibility used for every canonical Research Idea
- **AND** the response does not require a Kaoju-specific graph mode or payload parser

#### Scenario: Mixed DeepSci and Kaoju topic is read
- **WHEN** one topic contains canonical Research Ideas realized by both DeepSci records and Kaoju Direction Sets
- **THEN** the canonical read model returns the union of eligible topic-scoped ideas and canonical Idea Lineage Edges under one source revision and applied predicate
- **AND** entering canonical graph mode because one family has ideas does not suppress canonical ideas from another family

#### Scenario: Legacy idea-bearing record lacks canonical projection
- **WHEN** the topic contains a legacy Direction Set or another idea-bearing record whose promised canonical Research Idea effects are absent
- **THEN** the read model or index diagnostics identify the unprojected record and the previewable migration or repair route
- **AND** the API does not parse the paradigm payload into authoritative transient GUI nodes or silently claim that the canonical portfolio is complete

#### Scenario: Paradigm-specific realization detail is opened
- **WHEN** a user opens the detail for a Research Idea realized by a Kaoju proposal or another paradigm-specific record
- **THEN** the list response remains lightweight and the detail route resolves the exact canonical Idea Realization and source object on demand
- **AND** portfolio filtering and graph topology do not depend on loading the source payload

### Requirement: Portfolio Read Models Preserve Revision Semantics
Canonical Research Idea state, decision membership, and lineage changes SHALL participate in topic index revision and read-model invalidation.

#### Scenario: Canonical portfolio state changes
- **WHEN** an accepted write changes a Research Idea facet, state transition, decision option membership, or Idea Lineage Edge
- **THEN** the effective topic index revision changes after derived read models are refreshed
- **AND** topic events identify the affected idea graph or timeline scopes without carrying heavy content

#### Scenario: Browser-only state changes
- **WHEN** a user changes graph selection, focus, layout, collapsed controls, a locally equivalent filter, or viewport state without a canonical write
- **THEN** the topic index revision does not change
- **AND** the backend does not persist that browser-only state as research data
