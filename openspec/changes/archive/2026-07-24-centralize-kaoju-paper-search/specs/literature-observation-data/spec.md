## ADDED Requirements

### Requirement: Literature Provider Execution Remains Agent-Driven
The system SHALL let research agents invoke literature-provider or general-purpose CLI and HTTPS tools directly while keeping `isomer-cli` limited to Isomer-owned literature data validation, recording, indexing, and query.

#### Scenario: Agent performs an external paper search
- **WHEN** a paper-search skill selects S2 or another bound provider approach
- **THEN** the agent invokes an available external provider-native or general-purpose CLI or bounded HTTPS tool according to the approach guidance
- **AND** `isomer-cli` does not proxy, dispatch, wrap, or reproduce the provider request

#### Scenario: Local literature command is inspected
- **WHEN** help or command metadata for `isomer-cli ext research literature` is inspected
- **THEN** it states that the group reads and writes only Isomer-owned local data
- **AND** the group exposes no provider-facing `search`, `resolve`, `recommend`, `find-citing-papers`, or `explore-cited-papers` command

#### Scenario: Provider tool is unavailable
- **WHEN** no compatible external tool or permitted HTTPS path is available for the selected Literature Provider Binding
- **THEN** the paper-search workflow reports a blocked or reduced local-only scope
- **AND** it does not treat a local literature query as a substitute for an external provider search

### Requirement: Literature Observations Use a Provider-Neutral Schema
The system SHALL define `isomer-literature-provider-observation.v1` for a normalized observation produced by one logical literature action.

#### Scenario: Normalized observation is validated
- **WHEN** an agent submits a literature observation for validation or recording
- **THEN** the payload declares its schema version, action, research purpose, evidence-use intent, observation time, provider binding ref, provider, access method, query or target, requested and applied bounds, normalized papers, normalized relationships, pagination, completeness, limitations, and provider provenance
- **AND** validation preserves missing fields, unresolved records, null provider records, partial failures, and continuation posture without inventing metadata

#### Scenario: Citation direction is normalized
- **WHEN** the observation contains a provider-reported citation relationship
- **THEN** the relationship identifies normalized citing and cited paper keys, the forward or backward route relative to the requested target, the parent seed when applicable, and its source observation
- **AND** direction does not depend on provider response-wrapper names

#### Scenario: Provider-specific payload is submitted as canonical data
- **WHEN** a recording payload requires an S2-specific field, provider request body, authorization header, credential, or another provider-specific response shape for canonical validation
- **THEN** validation rejects the payload as non-portable or secret-bearing
- **AND** it reports that provider-specific mapping belongs to the agent's selected provider approach

### Requirement: One Logical Literature Action Produces One Canonical Observation
The literature recording service SHALL create one immutable provider-output Artifact for one logical paper-search action rather than one canonical record per provider page, paper candidate, or citation edge.

#### Scenario: Multi-page result is recorded
- **WHEN** an agent submits a valid normalized observation consolidated from several provider pages
- **THEN** `isomer-cli ext research literature record --payload-file OBSERVATION.json` records one provider-output Artifact with the exact page, record, bound, completeness, and partial-failure posture
- **AND** candidate papers and citation edges remain members of that Artifact rather than independent canonical lifecycle records

#### Scenario: Canonical observation is committed
- **WHEN** observation validation succeeds
- **THEN** recording stores the normalized payload through the existing research-record and structured-payload mechanisms with profile, schema, producer, actor, provider, source, and Provenance refs
- **AND** it refreshes a compatible literature projection only after the canonical record commit succeeds

#### Scenario: Literature projection is unavailable
- **WHEN** a valid observation is recorded while the compatible literature projection is missing or incompatible
- **THEN** the canonical Artifact commit succeeds and the result reports that an explicit index rebuild is required
- **AND** recording does not silently create or migrate the projection as a side effect of the canonical commit

### Requirement: Raw Provider Responses Are Optional Attachments
The literature observation contract SHALL permit redacted provider responses only as optional file-backed attachments and SHALL derive normalized literature indexes without reading them.

#### Scenario: Raw provider response is retained
- **WHEN** an agent elects to retain a provider response for diagnosis or reproducibility
- **THEN** the observation references a file-backed attachment with media type, checksum, provider provenance, and redaction posture
- **AND** the attachment excludes credentials, authorization headers, secret query values, and other sensitive material

