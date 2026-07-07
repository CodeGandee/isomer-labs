## ADDED Requirements

### Requirement: Exact Primary Idea Source Fragments
The system SHALL treat the main content source for a Primary Idea as an exact object-valued source fragment linked by an Idea Realization, not as the whole durable source record.

#### Scenario: Primary idea realization names exact object path
- **WHEN** a caller creates or updates the latest Idea Realization for a Primary Idea whose source record has a managed structured payload
- **THEN** the realization records a non-empty `source_json_path` that resolves to one JSON object in that payload
- **AND** the resolved object represents the selected Research Idea entry rather than a payload root, list, filter note, route note, or record context section
- **AND** supported source paths use the deterministic subset `$`, `$.field`, nested dot paths, and numeric list indexes such as `$.sections.raw_ideas[0]`

#### Scenario: Source labels remain aliases
- **WHEN** the resolved source fragment uses a source-local label such as `R1`, `C3`, or a draft-local candidate id
- **THEN** the canonical Research Idea preserves that label as an alias or realization metadata
- **AND** the source label does not replace the semantic topic-scoped `idea_id`

#### Scenario: Broad source path is invalid for primary preview
- **WHEN** a Primary Idea realization source path resolves to the payload root, a list, or a context-only section
- **THEN** validation reports a source-fragment diagnostic naming the idea id, record id, and source path
- **AND** the path is not accepted as the main idea preview source

#### Scenario: Invalid latest primary source is rejected on write
- **WHEN** a mutating CLI, API, or record-write convenience creates or updates a latest realization for a Primary Idea
- **THEN** invalid missing, broad, unresolved, or non-object source paths are rejected as write-time errors
- **AND** historical or supporting realizations may remain stored but do not power the default Primary Idea preview

### Requirement: Idea Detail Source Resolution
The idea detail read model SHALL distinguish idea content from source-record provenance.

#### Scenario: Exact source fragment is available
- **WHEN** the latest realization source path resolves to an exact idea fragment
- **THEN** the idea detail payload exposes that fragment as `idea_content` together with canonical Research Idea metadata
- **AND** it exposes the source record id, payload digest, payload locator, rendered record locator, and source diagnostics as `source_provenance`
- **AND** it may include the existing `source` object as compatibility metadata for one release

#### Scenario: Source fragment is unresolved
- **WHEN** the latest realization source path is missing, stale, or unresolved
- **THEN** the idea detail payload uses canonical Research Idea metadata as `idea_content`
- **AND** it reports diagnostics for the broken source path
- **AND** it does not fall back to the full source record payload as the main idea content

#### Scenario: User opens source record
- **WHEN** the user opens the linked source record from an idea detail tab
- **THEN** the GUI opens the durable record detail or rendered record view through an `Open Source Record` action or equivalent provenance control
- **AND** that record view may show slate-level notes, filter notes, route context, and other full-record material as provenance

### Requirement: Idea Source Validation CLI
The CLI SHALL expose deterministic validation and repair behavior for idea source fragments.

#### Scenario: Validate reports source integrity
- **WHEN** an operator runs `isomer-cli --print-json ext research ideas validate` for a Topic Workspace
- **THEN** the command reports missing source records, missing structured payloads, unresolved source paths, broad source paths, non-object source fragments, stale latest flags, duplicate latest realizations, and source fragments whose aliases or ids do not match the canonical Research Idea
- **AND** latest Primary Idea source violations are reported as errors while historical or supporting realization source issues are reported as warnings unless they also break topic or record integrity

#### Scenario: Repair previews deterministic changes
- **WHEN** an operator runs an idea repair or import command without an apply flag
- **THEN** the command returns a deterministic plan that names the records, payload paths, idea ids, aliases, realization updates, latest-flag changes, lineage or generation updates, and any optional payload-file updates it would write
- **AND** it does not mutate Workspace Runtime or payload files

#### Scenario: Repair applies exact paths
- **WHEN** an operator applies a repair plan for legacy idea source data
- **THEN** the command updates canonical idea rows and Idea Realizations to exact payload paths
- **AND** it does not mutate managed payload files unless the operator explicitly enables payload updates
- **AND** it records repair provenance or metadata without deleting source records or generated views

### Requirement: Profile-aware Idea Import
The system SHALL import idea source fragments through profile-aware mappings instead of generic key guesses.

#### Scenario: Raw idea slate import
- **WHEN** `import-from-record` or a record-write convenience imports a DeepSci raw idea slate payload
- **THEN** it maps idea entries from `$.sections.raw_ideas[N]`
- **AND** it treats `$.sections.filter_notes` as record context rather than idea content

#### Scenario: Candidate and selected idea imports
- **WHEN** import handles candidate frontier, pre-idea draft, selected hypothesis, selected idea draft, rejected/deferred idea, or paper-facing idea seed profiles
- **THEN** it uses the profile's declared idea-bearing section paths to create or update Research Ideas and Idea Realizations
- **AND** it reports a diagnostic rather than guessing when the profile has no declared idea-bearing section

#### Scenario: Shared source registry owns executable mappings
- **WHEN** CLI, query-index, API, or web code resolves profile-aware idea-bearing sections
- **THEN** it uses one shared Python source-fragment registry
- **AND** DeepSci skill and placeholder-binding text documents the mappings but is not the executable source of truth

### Requirement: Flash-attention Topic Source Migration
The flash-attention topic fixture SHALL be repaired to match the exact Primary Idea source contract.

#### Scenario: Existing topic validates under latest standard
- **WHEN** validation runs against `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`
- **THEN** Primary Idea realizations resolve to exact idea fragments
- **AND** no Primary Idea preview depends on a full raw slate, candidate frontier, filter notes, or route-decision payload

#### Scenario: Idea previews show true idea content
- **WHEN** the GUI opens a Primary Idea from the flash-attention idea-lineage graph
- **THEN** the main panel renders the Research Idea and exact source fragment
- **AND** slate-level filter notes and source-record context appear only through provenance, diagnostics, side metadata, or the source record view