#### Scenario: Raw provider response is absent
- **WHEN** a valid normalized observation has no raw provider attachment
- **THEN** validation and recording accept the observation
- **AND** index rebuild derives the same normalized paper and citation fields available from the canonical payload

#### Scenario: Index rebuild encounters raw attachment
- **WHEN** a normalized observation includes one or more raw provider attachment refs
- **THEN** literature index extraction ignores provider-specific attachment contents
- **AND** it uses only the validated normalized observation payload

### Requirement: Isomer CLI Manages Local Literature Data
The system SHALL expose provider-neutral `isomer-cli ext research literature` commands for normalized observation recording and Isomer-owned local data queries.

#### Scenario: Observation records are inspected
- **WHEN** an actor invokes `ext research literature observations list` or `observations show`
- **THEN** the command returns matching canonical literature-observation records and their validation, provenance, completeness, and projection posture
- **AND** it performs no provider or network request

#### Scenario: Recorded paper is queried
- **WHEN** an actor invokes `ext research literature papers query` with a supported normalized DOI, arXiv id, provider-qualified id, title, year, or observation selector
- **THEN** the command returns matching derived paper occurrences with their canonical observation refs and normalized source fields
- **AND** it does not promote an occurrence to an independent Artifact or source identity

#### Scenario: Recorded citations are queried
- **WHEN** an actor invokes `ext research literature citations query` with a normalized paper key and forward or backward direction
- **THEN** the command returns matching derived citation edges and their source observation refs
- **AND** it labels the edge as provider-reported rather than verified full-text evidence

#### Scenario: Query projection is missing
- **WHEN** a read-only paper or citation query finds no compatible literature projection
- **THEN** it reports the missing projection schema and the explicit rebuild command
- **AND** it does not create, migrate, repair, or rebuild tables

### Requirement: Literature Query Projection Is Separately Versioned
The system SHALL store a rebuildable `isomer-literature-query-index.v1` projection inside Workspace Runtime without revising the canonical `isomer-workspace-runtime.v1` schema version.

#### Scenario: Literature projection is initialized
- **WHEN** an actor explicitly invokes `ext research literature index rebuild`
- **THEN** the command creates or replaces literature observation, paper, citation-edge, and projection-metadata rows from valid canonical normalized observations
- **AND** it changes no canonical lifecycle record, structured payload, Discovery Ledger, Reading List, Finding, Evidence Item, or Provenance Record

#### Scenario: Projection metadata is inspected
- **WHEN** a local literature query or index-validation command reports projection posture
- **THEN** it includes `isomer-literature-query-index.v1`, source observation counts, payload-digest posture, rebuild time, and missing, stale, incompatible, or complete status
- **AND** it reports Workspace Runtime v1 independently from the literature projection version

#### Scenario: Literature projection is rebuilt twice
- **WHEN** unchanged canonical observations are rebuilt more than once
- **THEN** each rebuild produces deterministic paper and citation-edge identities and equivalent query results
- **AND** no duplicate derived occurrence or edge survives the replacement

#### Scenario: Literature projection is validated
- **WHEN** an actor invokes `ext research literature index validate`
- **THEN** validation reports schema compatibility, missing source records, payload-digest drift, malformed normalized paper keys, missing citation endpoints, and orphaned rows without mutation
- **AND** repair requires a separate explicit rebuild

### Requirement: Literature Observations Preserve Evidence Boundaries
Canonical literature observations and their derived query rows SHALL remain provider output until existing research owners accept and promote applicable information.

#### Scenario: Candidate is selected for a Kaoju survey
- **WHEN** a locally queried paper candidate participates in reading-list or direction-expansion work
- **THEN** `isomer-kaoju-discover` records selection, exclusion, duplicate, version-family, blocker, and priority judgment through its existing outputs
- **AND** the literature observation and derived index do not write the Discovery Ledger or Reading List

#### Scenario: Citation edge is used in a claim-bearing workflow
- **WHEN** a derived citation edge is relevant to a Research Claim
- **THEN** the workflow routes source acquisition and examination through the applicable owners before creating accepted Evidence Item links
- **AND** provider-reported citation metadata alone does not support or contradict the claim
